#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# import json
import re
import subprocess
import threading
import urllib.parse
from DrissionPage import ChromiumPage, ChromiumOptions
# import webbrowser
import win32con
import yaml
from bs4 import BeautifulSoup
import base64
import os
import time
import traceback
# import urllib3
import win32api
import psutil
import requests
from tqdm import tqdm
import logging
import cmd_on_color
from urllib.parse import unquote
# from SS2 import get_config_information as get_config_informationurl_SS2
from datetime import datetime

from download_files import download_file
from notification_simulator import show_notification
from run_port_exe import run_exe
from upload_node import upload

# from GoflywayTools import check_proxy_connection

logging.captureWarnings(True)  # 强制取消证书验证警告
# url2 = "https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
# url1 = "https://dgithub.xyz/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
# url3 = "https://gitlab.com/zhifan999/fq/-/wikis/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
# # url3 = "https://s3.us-west-2.amazonaws.com/zhifan2/ss.html"#备用

url3 = "https://s3.dualstack.us-west-2.amazonaws.com/zhifan2/ss.html"
# url2 = "https://tr3.freeair888.club/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7/"
url1 = "https://gitlab.com/zhifan999/fq/-/wikis/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"  #github.com的镜像
url2 = "https://github.com/Alvin9999-newpac/fanqiang/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"

# url1 = "https://github.com/Alvin9999-newpac/fanqiang/wiki/Goflyway%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
# url2 = "https://gitlab.com/zhifan999/fq/-/wikis/Goflyway%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
# url3 = "https://s3.us-west-2.amazonaws.com/zhifan2/goflyway.html"

type_ = os.path.basename(__file__).replace('.py', '')
# open_Shadowsocks1 = os.getcwd() + fr'\{type_}\Shadowsocks1.exe'
# print('open_Shadowsocks128',open_Shadowsocks1)
pid = os.getpid()  # 当前进程的PID
# object_name = fr'{os.getcwd()}\{type_}'
object_name = fr'{os.getcwd()}'
isExists = os.path.exists(object_name)
# 判断结果
if not isExists:
    # 如果不存在则创建目录
    os.makedirs(object_name)
    print(object_name + ' 目录创建成功')
object_name_output_log = os.path.join(object_name, f"{type_}_output_log")
os.makedirs(object_name_output_log, exist_ok=True)
exe_name = f"ssrlocal_clash_{type_}.exe"#ssrlocal_clash_SSR1
exe_name_path = fr"{object_name}\{exe_name}"

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


