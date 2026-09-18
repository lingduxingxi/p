import os
import signal
import re
# import threading
# import time
import traceback
from pathlib import Path
from typing import Optional

import cmd_on_color
import psutil
import time
import concurrent.futures


def kill_process_by_name(process_name: str) -> None:
    """通过进程名终止所有匹配的进程"""
    terminated_pids = []
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            try:
                proc.terminate()  # 发送终止信号
                terminated_pids.append(proc.pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass  # 进程可能已关闭或权限不足
            except Exception:
                pass  # 忽略其他异常
    return process_name, terminated_pids


def wait_for_processes_to_die(process_names: list[str], timeout: int = 5) -> None:
    """等待进程终止，带超时机制"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        running_processes = {proc.info['name'] for proc in psutil.process_iter(['name'])}
        if not any(name in running_processes for name in process_names):
            return
        time.sleep(0.1)


def main2():


    print(f"正在查找并终止 {len(process_name_list)} 个进程...")

    # 使用线程池并行终止进程
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(kill_process_by_name, process_name_list))

    # 输出终止结果
    for name, pids in results:
        if pids:
            print(f"已终止 {name}: {pids}")

    # 等待所有进程终止
    wait_for_processes_to_die(process_name_list)

    # 检查是否有进程仍在运行
    remaining_processes = {}
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in process_name_list:
            remaining_processes[proc.info['name']] = proc.pid

    if remaining_processes:
        print("\n以下进程仍在运行，尝试强制终止:")
        for name, pid in remaining_processes.items():
            try:
                psutil.Process(pid).kill()  # 强制终止
                print(f"已强制终止 {name} (PID: {pid})")
            except Exception:
                print(f"无法终止 {name} (PID: {pid})")
    else:
        print("\n所有指定进程已成功终止")


def extract_pid_from_filename(filename: str) -> Optional[int]:
    """从文件名中提取PID"""
    match = re.search(r'=》(\d+)\.txt', filename)
    if match:
        return int(match.group(1))
    return None

def kill_processes_by_pid(pids: list[int]) -> None:
    """尝试杀死指定PID的进程"""
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
            cmd_on_color.printGre(f"已发送终止信号到进程 {pid}")
        except ProcessLookupError:
            cmd_on_color.printRed(f"错误: 进程 {pid} 不存在")
        except PermissionError:
            cmd_on_color.printRed(f"错误: 没有权限终止进程 {pid}")
        except Exception as e:
            cmd_on_color.printRed(f"错误: 终止进程 {pid} 时发生异常: {e}")

def kill_pid(all_ = '=》'):
    folder_path = Path('python_name_pid')
    
    # 检查文件夹是否存在
    if not folder_path.exists() or not folder_path.is_dir():
        cmd_on_color.printRed(f"错误: 文件夹 {folder_path} 不存在或不是目录")
        return
    
    # 提取所有PID
    pids = []
    for entry in folder_path.iterdir():
        if entry.is_file():
            if all_ in entry.name:
                pid = extract_pid_from_filename(entry.name)
                if pid is not None:
                    pids.append(pid)
    
    if not pids:
        cmd_on_color.printRed("未找到有效的PID")
        return
    
    print(f"找到 {len(pids)} 个PID: {pids}")
    kill_processes_by_pid(pids)
    # 确认是否杀死进程
    # confirm = input("确定要杀死这些进程吗？(y/n): ").strip().lower()
    # if confirm == 'y':
    #     kill_processes_by_pid(pids)
    #     print("进程终止操作已完成")
    # else:
    #     print("操作已取消")

def kill_process_by_name_old(process_name: str) -> None:
    """通过进程名终止所有匹配的进程"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            try:
                proc.terminate()  # 发送终止信号
                cmd_on_color.printGre(f"已发送终止信号到进程: {proc.info['name']} (PID: {proc.pid})")
            except psutil.NoSuchProcess:
                cmd_on_color.printRed(f"错误: 进程 (PID: {proc.pid}) 不存在")
            except psutil.AccessDenied:
                cmd_on_color.printRed(f"错误: 没有权限终止进程 (PID: {proc.pid})")
            except Exception as e:
                cmd_on_color.printRed(f"错误: 终止进程 (PID: {proc.pid}) 时发生异常: {e}")
        else:
            # cmd_on_color.printMag(f'未找到{process_name}进程')
            pass

def kill_exe(exe_name):
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
                if exe_name in p.name() :
                    not_kill_list.append('未杀死！')
                    #os.system("taskkill /PID " + str(p.pid))
                    #os.system('taskkill /pid ' + str(p.pid) + ' /f')
                else:
                    pass
            except:
                pass

        if len(not_kill_list) != 0:
            print(f'终止{exe_name}失败！准备开始重新终止！')
            try:
                #os.system("taskkill /PID " + str(p.pid))
                #os.system('taskkill /pid ' + str(p.pid) + ' /f')
                os.system(f"taskkill /F /IM {exe_name}")
            except:
                traceback.print_exc()
                pass
        else:
            cmd_on_color.printGre(f'终止{exe_name}成功！')
            break

        time.sleep(2)
        if n >= 2:
            break
        n += 1




if __name__ == "__main__":
    process_name_list = [
        "goflyway.exe", "goflyway_all.exe", "obfs-local.exe",
        "sslocal_all.exe", "sslocal_SS1.exe", "sslocal_SS2.exe",
        "ssrlocal_clash_all.exe", "ssrlocal_clash_SSR1.exe",
        "ssrlocal_clash_SSR2.exe", "tcping.exe", "v2ray1.exe",
        "v2ray_all.exe", "v2ray2.exe", "v2ray-plugin.exe"
    ]
    kill_pid('=》')#终止pid
    print('ok')
    # main2()#终止exe
    for process_name in process_name_list:
        os.system(f"taskkill /F /IM {process_name}")