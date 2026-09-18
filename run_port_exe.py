# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import subprocess
import sys
import threading
import time
import traceback
from collections import deque
import datetime
from threading import Lock, Event

import requests
import logging

import win32api
import win32con

import cmd_on_color
from download_files import download_file
from notification_simulator import show_notification
from func_timeout import func_set_timeout

from upload_node import download_file2, get_clash2, get_clash1

logging.captureWarnings(True)  # 强制取消证书验证警告

import faulthandler
import signal

# 启用 faulthandler
faulthandler.enable()

# 设置超时（5秒无响应后打印堆栈）
faulthandler.dump_traceback_later(5)


def handle_sigint(signum, frame):
    print("\n用户手动触发调试：")
    faulthandler.dump_traceback()  # 打印堆栈
    # 可以在这里进入 pdb 调试
    import pdb
    pdb.set_trace()


signal.signal(signal.SIGINT, handle_sigint)

# 全局锁，用于保护全局变量的访问
global_lock = threading.Lock()

connection_success_printed = False
connection_success_printed2 = False
network_err = 1
all_net_err = ''

import chardet


def write_with_limit(file_path, content, max_lines=28):
    """写入内容到文件，并在超过最大行数时删除第一行"""
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 检测文件编码
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(1024)  # 读取前1024字节用于检测编码
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'
    except FileNotFoundError:
        encoding = 'utf-8'

    # 读取现有内容
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    # 添加新内容
    lines.append(content + '\n')

    # 检查是否超过最大行数
    if len(lines) > max_lines:
        lines = lines[-max_lines:]  # 保留最后max_lines行

    # 写回文件，统一使用utf-8编码
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def ask_yes_no_question_old(question):
    import tkinter as tk
    from tkinter import messagebox
    """
    创建一个弹窗，显示问题并提供是/否选项

    参数:
    question (str): 要显示的问题

    返回:
    bool: 用户选择True(是)或False(否)
    """
    # 创建主窗口
    root = tk.Tk()
    # 确保窗口在所有其他窗口前面
    root.attributes('-topmost', True)
    # 隐藏主窗口
    root.withdraw()

    # 显示消息框并获取结果
    result = messagebox.askyesno("提示", question)

    # 关闭主窗口
    root.destroy()

    return result

def ask_yes_no_question(question):
    """
    使用 Win32 API 创建是/否对话框，线程安全。
    """
    result = win32api.MessageBox(
        None,
        question,
        "提示",
        win32con.MB_YESNO | win32con.MB_ICONQUESTION | win32con.MB_TOPMOST
    )
    return result == win32con.IDYES

class LogManager:
    def __init__(self, base_dir, log_type):
        self.base_dir = base_dir
        self.log_type = log_type
        self.current_hour = None
        self.current_file = None
        self.file_handle = None
        self.log_buffer = []
        self.flush_interval = 1
        self.last_flush_time = time.time()
        self.lock = threading.Lock()  # 线程锁保护日志操作
        self._open_log_file()

    def _get_log_filename(self):
        now = datetime.datetime.now()
        return os.path.join(
            self.base_dir,
            f"{self.log_type}_log_{now.strftime('%Y%m%d_%H0000')}.txt"
        )

    def _open_log_file(self):
        # 调用者必须已持有 self.lock
        now = datetime.datetime.now()
        current_hour = now.strftime('%Y%m%d_%H')
        if current_hour != self.current_hour or not self.file_handle:
            try:
                if self.file_handle:
                    self.file_handle.close()
                self.current_hour = current_hour
                self.current_file = self._get_log_filename()
                os.makedirs(os.path.dirname(self.current_file), exist_ok=True)
                self.file_handle = open(self.current_file, 'a', encoding='utf-8')
            except Exception as e:
                print(f"日志文件打开失败: {str(e)}")
                self.file_handle = None
    def write(self, message):
        now = datetime.datetime.now()
        current_hour = now.strftime('%Y%m%d_%H')
        # print(f"线程{threading.current_thread().name}尝试获取日志锁")
        # acquired = self.lock.acquire(timeout=5)  # 5秒超时
        # if not acquired:
        #     print(f"日志写入超时: {message[:50]}...")
        #     return

        try:
            with self.lock:
                # print(f"线程{threading.current_thread().name}获取到日志锁")
                if not self.file_handle:
                    self._open_log_file()
                if self.file_handle:
                    self.log_buffer.append(message + "\n")  # 确保每行都有换行符
                    # 关键信息实时写入，普通信息批量写入
                    if any(keyword in message for keyword in ['错误', '失败', '拒绝', '成功']):
                        self._safe_flush()
                    elif time.time() - self.last_flush_time >= self.flush_interval:
                        self._safe_flush()
        except Exception as e:
            print(f"日志写入异常: {str(e)}")
            # 确保锁被释放
            # if self.lock.locked():
            #     self.lock.release()
        # print(f"{current_hour}||线程{threading.current_thread().name}释放日志锁")

    def _safe_flush(self):
        try:
            if self.log_buffer and self.file_handle:
                self.file_handle.writelines(self.log_buffer)
                self.file_handle.flush()
                self.log_buffer.clear()
                self.last_flush_time = time.time()
        except Exception as e:
            print(f"日志写入失败: {str(e)}")
            self.file_handle = None
            self._open_log_file()

    def close(self):
        with self.lock:
            self._safe_flush()
            if self.file_handle:
                self.file_handle.close()
                self.file_handle = None