def download_file_state(file_path, url, proxy_port):
    print('测试下载图片的地址为：' + str(url))
    print('测试下载本地的路径为：' + str(file_path))
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
            with open(file_path, 'wb') as file, tqdm(
                    desc=file_path,
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


def kill_exe(exe_name = exe_name):
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
            print(f'终止{exe_name}失败！准备开始重新终止！')
            try:
                # os.system("taskkill /PID " + str(p.pid))
                # os.system('taskkill /pid ' + str(p.pid) + ' /f')
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

port88_err_num = 1
def start_exe(local_port, run_type='单独', err_node_number=None,show_notification_state = True):
    global port88_err_num
    if run_type=='所有':
        exe_name = f"ssrlocal_clash_all.exe"
    else:
        exe_name = f"ssrlocal_clash_{type_}.exe"
    exe_name_path = fr"{object_name}\{exe_name}"
    print(f'开始启动{exe_name}')
    file_path = f'{type_}_clash_config_port{local_port}.yaml'  # 替换为实际文件路径
    state = f'不可以上网'
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            print(f"文件 '{file_path}' 存在")
            # state = run_exe(local_port, run_type)
            cmd = fr'{exe_name_path} -f {object_name}\{type_}_clash_config_port{local_port}.yaml'  # ssrlocal_clash_SSR1.exe -f clash_config.yaml
            # f'{type_}_clash_config_port10805.yaml'
            state = str(run_exe(local_port, run_type,cmd,object_name_output_log,type_,exe_name,object_name,exe_name_path,err_node_number,show_notification_state))
            if '表示子进程已经终止' in state or '端口冲突' in state:
                port88_err_num += 1
                print('port88_err_num190', port88_err_num)
                if port88_err_num < 8:
                    today_num = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                    if '表示子进程已经终止' in state:
                        cmd_on_color.printRed(f"{today_num} 程序{exe_name}被杀死，准备重启！")
                    if '端口冲突' in state:
                        kill_exe(exe_name)
                        cmd_on_color.printRed(f"{today_num} 端口{local_port}冲突，准备重启！")
                    state = start_exe(local_port, run_type, err_node_number)
                else:
                    state = f'不可以上网，似乎{type_}程序在进行测速'
                    port88_err_num = 1
        else:
            print(f"'{file_path}' 存在，但不是文件")
    else:
        print(f"文件 '{file_path}' 不存在")
        state = f'不可以上网，配置文件不存在'
    if f'不可以上网' in state or f'不可知的异常' in state:
        # os.system(f"taskkill /F /IM {exe_name}")
        pass
    return state


def parse_ss_url_old(ss_url):
    """
    解析Shadowsocks的ss://链接，支持标准格式和变种格式
    返回包含连接信息的字典，解析失败返回None
    """
    ss_url = ss_url.strip("'\" ")  # 清理两端的空白和引号

    try:
        # 分离基本部分和备注
        parts = ss_url.split('#', 1)
        url_part = parts[0]
        remark = unquote(parts[1]) if len(parts) > 1 else ""

        # 处理插件参数
        plugin = ""
        if '?plugin=' in url_part:
            url_part, plugin_part = url_part.split('?plugin=', 1)
            plugin = f'?plugin={plugin_part}'

        # 提取认证信息部分
        if url_part.startswith('ss://'):
            url_part = url_part[5:]

        # 处理两种不同编码格式
        if '@' in url_part:
            # 标准格式: base64(method:password)@host:port
            auth_server = url_part.split('@', 1)
            auth_part = auth_server[0]
            server_part = auth_server[1]
        else:
            # 变种格式: base64(method:password@host:port)
            decoded = base64.urlsafe_b64decode(url_part + '=' * (4 - len(url_part) % 4)).decode()
            if '@' not in decoded:
                raise ValueError("Invalid encoded format")
            auth_part, server_part = decoded.split('@', 1)
            # 重新编码为标准格式用于后续处理
            auth_part = base64.urlsafe_b64encode(auth_part.encode()).decode().rstrip('=')

        # 解析服务器地址和端口
        server_info = server_part.split('/')[0]  # 去除路径
        server_info = server_info.split('?')[0]  # 去除查询参数

        # 处理IPv6地址格式
        if server_info.startswith('['):
            end = server_info.index(']')
            ip = server_info[1:end]
            port = server_info[end + 2:]
        else:
            ip_port = server_info.rsplit(':', 1)  # 从右边分割处理可能包含冒号的IPv4
            if len(ip_port) != 2:
                raise ValueError("Invalid server format")
            ip, port = ip_port

        # 解码认证信息
        auth_decoded = base64.urlsafe_b64decode(auth_part + '=' * (4 - len(auth_part) % 4)).decode()
        method, password = auth_decoded.split(':', 1)

        # 处理备注信息
        remark_info = {}
        if '|' in remark:
            parts = remark.split('|')
            remark_info.update({
                'prefix': parts[0].strip(),
                'location': parts[1].strip() if len(parts) > 1 else '',
                'bandwidth': parts[2].strip() if len(parts) > 2 else ''
            })
        else:
            remark_info['full_remark'] = remark

        return {
            'method': method,
            'password': password,
            'server': ip,
            'port': port,
            'remark': remark,
            'remark_info': remark_info,
            'plugin': plugin or None
        }

    except Exception as e:
        print(f"解析失败: {str(e)}")
        traceback.print_exc()
        return None


def parse_plugin(plugin_str):
    """
    解析Shadowsocks插件参数
    输入示例:
      "v2ray-plugin;mode=websocket;mux=8;path=/utvbnrzejpmt;host=hkkh11v1.xpmc.cc;tls"
      "obfs-local;obfs=http;obfs-host=download.microsoft.com"
    返回: {
        'plugin_name': 'v2ray-plugin',
        'params': {
            'mode': 'websocket',
            'mux': '8',
            'path': '/utvbnrzejpmt',
            'host': 'hkkh11v1.xpmc.cc',
            'tls': True
        }
    }
    """
    if not plugin_str:
        return None

    # 解码URL编码字符（%3B转分号，%3D转等号）
    decoded = unquote(plugin_str)

    # 分割插件名称和参数
    parts = decoded.split(';')
    plugin_name = parts[0]
    params = {}

    # 解析参数
    for param in parts[1:]:
        if '=' in param:
            key, value = param.split('=', 1)
            # 处理布尔型参数（如tls）
            if value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
            params[key] = value
        else:
            # 无值的参数视为布尔True（如tls）
            params[param] = True

    return {
        'plugin_name': plugin_name,
        'params': params
    }


def parse_ss_url_with_plugin(ss_url):
    """
    完整解析带插件的SS链接
    """
    # 提取插件部分
    plugin_match = re.search(r'\?plugin=([^#]+)', ss_url)
    if not plugin_match:
        return None

    plugin_str = plugin_match.group(1)
    plugin_info = parse_plugin(plugin_str)

    # 示例输出
    print(f"插件名称: {plugin_info['plugin_name']}")
    print("插件参数:")
    for k, v in plugin_info['params'].items():
        print(f"  {k}: {v}")

    return plugin_info





def decode_base64_old(data):
    # 补齐 base64 字符串
    data += '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data.encode('utf-8')).decode('utf-8')


def decode_base64(data: str) -> str:
    data = data.strip().replace('-', '+').replace('_', '/')
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return base64.b64decode(data).decode('utf-8', errors='ignore')

def parse_ssr(ssr_url):
    if not ssr_url.startswith('ssr://'):
        return None
    try:
        decoded = decode_base64(ssr_url[6:])
        parts = decoded.split('/?')
        server_info = parts[0].split(':')
        params = {}
        if len(parts) > 1:
            query = parts[1]
            for pair in query.split('&'):
                if '=' in pair:
                    key, val = pair.split('=', 1)
                    params[key] = unquote(decode_base64(val)) if val else ''
        server = server_info[0].rstrip()

        # 处理端口号可能包含非数字字符的情况
        port_str = server_info[1].rstrip()
        try:
            port = int(port_str)
        except ValueError:
            # 如果端口不是纯数字，尝试将其视为Base64编码
            try:
                port = int(decode_base64(port_str))
            except:
                # 如果仍然无法转换，使用默认端口或抛出异常
                port = 0  # 或者可以使用一个默认端口

        protocol = server_info[2].rstrip()
        method = server_info[3].rstrip()
        obfs = server_info[4].rstrip()
        password = decode_base64(server_info[5]).rstrip()

        if method == 'rc4':
            return {'error': str(method), 'original': ssr_url}
        else:
            return {
                "name": f"{server}:{port}",
                "type": "ssr",
                "server": server,
                "port": port,
                "password": password,
                "cipher": method,
                "obfs": obfs,
                "protocol": protocol,
                "obfs-param": params.get('obfsparam', ''),
                "protocol-param": params.get('protoparam', ''),
                "remarks": params.get('remarks', '')
            }
    except Exception as e:
        return {'error': str(e), 'original': ssr_url}

def parse_ssr_old(ssr_url):
    if not ssr_url.startswith('ssr://'):
        return None
    try:
        decoded = decode_base64(ssr_url[6:])
        parts = decoded.split('/?')
        server_info = parts[0].split(':')
        params = {}
        if len(parts) > 1:
            query = parts[1]
            for pair in query.split('&'):
                if '=' in pair:
                    key, val = pair.split('=', 1)
                    params[key] = unquote(decode_base64(val)) if val else ''
        server = server_info[0].rstrip()
        port = server_info[1].rstrip()
        protocol = server_info[2].rstrip()
        method = server_info[3].rstrip()
        obfs = server_info[4].rstrip()
        password = decode_base64(server_info[5]).rstrip()
        if method == 'rc4':
            return {'error': str(method), 'original': ssr_url}
        else:
            return {
                "name": f"{server}:{port}",
                "type": "ssr",
                "server": server,
                "port": int(port),
                "password": password,
                "cipher": method,
                "obfs": obfs,
                "protocol": protocol,
                "obfs-param": params.get('obfsparam', ''),
                "protocol-param": params.get('protoparam', ''),
                "remarks": params.get('remarks', '')
            }
    except Exception as e:
        return {'error': str(e), 'original': ssr_url}


def parse_ssr_old(ssr_url):
    if not ssr_url.startswith('ssr://'):
        return None
    try:
        decoded = decode_base64(ssr_url[6:])
        parts = decoded.split('/?')
        server_info = parts[0].split(':')
        params = {}
        if len(parts) > 1:
            query = parts[1]
            for pair in query.split('&'):
                if '=' in pair:
                    key, val = pair.split('=', 1)
                    params[key] = unquote(decode_base64(val)) if val else ''

        # return {
        #     'server': server_info[0],
        #     'port': server_info[1],
        #     'protocol': server_info[2],
        #     'method': server_info[3],
        #     'obfs': server_info[4],
        #     'password': decode_base64(server_info[5]),
        #     'params': params
        # }
        server = server_info[0].rstrip()
        port =  server_info[1].rstrip()
        protocol =  server_info[2].rstrip()
        method = server_info[3].rstrip()
        obfs = server_info[4].rstrip()
        password = decode_base64(server_info[5]).rstrip()
        params = params
        if method == 'rc4':
            return {'error': str(method), 'original': ssr_url}
        else:
            return {
                "name": f"{server}:{port}",
                "type": "ssr",
                "server": server,
                "port": int(port),
                "password": password,
                "cipher": method,
                "obfs": obfs,
                "protocol": protocol,
                "obfs-param": params.get('obfsparam', ''),
                "protocol-param": params.get('protoparam', '')
            }
    except Exception as e:
        return {'error': str(e), 'original': ssr_url}


def base64_decoded_str(encoded_str):
    # 解码Base64字符串
    decoded_bytes = base64.urlsafe_b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8', errors='replace')

    # 替换字符
    replacement_char = ''
    modified_str = decoded_str.replace('/', replacement_char)
    return modified_str



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


def get_config_informationurl(local_port):
    # http = urllib3.PoolManager()

    config = ''
    not_ip = ''
    data = ''
    rsp = ''
    res_list = []
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
    #     np2 = 0
    #     np3 = 0
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
            html = webpage.text
            # html = Drission_get_Page(url1)
            if html:
            #     link_url1_successful = '连接1成功！'
            #     print(link_url1_successful)
                # print(webpage)
                # 读取页面内容
                # html = webpage.read()
                # html = webpage.content
                # html = webpage.text
                # html = webpage
                # print(html)
                # 解析成文档对象
                # print('解析成文档对象508',html)
                # soup = BeautifulSoup(html, 'html.parser')  # 文档对象
                code = BeautifulSoup(html, 'html.parser')
                # p_list = code.find_all('p')
                p_list = code.find_all('pre')

                err = ''
                # with open(os.getcwd() + r'\ssr.txt', 'w', encoding='utf-8') as f:
                #     f.write('')
                for p in p_list:

                    if 'ssr://' in str(p):
                        # print(p)
                        # with open(os.getcwd() + r'\ssr.txt', 'a', encoding='utf-8') as f:
                        #     f.write('\n' + p.text)
                        # f.close()
                        ssr = p.text
                        res_list.append(ssr)
                        print('ssr489', ssr)
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

                link_url2_successful = '连接2成功！'
                print(link_url2_successful)
                # print(webpage)
                # 读取页面内容
                # html = webpage.read()
                html = webpage.content
                # print(html)
                # 解析成文档对象
                print('解析成文档对象508')
                # soup = BeautifulSoup(html, 'html.parser')  # 文档对象
                code = BeautifulSoup(html, 'html.parser')
                # p_list = code.find_all('p')
                p_list = code.find_all('pre')

                err = ''
                # with open(os.getcwd() + r'\ssr.txt', 'w', encoding='utf-8') as f:
                #     f.write('')
                for p in p_list:

                    if 'ssr://' in str(p):
                        # print(p)
                        # with open(os.getcwd() + r'\ssr.txt', 'a', encoding='utf-8') as f:
                        #     f.write('\n' + p.text)
                        # f.close()
                        ssr = p.text
                        res_list.append(ssr)
                        print('ssr489', ssr)
                break

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

                    link_url3_successful = '连接3成功！'
                    print(link_url3_successful)
                    # print(webpage)
                    # 读取页面内容
                    # html = webpage.read()
                    html = webpage.content
                    # print(html)
                    # 解析成文档对象
                    print('解析成文档对象508')
                    # soup = BeautifulSoup(html, 'html.parser')  # 文档对象
                    code = BeautifulSoup(html, 'html.parser')
                    # p_list = code.find_all('p')
                    p_list = code.find_all('pre')

                    err = ''
                    # with open(os.getcwd() + r'\ssr.txt', 'w', encoding='utf-8') as f:
                    #     f.write('')
                    for p in p_list:

                        if 'ssr://' in str(p):
                            # print(p)
                            # with open(os.getcwd() + r'\ssr.txt', 'a', encoding='utf-8') as f:
                            #     f.write('\n' + p.text)
                            # f.close()
                            ssr = p.text
                            res_list.append(ssr)
                            print('ssr489', ssr)
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

    ssr_links = res_list
    # time.sleep(188)
    congfig_list = []
    congfig_err_list = []
    password = method = remarks = ''
    # with open(os.getcwd() + r'\ssr.txt', 'w', encoding='utf-8') as f:
    #     f.write('')
    # 解析所有节点

    # 批量处理
    # nodes = []
    # for link in res_list:
    #     if node := decode_ssr(link):
    #         nodes.append(node)
    #     else:
    #         print(f"无法解析链接: {link[:50]}...")
    #
    # print(f"\n成功解析 {len(nodes)}/{len(res_list)} 个节点")

    # 解析所有 SSR 链接
    congfig_list = [parse_ssr(link) for link in ssr_links]


    print('get_config_informationurl_ssr_links629节点', len(congfig_list))
    if len(congfig_list)!=0:
        unique_proxies = []
        seen = set()

        for proxy in congfig_list:
            # 将字典转换为可哈希的元组表示
            proxy_tuple = tuple(sorted(proxy.items()))
            if proxy_tuple not in seen:
                seen.add(proxy_tuple)
                if not str(proxy['cipher']).isdigit():
                    unique_proxies.append(proxy)

        proxies = unique_proxies
        print('proxies651',proxies)
        clash_config = {
            "mixed-port": 7892,
            "socks-port": local_port,  # 固定 SOCKS5 端口
            "allow-lan": False,
            "mode": "rule",
            "log-level": "info",
            "proxies": proxies,
            "proxy-groups": [
                {
                    "name": "自动选最优",
                    "type": "url-test",
                    "url": "http://www.gstatic.com/generate_204",
                    "interval": 300,
                    "tolerance": 50,
                    "proxies": [p["name"] for p in proxies]  # 所有节点参与测速
                },
                {
                    "name": "负载均衡",
                    "type": "load-balance",
                    "strategy": "consistent-hashing",
                    "proxies": [p["name"] for p in proxies]
                }
            ],
            "rules": [
                "DOMAIN-SUFFIX,cn,DIRECT",
                "IP-CIDR,127.0.0.0/8,DIRECT",
                "IP-CIDR,192.168.0.0/16,DIRECT",
                "MATCH,自动选最优"  # 默认使用最快节点
            ]
        }
        return clash_config



def get_config_informationurl_old(local_port):
    congfig_list1 = []
    congfig_list2 = []
    congfig_list3 = []
    # try:
    #     congfig_list1 = get_config_informationurl1(local_port)
    # except:
    #     traceback.print_exc()
    # try:
    #     congfig_list2 = get_config_informationurl2(local_port)
    # except:
    #     traceback.print_exc()
    # try:
    #     congfig_list3 = get_config_informationurl3(local_port)
    # except:
    #     traceback.print_exc()

    # config, congfig_list_SS2 = get_config_informationurl_SS2()
    # congfig_list_SS2 = []
    # print(type(congfig_list1))
    # print(type(congfig_list2))
    # print(type(congfig_list3))
    # proxies = list(set(congfig_list1 + congfig_list2 + congfig_list3))
    # congfig_list = congfig_list1
    # configs = ','.join(congfig_list)
    # # print('configs722',configs)
    # config = get_config(configs, local_port)
    # congfig_list = {**congfig_list1, **congfig_list2,**congfig_list3}
    # 将字典转换为元组（键值对的元组），再进行去重
    unique_proxies = []
    seen = set()

    for proxy in congfig_list1 + congfig_list2 + congfig_list3:
        # 将字典转换为可哈希的元组表示
        proxy_tuple = tuple(sorted(proxy.items()))
        if proxy_tuple not in seen:
            seen.add(proxy_tuple)
            unique_proxies.append(proxy)

    proxies = unique_proxies
    clash_config = {
        "mixed-port": 7890,
        "socks-port": local_port,  # 固定 SOCKS5 端口
        "allow-lan": False,
        "mode": "rule",
        "log-level": "info",
        "proxies": proxies,
        "proxy-groups": [
            {
                "name": "自动选最优",
                "type": "url-test",
                "url": "http://www.gstatic.com/generate_204",
                "interval": 300,
                "tolerance": 50,
                "proxies": [p["name"] for p in proxies]  # 所有节点参与测速
            },
            {
                "name": "负载均衡",
                "type": "load-balance",
                "strategy": "consistent-hashing",
                "proxies": [p["name"] for p in proxies]
            }
        ],
        "rules": [
            "DOMAIN-SUFFIX,cn,DIRECT",
            "IP-CIDR,127.0.0.0/8,DIRECT",
            "IP-CIDR,192.168.0.0/16,DIRECT",
            "MATCH,自动选最优"  # 默认使用最快节点
        ]
    }
    return clash_config

def get_config(server, server_port, password, method, protocol, obfs,obfsparam,remarks_base64):
    config1 = '''
{
    "configs" : [
        {'''
    config2 = '''
            "remarks" : "UFO2",
            "id" : "C5AF045C075A312EE4E03443D46BF272",
            "server" : "{0}",
            "server_port" : {1},
            "server_udp_port" : 0,
            "password" : "{2}",
            "method" : "{3}",
            "protocol" : "{4}",
            "protocolparam" : "",
            "obfs" : "{5}",
            "obfsparam" : "{6}",
            "remarks_base64" : "{7}",
            "group" : "https://git.io/v9999",
            "enable" : true,
            "udp_over_tcp" : false'''.format(server, server_port, password, method, protocol, obfs,obfsparam,remarks_base64)
    config3 = '''
        }
    ],
    "index" : 0,
    "random" : true,
    "sysProxyMode" : 1,
    "shareOverLan" : false,
    "localPort" : 10806,
    "localAuthPassword" : "GAvbtagMG82jE9n_eeXK",
    "dnsServer" : "",
    "reconnectTimes" : 2,
    "randomAlgorithm" : 3,
    "randomInGroup" : false,
    "TTL" : 0,
    "connectTimeout" : 5,
    "proxyRuleMode" : 2,
    "proxyEnable" : false,
    "pacDirectGoProxy" : false,
    "proxyType" : 0,
    "proxyHost" : "",
    "proxyPort" : 0,
    "proxyAuthUser" : "",
    "proxyAuthPass" : "",
    "proxyUserAgent" : "",
    "authUser" : "",
    "authPass" : "",
    "autoBan" : false,
    "sameHostForSameTarget" : false,
    "keepVisitTime" : 180,
    "isHideTips" : false,
    "nodeFeedAutoUpdate" : true,
    "serverSubscribes" : [

    ],
    "token" : {

    },
    "portMap" : {

    }
}'''
    list_data = ''
    config = config1 + config2 + config3
    return config


def get_config_old(configs, local_port=10806):
    config1 = '''
{
  "version": "4.1.10.0",
  "configs": [
    '''
    config2 = configs
    config3 = '''

  ],
  "strategy": "com.shadowsocks.strategy.balancing",
  "index": -1,
  "global": false,
  "enabled": false,
  "shareOverLan": false,
  "isDefault": false,
  "isIPv6Enabled": false,
  "localPort": 10806,
  "portableMode": true,
  "showPluginOutput": false,
  "pacUrl": null,
  "gfwListUrl": null,
  "useOnlinePac": false,
  "secureLocalPac": true,
  "availabilityStatistics": false,
  "autoCheckUpdate": false,
  "checkPreRelease": false,
  "isVerboseLogging": false,
  "logViewer": {
    "topMost": false,
    "wrapText": false,
    "toolbarShown": false,
    "Font": "Consolas, 8pt",
    "BackgroundColor": "Black",
    "TextColor": "White"
  },
  "proxy": {
    "useProxy": false,
    "proxyType": 0,
    "proxyServer": "",
    "proxyPort": 0,
    "proxyTimeout": 3,
    "useAuth": false,
    "authUser": "",
    "authPwd": ""
  },
  "hotkey": {
    "SwitchSystemProxy": "",
    "SwitchSystemProxyMode": "",
    "SwitchAllowLan": "",
    "ShowLogs": "",
    "ServerMoveUp": "",
    "ServerMoveDown": "",
    "RegHotkeysAtStartup": false
  }
}
'''
    config = config1 + config2 + config3
    return config


def main_proxy(local_port=10806):
    download_file(f"http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/{type_}_clash_config_port{local_port}.yaml", f"{type_}_clash_config_port{local_port}.yaml")
    download_file(f"http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/{type_}_configs_port88.json", f"{type_}_clash_config_port88.yaml")
    time.sleep(2)

    # 启动监控进程
    subprocess.Popen([sys.executable, "monitor.py", str(pid), f"{type_}"])
    kill_exe()



    cmd_on_color.printCya(f'++++++++++++++++++++++++++++++++启动{type_}中，请耐心等待............++++++++++++++++++++++++++++++++')
    n=0
    while True:
        try:
            state_ = start_exe(local_port,err_node_number=n+1)
            print('state_1032',state_)
            # time.sleep(188)
            # break
            if f'不可以上网' in state_ or f'不可知的异常' in state_:
                if n <= 2:
                    show_notification(f"端口 {local_port} 链接错误！准备更新配置", f"不可以上网！【第{n+1}次检测)】", "error")
                print(f'代理错误，疑似代理或IP配置有错误？开始重新获取最新IP配置=={type_}')
                clash_config = get_config_informationurl(local_port)
                # config = get_config_informationurl1()
                # config = get_config_informationurl3()
                if clash_config:
                    # 保存配置文件
                    with open(f'{type_}_clash_config_port{local_port}.yaml', 'w', encoding='utf-8') as f:
                        clash_config["socks-port"] = local_port
                        yaml.dump(clash_config, f, allow_unicode=True)
                    with open(f'{type_}_clash_config_port88.yaml', 'w', encoding='utf-8') as f:
                        clash_config["socks-port"] = 88
                        yaml.dump(clash_config, f, allow_unicode=True)
                    # time.sleep(2)
                    # upload(f'{type_}_clash_config_port{local_port}.yaml')
                    # upload(f'{type_}_clash_config_port88.yaml')
                print(f'开始杀死进程{exe_name}')
                kill_exe()  # exe_name, exe_name_path, object_name
            if state_ == f'有一个在运行，不能同时运行2个':
                def popup():
                    win32api.MessageBox(None, f'有一个在运行，不能同时运行2个{type_}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)

                threading.Thread(target=popup).start()

                break

            if n>18:
                n = 0
                download_file(f"http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/{type_}_clash_config_port{local_port}.yaml", f"{type_}_clash_config_port{local_port}.yaml")
                download_file(f"http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/{type_}_configs_port88.json", f"{type_}_clash_config_port88.yaml")
                time.sleep(2)

                pass
                # time.sleep(88)
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
def SS1_old():
    cmd_on_color.printCya(f'++++++++++++++++++++++++++++++++更新{type_}中，请耐心等待............++++++++++++++++++++++++++++++++')

    print(f'开始检查进程{exe_name}是否正常打开？')
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
    if f'sslocal_{type_}.exe' in p_name_all:
        print(f'进程sslocal_{type_}.exe，已经启动！无需再次启动！')
    else:
        print(f'进程sslocal_{type_}.exe，未启动！再次开始启动！')
        # state = start_exe()
        # if success == f'启动{exe_name}成功':
        #     cmd_on_color.printGre(f'success642==>>{success}')
        # time.sleep(2)
    print('开始检查代理是否可以上网')
    n = 0
    while True:
        # print(n)
        import download_files
        state, average_speed = download_files.download_file_state('https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif', os.getcwd() + r"\test_speed.gif", '10806')
        if state == '下载失败':
            print('代理错误，疑似代理或IP配置有错误？开始重新获取最新IP配置')
            # config = get_config_informationurl(10806)
            # config = get_config_informationurl1()
            # config = get_config_informationurl3()


            # with open(object_name + f'\{type_}_configs_port10805.json', 'w+', encoding='utf-8') as f:
            #     f.write(config.replace('88', '10806'))
            # with open(object_name + f'\{type_}_configs_port88.json', 'w+', encoding='utf-8') as f:
            #     f.write(config.replace('10806', '88'))
            print(f'开始杀死进程{exe_name}')
            kill_exe()  # exe_name, exe_name_path, object_name
            print(f'开始启动进程{exe_name}')
            # state = start_exe()  # exe_name,exe_name_path,object_name
            # if success == f'启动{exe_name}成功':
            #     cmd_on_color.printGre(f'success642==>>{success}')
        else:
            status = '可以上网'
            # with open(os.getcwd() + r'\ssr2.txt', 'r+', encoding='utf-8') as f:
            #     old_data = f.read()
            # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
            #     f.write(old_data)
            # f.close()
            status = cmd_on_color.printGre(status)
            cmd_on_color.printGre('此代理可以上网！端口为===============》》》》》》》》》》》》》》》》》》》：10806【Shadowsocks1】')
            break
        if n >= 2:
            status = '不可上网'
            status = cmd_on_color.printRed(status)
            cmd_on_color.printRed('10806【Shadowsocks1】此代理最终不可以上网！请更换下一个代理！')
            break
        n += 1
    return status, average_speed


def run_exe_old(local_port, run_type):
    # server_address, port, password = read_config()
    success = ''
    cmd = fr'{exe_name_path} -f {object_name}\{type_}_clash_config_port{local_port}.yaml'  # ssrlocal_clash_SSR1.exe -f clash_config.yaml
    #f'{type_}_clash_config_port10805.yaml'
    print('cmd1082', cmd)
    object_name_output_log = fr'{object_name}/{type_}_output_log'
    isExists = os.path.exists(object_name_output_log)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(object_name_output_log)
        print(object_name_output_log + ' 目录创建成功')
    # 生成带时间戳的日志文件名
    log_filename = f"{object_name_output_log}/{type_}_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # 首先将命令本身写入日志文件
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(f"执行的命令: {cmd}\n\n")
        log_file.flush()  # 立即写入文件

        try:
            print(f"正在启动 {exe_name}...")
            log_file.write(f"正在启动 {exe_name}...\n")

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
                        if exe_name in p.name():
                            start_list.append('未杀死！')
                            pass
                        else:
                            pass
                    except:
                        pass

                # my_file = Path(open_Shadowsocks1)
                if len(start_list) != 0:
                    # success = f'启动{exe_name}成功'
                    # print(f'启动{exe_name}成功')
                    break
                else:
                    print(f'启动{exe_name}失败！准备开始重启！')
                    # win32api.ShellExecute(0, 'open', open_Shadowsocks1, '', '', 0)
                    # state = run_exe(local_port, run_type)
                time.sleep(2)
                if n >= 2:
                    break
                n += 1
            # 实时读取输出并写入文件和打印到控制台
            while True:
                output = process.stdout.readline()
                print('output1187',output)
                if output == '' and process.poll() is not None:
                    state = f'不可知的异常{process.poll()}，1 表示子进程已经终止'
                    log_file.write(state)
                    print('state1142', state)
                    break
                if output:
                    # state_url, state_url_list = check_proxy_connection(local_port)
                    # print('output.strip()719', output.strip())  # AddrInUse, message: "通常每个套接字地址(协议/网络地址/端口)只允许使用一次。" }
                    print(f'{type_}==>>{output.strip()}')
                    with open(object_name + r'\goflyway_status.txt', 'r+', encoding='utf-8') as f:
                        goflyway_status = f.read()  # 可以上网    可以退出当前代理，优先选择 goflyway  goflyway_status == '可以上网'
                    n8 = 0
                    while True:
                        pids = psutil.pids()
                        start_list = []
                        for pid in pids:
                            try:
                                p = psutil.Process(pid)
                                if exe_name in p.name():
                                    start_list.append('未杀死！')
                                    pass
                                else:
                                    pass
                            except:
                                pass

                        # my_file = Path(open_Shadowsocks1)
                        if len(start_list) != 0:
                            # success = f'启动{exe_name}成功'
                            # print(f'启动{exe_name}成功')
                            break
                        else:
                            print(f'启动{exe_name}失败！准备开始重启！')
                            if '系统找不到指定的文件' in output.strip() and '.exe' in output.strip():
                                win32api.MessageBox(None, f'系统找不到{exe_name_path}，请将该exe放入{object_name}内！然后点击确定', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
                                # def popup():
                                #     win32api.MessageBox(None, f'系统找不到{exe_name}，请检查！', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
                                # threading.Thread(target=popup).start()
                                state = '不可以上网'
                                break
                            if '系统找不到指定的文件' in output.strip() and '.json' in output.strip():
                                cmd_on_color.printRed(f"系统找不到json")
                                state = '不可以上网'
                                break
                            # win32api.ShellExecute(0, 'open', open_Shadowsocks1, '', '', 0)
                            # state = run_exe(local_port, run_type)
                        time.sleep(2)
                        if n8 >= 2:
                            break
                        n8 += 1
                    if '只允许使用一次' in output.strip():
                        with open(object_name + r'\ss1_err.txt', 'a+', encoding='utf-8') as f:
                            f.write(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}==>>{output.strip()}\n")
                        if run_type == '所有':
                            state = f'有一个在运行，不能同时运行2个'
                            break
                    if '系统找不到指定的文件' in output.strip() or 'json parse error' in output.strip() or 'expected array, boolean, null, number, object, or string' in output.strip():
                        # if 'shadowsocks' not in output.strip() and 'INFO' not in output.strip() and 'build' not in output.strip():
                        cmd_on_color.printRed('代理格式出错！重新写入格式')
                        # config = get_config_informationurl()
                        # config = get_config_informationurl1()
                        # config = get_config_informationurl3()
                        # with open(object_name + '\gui-config.json', 'w+', encoding='utf-8') as f:
                        # with open(object_name + f'\{type_}_configs_port10805.json', 'w+', encoding='utf-8') as f:
                        #     f.write(config.replace('88', '10806'))
                        # with open(object_name + f'\{type_}_configs_port88.json', 'w+', encoding='utf-8') as f:
                        #     f.write(config.replace('10806', '88'))

                    # if '由于目标计算机积极拒绝' in output.strip() and state_url != '连接成功':#handler error: 由于目标计算机积极拒绝，无法连接。 (os error 10061)
                    if '由于目标计算机积极拒绝' in output.strip() or '连接尝试失败' in output.strip() or '没有正确答复' in output.strip():  # handler error: 由于目标计算机积极拒绝，无法连接。 (os error 10061)
                        ###由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败  #不可以上网
                        # error: 你的主机中的软件中止了一个已建立的连接。 (os error 10053)  #这个是可以上网的
                        state = '不可以上网'
                        cmd_on_color.printRed(f'该代理不可上网，跳出！更换其它代理')
                        break
                    log_file.write(output)
                    log_file.flush()  # 确保每次写入后立即保存到文件
                # 删除多余的log
                log_list = os.listdir(object_name_output_log)
                for i, log_name in enumerate(log_list):
                    if len(log_list) > 18:
                        # if len(log_list) > 3:  # 测试
                        if i < 18:  # 删除前29个
                            # if i < 2:  # 测试
                            print(f'开始删除log==>>{object_name_output_log}/{log_name}')
                            log_file.write(f'开始删除log==>>{object_name_output_log}/{log_name}')
                            try:
                                os.remove(f'{object_name_output_log}/{log_name}')
                            except:
                                traceback.print_exc()
            # state = '不可以上网'
            print(f"{exe_name} 已正常退出")
            log_file.write(f"{exe_name} 已正常退出\n")

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


def extract_and_decode_plugin_params(url_param):
    plugin_params_decoded = urllib.parse.unquote(url_param)
    plugin_name = plugin_params_decoded.split(';')[0].split('=')[-1]
    plugin_params = ';'.join(plugin_params_decoded.split(';')[1:])
    # print(plugin_name,plugin_params)
    return plugin_name, plugin_params

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
    # get_config_informationurl(10806)
    # print(parse_ssr('ssr://MjAwMTpiYzg6MTIwMzoxMDY6OjMwMTo2MDA2NjphdXRoX2NoYWluX2E6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2F1dGg6Wkc5dVozUmhhWGRoYm1jdVkyOXQvP29iZnNwYXJhbT0mcmVtYXJrcz1VMU5TNklxQzU0SzVMV2x3ZGpZ'))