#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import subprocess
from DrissionPage import ChromiumPage, ChromiumOptions
import threading
from datetime import datetime
import win32con
from bs4 import BeautifulSoup
import win32api, os, time
import requests
import psutil
import traceback
from tqdm import tqdm
import logging
import cmd_on_color
from download_files import download_file
from notification_simulator import show_notification
from run_port_exe import run_exe
# from upload_node import upload

# url1 = "https://dgithub.xyz/Alvin9999/new-pac/wiki/Goflyway%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
# url1 = "https://bgithub.xyz/Alvin9999-newpac/fanqiang/wiki/Goflyway%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
url1 = "https://github.com/Alvin9999-newpac/fanqiang/wiki/Goflyway%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
url2 = "https://gitlab.com/zhifan999/fq/-/wikis/Goflyway%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
url3 = "https://s3.us-west-2.amazonaws.com/zhifan2/goflyway.html"

goflyway_exe = 'goflyway.exe'
pid = os.getpid()  # 当前进程的PID
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
    f.close()
proxy_port_list = [8100, 10801, 10802, 10805, 10806, 10888, 10822, 10899, 10999, 88, 0]
logging.captureWarnings(True)  # 强制取消证书验证警告
timeout = 99
##########################GoflywayTools代理更新
open_GoflywayTools = os.getcwd() + r'\goflyway.exe'
GoflywayTools_path = os.getcwd()
isExists = os.path.exists(GoflywayTools_path)
if not isExists:
    os.makedirs(GoflywayTools_path)

object_name_output_log = fr'./{type_}_output_log/'
isExists = os.path.exists(object_name_output_log)
# 判断结果
if not isExists:
    # 如果不存在则创建目录
    os.makedirs(object_name_output_log)
    print(object_name_output_log + ' 目录创建成功')

object_name = fr'{os.getcwd()}'
isExists = os.path.exists(object_name)
# 判断结果
if not isExists:
    # 如果不存在则创建目录
    os.makedirs(object_name)
    print(object_name + ' 目录创建成功')
exe_name_path = open_GoflywayTools

import sys


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


def config_GoflywayTools(IP, port, passwd, http, last_time, local_port):
    # config = '[BasisConfig]\nFile=..\Goflyway\goflyway.exe\nOther Parameters=\nProxy Mode=0\nLocal port=8100\nWeb port=8101\nRun=true\n[NodeList]\nNum=1\nSelect node=0\n[MoreSettings]\nTest URL=https://www.google.com\nTimeout=10\nLog level=3\n[Node]\nNode1=45.76.175.114 12345 dongtaiwang.com 0 外星世界'
    config = r'''[BasisConfig]
File=..\Goflyway\goflyway.exe
Other Parameters=
Proxy Mode=0
Local port={4}
Web port=8101
Run=true
[NodeList]
Num=1
Select node=0
[MoreSettings]
Test URL=https://www.google.com
Timeout=10
Log level=3
[Node]
Node1={0} {1} {2} 0 UFO
'''.format(IP, port, passwd, http, local_port)
    # print(config)
    # time.sleep(999)
    return config


def kill_GoflywayTools_exe(goflyway_exe='goflyway.exe'):
    print(f'开始终止{goflyway_exe}')
    n = 0
    while True:
        os.system(f"taskkill /F /IM {goflyway_exe}")
        not_kill_list = []
        pids = psutil.pids()
        for pid in pids:
            try:
                p = psutil.Process(pid)
                if 'goflyway' in p.name() or 'GoflywayTools' in p.name():
                    not_kill_list.append('未杀死！')
                else:
                    pass
            except:
                pass

        if len(not_kill_list) != 0:
            print('终止GoflywayTools失败！准备开始重新终止！')
            os.system(f"taskkill /F /IM {goflyway_exe}")
        else:
            print('终止GoflywayTools成功！')
            break

        time.sleep(2)
        if n > 9:
            break
        n += 1


port88_err_num = 1