def run_exe(local_port, run_type, cmd, object_name_output_log, type_, exe_name, object_name, exe_name_path,
            err_node_number, show_notification_state=True):
    global connection_success_printed, connection_success_printed2, network_err, all_net_err

    # port8100_success = '未知状态'
    final_state = '手动退出'
    other_path = os.path.join(object_name_output_log, f'{type_}_{local_port}_err_other.txt')
    log_manager = LogManager(object_name_output_log, f'{type_}_{local_port}')
    log_manager.write(f"===== run_exe 开始 (端口 {local_port}) =====\n")
    print('CMD:', cmd)
    log_manager.write(f"执行的命令: {cmd}\n\n")
    port8100_success = os.path.join(fr'{os.getcwd()}\GoflywayTools_output_log', f'GoflywayTools_success_port8100.txt')

    # 进程对象和线程对象的引用，用于后续清理
    process = None
    checker_thread = None
    reader_thread = None

    # 创建事件对象用于线程同步
    network_checker_exited = Event()
    output_reader_exited = Event()
    # 新增：网络失败事件，当网络检测彻底失败时设置
    network_failed_event = Event()

    try:
        print(f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}||启动 {exe_name}【{type_}】...")
        log_manager.write(f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}||启动 {exe_name}【{type_}】...\n")

        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,  # 行缓冲
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        state_container = {
            'code': None,
            'message': '',
            'source': '',
            'lock': Lock(),
            'stop': False,
            'output_completed': False,
            'exit_immediately': False
        }

        def update_state(code, msg, src):
            log_manager.write(f"线程{threading.current_thread().ident} 尝试获取状态锁")
            with state_container['lock']:
                log_manager.write(f"线程{threading.current_thread().ident} 已获取状态锁")
                state_container.update({'code': code, 'message': msg, 'source': src})
                log_manager.write(f"线程{threading.current_thread().ident} 将释放状态锁")
            log_manager.write(f"线程{threading.current_thread().ident} 已释放状态锁")
        def get_final_state():
            # 尝试获取锁，超时5秒
            if not state_container['lock'].acquire(timeout=5):
                log_manager.write("严重错误：获取状态锁超时，可能死锁")
                return "状态锁超时"
            try:
                if state_container['code'] is not None:
                    details = []
                    if state_container['source']:
                        details.append(f"来源:{state_container['source']}")
                    if state_container['message']:
                        details.append(state_container['message'])
                    return f"错误({state_container['code']}): {'; '.join(details)}"
                if process.returncode == 0:
                    return "成功"
                return f"进程异常(退出码:{process.returncode})"
            finally:
                state_container['lock'].release()

        port_coincide_path = os.path.join(object_name_output_log, f'{type_}_err_port{local_port}_coincide.txt')
        with open(port_coincide_path, 'w') as f:
            f.write("")

        network_status = {'alive': True, 'lock': Lock()}

        def network_checker():
            global connection_success_printed2
            global connection_success_printed
            global network_err
            global all_net_err

            try:
                test_url = "https://api.ipify.org"
                attempt_count = 8  # 固定尝试次数为3次

                # 根据端口和错误节点号设置不同的尝试间隔
                if local_port == 88:
                    if err_node_number < 2:
                        sleep_interval = 1
                    elif 2 < err_node_number < 8:
                        sleep_interval = 2
                    else:
                        sleep_interval = 8
                else:
                    if err_node_number < 8:
                        if 'GoflywayTools' in str(type_):
                            sleep_interval = 8
                            attempt_count = 18
                        else:
                            sleep_interval = 2
                    else:
                        sleep_interval = 8
                        attempt_count = 18
                time.sleep(8)

                while (getattr(threading.current_thread(), "do_run", True) and
                       not state_container['exit_immediately'] and
                       not network_checker_exited.is_set()):

                    try:
                        with open(port_coincide_path, 'r') as f:
                            port_coincide_state = f.read()
                        port_coincide_state = True  # 固定为True，假设端口未被占用

                        if port_coincide_state:
                            proxies = {'http': f'socks5h://127.0.0.1:{local_port}',
                                       'https': f'socks5h://127.0.0.1:{local_port}'}
                            success = False
                            port8100_state = ''
                            for attempt in range(attempt_count):
                                try:
                                    resp = requests.get(test_url, proxies=proxies, timeout=8)
                                    if resp.status_code == 200:
                                        with global_lock:
                                            network_err = 1
                                        with network_status['lock']:
                                            network_status['alive'] = True
                                        connection_success_printed = True
                                        log_manager.write(
                                            f'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}||端口{local_port}（{exe_name}）【{type_}】连接成功！可以上网啦！207==>>{line}\n')
                                        cmd_on_color.printGre(
                                            f'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}||端口{local_port}（{exe_name}）【{type_}】连接成功！可以上网啦！207')
                                        if 'GoflywayTools' in str(type_) and '8100' in str(local_port):
                                            write_with_limit(port8100_success,
                                                             f"{datetime.datetime.now()}连接成功")

                                        if not connection_success_printed and not connection_success_printed2 and show_notification_state:
                                            local_port_secondary = '未知'
                                            if 'GoflywayTools' in type_:
                                                local_port_secondary = 8100
                                            if 'SS1' in type_:
                                                local_port_secondary = 10801
                                            if 'SS2' in type_:
                                                local_port_secondary = 10802
                                            if 'SSR1' in type_:
                                                local_port_secondary = 10805
                                            if 'SSR2' in type_:
                                                local_port_secondary = 10806
                                            if 'v2ray1' in type_:
                                                local_port_secondary = 10822
                                            if 'v2ray2' in type_:
                                                local_port_secondary = 10999
                                            if err_node_number > 0:
                                                show_notification(f'端口{local_port}({local_port_secondary})连接成功！',
                                                                  f"可以上网啦！【第{err_node_number}次检测】", "success")
                                            with global_lock:
                                                connection_success_printed = True
                                                connection_success_printed2 = True
                                        success = True
                                        all_net_err = ''
                                        break
                                    else:
                                        cmd_on_color.printRed(
                                            f"{local_port}端口（{exe_name}）网络第{attempt + 1}次尝试链接失败，状态码: {resp.status_code}")
                                        log_manager.write(
                                            f"{local_port}端口（{exe_name}）网络第{attempt + 1}次尝试链接失败，状态码: {resp.status_code}\n")
                                        if 'GoflywayTools' in str(type_) and '8100' in str(local_port) and attempt >= 2:
                                            with open(port8100_success, 'w') as f:
                                                f.write("")
                                except Exception as err:
                                    cmd_on_color.printRed(
                                        f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}||{local_port}端口（{exe_name}）【{type_}】网络检测尝试第{attempt + 1}次失败: {str(err)}")
                                    log_manager.write(
                                        f"{local_port}端口（{exe_name}）第{attempt + 1}次失败: {str(err)}\n")
                                    time.sleep(sleep_interval)
                                    if 'GoflywayTools' in str(type_) and '8100' in str(local_port) and attempt >= 2:
                                        with open(port8100_success, 'w') as f:
                                            f.write("")

                                if attempt >= 0 and 'GoflywayTools' not in str(type_) and run_type == '所有':
                                    try:
                                        with open(port8100_success, 'r') as f:
                                            port8100_success_list = f.read().split('\n')
                                    except:
                                        with open(port8100_success, 'w') as f:
                                            f.write("")
                                        port8100_success_list = []
                                    print('port8100_success_list282', port8100_success, port8100_success_list,
                                          len(port8100_success_list))
                                    if len(port8100_success_list) >= 8:
                                        answer = True  # 一直切换为端口8100
                                        if answer:
                                            port8100_state = '切换为端口8100'
                                            cmd_on_color.printMag(port8100_state)
                                            break

                        log_manager.write(f"{local_port}端口（{exe_name}）【{type_}】=={success}365\n")
                        if not success:  # 所有尝试都失败
                            all_net_err = f'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}||{local_port}端口（{exe_name}）【{type_}】所有网络连接尝试都失败367'
                            cmd_on_color.printRed(all_net_err)
                            update_state(100,
                                         f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}||{local_port}端口（{exe_name}）【{type_}】所有网络连接失败，不可以上网，{port8100_state}",
                                         "network")
                            log_manager.write(
                                f"{local_port}端口（{exe_name}）【{type_}】所有网络连接尝试都失败286\n")
                            with global_lock:
                                connection_success_printed = False
                                connection_success_printed2 = False
                            log_manager.write(
                                f"{local_port}端口（{exe_name}）网络检测线程准备退出循环372\n")
                            with network_status['lock']:
                                network_status['alive'] = False
                            # 设置网络失败事件
                            network_failed_event.set()
                            log_manager.write(
                                f"{local_port}端口（{exe_name}）网络检测线程准备退出循环376\n")
                            if 'GoflywayTools' in str(type_) and '8100' in str(local_port):
                                with open(port8100_success, 'w') as f:
                                    f.write("")
                            break

                    except Exception as e:
                        cmd_on_color.printRed(f"网络检测异常302: {str(e)}")
                        log_manager.write(f"网络检测异常302: {str(e)}\n")
                        update_state(999, f"网络检测异常302，不可以上网: {str(e)}", "network")
                        with network_status['lock']:
                            network_status['alive'] = False
                        # 设置网络失败事件
                        network_failed_event.set()
                        if 'GoflywayTools' in str(type_) and '8100' in str(local_port):
                            with open(port8100_success, 'w') as f:
                                f.write("")
                        break

                    # 检查是否应该退出
                    if (not getattr(threading.current_thread(), "do_run", True) or
                            state_container['exit_immediately'] or
                            network_checker_exited.is_set()):
                        break

                    time.sleep(sleep_interval)

            except Exception as e:
                log_manager.write(f"网络检测线程异常: {str(e)}\n")
                traceback.print_exc()
            finally:

                # ----- 调试打印：线程退出前 -----
                debug_msg = f"网络检测线程退出中 (alive={network_status['alive']}, exit_immediately={state_container.get('exit_immediately', False)})"
                cmd_on_color.printMag(debug_msg)
                log_manager.write(f"{debug_msg}\n")

                network_checker_exited.set()  # 设置退出标志
                cmd_on_color.printMag('网络检测线程已退出308')
                log_manager.write(f"{local_port}端口（{exe_name}）网络检测线程已退出\n")
                cmd_on_color.printMag('网络检测线程已退出422')
                debug_msg = f"网络检测线程退出中 (alive={network_status['alive']}, exit_immediately={state_container.get('exit_immediately', False)})"
                cmd_on_color.printMag(debug_msg)
                log_manager.write(f"{debug_msg}\n")
                network_checker_exited.set()
                log_manager.write(f"网络检测线程({threading.current_thread().ident})已退出\n")
                # ----- 调试结束 -----

        checker_thread = threading.Thread(target=network_checker)
        checker_thread.daemon = True
        checker_thread.do_run = True
        checker_thread.start()
        print(f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}||network_checker428执行结束={type_, exe_name}", network_status)


        def output_handler(line):
            global connection_success_printed
            global connection_success_printed2
            global network_err
            global all_net_err

            log_manager.write(f'{type_}==>>{line}【315】')

            if '系统找不到指定的文件' in line:
                update_state(801, "EXE缺失，不可以上网", "output")
                win32api.MessageBox(0, f'缺失文件: {exe_name_path}', '错误', win32con.MB_ICONWARNING)
                return 'EXE缺失'
            elif 'json parse error' in line or 'json: cannot' in line or 'expected array, boolean' in line:
                update_state(800, "配置缺失，不可以上网", "output")
                return '配置缺失'
            elif 'cipher not supported' in line:
                with network_status['lock']:
                    network_status['alive'] = False
                update_state(108, "不支持的加密模式，不可以上网", "output")
                with open(port_coincide_path, 'w') as f:
                    f.write(f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}||{line}==>>不支持的加密模式\n")
                win32api.MessageBox(0,
                                    f'错误：{line}==>>【不支持的加密模式】，程序：{type_}.py',
                                    f'不支持的加密模式',
                                    win32con.MB_ICONWARNING
                                    )
                return '不支持的加密模式'
            elif '只允许使用一次' in line or 'Address already in use' in line or 'Only one usage of each socket address' in line:
                cmd_on_color.printRed(f'错误：{line}==>>【端口{local_port}被占用】，程序：{type_}.py')
                with open(port_coincide_path, 'w') as f:
                    f.write(f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}||{line}==>>只允许使用一次，端口：{local_port}\n")
                return '端口被占用'

            # 检查网络错误
            with network_status['lock']:
                if not network_status['alive']:
                    return '网络连接失败'

            return None

        output_queue = deque(maxlen=200)
        output_lock = Lock()

        def output_reader():
            try:
                while not state_container['stop'] and not output_reader_exited.is_set():
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        with output_lock:
                            output_queue.append(line.strip())
            except Exception as e:
                log_manager.write(f"输出读取线程异常: {str(e)}\n")
            finally:
                with state_container['lock']:
                    state_container['output_completed'] = True
                output_reader_exited.set()

        reader_thread = threading.Thread(target=output_reader)
        reader_thread.daemon = True
        reader_thread.start()

        process_start_time = time.time()
        last_check = time.time()
        early_return_value = None
        # ----- 启用超时机制 -----
        # max_execution_time = 120  # 最大执行时间2分钟（120秒）
        max_execution_time = 888  # 原注释保留

        # 保存主线程引用用于检查
        main_thread = threading.current_thread()

        # ----- 添加循环计数器用于调试 -----
        loop_count = 0
        debug_interval = 100  # 每100次打印一次调试信息
        # ========== 新增：心跳超时检测变量 ==========
        last_heartbeat = time.time()
        HEARTBEAT_TIMEOUT = 30  # 30秒未更新视为卡死
        while True:

            loop_count += 1

            # ========== 新增：心跳超时检测 ==========
            if time.time() - last_heartbeat > HEARTBEAT_TIMEOUT:
                heartbeat_msg = f"\n{'=' * 60}\n" \
                                f"⚠️ 警告：主循环心跳超时（超过{HEARTBEAT_TIMEOUT}秒未更新）\n" \
                                f"当前时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
                                f"loop_count: {loop_count}\n" \
                                f"net_alive: {network_status['alive']}\n" \
                                f"net_exited: {network_checker_exited.is_set()}\n" \
                                f"out_exited: {output_reader_exited.is_set()}\n" \
                                f"exit_immediate: {state_container['exit_immediately']}\n" \
                                f"process_returncode: {process.poll()}\n" \
                                f"output_queue长度: {len(output_queue)}\n" \
                                f"{'=' * 60}\n"

                # 写入日志文件
                log_manager.write(heartbeat_msg)
                # 打印到控制台
                print(heartbeat_msg)

                # 打印所有线程堆栈
                print("\n===== 所有线程堆栈信息 =====")
                faulthandler.dump_traceback(file=sys.stdout)
                print("===== 堆栈打印结束 =====\n")

                # 重置心跳时间，避免无限打印（可选：如果你只想打印一次，就注释掉这行）
                last_heartbeat = time.time()
            # =======================================

            if loop_count % 100 == 0:  # 每100次打印一次
                log_manager.write(
                    f"主循环 #{loop_count} time={datetime.datetime.now().strftime('%H%M%S')} "
                    f"net_alive={network_status['alive']} "
                    f"net_exited={network_checker_exited.is_set()} "
                    f"out_exited={output_reader_exited.is_set()} "
                    f"exit_immediate={state_container['exit_immediately']} "
                    f"process_returncode={process.poll()}\n"
                )




            # ----- 调试打印：定期输出循环状态 -----
            if loop_count % debug_interval == 0:
                debug_msg = (
                    f"590主循环 #{loop_count} 时间={datetime.datetime.now().strftime('%H%M%S')} "
                    f"net_alive={network_status['alive']} "
                    f"net_exited={network_checker_exited.is_set()} "
                    f"out_exited={output_reader_exited.is_set()} "
                    f"exit_immediate={state_container['exit_immediately']} "
                    f"process_returncode={process.poll()}"
                )
                print(debug_msg)
                log_manager.write(debug_msg + "\n")

            # 异步日志清理
            if time.time() - last_check > 30:
                threading.Thread(target=lambda: _async_log_clean(object_name_output_log), daemon=True).start()
                last_check = time.time()

            # 处理输出队列
            with output_lock:
                while output_queue:
                    line = output_queue.popleft()
                    error_state = output_handler(line)
                    if error_state:
                        cmd_on_color.printRed(f'262不可以上网：{error_state}')
                        with global_lock:
                            connection_success_printed = False
                            connection_success_printed2 = False
                        with state_container['lock']:
                            state_container['value'] = f'不可以上网'
                            state_container['exit_immediately'] = True
                            final_state = '不可以上网'
                        early_return_value = final_state
                        break

            if early_return_value is not None:
                log_manager.write(f"主循环因early_return_value={early_return_value}准备退出\n")
                break

            # 新增：检查网络失败事件
            if network_failed_event.is_set():
                log_manager.write(f"主循环因网络失败事件准备退出 (network_failed_event)\n")
                final_state = '网络连接失败'
                break

            # 网络状态检查
            with network_status['lock']:
                if not network_status['alive']:
                    log_manager.write(f"主循环因网络状态检查失败准备退出 (network_status['alive']=False)\n")
                    final_state = '网络连接失败'
                    break

            # 进程状态检查
            if process.poll() is not None:
                if process.returncode is not None:
                    if 'time="' not in line:
                        update_state(process.returncode, f"进程退出代码 {process.returncode}==>>1 表示子进程已经终止，不可以上网", "process")
                    else:
                        update_state(process.returncode, f"进程退出代码 {process.returncode}==>>似乎配置文件不存在或格式有问题，不可以上网", "process")
                else:
                    update_state(-1, "进程意外终止，不可以上网", "process")
                log_manager.write(f"主循环因进程状态检查失败准备退出，returncode={process.returncode}\n")
                if 'GoflywayTools' in str(type_) and '8100' in str(local_port):
                    with open(port8100_success, 'w') as f:
                        f.write("")
                break

            # 状态码检查
            with state_container['lock']:
                if state_container['code'] is not None:
                    final_state = get_final_state()
                    log_manager.write(f"主循环因状态码检查失败准备退出，code={state_container['code']}\n")
                    break

            # 检查线程事件
            if network_checker_exited.is_set() and output_reader_exited.is_set():
                log_manager.write(f"所有子线程都已退出，主循环准备退出 (network_exited={network_checker_exited.is_set()}, output_exited={output_reader_exited.is_set()})\n")
                final_state = '所有线程已退出'
                break

            # 检查超时（连接未成功）
            if (time.time() - process_start_time) > max_execution_time and not connection_success_printed:
                update_state(998, "执行超时，不可以上网", "timeout")
                log_manager.write(f"主循环执行时间超过{max_execution_time}秒，准备退出\n")
                final_state = "执行超时，不可以上网"
                all_net_err = ''
                if 'GoflywayTools' in str(type_) and '8100' in str(local_port):
                    with open(port8100_success, 'w') as f:
                        f.write("")
                break
            # ========== 新增：每次循环末尾更新心跳时间 ==========
            last_heartbeat = time.time()
            time.sleep(0.1)  # 100ms间隔，平衡响应速度和CPU使用率

        # ----- 调试：退出原因 -----
        cmd_on_color.printMag(f"主循环退出，final_state={final_state}")
        log_manager.write(f"主循环退出，final_state={final_state}\n")

        # 清理资源
        log_manager.write(f"开始清理线程资源\n")

        # 设置退出标志
        with state_container['lock']:
            state_container['stop'] = True
            state_container['exit_immediately'] = True

        # 设置事件标志
        network_checker_exited.set()
        output_reader_exited.set()

        # 停止网络检测线程
        if checker_thread and checker_thread.is_alive():
            checker_thread.do_run = False
            checker_thread.join(timeout=2)
            if checker_thread.is_alive():
                log_manager.write(f"警告: 网络检测线程未能在2秒内正常退出\n")
                # 强制打印线程堆栈
                print("强制打印网络检测线程堆栈:")
                for thread_id, frame in sys._current_frames().items():
                    if thread_id == checker_thread.ident:
                        traceback.print_stack(frame)
                        break

        # 停止输出读取线程
        if reader_thread and reader_thread.is_alive():
            reader_thread.join(timeout=2)
            if reader_thread.is_alive():
                log_manager.write(f"警告: 输出读取线程未能在2秒内正常退出\n")
                # 强制打印线程堆栈
                print("强制打印输出读取线程堆栈:")
                for thread_id, frame in sys._current_frames().items():
                    if thread_id == reader_thread.ident:
                        traceback.print_stack(frame)
                        break

        # 处理剩余输出
        with output_lock:
            while output_queue:
                line = output_queue.popleft()
                output_handler(line)

        # 终止子进程
        if process and process.poll() is None:
            try:
                log_manager.write(f"尝试优雅终止子进程 {process.pid}...\n")
                process.terminate()
                process.wait(timeout=3)  # 等待3秒让进程优雅退出
                if process.poll() is None:
                    log_manager.write(f"警告: 子进程 {process.pid} 未能在3秒内优雅退出，尝试强制终止...\n")
                    process.kill()
                    process.wait(timeout=2)
            except Exception as e:
                log_manager.write(f"错误: 终止子进程时发生异常: {str(e)}\n")

        # 最终状态判定
        if state_container['code'] is not None:
            final_state = get_final_state()
        elif 'value' in state_container and state_container['value']:
            final_state = state_container['value']
        elif process.returncode is not None:
            final_state = f'错误码:{process.returncode}'
        else:
            with network_status['lock']:
                final_state = '网络连接失败' if not network_status['alive'] else '未知错误'

        print(f'进程最终状态: {final_state}')
        log_manager.write(f"进程最终状态已确定: {final_state}\n")

        # 错误分析
        if '错误码' in final_state:
            if 'GoflywayTools' in str(type_) and '8100' in str(local_port):
                with open(port8100_success, 'w') as f:
                    f.write("")
            print("\n===== 错误分析 =====")
            try:
                current_log_file = log_manager.current_file
                if current_log_file and os.path.exists(current_log_file):
                    with open(current_log_file, 'r', encoding='utf-8') as f:
                        log_lines = f.readlines()
                        print("\n最近10行日志:")
                        for line in log_lines[-10:]:
                            print(line.strip())
                        print("\n所有错误日志:")
                        for line in log_lines:
                            if any(keyword in line for keyword in ['错误', '失败', '拒绝', '缺失', '异常']):
                                print(line.strip())
            except Exception as e:
                print(f"日志分析失败: {str(e)}")
                log_manager.write(f"错误分析失败: {str(e)}\n")

        log_manager.write(f"\n{datetime.datetime.now()}进程的最终状态: {final_state}\n")
        log_manager.write(f"===== run_exe 结束，final_state={final_state} =====\n")
        return final_state

    except Exception as e:
        traceback.print_exc()
        final_state = f'异常: {str(e)}'
        log_manager.write(f"\n{datetime.datetime.now()}异常: {final_state}\n")
        log_manager.write(f"===== run_exe 结束，final_state={final_state} =====\n")
        return final_state
    finally:
        print(f"进程结束，状态: {final_state}")
        # 在 run_exe 函数的 finally 块中
        log_manager.write("=== 开始清理资源 ===\n")

        # 1. 终止子进程
        log_manager.write("清理步骤: 终止子进程...\n")
        if process and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=3)
                if process.poll() is None:
                    log_manager.write("子进程未优雅退出，尝试强制终止...\n")
                    process.kill()
                    process.wait(timeout=2)
            except Exception as e:
                log_manager.write(f"终止子进程异常: {e}\n")
        log_manager.write("清理步骤: 子进程终止完成\n")

        # 2. 停止网络检测线程
        log_manager.write("清理步骤: 停止网络检测线程...\n")
        if checker_thread and checker_thread.is_alive():
            checker_thread.do_run = False
            checker_thread.join(timeout=2)
            if checker_thread.is_alive():
                log_manager.write(f"警告: 网络检测线程({checker_thread.ident})未退出，打印堆栈:\n")
                # 捕获堆栈并写入日志
                for tid, frame in sys._current_frames().items():
                    if tid == checker_thread.ident:
                        stack = ''.join(traceback.format_stack(frame))
                        log_manager.write(stack + "\n")
                        break
            else:
                log_manager.write("网络检测线程已正常退出\n")
        else:
            log_manager.write("网络检测线程已不存在\n")

        # 3. 停止输出读取线程
        log_manager.write("清理步骤: 停止输出读取线程...\n")
        if reader_thread and reader_thread.is_alive():
            reader_thread.join(timeout=2)
            if reader_thread.is_alive():
                log_manager.write(f"警告: 输出读取线程({reader_thread.ident})未退出，打印堆栈:\n")
                for tid, frame in sys._current_frames().items():
                    if tid == reader_thread.ident:
                        stack = ''.join(traceback.format_stack(frame))
                        log_manager.write(stack + "\n")
                        break
            else:
                log_manager.write("输出读取线程已正常退出\n")
        else:
            log_manager.write("输出读取线程已不存在\n")

        log_manager.write("=== 清理完成 ===\n")
        try:
            # 确保所有线程和进程都已停止
            network_checker_exited.set()
            output_reader_exited.set()

            if checker_thread and checker_thread.is_alive():
                checker_thread.do_run = False
                checker_thread.join(timeout=1)

            if reader_thread and reader_thread.is_alive():
                reader_thread.join(timeout=1)

            if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=2)
                except:
                    pass
                finally:
                    if process.poll() is None:
                        try:
                            process.kill()
                        except:
                            pass

            # 记录最终状态
            if log_manager:
                log_manager.write(f"\n结束时间: {datetime.datetime.now()}进程结束，状态: {final_state}\n")

            # 记录错误状态
            if '错误码' in final_state:
                if 'GoflywayTools' in str(type_) and '8100' in str(local_port):
                    with open(port8100_success, 'w') as f:
                        f.write("")
                with open(other_path, 'a') as f:
                    f.write(f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}||{final_state}\n")
                win32api.MessageBox(0, f'错误：{final_state}，程序：{type_}.py', '错误', win32con.MB_ICONWARNING)

        except Exception as e:
            print(f"清理过程中发生错误: {str(e)}")
            traceback.print_exc()

        finally:
            # 确保日志管理器关闭
            if log_manager:
                log_manager.close()

            # 重置全局状态
            with global_lock:
                network_err = 1
                connection_success_printed = False
                connection_success_printed2 = False


