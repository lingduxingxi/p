#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import subprocess
import time
# import time
import traceback

import psutil
import win32api
import win32con

# import time

# from tensorflow.python.distribute.mirrored_strategy import all_local_devices

import cmd_on_color
from GoflywayTools import start_GoflywayTools_exe
from SS1 import start_exe as start_SS1_exe
from SS2 import start_exe as start_SS2_exe
from SSR1 import start_exe as start_SSR1_exe
from SSR2 import start_exe as start_SSR2_exe
# from kill_all_pid_from_filenames_python_name_pid import kill_pid
from v2ray1 import start_exe as start_v2ray1_exe
from v2ray2 import start_exe as start_v2ray2_exe
from notification_simulator import show_notification

# from SS1 import get_config_informationurl, get_config


import sys
from datetime import datetime

import faulthandler
import threading
import sys
import time

# 启用 faulthandler（输出到 stdout，方便和 print 混在一起看）
faulthandler.enable(file=sys.stdout)

def run_with_timeout(func, timeout=18, *args, **kwargs):
    """
    运行某个函数，如果超过 timeout 秒没返回，就打印堆栈。
    """
    # 标记函数是否完成
    finished = threading.Event()

    def watchdog():
        if not finished.is_set():
            print(f"\n⚠️ 检测到函数超过 {timeout} 秒未返回，打印堆栈：")
            # faulthandler.dump_traceback(file=sys.stdout)

    timer = threading.Timer(timeout, watchdog)
    timer.start()

    try:
        result = func(*args, **kwargs)
    finally:
        finished.set()
        timer.cancel()

    return result


type_ = os.path.basename(__file__).replace('.py', '')
# open_Shadowsocks1 = os.getcwd() + fr'\{type_}\Shadowsocks1.exe'
# print('open_Shadowsocks128',open_Shadowsocks1)
pid = os.getpid()#当前进程的PID
# object_name = fr'{os.getcwd()}\{type_}'
object_name = fr'{os.getcwd()}'
isExists = os.path.exists(object_name)
# 判断结果
if not isExists:
    # 如果不存在则创建目录
    os.makedirs(object_name)
    print(object_name + ' 目录创建成功')


# 日志目录处理（使用快速路径操作）
object_name_output_log = os.path.join(object_name, f"{type_}_output_log")
os.makedirs(object_name_output_log, exist_ok=True)

# 定义文件夹路径
folder_path = os.getcwd() + f'/python_name_pid'
try:
    os.mkdir(folder_path)  # 创建文件夹
    print(f"文件夹 '{folder_path}' 创建成功！")
except FileExistsError:
    print(f"文件夹 '{folder_path}' 已存在！")
except Exception as e:
    print(f"创建文件夹失败: {e}")
with open(fr'{folder_path}\{type_}=》{pid}.txt', 'w+', encoding='utf-8') as f:
    f.write(f'{type_}=>{pid}')
    f.close()