def start_GoflywayTools_exe(local_port=8100, run_type='单独', err_node_number=1, show_notification_state=True):
    global port88_err_num
    if run_type == '所有':
        goflyway_exe = f"goflyway_all.exe"
    else:
        goflyway_exe = f"goflyway.exe"
    exe_name_path = fr"{object_name}\{goflyway_exe}"
    print(f'开始启动{goflyway_exe}')

    success = ''
    # print('open_GoflywayTools82',open_GoflywayTools)
    # time.sleep(8)
    # win32api.ShellExecute(0, 'open', open_GoflywayTools, '', '', 1)
    # state_goflyway = run_goflyway(all_local_port,run_type,goflyway_exe)
    # if '表示子进程已经终止' in state_goflyway:
    #     today_num = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    #     cmd_on_color.printRed(f"{today_num} 程序被杀死，准备重启！105")
    #     state_goflyway = start_GoflywayTools_exe(all_local_port,goflyway_exe)
    # result = subprocess.run(['cscript', f'{GoflywayTools_path}/goflyway_exe_run.vbs'], capture_output=True, text=True, check=True)
    # print("goflyway_exe_run.vbs 执行完成，其输出信息如下：")
    # print(result.stdout)
    file_path = GoflywayTools_path + r'\goflyway_config.ini'  # 替换为实际文件路径
    state = f'不可以上网'
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            print(f"文件 '{file_path}' 存在")
            # state = run_goflyway(all_local_port, run_type,goflyway_exe)
            server_address, port, password, err_ = read_config()
            if err_ == '没有配置参数':
                state = f'不可以上网'
            else:
                # cmd = r'goflyway.exe -up="163.172.120.27:26677" -k="dongtaiwang.co" -l=":88" -lv=info -t=8 -mux=2' # local_port=88 or 8100
                # cmd = f'{goflyway_exe} -up="{server_address}:{port}" -k="{password}" -l=":{local_port}" -lv=dbg0 -t=30 -mux=2' # dbg0（最高详细级别日志）
                cmd = f'{exe_name_path} -up="{server_address}:{port}" -k="{password}" -l=":{local_port}" -lv=dbg0 -t=8 -mux=2'  # dbg0（最高详细级别日志）
                state = str(run_exe(local_port, run_type, cmd, object_name_output_log, type_, goflyway_exe, object_name, exe_name_path, err_node_number, show_notification_state))
                if '表示子进程已经终止' in state or '端口冲突' in state:
                    port88_err_num += 1
                    print('port88_err_num177', port88_err_num)
                    if port88_err_num < 8:
                        today_num = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                        if '表示子进程已经终止' in state:
                            cmd_on_color.printRed(f"{today_num} 程序{goflyway_exe}被杀死，准备重启！")
                        if '端口冲突' in state:
                            kill_GoflywayTools_exe(goflyway_exe)
                            cmd_on_color.printRed(f"{today_num} 端口{local_port}冲突，准备重启！")
                        state = start_GoflywayTools_exe(local_port, run_type, err_node_number)
                    else:
                        state = f'不可以上网，似乎{type_}程序在进行测速'
                        port88_err_num = 1

        else:
            print(f"'{file_path}' 存在，但不是文件")
    else:
        print(f"文件 '{file_path}' 不存在")
        state = f'不可以上网，配置文件不存在'
    if f'不可以上网' in state or f'不可知的异常' in state:
        # os.system("taskkill /F /IM goflyway.exe")

        pass
    return state


def download_file_state(fname: str, url: str, proxy_port: str):
    print('测速下载图片的地址为：' + str(url))
    print('测速下载本地的路径为：' + str(fname))
    n = 0

    while True:
        err = ''
        try:
            # 用流stream的方式获取url的数据
            proxy_port = str(proxy_port)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}
            print('走代理下载中……端口：' + proxy_port)
            proxies = {"http": "socks5h://127.0.0.1:" + str(proxy_port), "https": "socks5h://127.0.0.1:" + str(proxy_port)}
            resp = requests.get(url, stream=True, timeout=29, headers=headers, proxies=proxies, verify=False)
            # 拿到文件的长度，并把total初始化为0
            total = int(resp.headers.get('content-length', 0))
            # 打开当前目录的fname文件(名字你来传入)
            # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
            bar_list = []
            with open(fname, 'wb') as file, tqdm(
                    desc=fname,
                    total=total,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
            ) as bar:
                for i, data in enumerate(resp.iter_content(chunk_size=1024)):  # chunk_size=8192#chunk_size=1024
                    size = file.write(data)
                    bar.update(size)
            break
        except Exception as e:
            print(e)  # timed out  #port=443
            # traceback.print_exc()
            err = '下载错误'
            print('下载错误！2秒后重试！')
            n += 1
            pass
        if n >= 2:
            # if n > 1 :#test
            break
        time.sleep(2)
    return err