def remove_first_18_lines(file_path):
    try:
        # 使用GBK编码读取文件
        with open(file_path, 'r', encoding='gbk') as file:
            lines = file.readlines()

        # 检查文件是否有足够的行数
        if len(lines) <= 18888:
            print(f"文件行数不足18888行，共有{len(lines)}行。")
            return False

        # 删除前18888行  相当于2M
        remaining_lines = lines[18888:]

        # 写回文件
        with open(file_path, 'w', encoding='gbk') as file:
            file.writelines(remaining_lines)

        print(f"已成功删除{file_path}的前18888行内容。")
        return True

    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}")
        return False
    except Exception as e:
        print(f"错误：处理文件时发生异常: {e}")
        return False


# 日志清理函数
def _async_log_clean(base_dir):
    try:
        # 指定文件夹路径
        folder_path = base_dir

        def get_folder_size(folder):
            """获取文件夹的总大小（字节）"""
            total_size = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except OSError:
                        print(f"无法获取文件 {file_path} 的大小")
            return total_size

        def clear_large_files(folder):
            """按修改时间倒序清空超过20MB的.log和.txt文件内容，跳过最新的前2个文件"""
            # 收集所有符合条件的文件及其修改时间
            log_txt_files = []

            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(('.log', '.txt')):
                        file_path = os.path.join(root, file)
                        try:
                            # 获取文件修改时间和大小
                            mtime = os.path.getmtime(file_path)
                            file_size = os.path.getsize(file_path)
                            log_txt_files.append((file_path, mtime, file_size))
                        except OSError as e:
                            print(f"无法处理文件 {file_path}: {e}")

            # 按修改时间倒序排序（从新到旧）
            log_txt_files.sort(key=lambda x: x[1], reverse=True)

            # 跳过最新的前2个文件
            files_to_process = log_txt_files[2:]

            print(f"找到 {len(log_txt_files)} 个符合条件的文件，跳过最新的2个，处理剩余的 {len(files_to_process)} 个文件")

            # 处理筛选后的文件
            for file_path, mtime, file_size in files_to_process:
                try:
                    # 再次检查文件大小（避免在排序期间文件被修改）
                    current_size = os.path.getsize(file_path)
                    if current_size > 18 * 1024 * 1024:  # 20MB
                        remove_first_18_lines(file_path)
                        print(f"已清空文件: {file_path} (修改时间: {time.ctime(mtime)})")
                except OSError as e:
                    print(f"无法处理文件 {file_path}: {e}")

        # 计算文件夹总大小
        folder_size = get_folder_size(folder_path)
        # print(f"文件夹总大小: {folder_size / (1024 * 1024):.2f} MB")

        # 如果总大小超过2GB，清空超过20MB的文件（按修改时间倒序，跳过最新的2个）
        if folder_size > 188 * 1024 * 1024:  # 200MB
            print("总大小超过2GB，开始按修改时间倒序清空超过20MB的文件（跳过最新的2个）...")
            clear_large_files(folder_path)
        else:
            pass

        logs = sorted(os.listdir(base_dir), key=lambda x: os.path.getmtime(os.path.join(base_dir, x)))
        while len(logs) > 18:
            cmd_on_color.printRed(f"删除{os.path.join(base_dir, logs.pop(0))}")
            try:
                os.remove(os.path.join(base_dir, logs.pop(0)))
            except:
                pass
    except Exception as e:
        pass


if __name__ == "__main__":
    pass
    # download_file("http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/goflyway_config.ini", "goflyway_config.ini")
    # download_file2(f"https://ghfile.geekertao.top/https://raw.githubusercontent.com/PuddinCat/BestClash/refs/heads/main/proxies.yaml", "clash2.yaml")
    # get_clash1()