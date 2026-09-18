import os
import time
from datetime import datetime
import subprocess

import psutil
import win32api
import win32con

pid = os.getpid()#当前进程的PID
type_ = os.path.basename(__file__).replace('.py', '')

# 定义文件夹路径
folder_path = os.getcwd() + r'\python_name_pid'
try:
    os.mkdir(folder_path)  # 创建文件夹
    print(f"文件夹 '{folder_path}' 创建成功！")
except FileExistsError:
    print(f"文件夹 '{folder_path}' 已存在！")
except Exception as e:
    print(f"创建文件夹失败: {e}")
with open(fr'{folder_path}\{type_}=》{pid}.txt', 'w+', encoding='utf-8') as f:
    f.write(f'{type_}=>{pid}')


def start_vbs(param):

    # 指定vbs文件路径
    vbs_path = param  # 根据实际情况修改路径

    try:
        # 使用subprocess启动vbs文件
        result = subprocess.run(
            ['cscript', '//nologo', vbs_path],
            capture_output=True,
            text=True,
            check=True
        )
        print("脚本执行成功！")
        print("输出:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"脚本执行失败: {e}")
        print("错误信息:", e.stderr)
    pass


def monitor_process(pid, program_name):
    pass
def monitor_process_old(pid, program_name):
    object_name = fr'{os.getcwd()}'
    type_ = os.path.basename(__file__).replace('.py', '')
    object_name_output_log = os.path.join(object_name, f"pid_err_{type_}_output_log")
    os.makedirs(object_name_output_log, exist_ok=True)
    log_file = f"{object_name_output_log}/pid_err_{type_}_{program_name}_crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    last_active = time.time()
    try:
        while True:
            if not psutil.pid_exists(pid):
                with open(log_file, "a") as f:
                    f.write(f"[{time.ctime()}] {program_name} (PID:{pid}) crashed unexpectedly\n")
                win32api.MessageBox(None, f'严重错误_PDI:{pid}，点击确定可重启程序继续运行，但还请务必检查！，程序:{program_name}，错误详细请查看{log_file}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
                if 'AI_all_auto' in program_name:
                    # start_vbs('AI_all_auto.vbs')
                    os.system('AI_all_auto.bat')
                break
            # 检查程序是否响应
            try:
                p = psutil.Process(pid)
                if p.status() == psutil.STATUS_ZOMBIE:
                    raise Exception("Process is zombie")
                last_active = time.time()
            except:
                # 处理无响应情况
                break

            if time.time() - last_active > 30:  # 30秒无响应视为卡死
                # 强制重启逻辑
                break
            time.sleep(5)  # 每5秒检查一次
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"[{time.ctime()}] Monitor error: {str(e)}\n")
        win32api.MessageBox(None, f'检查PDI是否存在的程序出错，错误原因:{e}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python monitor.py <PID> <ProgramName>")
        sys.exit(1)
    
    monitor_process(int(sys.argv[1]), sys.argv[2])