def Drission_get_Page(url='https://scitechdaily.com/news/space/', max_retries=3):
    """获取页面内容，带重试机制"""

    for attempt in range(max_retries):
        page = None
        try:
            print(f"尝试获取页面 {attempt + 1}/{max_retries}: {url}")

            co = ChromiumOptions()
            # 关键参数
            co.set_argument('--app=data:,')
            co.set_argument('--disable-blink-features=AutomationControlled')
            co.set_argument('--window-position=-32000,-32000')

            # 添加更多稳定性参数
            co.set_argument('--disable-background-timer-throttling')
            co.set_argument('--disable-backgrounding-occluded-windows')
            co.set_argument('--disable-renderer-backgrounding')

            # 伪装 webdriver
            co.set_user_agent(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/122.0.0.0 Safari/537.36'
            )

            # 可选：关闭图片加载（更快）
            co.set_argument('--disable-images')

            page = ChromiumPage(co)

            # 访问页面
            page.get(url)

            # 正确的等待方法
            time.sleep(3)  # 基础等待
            page.wait.doc_loaded()  # 等待文档加载完成

            # 等待页面稳定（检查是否有内容）
            for _ in range(5):  # 最多等待5秒
                time.sleep(1)
                if page.html and len(page.html) > 500:
                    break

            # 获取HTML
            html = page.html

            # 验证HTML内容
            if html and len(html) > 100:
                print(f"成功获取页面，长度: {len(html)} 字符")
                return html
            else:
                print(f"获取的HTML内容过短: {len(html) if html else 0}")
                raise Exception("HTML内容无效")

        except Exception as e:
            print(f"尝试 {attempt + 1} 失败: {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                print("所有重试均失败")
                raise
        finally:
            if page:
                try:
                    page.quit()
                except:
                    pass

    return None


def get_config_information(local_port):
    IP = passwd = http = last_time = port = ''
    cmd_on_color.printCya('++++++++++++++++++++++++++++++++更新GoflywayTools配置中，请耐心等待............++++++++++++++++++++++++++++++++')

    html = ''
    webpage = ''
    link_url1_successful = ''
    link_url2_successful = ''
    link_url3_successful = ''
    n = 0
    headers = {"accept": "text/fragment+html", "accept-encoding": "gzip, deflate, br", "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6", "cache-control": "no-cache",
               "cookie": "_octo=GH1.1.1758989851.1648175506; logged_in=no; _device_id=b40a09d7ac237ca5865586e568e48c37; _gh_sess=PEtZgdLYYIZ%2FLPlo9ttBoDAonIJ%2B1rR3OdNKLczOAEFCTmiVXUm7dwJl6PtLuDGNWGD572PnqCw%2BN7mr3IMKNh79dnMVnjRoW6%2BBXEJHAHLNT4d7bAJ6TixdZqzi7DPIEQvZbkTd8NcXQ4zwWt62IcXBzPIoZjQvF4lwkRaTR5bL3khjZsiJWWMAqo5yg93b%2BPvWUvbpk2G1u8HcBATJoG8J2yQChArcPy42g6RZjWcz6y6fxnE%2Fo7LqOnhRPcibtRMdzbqjPF%2BozCglBof3cg%3D%3D--jrVlTPQrlvBbGQNx--76eLAMtsJL8KZIqufSYcuQ%3D%3D; tz=Asia%2FShanghai",
               "pragma": "no-cache", "referer": "https://github.com/Alvin9999/new-pac/wiki/Goflyway%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7",
               "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Microsoft Edge\";v=\"101\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-dest": "empty",
               "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39", "x-requested-with": "XMLHttpRequest"}
    # for proxy_ports in proxy_port_list:
    #     # if int(proxy_port) == proxy_ports :#指定代理
    #     # print('走代理,IP:', proxy_ports)
    #     proxies = {"http": "socks5h://127.0.0.1:" + str(proxy_ports), "https": "socks5h://127.0.0.1:" + str(proxy_ports)}
    np2 = 0
    #     np3 = 0
    while True:
        try:
            while True:
                print(f'使用连接1{url1}进行更新！')
                try:
                    # req = urllib.request.Request(url1)
                    # webpage = urllib.request.urlopen(req)
                    # proxies = None
                    if n > 2:
                        print('使用AI_all_auto代理88')
                        proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
                        webpage = requests.get(url1, headers=headers, timeout=8, proxies=proxies)
                    else:
                        print('不使用代理')
                        webpage = requests.get(url1, headers=headers, timeout=8)

                    if webpage.status_code == 200:
                        link_url1_successful = '连接1成功！'
                        print('291link_url1_successful',link_url1_successful)
                        html = webpage.content
                        break

                except Exception as err:
                    print(err)
                    print('连接1错误，2秒后重试！')
                    time.sleep(2)
                # print(n)
                if n >= 8:
                    break
                n += 1
            if link_url1_successful != '连接1成功！':
                n2 = 0
                print(f'连接{url1}失败，开始使用连接2{url2}更新！')
                while True:
                    try:
                        # req = urllib.request.Request(url2)
                        if n > 2:
                            print('使用AI_all_auto代理88')
                            proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
                            webpage = requests.get(url2, headers=headers, timeout=8, proxies=proxies)
                        else:
                            print('不使用代理')
                            webpage = requests.get(url2, headers=headers, timeout=8)
                        #
                        if webpage.status_code == 200:
                            link_url2_successful = '连接2成功！'
                            print(link_url2_successful)
                            html = webpage.content
                            break
                        # html = Drission_get_Page(url2)
                        # if html:
                        #     link_url2_successful = '连接2成功！'
                        #     print(link_url2_successful)
                        #     break
                    except Exception as err:
                        print(f'连接2{url2}错误，2秒后重试！==>>{err}')
                        time.sleep(2)
                    if n2 >= 8:
                        break
                    n2 += 1
                if link_url2_successful != '连接2成功！':
                    n3 = 0
                    print(f'连接12都失败，开始使用连接3{url3}更新！')
                    while True:
                        try:
                            # req = urllib.request.Request(url3)
                            if n3 > 2:
                                print('使用AI_all_auto代理88')
                                proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
                                webpage = requests.get(url3, headers=headers, timeout=8, proxies=proxies)
                            else:
                                print('不使用代理')
                                webpage = requests.get(url3, headers=headers, timeout=8)
                            if webpage.status_code == 200:
                                link_url3_successful = '连接3成功！'
                                print(link_url3_successful)
                                html = webpage.content
                                break

                        except Exception as err:
                            print('连接3错误，2秒后重试！')
                            time.sleep(2)
                        if n3 >= 8:
                            break
                        n3 += 1
                    if link_url3_successful != '连接3成功！':
                        print('连接123都失败，请使用其它代理！')
                    else:
                        print('连接3成功，准备更新！')
                else:
                    print('连接2成功，准备更新！')
            else:
                print('连接1成功，准备更新！')
            # print('webpage356',webpage)

            # 读取页面内容
            # html = webpage.read()

            # print(html)
            # 解析成文档对象
            print('解析成文档对象')
            soup = BeautifulSoup(html, 'html.parser')  # 文档对象
            # print(soup.encode('gbk', 'ignore').decode('gbk'))
            print('成功解析文档对象')

            # filepath = os.getcwd() + r'\Goflyway\\'
            # isExists = os.path.exists(filepath)
            # if not isExists:
            #     os.makedirs(filepath)
            # filepath_goflyway_txt = filepath + 'all_configure_goflyway.txt'
            IP, port, passwd, http, last_time = soup_text(soup)
            if IP != '':
                config = config_GoflywayTools(IP, port, passwd, http, last_time, local_port)
                print('config257', config)
                # time.sleep(88)
                return config
            break
        except:
            pass
        if np2 >= 88:
            win32api.MessageBox(None, '是断网了吗？，请检查！', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
            break
        np2 += 1


def main_proxy(local_port=8100):
    download_file("http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/goflyway_config.ini", "goflyway_config.ini")
    time.sleep(2)

    # 启动监控进程
    subprocess.Popen([sys.executable, "monitor.py", str(pid), f"{type_}"])
    kill_GoflywayTools_exe()
    port8100_success = os.path.join(fr'{os.getcwd()}\GoflywayTools_output_log', f'GoflywayTools_success_port8100.txt')
    with open(port8100_success, 'w') as f:
        f.write("")
    cmd_on_color.printCya('++++++++++++++++++++++++++++++++启动GoflywayTools中，请耐心等待............++++++++++++++++++++++++++++++++')
    n = 0
    while True:
        try:
            state_ = start_GoflywayTools_exe(err_node_number=n + 1)
            print('state_goflyway322', state_,n)
            # break
            ######state = f'有一个在运行，不能同时运行2个'
            if f'不可以上网' in state_ or f'不可知的异常' in state_:
                os.system("taskkill /F /IM goflyway.exe")
                if n <= 2:
                    show_notification(f"端口 {local_port} 链接错误！准备更新配置", f"不可以上网！【第{n + 1}次检测)】", "error")
                print('代理错误，疑似代理或IP配置有错误？开始重新获取最新IP配置==GoflywayTools')
                config = get_config_information(local_port)
                if config:
                    with open(GoflywayTools_path + r'\goflyway_config.ini', 'w+', encoding='utf-8') as f:
                        f.write(str(config))
                    # upload("goflyway_config.ini")
                    cmd_on_color.printGre('GoflywayTools配置成功！')
                print('开始杀死进程goflyway.exe')
                kill_GoflywayTools_exe()
            if state_ == f'有一个在运行，不能同时运行2个':
                def popup():
                    win32api.MessageBox(None, '有一个在运行，不能同时运行2个goflyway.exe', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)

                threading.Thread(target=popup).start()

                break
            if n > 18:
                n = 0
                download_file("http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/goflyway_config.ini", "goflyway_config.ini")
                time.sleep(2)

                # time.sleep(88)
                pass
                # def popup():
                #     win32api.MessageBox(None, f'端口{local_port}最终不能上网，请更换其它端口', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
                # threading.Thread(target=popup).start()
                # break

        except Exception as err:
            traceback.print_exc()
            # 获取堆栈跟踪信息的字符串
            error_msg = traceback.format_exc()

            # 将错误信息写入文件
            with open(f'{object_name_output_log}/{type_}_serious_error_log.txt', 'w', encoding='utf-8') as f:
                f.write(error_msg)
            if "can't encode character" in error_msg:
                pass
            else:
                win32api.MessageBox(None, f'严重错误:{err}，程序:{type_}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
        n += 1


def GoflywayTools_old(local_port=8100):
    cmd_on_color.printCya('++++++++++++++++++++++++++++++++启动GoflywayTools中，请耐心等待............++++++++++++++++++++++++++++++++')
    state_goflyway = start_GoflywayTools_exe()
    # os.system("taskkill /F /IM goflyway.exe")#终止进程
    # os.system("taskkill /F /IM goflyway.exe")
    # time.sleep(2)
    # kill_GoflywayTools_exe()# 终止进程
    # open_Goflyway = GoflywayTools_path + '\goflyway.exe'#启动进程
    # win32api.ShellExecute(0, 'open', open_Goflyway, '', '', 1)
    # print('终止进程GoflywayTools成功！')

    # print(IP, port, passwd, http, last_time)
    # all_configure = str((IP, port, passwd, http, last_time))
    # print(all__configure)
    #
    # list_data = ''
    # try:
    #     with open(filepath_goflyway_txt, 'r+', encoding='utf-8') as f:
    #         list_data = f.read()
    #     f.close()
    # except:
    #     with open(filepath_goflyway_txt, 'a+', encoding='utf-8') as f:
    #         f.write('')
    #     f.close()
    #
    # repead = list_data.find(all_configure)
    # if repead == -1:
    #     print('有配置更新，开始更新')
    #     config_GoflywayTools(IP, port, passwd, http, last_time)
    #     with open(filepath_goflyway_txt, 'w+', encoding='utf-8') as f:
    #         f.write(str(all_configure))
    #     f.close()
    #     print('开始杀死进程goflyway.exe')
    #     kill_GoflywayTools_exe()
    #     print('开始启动进程goflyway.exe')
    #     start_GoflywayTools_exe()
    # else :
    # print('配置未更新！开始检查进程goflyway.exe是否正常打开？')
    state_goflyway = ''
    average_speed = ''
    print('开始检查进程goflyway.exe是否正常打开？')
    pids = psutil.pids()
    p_name_list = []
    p = ''
    for pid in pids:
        try:
            p = psutil.Process(pid)
        except:
            # traceback.print_exc()
            pass
        # print(p.name())
        p_name_list.append(p.name())
        # print('pid-%s,pname-%s' % (pid, p.name()))
    p_name_all = ','.join(p_name_list)
    # if 'goflyway.exe' in p_name_all:
    if 'goflyway.exe' in p_name_all:
        print('进程goflyway.exe，已经启动！无需再次启动！')
    else:
        print('进程goflyway.exe，未启动！再次开始启动！')
        state_goflyway = start_GoflywayTools_exe()
        # time.sleep(2)
    print('开始检查代理是否可以上网')
    n = 0
    while True:
        # print(n)
        # import download_files
        # state,average_speed = download_files.download_file_state('https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif', os.getcwd() + r"\test_speed.gif", local_port)
        # if state == '下载失败' or state_goflyway == f'不可以上网' or f'不可知的异常' in state_goflyway:
        if state_goflyway == f'不可以上网' or f'不可知的异常' in state_goflyway:
            print('代理错误，疑似代理或IP配置有错误？开始重新获取最新IP配置==GoflywayTools')
            # config = get_config_information(local_port)
            # with open(GoflywayTools_path + r'\goflyway_config.ini', 'w+', encoding='utf-8') as f:
            #     f.write(str(config))

            print('配置成功！')
            print('开始杀死进程goflyway.exe')
            kill_GoflywayTools_exe()
            print('开始启动进程goflyway.exe')
            state_goflyway = start_GoflywayTools_exe()

        else:
            status = '可以上网'
            status = cmd_on_color.printGre(status)
            cmd_on_color.printGre('此代理可以上网！端口为===============》》》》》》》》》》》》》》》》》》》：8100【GoflywayTools】')
            with open(GoflywayTools_path + r'\goflyway_status.txt', 'w+', encoding='utf-8') as f:
                f.write(str(status))
            # break
        if n >= 2:
            status = '不可上网'
            status = cmd_on_color.printRed(status)
            cmd_on_color.printRed('8100【GoflywayTools】此代理最终不可以上网！请更换下一个代理！')
            if local_port == 88:  # 检查AI_all_auto 全部的 才跳出去  然后进行下一个代理模式
                break
                pass
        n += 1
    return status, average_speed


def soup_text(soup):
    IP = port = passwd = http = last_time = ''
    ks_list = []
    td_list = []
    # for i,ks in enumerate(soup.find_all('div',class_ = 'highlight highlight-source-shell notranslate position-relative overflow-auto')):
    # ks_list = ks.text.split('</pre></div>')[0]
    for i, ks in enumerate(soup.find_all('table')):
        if '端口' in str(ks):
            td_list = ks.find_all('td')
            print('td_list359', td_list)
            # [<td>IP</td>, <td>38.114.103.196</td>, <td>端口</td>, <td>12345</td>, <td>密码</td>, <td>dongtaiwang.com</td>, <td>客户端协议</td>, <td>HTTP</td>]
            # ks_list = ks.text.split('</pre></div>')[0]
            # print(i,'===========')
            # print(ks_list)
        # break
    for i, parameter in enumerate(td_list):
        if i == 1:
            IP = parameter.text
        if i == 3:
            port = parameter.text
        if i == 5:
            passwd = parameter.text
        if i == 7:
            http = parameter.text
        print('parameter367', parameter)
    print('parameter377', IP, port, passwd, http, last_time)
    # time.sleep(899)
    for i, ks in enumerate(soup.find_all('div', class_='highlight highlight-source-shell notranslate position-relative overflow-auto')):
        ks_list = ks.text.split('</pre></div>')[0]
    for k in str(ks_list).split('\n\n'):
        #     if 'IP：' in str(k) :
        #         IP = str(k).replace('<p>','').replace('</p>','').replace('IP：','')
        #         print(IP)
        #     if '端口：' in str(k) :
        #         port = str(k).replace('<p>','').replace('</p>','').replace('端口：','')
        #         print(port)
        #     if '密码：' in str(k) :
        #         passwd = str(k).replace('<p>','').replace('</p>','').replace('密码：','')
        #         print(passwd)
        #     if '客户端协议：' in str(k) :
        #         http = str(k).replace('<p>','').replace('</p>','').replace('客户端协议：','')
        #         print(http)
        if '北京时间' in str(k):
            last_time = str(k).replace('<p>', '').replace('</p>', '').replace('<strong>', '').replace('</strong>', '').split('。')[0]
    # passwd = '123'#测试
    print(IP, port, passwd, http, last_time)
    # time.sleep(899)
    return IP, port, passwd, http, last_time


def read_config():
    with open(GoflywayTools_path + r'\goflyway_config.ini', "r+") as f:
        config_text = f.read()
    # print(config_text)
    pattern = r'Node1=(\S+) (\S+) (\S+)'
    match = re.search(pattern, config_text)
    server_address = port = password = ''
    if match:
        server_address = match.group(1)
        port = match.group(2)
        password = match.group(3)
        print(f"服务器地址: {server_address}")
        print(f"端口: {port}")
        print(f"密码: {password}")
        err_ = '有配置参数'
    else:
        print("未找到匹配的信息。")
        err_ = '没有配置参数'
    return server_address, port, password, err_


def check_proxy_connection(local_port):
    '''

    11111111111111
    output.strip()480 连接成功 2025-05-09 13:20:25.704 CST,main.go:267, INFO ,goflyway 181021015134
    output.strip()480 连接成功 2025-05-09 13:20:25.722 CST,main.go:272, INFO ,TCP multiplexer: 2 masters
    output.strip()480 连接成功 2025-05-09 13:20:25.729 CST,main.go:278, WARNING ,Failed to read ACL config: open chinalist.txt: The system cannot find the file specified.
    output.strip()480 连接成功 2025-05-09 13:20:25.730 CST,main.go:436, INFO ,Upstream config: 163.172.120.27:26677
    output.strip()480 连接成功 2025-05-09 13:20:25.730 CST,main.go:416, INFO ,Client b76c393 started: you->0.0.0.0:88->163.172.120.27:26677
    output.strip()480 连接成功 2025-05-09 13:20:25.730 CST,main.go:412, INFO ,Web console started at 127.0.0.1:98


    22222222222222
    output.strip()480 连接失败 2025-05-09 13:16:57.695 CST,main.go:267, INFO ,goflyway 181021015134
    output.strip()480 连接失败 2025-05-09 13:16:57.715 CST,main.go:272, INFO ,TCP multiplexer: 2 masters
    output.strip()480 连接失败 2025-05-09 13:16:57.721 CST,main.go:278, WARNING ,Failed to read ACL config: open chinalist.txt: The system cannot find the file specified.
    output.strip()480 连接失败 2025-05-09 13:16:57.722 CST,main.go:436, INFO ,Upstream config: 163.172.120.22:26677
    output.strip()480 连接失败 2025-05-09 13:16:57.722 CST,main.go:416, INFO ,Client b76c393 started: you->0.0.0.0:88->163.172.120.22:26677
    output.strip()480 连接失败 2025-05-09 13:16:57.722 CST,main.go:412, INFO ,Web console started at 127.0.0.1:98
    output.strip()480 连接失败 2025-05-09 13:17:40.254 CST,client.go:394, ERROR ,"Dial failed: dial 163.172.120.22:26677, Connection timed out"
    不可以上网
    goflyway 已正常退出
    进程已结束

    333333333333
    output.strip()480 连接失败 2025-05-09 13:20:25.704 CST,main.go:267, INFO ,goflyway 181021015134
    output.strip()480 连接失败 2025-05-09 13:20:25.722 CST,main.go:272, INFO ,TCP multiplexer: 2 masters
    output.strip()480 连接成功 2025-05-09 13:20:25.729 CST,main.go:278, WARNING ,Failed to read ACL config: open chinalist.txt: The system cannot find the file specified.
    output.strip()480 连接成功 2025-05-09 13:20:25.730 CST,main.go:436, INFO ,Upstream config: 163.172.120.27:26677
    output.strip()480 连接成功 2025-05-09 13:20:25.730 CST,main.go:416, INFO ,Client b76c393 started: you->0.0.0.0:88->163.172.120.27:26677
    output.strip()480 连接成功 2025-05-09 13:20:25.730 CST,main.go:412, INFO ,Web console started at 127.0.0.1:98



    :param local_port:
    :return:
    '''

    state_url_list = []
    proxy = {
        'http': f'http://127.0.0.1:{local_port}',
        'https': f'http://127.0.0.1:{local_port}'
    }
    test_url = "https://www.google.com"

    # while True:
    try:
        start_time = time.time()
        response = requests.get(test_url, proxies=proxy, timeout=8)
        elapsed = (time.time() - start_time) * 1000  # 毫秒

        if response.status_code == 200:
            state = '连接成功'
            # print(f"[{time.strftime('%H:%M:%S')}] ✅ 连接成功 | 状态码: {response.status_code} | 延迟: {elapsed:.0f}ms")
        else:
            # print(f"[{time.strftime('%H:%M:%S')}] ⚠️ 连接异常 | 状态码: {response.status_code}")
            state = '连接异常'
    except requests.exceptions.RequestException as e:
        # print(f"[{time.strftime('%H:%M:%S')}] ❌ 连接失败: {str(e)}")
        state = '连接失败'
    # time.sleep(2)  # 每2秒检查一次
    return state, state_url_list


def run_goflyway_old():
    # kill_GoflywayTools_exe()
    server_address, port, password, err_ = read_config()
    # cmd = r'D:\客户端集合代理\Goflyway\goflyway.exe -up="163.172.120.27:26677" -k="dongtaiwang.com" -l=":8100"'
    # cmd = r'goflyway.exe -up="163.172.120.27:26677" -k="dongtaiwang.com" -l=":8100"'
    cmd = f'goflyway.exe -up="{server_address}:{port}" -k="{password}" -l=":8100"'
    object_name = fr'./{type_}_output_log/'
    isExists = os.path.exists(object_name)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(object_name)
        print(object_name + ' 目录创建成功')
    # 生成带时间戳的日志文件名
    log_filename = f"{object_name}/goflyway_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # 首先将命令本身写入日志文件
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(f"执行的命令: {cmd}\n\n")
        log_file.flush()  # 立即写入文件

        try:
            print("正在启动 goflyway...")
            log_file.write("正在启动 goflyway...\n")

            # 启动进程并实时捕获输出
            process = subprocess.Popen(cmd, shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       text=True,
                                       encoding='utf-8',
                                       errors='replace')

            # 实时读取输出并写入文件和打印到控制台
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print('output.strip()480', output.strip())
                    # if 'ERROR ,"Dial failed' in output.strip():
                    #     cmd_on_color.printRed(f'不可以上网！')
                    #     log_file.write(f'不可以上网！')
                    #     log_file.flush()  # 确保每次写入后立即保存到文件
                    #     break
                    log_file.write(output)
                    log_file.flush()  # 确保每次写入后立即保存到文件
                # 删除多余的log
                log_list = os.listdir(object_name)
                for i, log_name in enumerate(log_list):
                    if len(log_list) > 18:
                        # if len(log_list) > 3:  # 测试
                        if i < 18:  # 删除前29个
                            # if i < 2:  # 测试
                            print(f'开始删除log==>>{object_name}/{log_name}')
                            log_file.write(f'开始删除log==>>{object_name}/{log_name}')
                            try:
                                os.remove(f'{object_name}/{log_name}')
                            except:
                                traceback.print_exc()
            print("goflyway 已正常退出")
            log_file.write("goflyway 已正常退出\n")

        except KeyboardInterrupt:
            print("\n用户手动终止 (Ctrl+C)")
            log_file.write("\n用户手动终止 (Ctrl+C)\n")
        except Exception as e:
            # with open(log_filename, 'a', encoding='utf-8') as file:
            #     # 将错误信息写入文件
            #     traceback.print_exc(file=file)
            print(f"程序异常终止: {e}")
            log_file.write(f"程序异常终止: {e}\n")
        finally:
            print("进程已结束")
            log_file.write("进程已结束\n")
            log_file.write(f"\n日志结束时间: {datetime.now()}\n")


def run_goflyway(local_port, run_type, goflyway_exe):
    state = ''
    # kill_GoflywayTools_exe()
    server_address, port, password, err_ = read_config()
    # cmd = r'goflyway.exe -up="163.172.120.27:26677" -k="dongtaiwang.co" -l=":88" -lv=info -t=8 -mux=2'
    cmd = f'{goflyway_exe} -up="{server_address}:{port}" -k="{password}" -l=":{local_port}" -lv=info -t=8 -mux=2'  # local_port=88 or 8100
    print('cmd582', cmd)
    object_name = fr'./{type_}_output_log/'
    isExists = os.path.exists(object_name)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(object_name)
        print(object_name + ' 目录创建成功')
    # 生成带时间戳的日志文件名
    log_filename = f"{object_name}/goflyway_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # 首先将命令本身写入日志文件
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(f"执行的命令: {cmd}\n\n")
        log_file.flush()  # 立即写入文件

        try:
            print("正在启动 goflyway...")
            log_file.write("正在启动 goflyway...\n")

            # 启动进程并实时捕获输出
            process = subprocess.Popen(cmd, shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       text=True,
                                       encoding='utf-8',
                                       errors='replace')
            n = 0
            while True:
                pids = psutil.pids()
                start_list = []
                for pid in pids:
                    try:
                        p = psutil.Process(pid)
                        # if 'GoflywayTools' in p.name():
                        if 'goflyway' in p.name():
                            start_list.append('未杀死！')
                            pass
                        else:
                            pass
                    except:
                        pass

                # my_file = Path(open_GoflywayTools)
                if len(start_list) != 0:
                    success = '启动GoflywayTools成功'
                    print('启动GoflywayTools成功！')

                    break
                else:
                    print('启动GoflywayTools失败！准备开始重启！')
                    # win32api.ShellExecute(0, 'open', open_GoflywayTools, '', '', 0)
                    state = run_goflyway(local_port, run_type, goflyway_exe)
                    # result = subprocess.run(['cscript', f'{GoflywayTools_path}/goflyway_exe_run.vbs'], capture_output=True, text=True, check=True)
                    # print("goflyway_exe_run.vbs 执行完成，其输出信息如下：")
                    # print(result.stdout)
                time.sleep(2)
                if n > 2:
                    break
                n += 1
            # 实时读取输出并写入文件和打印到控制台
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    log_file.write(f'不可知的异常{process.poll()}，1 表示子进程已经终止')
                    state = f'不可知的异常{process.poll()}，1 表示子进程已经终止'
                    print('state648', state)
                    break
                if output:
                    # state_url,state_url_list =  check_proxy_connection(local_port)
                    # print(f'output.strip()652==>>{output.strip()}')
                    print(f'{type_}==>>{output.strip()}')
                    ## CST,main.go:412, FATAL ,"listen 127.0.0.1:8110, Address already in use"
                    ## CST,main.go:417, FATAL ,"listen :8100, Address already in use"
                    if 'Address already in use' in output.strip():
                        print('output.strip690', output.strip())
                        with open(object_name + r'\goflyway_err.txt', 'a+', encoding='utf-8') as f:
                            f.write(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}==>>{output.strip()}\n")
                        kill_GoflywayTools_exe()
                        if run_type == '所有':
                            state = f'有一个在运行，不能同时运行2个'
                            break
                    # output.strip()480 连接成功 2025-05-10 11:50:44.293 CST,io.go:68, ERROR ,"Bridge: write 127.0.0.1:5981, Software caused connection abort"
                    # output.strip()480 连接成功 2025-05-10 11:50:49.128 CST,io.go:84, ERROR ,"Bridge: read 127.0.0.1:7801, Software caused connection abort"
                    # if 'ERROR ,"Dial failed' in output.strip() and state_url != '连接成功':#client.go:541, ERROR ,"Dial failed: dial 163.172.120.27:26672, Connection refused"
                    if 'ERROR ,"Dial failed' in output.strip():  # client.go:541, ERROR ,"Dial failed: dial 163.172.120.27:26672, Connection refused"
                        # if str(state_url_list) != '连接成功':#client.go:541, ERROR ,"Dial failed: dial 163.172.120.27:26672, Connection refused"
                        kill_GoflywayTools_exe()
                        state = f'不可以上网'
                        cmd_on_color.printRed(f'不可以上网')
                        log_file.write(f'不可以上网')
                        log_file.flush()  # 确保每次写入后立即保存到文件
                        break
                    else:
                        state = '可以上网'
                        # status = cmd_on_color.printGre(status)
                        # cmd_on_color.printGre(f'此代理可以上网！端口为===============》》》》》》》》》》》》》》》》》》》：{local_port}【GoflywayTools】')
                        with open(object_name_output_log + r'\goflyway_status.txt', 'w+', encoding='utf-8') as f:
                            f.write(str(state))
                    log_file.write(output)
                    log_file.flush()  # 确保每次写入后立即保存到文件
                # 删除多余的log
                log_list = os.listdir(object_name)
                for i, log_name in enumerate(log_list):
                    if len(log_list) > 18:
                        # if len(log_list) > 3:  # 测试
                        if i < 18:  # 删除前29个
                            # if i < 2:  # 测试
                            print('开始删除log')
                            log_file.write(f'开始删除log==>>{object_name}/{log_name}')
                            try:
                                os.remove(f'{object_name}/{log_name}')
                            except:
                                traceback.print_exc()
            # state = f'不可以上网'
            print("goflyway 已正常退出")
            log_file.write("goflyway 已正常退出\n")

        except KeyboardInterrupt:
            print("\n用户手动终止 (Ctrl+C)")
            log_file.write("\n用户手动终止 (Ctrl+C)\n")
        except Exception as e:
            # with open(log_filename, 'a', encoding='utf-8') as file:
            #     # 将错误信息写入文件
            #     traceback.print_exc(file=file)
            print(f"程序异常终止: {e}")
            log_file.write(f"程序异常终止: {e}\n")
        finally:
            print("进程已结束")
            log_file.write("进程已结束\n")
            log_file.write(f"\n日志结束时间: {datetime.now()}\n")
    return state


def main_proxy_log():
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
    main_proxy()

    # 可选：恢复标准输出
    # sys.stdout = sys.__stdout__


if __name__ == "__main__":
    # main_proxy()

    main_proxy_log()

    # get_config_information(8100)

    # https: // clients2.googleusercontent.com / crx / blobs / AeKPYwwmtjxLc9ayiudBGaO7wwLA0teTicFrr4lLhigZF2YxOhAPfxZOwXcXZiw17ewS7OlB_61T0C18lD8cpEPLDv - wX65jGqAv7jCr2qqgKDuSY0yiAMZSmuVzE905olhxi8jWwx5p3bNITL96Ng / PADEKGCEMLOKBADOHGKIFIJOMCLGJGIF_2_5_21_0.crx

    # import ctypes, sys
    # def is_admin():
    #     try:
    #         return ctypes.windll.shell32.IsUserAnAdmin()
    #     except:
    #         return False
    # if is_admin():
    #     GoflywayTools()
    #     # 主程序写在这里
    # else:
    #     # 以管理员权限重新运行程序
    #     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    # kill_GoflywayTools_exe()
    # os.system("taskkill /F /IM goflyway_all.exe")
    # time.sleep(88)
    # GoflywayTools()

    # GoflywayTools_log()
    # os.system("taskkill /F /IM goflyway.exe")
    # os.system(r'D:\客户端集合代理\GoflywayTools.vbs')
    # print('**'*19)
    # print('若更新失败，可联系我')