# 全局异常捕获
def exception_hook(exctype, value, tb):

    error_msg = "".join(traceback.format_exception(exctype, value, tb))
    print(f"全局异常捕获:\n{error_msg}")
    log_filename = os.path.join(
        object_name_output_log,
        f"{type_}_global_err_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    with open(log_filename, "a") as f:
        f.write(error_msg + "\n")
    # sys.exit(1)


sys.excepthook = exception_hook




def kill_exe(exe_name):
    # exe_name = f"{type_}.exe"
    # exe_name_path = fr"{object_name}\{exe_name}"
    print(f'开始终止{exe_name}')
    n = 0
    p = ''
    while True:
        os.system(f"taskkill /F /IM {exe_name}")
        not_kill_list = []
        pids = psutil.pids()
        for pid in pids:
            try:
                p = psutil.Process(pid)
                if exe_name in p.name():
                    not_kill_list.append('未杀死！')
                    # os.system("taskkill /PID " + str(p.pid))
                    # os.system('taskkill /pid ' + str(p.pid) + ' /f')
                else:
                    pass
            except:
                pass

        if len(not_kill_list) != 0:
            cmd_on_color.printRed(f'终止{exe_name}失败！准备开始重新终止！')
            try:
                # os.system("taskkill /PID " + str(p.pid))
                # os.system('taskkill /pid ' + str(p.pid) + ' /f')
                os.system(f"taskkill /F /IM {exe_name}")
            except:
                traceback.print_exc()
                pass
        else:
            print(f'终止{exe_name}成功！')
            break

        time.sleep(2)
        if n >= 2:
            break
        n += 1


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
    返回 True 表示用户点击“是”，False 表示“否”。
    """
    result = win32api.MessageBox(
        None,
        question,
        "提示",
        win32con.MB_YESNO | win32con.MB_ICONQUESTION | win32con.MB_TOPMOST
    )
    return result == win32con.IDYES

object_name = fr'{os.getcwd()}'
all_local_port = 88
show_notification_n = 18  #循环18次后 才不提示消息
# show_notification_n = 2
show_notification_state = True
notification_tip = True
def run_all(state_all='所有'):
    global show_notification_state
    global notification_tip
    # 启动监控进程
    subprocess.Popen([sys.executable, "monitor.py", str(pid), f"{type_}"])

    n = 1
    while True:
        try:
            if n>=8:
                if notification_tip:
                    notification_tip = False
                    answer = ask_yes_no_question("通知过于频繁？是否需要关闭所有通知？")
                    if answer:
                        show_notification_state = False  # 关闭通知
            # os.system("taskkill /F /IM goflyway_all.exe")
            kill_exe('goflyway_all.exe')
            state_goflyway = start_GoflywayTools_exe(all_local_port,'所有',n,show_notification_state)
            kill_exe('goflyway_all.exe')
            # state_goflyway = f'不可以上网' #测试用

            print('state_goflyway13', state_goflyway)
            # time.sleep(88)
            if  f'不可以上网' in state_goflyway or f'不可知的异常' in state_goflyway:
                cmd_on_color.printRed(f"goflyway 不可以上网，准备更换SS1")
                if n<=show_notification_n:
                    show_notification(f"端口 8100 链接错误！\n准备更换端口为 10801", "不可以上网！","error")
                # os.system("taskkill /F /IM sslocal_all.exe")
                kill_exe('sslocal_all.exe')
                state_SS1 = start_SS1_exe(all_local_port,'所有',n,show_notification_state)
                kill_exe('sslocal_all.exe')
                # state_SS1 = f'不可以上网'  # 测试用
                print('182state_SS1', state_SS1)
                if '切换为端口8100' in state_SS1:
                    n+=1
                    continue
                if  f'不可以上网' in state_SS1 or f'不可知的异常' in state_SS1:
                    cmd_on_color.printRed(f"SS1不可以上网，准备更换SS2")
                    if n <= show_notification_n:
                        show_notification(f"端口 10801 链接错误！\n准备更换端口为 10802", "不可以上网！","error")
                    # os.system("taskkill /F /IM sslocal_all.exe")
                    kill_exe('sslocal_all.exe')
                    state_SS2 = start_SS2_exe(all_local_port, '所有',n,show_notification_state)
                    kill_exe('sslocal_all.exe')
                    # state_SS2 = f'不可以上网'  # 测试用
                    if  '切换为端口8100' in state_SS2:
                        n += 1
                        continue
                    if  f'不可以上网' in state_SS2 or f'不可知的异常' in state_SS2:
                        cmd_on_color.printRed(f"SS2不可以上网，准备更换SSR1")
                        if n <= show_notification_n:
                            show_notification(f"端口 10802 链接错误！\n准备更换端口为 10805", "不可以上网！","error")
                        # os.system("taskkill /F /IM ssrlocal_clash_all.exe")
                        kill_exe('ssrlocal_clash_all.exe')
                        state_SSR1 = start_SSR1_exe(all_local_port, '所有',n,show_notification_state)
                        kill_exe('ssrlocal_clash_all.exe')
                        if '切换为端口8100' in state_SSR1:
                            n += 1
                            continue
                        if  f'不可以上网' in state_SSR1 or f'不可知的异常' in state_SSR1:
                            cmd_on_color.printRed(f"SSR1 不可以上网，准备更换 SSR2")
                            if n <= show_notification_n:
                                show_notification(f"端口 10805 链接错误！\n准备更换端口为 10806", "不可以上网！", "error")
                            # os.system("taskkill /F /IM ssrlocal_clash_all.exe")
                            kill_exe('ssrlocal_clash_all.exe')
                            state_SSR2 = start_SSR2_exe(all_local_port, '所有',n,show_notification_state)
                            kill_exe('ssrlocal_clash_all.exe')
                            if '切换为端口8100' in state_SSR2:
                                n += 1
                                continue
                            if  f'不可以上网' in state_SSR2 or f'不可知的异常' in state_SSR2:
                                cmd_on_color.printRed(f"SSR2 不可以上网，准备更换 v2ray1")
                                if n <= show_notification_n:
                                    show_notification(f"端口 10806 链接错误！\n准备更换端口为 10822", "不可以上网！", "error")
                                # os.system("taskkill /F /IM v2ray_all.exe")
                                kill_exe('v2ray_all.exe')
                                state_v2ray1 = start_v2ray1_exe(all_local_port, '所有',n,show_notification_state)
                                kill_exe('v2ray_all.exe')
                                if '切换为端口8100' in state_v2ray1:
                                    n += 1
                                    continue
                                if f'不可以上网' in state_v2ray1 or f'不可知的异常' in state_v2ray1:
                                    cmd_on_color.printRed(f"v2ray1 不可以上网，准备更换 v2ray2")
                                    if n <= show_notification_n:
                                        show_notification(f"端口 10822 链接错误！\n准备更换端口为 10999", "不可以上网！", "error")
                                    # os.system("taskkill /F /IM v2ray_all.exe")
                                    kill_exe('v2ray_all.exe')
                                    state_v2ray2 = start_v2ray2_exe(all_local_port, '所有', n,show_notification_state)
                                    kill_exe('v2ray_all.exe')
                                    if '切换为端口8100' in state_v2ray2:
                                        n += 1
                                        continue
                                    if f'不可以上网' in state_v2ray2 or f'不可知的异常' in state_v2ray2:
                                        cmd_on_color.printRed(f"循环{n}次后，都不能上网，又开始使用端口 8100 进行下一个循环")
                                        if n <= show_notification_n:
                                            show_notification(f"循环{n}次后，都不能上网，又开始使用端口 8100 进行下一个循环", "不可以上网！", "error")
                                        states = f"{state_goflyway}、{state_SS1}、{state_SS2}、{state_SSR1}、{state_SSR2}、{state_v2ray1}、{state_v2ray2}"
                                        if '配置文件不存在' not in states:#配置文件存在
                                            if notification_tip:
                                                notification_tip = False
                                                answer = ask_yes_no_question("通知过于频繁？是否需要关闭所有通知？")
                                                if answer:
                                                    show_notification_state = False  # 关闭通知
                                        else:#配置文件不存在
                                            pass
        except Exception as err:
            try:
                # traceback.print_exc()
                # 获取堆栈跟踪信息的字符串
                error_msg = traceback.format_exc()

                # 将错误信息写入文件
                with open(f'{object_name_output_log}/{type_}_port_{all_local_port}serious_error_log.txt', 'w', encoding='utf-8') as f:
                    f.write(error_msg)
                if "can't encode character" in error_msg:
                    pass
                else:
                    win32api.MessageBox(None, f'严重错误:{err}，程序:{type_}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
            except Exception as err2:
                err_2 = str(err2)
                win32api.MessageBox(None, f'严重错误2:{err_2}，程序:{type_}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
                with open(f'{object_name_output_log}/{type_}_port_{all_local_port}serious_error2_log.txt', 'w', encoding='utf-8') as f:
                    f.write(f"严重错误2={err_2}")
def run_all_log(sys_state):
    # 调用，设定超时时间 5 秒
    run_with_timeout(run_all_log_timeout, timeout=5)
def run_all_log_timeout():
    # 确保目录存在
    os.makedirs(object_name_output_log, exist_ok=True)

    # 构建文件路径
    log_file = f"{object_name_output_log}/{type_}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_output_log.txt"

    class Logger:
        def __init__(self, log_file):
            self.terminal = sys.stdout
            self.log = open(log_file, "a", encoding="utf-8")

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)
            self.log.flush()  # 确保实时写入文件

        def flush(self):
            # 必须实现flush方法
            pass

    # 使用示例
    # if __name__ == "__main__":
    # 重定向输出到控制台和日志文件
    sys.stdout = Logger(log_file)
    run_all()

    # 可选：恢复标准输出
    # sys.stdout = sys.__stdout__


def delete_all_files_in_folder(folder_path):
    """
    删除指定文件夹内的所有文件（不删除子文件夹）

    Args:
        folder_path (str): 目标文件夹路径
    """
    with open(r'watchdog_stack.log', 'w+', encoding='utf-8') as f:
        f.write('')
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误：文件夹 '{folder_path}' 不存在！")
        return

    if not os.path.isdir(folder_path):
        print(f"错误：'{folder_path}' 不是一个有效的文件夹！")
        return

    # 遍历文件夹内的所有内容
    for file_name in os.listdir(folder_path):
        # 拼接完整的文件路径
        file_path = os.path.join(folder_path, file_name)

        # 只删除文件，跳过子文件夹
        if os.path.isfile(file_path):
            try:
                # 删除文件
                os.remove(file_path)
                print(f"成功删除文件：{file_path}")
            except Exception as e:
                print(f"删除文件失败 {file_path}：{str(e)}")
        else:
            print(f"跳过子文件夹：{file_path}")

if __name__ == "__main__":
    # 目标文件夹路径（注意路径中的反斜杠转义，也可以用原始字符串 r''）
    target_folder = r"D:\客户端集合代理\python_name_pid"

    # 执行删除操作
    delete_all_files_in_folder(target_folder)

    print("文件删除操作执行完毕！")
    # run_all('开机')  #开机 自动启动 88代理 ,代理不可用 后 自动切换其它代理   但不更新代理
    run_all_log('开机')  #开机 自动启动 88代理 ,代理不可用 后 自动切换其它代理   但不更新代理

