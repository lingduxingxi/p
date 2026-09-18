#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# import json
import json
import re
import subprocess
import threading
import urllib.parse
# import asyncio
import win32con
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage
from bs4 import BeautifulSoup
import base64
import os
import time
import traceback
import urllib3
import win32api
import psutil
import requests
from tqdm import tqdm
import logging
import cmd_on_color
from urllib.parse import unquote
# from SS2 import get_config_information as get_config_informationurl_SS2
from datetime import datetime
from collections import deque

from download_files import download_file
from notification_simulator import show_notification
from run_port_exe import run_exe
from upload_node import upload

today = time.strftime('%Y%m%d', time.localtime(time.time()))
# from GoflywayTools import check_proxy_connection
# import yaml
logging.captureWarnings(True)  # 强制取消证书验证警告

url1 = "https://www.cfmem.com/"  # ss
# url1 = "https://clashgithub.com/"  # ss


url2_list = ["https://ghfile.geekertao.top/https://raw.githubusercontent.com/ripaojiedian/freenode/refs/heads/main/sub",
             "https://ghfile.geekertao.top/https://raw.githubusercontent.com/abshare3/abshare3.github.io/main/README.md","https://ghfile.geekertao.top/https://raw.githubusercontent.com/mksshare/mksshare.github.io/main/README.md","https://ghfile.geekertao.top/https://raw.githubusercontent.com/hello-world-1989/v2-sub/refs/heads/main/end-gfw-together-ss",
             "https://ghfile.geekertao.top/https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/refs/heads/master/list.txt",
             "https://ghfile.geekertao.top/https://raw.githubusercontent.com/nodesfree/clashnode/refs/heads/main/v2ray.txt",
             "https://ghfile.geekertao.top/https://raw.githubusercontent.com/shabane/kamaji/refs/heads/master/hub/ss.txt",
             f"https://yoyapai.com/mianfeijiedian/{time.strftime('%Y%m%d', time.localtime(time.time()))}-ssr-v2rayvpnjiedian-yoyapai.com.txt",
             f"https://clashgithub.com/clashnode-{time.strftime('%Y%m%d', time.localtime(time.time()))}.html",
             ]#备用 可筛选可用的ss   镜像网站
url2_source_list = ["https://raw.githubusercontent.com/ripaojiedian/freenode/refs/heads/main/sub",
                    "https://github.com/abshare3/abshare3.github.io",
                    "https://github.com/mksshare/mksshare.github.io",
                    "https://raw.githubusercontent.com/hello-world-1989/v2-sub/refs/heads/main/end-gfw-together-ss",
                    "https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/refs/heads/master/list.txt",
                    "https://raw.githubusercontent.com/nodesfree/clashnode/refs/heads/main/v2ray.txt",
                    "https://raw.githubusercontent.com/shabane/kamaji/refs/heads/master/hub/ss.txt",
                    f""]#备用 可筛选可用的ss   原生网站

# url3 = "https://github.com/aiboboxx/v2rayfree"#备用  可用的ss
url3 = "https://github.com/free-nodes/v2rayfree"#备用  可用的ss
url8 = "https://ghfile.geekertao.top/https://raw.githubusercontent.com/free-nodes/v2rayfree/refs/heads/main/README.md"#备用  可用的ss 多  9小时更新


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
exe_name = f"sslocal_{type_}.exe"
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
    print('下载图片的地址为：' + str(url))
    print('下载本地的路径为：' + str(file_path))
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

port88_err_num = 1
def start_exe(local_port, run_type='单独', err_node_number=1,show_notification_state = True):
    global port88_err_num
    if run_type=='所有':
        exe_name = f"sslocal_all.exe"
    else:
        exe_name = f"sslocal_{type_}.exe"
    exe_name_path = fr"{object_name}\{exe_name}"
    print(f'开始启动{exe_name}')
    # if '表示子进程已经终止' in state:
    #     today_num = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    #     cmd_on_color.printRed(f"{today_num} 程序被杀死，准备重启！105")
    #     state = start_exe(local_port,run_type)
    # print(f'开始启动{exe_name}')
    file_path = object_name + fr'\{type_}_configs_port{local_port}.json'  # 替换为实际文件路径
    state = f'不可以上网'
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            print(f"文件 '{file_path}' 存在")
            # cmd = f'"{exe_name_path}" -c "{object_name}\\{type_}_configs_port{local_port}.json" -vvv'
            cmd = f'"{exe_name_path}" -c "{object_name}\\{type_}_configs_port{local_port}.json"'
            state = str(run_exe(local_port, run_type,cmd,object_name_output_log,type_,exe_name,object_name,exe_name_path,err_node_number,show_notification_state))
            if '表示子进程已经终止' in state or '端口冲突' in state:
                port88_err_num += 1
                print('port88_err_num200', port88_err_num)
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
    import datetime
    cmd_on_color.printCya(f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}||state222=={state}")
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







# ================= Base64 解码 =================

def safe_b64decode(data):

    if not data:
        return None

    data = data.strip()

    data = re.sub(r'[^A-Za-z0-9+/=_-]', '', data)

    data = data.replace('-', '+').replace('_', '/')

    padding = len(data) % 4

    if padding:
        data += '=' * (4 - padding)

    try:
        return base64.b64decode(data).decode('utf-8')
    except:
        try:
            return base64.b64decode(data).decode('latin1')
        except:
            return None

# ==================== 安全 Base64 解码 ====================

def safe_b64decode_bytes(data):
    if not data:
        return None

    cleaned = re.sub(r'[^A-Za-z0-9+/=_-]', '', data)
    cleaned = cleaned.replace('-', '+').replace('_', '/')

    missing = len(cleaned) % 4
    if missing:
        cleaned += '=' * (4 - missing)

    try:
        return base64.b64decode(cleaned)
    except:
        try:
            return base64.urlsafe_b64decode(cleaned)
        except:
            return None


def safe_b64decode_str(data):

    b = safe_b64decode_bytes(data)

    if b is None:
        return None

    for enc in ["utf-8", "gbk", "latin1"]:
        try:
            return b.decode(enc)
        except:
            pass

    return None

# ==================== 参数验证 ====================

def validate_params(method, password, server, port):

    try:
        port = int(port)
        if not (1 <= port <= 65535):
            return False
    except:
        return False

    if not password:
        return False

    if not server:
        return False

    return True
# ==================== 默认加密 ====================

DEFAULT_METHODS = [
    "chacha20-ietf-poly1305",
    "aes-256-gcm",
    "aes-256-cfb",
    "aes-128-gcm",
    "aes-128-cfb",
    "rc4-md5",
]


VALID_METHODS = {
    "aes-256-gcm",
    "aes-128-gcm",
    "chacha20-ietf-poly1305",
    "aes-256-cfb",
    "aes-128-cfb",
    "rc4-md5",
    "none",
}

# ================= 参数校验 =================

def validate(method, password, server, port):

    if not password:
        return False

    try:
        port = int(port)
        if not (1 <= port <= 65535):
            return False
    except:
        return False

    if not server:
        return False

    return True


# ================= server:port 解析 =================

def parse_server_port(server_part):

    if server_part.startswith("["):

        end = server_part.index("]")

        server = server_part[1:end]

        port = server_part[end + 2:]

    else:

        parts = server_part.rsplit(":", 1)

        if len(parts) != 2:
            return None, None

        server, port = parts

    return server, port


# ================= auth 解析 =================

def parse_auth(auth):

    method = None
    password = None

    if ":" in auth:

        method, password = auth.split(":", 1)

        if method not in VALID_METHODS:

            password = method + ":" + password
            method = None

    else:

        password = auth

    return method, password


# ================= SS URL 解析 =================
import re

def parse_ss_url(ss_url):
    try:
        ss_url = ss_url.strip().strip("'\"")
        if not ss_url.startswith("ss://"):
            return None
        ss_url = ss_url[5:]

        # ---------- remark ----------
        remark = ""
        if "#" in ss_url:
            ss_url, remark = ss_url.split("#", 1)
            remark = unquote(remark)

        # ---------- plugin ----------
        plugin = None
        if "?plugin=" in ss_url:
            ss_url, plugin = ss_url.split("?plugin=", 1)
            plugin = unquote(plugin)

        # ---------- Base64整段 ----------
        if "@" not in ss_url:
            decoded = safe_b64decode_str(ss_url)
            if not decoded:
                return None
            ss_url = decoded

        # ---------- 拆分 auth 和 server ----------
        if "@" not in ss_url:
            return None
        auth_part, server_part = ss_url.split("@", 1)

        # ⭐⭐⭐ 修改：仅当 auth_part 为纯 base64 字符时才解码 ⭐⭐⭐
        if ":" not in auth_part:
            # 检查是否只包含标准 base64 字符（允许填充 =）
            if re.match(r'^[A-Za-z0-9+/=]+$', auth_part):
                decoded = safe_b64decode_str(auth_part)
                if decoded and ":" in decoded:
                    auth_part = decoded
            # 否则直接跳过，auth_part 保持原样（如 UUID 字符串）

        # ---------- 解析 auth ----------
        if ":" in auth_part:
            method, password = auth_part.split(":", 1)
            if method not in VALID_METHODS:
                password = method + ":" + password
                method = None
        else:
            method = None
            password = auth_part

        # ---------- server ----------
        server_part = server_part.split("/")[0]
        if server_part.startswith("["):
            end = server_part.index("]")
            server = server_part[1:end]
            port = server_part[end + 2:]
        else:
            parts = server_part.rsplit(":", 1)
            if len(parts) != 2:
                return None
            server, port = parts

        # ---------- 自动 method ----------
        if method is None:
            for m in DEFAULT_METHODS:
                if validate_params(m, password, server, port):
                    method = m
                    break

        # ---------- 最终验证 ----------
        if not validate_params(method, password, server, port):
            return None

        return {
            "method": method,
            "password": password,
            "server": server,
            "port": port,
            "remark": remark,
            "plugin": plugin
        }

    except Exception as e:
        print("解析错误:", e)
        traceback.print_exc()
        return None



def parse_ss_url_old(ss_url):

    try:

        ss_url = ss_url.strip().strip("'\"")

        if not ss_url.startswith("ss://"):
            return None

        ss_url = ss_url[5:]

        # ---------- remark ----------

        remark = ""

        if "#" in ss_url:

            ss_url, remark = ss_url.split("#", 1)

            remark = unquote(remark)

        # ---------- plugin ----------

        plugin = None

        if "?plugin=" in ss_url:

            ss_url, plugin = ss_url.split("?plugin=", 1)

            plugin = unquote(plugin)

        # ---------- Base64整段 ----------

        if "@" not in ss_url:

            decoded = safe_b64decode_str(ss_url)

            if not decoded:
                return None

            ss_url = decoded

        # ---------- 拆分 auth 和 server ----------

        if "@" not in ss_url:
            return None

        auth_part, server_part = ss_url.split("@", 1)

        # ⭐⭐⭐ 新增逻辑：Base64 auth 自动识别 ⭐⭐⭐

        if ":" not in auth_part:

            decoded = safe_b64decode_str(auth_part)

            if decoded and ":" in decoded:

                auth_part = decoded

        # ---------- 解析 auth ----------

        if ":" in auth_part:

            method, password = auth_part.split(":", 1)

            if method not in VALID_METHODS:

                password = method + ":" + password
                method = None

        else:

            method = None
            password = auth_part

        # ---------- server ----------

        server_part = server_part.split("/")[0]

        if server_part.startswith("["):

            end = server_part.index("]")

            server = server_part[1:end]

            port = server_part[end + 2:]

        else:

            parts = server_part.rsplit(":", 1)

            if len(parts) != 2:
                return None

            server, port = parts

        # ---------- 自动 method ----------

        if method is None:

            for m in DEFAULT_METHODS:

                if validate_params(m, password, server, port):

                    method = m
                    break

        # ---------- 最终验证 ----------

        if not validate_params(method, password, server, port):
            return None

        return {
            "method": method,
            "password": password,
            "server": server,
            "port": port,
            "remark": remark,
            "plugin": plugin
        }

    except Exception as e:

        print("解析错误:", e)
        traceback.print_exc()

        return None





def Drission_get_Page(url):
    co = ChromiumOptions()
    # 关键参数
    co.set_argument('--app=data:,')
    co.set_argument('--disable-blink-features=AutomationControlled')
    co.set_argument('--window-position=-32000,-32000')
    # 伪装 webdriver
    co.set_user_agent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/122.0.0.0 Safari/537.36'
    )
    # 可选：关闭图片加载（更快）
    co.set_argument('--disable-images')
    page = ChromiumPage(co)
    page.get(url)
    page.wait.doc_loaded()
    html = page.html
    page.quit()
    return html


def get_ss(ss_url=f'https://v2rayse.com/fs/public/{today}/kdfbypk.txt'):
    # import requests
    proxies = {"http": "socks5h://127.0.0.1:" + '0', "https": "socks5h://127.0.0.1:" + '0'}
    # proxy_port_list = [0,88, 8100, 10801, 10802, 10805, 10806, 10822, 10999]
    proxy_port_list = [0,88, 8100, 10801, 10802, 10805, 10806, 10822, 10999]
    response = -1
    for proxy_ports in proxy_port_list:
        # if int(proxy_port) == proxy_ports :#指定代理
        # print('走代理,IP:', proxy_ports)
        proxies = {"http": "socks5h://127.0.0.1:" + str(proxy_ports), "https": "socks5h://127.0.0.1:" + str(proxy_ports)}
        np1 = 0
        np2 = 0
        np3 = 0
        while True:
            try:
                cookies = {
                    'nuxt-session': 'Fe26.2**f0e406bcc05cd71e99ec81ddefadb9b36aca2a692b0ac40279855f7f3bb3ab28*3sTC-ndjR7s2GmXHvlvQuA*ppcRjzv0u8IUwz7Xe17jx32rMhDuukkI3CnjJ8vhlz8gOuWKz594k4Av2XetOGlahFAJTJx6ti-7UC1ae4ghaX11BKTVJKcT9mFTugYhCsk1RPPj4KrM47Rv9zPOkbZc**158aeafd34f349434362cf1b5ed2b97ce7889eebfd5756f3350533a00ad5ed78*Hs7XLDDcITZgZp2wUCSBE6djD0YvYTHp8v20j31nKkA',
                    'i18n_redirected': 'zh',
                    'FCCDCF': '%5Bnull%2Cnull%2Cnull%2C%5B%22CQfQQUAQfQQUAEsACBZHCRFoAP_gAEPgAARoK1IB_C7EbCFCiDJ3IKMEMAhHABBAYsAwAAYBAwAADBIQIAQCgkEYBASAFCACCAAAKASBAAAgCAAAAUAAIAAFAABAAAwAIBAIIAAAgAAAAEAIAAAACIAAEQCAAAAEAEAAkAgAAAIASAAAAAAAAACBAAAAAAAAAAAAAAAABAEAAQAAQAAAAAAAiAAAAAAAABAIAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAABAAAAAAAQWEQD-F2I2EKFEGCuQUYIYBCuACAAxYBgAAwCBgAAGCQgQAgFJIIkCAEAIEAAEAAAQAgCAABQEBAAAIAAAAAqAACAABgAQCAQAIABAAAAgIAAAAAAEQAAIgEAAAAIAIABABAAAAQAkAAAAAAAAAECAAAAAAAAAAAAAAAAAAIAAEABgAAAAAABEAAAAAAAACAQIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAA.ILCIB_C7EbCFCiDJ3IKMEMAhXABBAYsAwAAYBAwAADBIQIAQCkkEaBASAFCACCAAAKASBAAAoCAgAAUAAIAAVAABAAAwAIBAIIEAAgAAAQEAIAAAACIAAEQCAAAAEAEAAkAgAAAIASAAAAAAAAACBAAAAAAAAAAAAAAAABAEAASAAwAAAAAAAiAAAAAAAABAIEAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAABAAAAAAAQAAAE%22%2C%222~61.89.122.161.184.196.230.314.442.445.494.550.576.827.1029.1033.1046.1047.1051.1097.1126.1166.1301.1342.1415.1725.1765.1942.1958.1987.2068.2072.2074.2107.2213.2219.2223.2224.2328.2331.2387.2416.2501.2567.2568.2575.2657.2686.2778.2869.2878.2908.2920.2963.3005.3023.3126.3234.3235.3253.3309.3731.6931.8931.13731.15731.33931~dv.%22%2C%22E7C28E42-3C5E-41AB-AB30-A6C940FA6C14%22%5D%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%227f8eb31e-b441-48af-9070-edef29f0ab1d%5C%22%2C%5B1770472636%2C212000000%5D%5D%22%5D%5D%5D',
                    '__gads': 'ID=0d42cc2cf63f9a23:T=1770472630:RT=1770512247:S=ALNI_MbE_vddkiRnECnMkWaXJ_Sfzl4mqg',
                    '__gpi': 'UID=0000131254a85703:T=1770472630:RT=1770512247:S=ALNI_MZA9g7pgKD2A3dynTJcMrnY6ezvFw',
                    '__eoi': 'ID=0e5d93d4c8fd02ee:T=1770472630:RT=1770512247:S=AA-AfjZGthmJ_H6IJzJls1GJZZxv',
                    'FCNEC': '%5B%5B%22AKsRol_dpbs00AvkTPvr6tEXMXhCVyJ0HQleflrK4qfTRCQICnzFFsKyImXXUA0ow_nleHHJopiM0WnWNcv1PZtNegu5-IPU6FCpQrYY3-l9tcOuCeuzQZl-DXFAkJwyN7X8lv77nBi3ghFUmZ-472Qi93v1Pt8K8g%3D%3D%22%5D%5D',
                }

                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                    'cache-control': 'max-age=0',
                    'priority': 'u=0, i',
                    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Microsoft Edge";v="144"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0',
                    # 'cookie': 'nuxt-session=Fe26.2**f0e406bcc05cd71e99ec81ddefadb9b36aca2a692b0ac40279855f7f3bb3ab28*3sTC-ndjR7s2GmXHvlvQuA*ppcRjzv0u8IUwz7Xe17jx32rMhDuukkI3CnjJ8vhlz8gOuWKz594k4Av2XetOGlahFAJTJx6ti-7UC1ae4ghaX11BKTVJKcT9mFTugYhCsk1RPPj4KrM47Rv9zPOkbZc**158aeafd34f349434362cf1b5ed2b97ce7889eebfd5756f3350533a00ad5ed78*Hs7XLDDcITZgZp2wUCSBE6djD0YvYTHp8v20j31nKkA; i18n_redirected=zh; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CQfQQUAQfQQUAEsACBZHCRFoAP_gAEPgAARoK1IB_C7EbCFCiDJ3IKMEMAhHABBAYsAwAAYBAwAADBIQIAQCgkEYBASAFCACCAAAKASBAAAgCAAAAUAAIAAFAABAAAwAIBAIIAAAgAAAAEAIAAAACIAAEQCAAAAEAEAAkAgAAAIASAAAAAAAAACBAAAAAAAAAAAAAAAABAEAAQAAQAAAAAAAiAAAAAAAABAIAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAABAAAAAAAQWEQD-F2I2EKFEGCuQUYIYBCuACAAxYBgAAwCBgAAGCQgQAgFJIIkCAEAIEAAEAAAQAgCAABQEBAAAIAAAAAqAACAABgAQCAQAIABAAAAgIAAAAAAEQAAIgEAAAAIAIABABAAAAQAkAAAAAAAAAECAAAAAAAAAAAAAAAAAAIAAEABgAAAAAABEAAAAAAAACAQIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAA.ILCIB_C7EbCFCiDJ3IKMEMAhXABBAYsAwAAYBAwAADBIQIAQCkkEaBASAFCACCAAAKASBAAAoCAgAAUAAIAAVAABAAAwAIBAIIEAAgAAAQEAIAAAACIAAEQCAAAAEAEAAkAgAAAIASAAAAAAAAACBAAAAAAAAAAAAAAAABAEAASAAwAAAAAAAiAAAAAAAABAIEAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAABAAAAAAAQAAAE%22%2C%222~61.89.122.161.184.196.230.314.442.445.494.550.576.827.1029.1033.1046.1047.1051.1097.1126.1166.1301.1342.1415.1725.1765.1942.1958.1987.2068.2072.2074.2107.2213.2219.2223.2224.2328.2331.2387.2416.2501.2567.2568.2575.2657.2686.2778.2869.2878.2908.2920.2963.3005.3023.3126.3234.3235.3253.3309.3731.6931.8931.13731.15731.33931~dv.%22%2C%22E7C28E42-3C5E-41AB-AB30-A6C940FA6C14%22%5D%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%227f8eb31e-b441-48af-9070-edef29f0ab1d%5C%22%2C%5B1770472636%2C212000000%5D%5D%22%5D%5D%5D; __gads=ID=0d42cc2cf63f9a23:T=1770472630:RT=1770512247:S=ALNI_MbE_vddkiRnECnMkWaXJ_Sfzl4mqg; __gpi=UID=0000131254a85703:T=1770472630:RT=1770512247:S=ALNI_MZA9g7pgKD2A3dynTJcMrnY6ezvFw; __eoi=ID=0e5d93d4c8fd02ee:T=1770472630:RT=1770512247:S=AA-AfjZGthmJ_H6IJzJls1GJZZxv; FCNEC=%5B%5B%22AKsRol_dpbs00AvkTPvr6tEXMXhCVyJ0HQleflrK4qfTRCQICnzFFsKyImXXUA0ow_nleHHJopiM0WnWNcv1PZtNegu5-IPU6FCpQrYY3-l9tcOuCeuzQZl-DXFAkJwyN7X8lv77nBi3ghFUmZ-472Qi93v1Pt8K8g%3D%3D%22%5D%5D',
                }

                # response = requests.get(ss_url, cookies=cookies, headers=headers,timeout=8)
                if proxy_ports==0:
                    response = requests.get(ss_url, headers=headers,timeout=(18,18)).text
                else:
                    response = requests.get(ss_url, headers=headers,proxies=proxies,timeout=(18,18),verify=False).text
                # print(response)
                if 'Just a moment' in response:
                    # response = Drission_get_Page(ss_url)
                    pass
                break
            except Exception as err:
                # traceback.print_exc()
                cmd_on_color.printRed(f"获取网站{ss_url}源代码出错，具体原因为：{err}")
                pass
            if np1 > 18:
                cmd_on_color.printRed(f'获取网站{ss_url}源代码最终出错，请检测！')
                # win32api.MessageBox(None, f'获取网站{url}源代码最终出错，请检测！', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
                break
            np1 += 1
            time.sleep(8)
        if response != -1:
            break
    soup = BeautifulSoup(str(response), 'html.parser')  # 文档对象
    # print(soup)
    # 2. 定位__NUXT_DATA__脚本标签（目标Base64串在这个标签里）
    nuxt_script = soup.find('script', id='__NUXT_DATA__')
    if not nuxt_script:
        print("未找到__NUXT_DATA__脚本标签")
    else:
        # 3. 提取脚本内的JSON数据
        nuxt_data_str = nuxt_script.string.strip()
        try:
            # 解析JSON数组（__NUXT_DATA__是数组格式）
            # nuxt_datas = json.loads(nuxt_data_str)
            for i,nuxt_data in enumerate(json.loads(nuxt_data_str)):
                # print('nuxt_data315',nuxt_data)
                if "'url': 392" in str(nuxt_data):
                    base64_str = json.loads(nuxt_data_str)[i+1]
                    return base64_str
            else:
                print("未找到目标Base64串")

        except json.JSONDecodeError as e:
            print(f"JSON解析失败：{e}")

    # 备用方案：如果上述方法失效，直接用正则全局匹配Base64串
    def extract_base64_by_regex(html_str):
        # 匹配以dmxlc3M6Ly8开头的Base64串（长度很长）
        pattern = re.compile(r'dmxlc[A-Za-z0-9+/=]+')
        matches = pattern.findall(html_str)
        if matches:
            return matches[0]  # 返回第一个匹配的长Base64串
        return None

    # 调用备用方案（可选）
    base64_backup = extract_base64_by_regex(str(response))
    if base64_backup:
        print("\n=== 备用方案提取的Base64串 ===")
        # print(base64_backup)
        return base64_backup



def get_config_informationurl1(timeout=2):
    http = urllib3.PoolManager()
    webpage = ''
    yaml_vpn_url = ''
    code_vpn = ''
    ss = ''
    n = 0
    proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}
    while True:
        print('使用连接1进行更新！')
        try:
            if n > 2:
                print('使用AI_all_auto代理88')

                webpage = requests.get(url1, headers=headers, timeout=8, proxies=proxies)
                data = webpage.content
                # data = html.data.decode()
                code = BeautifulSoup(data, 'html.parser')
                # print(code)

                for i, url_vpn in enumerate(code.find_all('h2')):
                    # print('url_vpn22',url_vpn)
                    if i == 0:
                        href_url = url_vpn.find('a').get('href')
                        print('href_url528', href_url)
                        # time.sleep(99)
                        # html = http.request('GET', href_url, timeout=8, headers=headers,proxies=proxies)
                        # data = html.data.decode()
                        data = requests.get(href_url, headers=headers, timeout=8, proxies=proxies).text
                        code_vpn = BeautifulSoup(data, 'html.parser')
            else:
                print('不使用代理')
                webpage = requests.get(url1, headers=headers, timeout=8)
                data = webpage.content
                # data = html.data.decode()
                code = BeautifulSoup(data, 'html.parser')
                # print(code)
                yaml_vpn_url = ''
                code_vpn = ''
                ss = ''
                for i, url_vpn in enumerate(code.find_all('h2')):
                    # print('url_vpn22',url_vpn)
                    if i == 0:
                        href_url = url_vpn.find('a').get('href')
                        print('href_url528', href_url)
                        # time.sleep(99)
                        # html = http.request('GET', href_url, timeout=8, headers=headers)
                        # data = html.data.decode()
                        data = requests.get(href_url, headers=headers, timeout=8, proxies=proxies).text
                        code_vpn = BeautifulSoup(data, 'html.parser')
            link_url1_successful = '连接1成功！'
            print(link_url1_successful)
            break

        except Exception as err:
            print(err)
            print('连接1错误，2秒后重试！')
            time.sleep(2)
        # print(n)
        if n >= 8:
            # os.system('python SS1_ip2.py')
            break
        n += 1
    # print('code_vpn705',code_vpn)
    # time.sleep(888)
    # for i,yaml_vpn in enumerate(code_vpn.find_all(class_ = 'md-fences md-end-block ty-contain-cm modeLoaded')):
    for div in code_vpn.find_all('div'):
        ss_url = div.get_text(strip=True)

        if ss_url.endswith('.txt') and ss_url.startswith('http'):
            print('ss_url718',ss_url)
            # print('ss_url710',ss_url)#https://v2rayse.com/fs/public/20260208/kdfbypk.txt
            ss = get_ss(ss_url)
            # print('562ss',ss)
        # if 'yaml' in yaml_vpn.text :
        #     yaml_vpn_url = yaml_vpn.text.split('即可更新订阅链接')[-1]
        #     print(yaml_vpn_url)
    # print('562ss', ss)
    b = bytes(ss, encoding='utf-8')
    b64 = base64.b64decode(b).decode().split('\n')
    # print(b64)
    res_list = []
    for i,sss in enumerate(b64 ):
        # print(i)
        # print('sss522',sss)
        if 'ss:' in sss[0:3] :
            print('sss227',sss)
            res_list.append(sss)
    congfig_list = []
    # print(res_list)
    plugin = ''
    for vpn_config in res_list :#ss://YWVzLTI1Ni1jZmI6YW1hem9uc2tyMDU=@35.90.10.174:443#%F0%9F%87%BA%F0%9F%87%B8_US_%E7%BE%8E%E5%9B%BD
        # if 'type: ss' in vpn_config :
        #     server = vpn_config.split('#')[0].split('@')[-1].split(':')[0]
        #     server_port = vpn_config.split('#')[0].split('@')[-1].split(':')[1]
        #     ss_s = vpn_config.split('ss://')[-1].split('=')[0] + '=='#YWVzLTI1Ni1jZmI6YW1hem9uc2tyMDU
        #     print('ss_s212',ss_s)
        #     b = bytes(ss_s, encoding='utf-8')
        #     b64 = base64.b64decode(b).decode(errors='replace')
        #     password = b64.split(':')[-1]
        #     method = b64.split(':')[0]
        #     remarks = vpn_config.split('#')[1]
            result = parse_ss_url(vpn_config)
            if result:
                method = result['method'].rstrip()
                password = result['password'].rstrip()
                server = result['server'].rstrip()
                server_port = result['port'].rstrip()
                remarks = result['remark'].rstrip()
                # print("加密方法:", result['method'])
                # print("密码:", result['password'])
                # print("服务器:", result['server'])
                # print("端口:", result['port'])
                # print("备注:", result['remark'])
                if 'remark_info' in result:
                    # print("\n备注解析:")
                    if 'prefix' in result['remark_info']:
                        print("前缀:", result['remark_info']['prefix'])
                    if 'location' in result['remark_info']:
                        print("位置:", result['remark_info']['location'])
                    if 'bandwidth' in result['remark_info']:
                        print("带宽:", result['remark_info']['bandwidth'])
                    if 'full_remark' in result['remark_info']:
                        print("完整备注:", result['remark_info']['full_remark'])

                if result['plugin']:
                    plugin = result['plugin']
                    print("\n插件信息:", result['plugin'])
                    plugin_name,plugin_params = extract_and_decode_plugin_params(plugin)
                    plugin = f''',
          "plugin": "{plugin_name}",
          "plugin_opts": "{plugin_params}",
'''
                else:
                    plugin = ''
                # print("-" * 50)
            else:
                method = ''
                password = ''
                server = ''
                server_port = ''
                remarks = ''
                print(f"无法解析URL: {vpn_config}")
                print("-" * 50)
            # print(server, server_port, password, method,remarks)
            if server != '':
                congfig_ = '''
    "server": "{0}",
    "server_port": {1},
    "password": "{2}",
    "method": "{3}",
    "remarks": "{4}",
    "timeout": {5}
    {6}
        '''.format(server, server_port, password, method,remarks,timeout,plugin)
                congfig_list.append('{' + congfig_ + '}')
            # congfig_list.append(congfig_)
    # configs = ','.join(congfig_list)
    # config = get_config(configs)

    print('get_config_informationurl1函数获得的节点SS数目为：', len(congfig_list))
    return congfig_list





def get_config_informationurl2(timeout=2):
    # http = urllib3.PoolManager()
    reg = ''
    soup = ''
    n = 1
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive"  # 保持长连接，避免频繁断开
}
    congfig_list = []
    res_list = []
    proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
    for i,url2 in enumerate(url2_list):
        if 'hello-world-1989' in url2 or 'kamaji' in url2 or 'yoyapai' in url2:
            res_list+= url22_get_ss_list(headers,url2,url2_source_list[i])
        else:
            while True:
                print(f'使用连接2:{url2}进行更新！')
                try:
                    if n > 2:
                        print('使用AI_all_auto代理88')

                        try:
                            reg = requests.get(url2_source_list[i], headers=headers, timeout=8, proxies=proxies).text
                        except:
                            traceback.print_exc()
                            reg = requests.get(url2, headers=headers, timeout=8, proxies=proxies).text

                    else:
                        print('不使用代理')
                        try:
                            reg = requests.get(url2, headers=headers, timeout=8).text
                        except:
                            traceback.print_exc()
                            reg = requests.get(url2_source_list[i], headers=headers, timeout=8).text
                    link_url2_successful = '连接2成功！'
                    print(link_url2_successful)
                    # print(soup)
                    break
                except Exception as err:
                    print(err)
                    print('连接2错误，2秒后重试！')
                    time.sleep(2)
                # print(n)
                if n >= 8:
                    # os.system('python SS1_ip2.py')
                    break
                n += 1
            # print('reg631',reg)
            soup = BeautifulSoup(reg, 'html.parser')
            # print('soup639',soup)

            # print('soup672',soup)
            if 'clashgithub' in url2:
                for all_node in soup.find('pre').text.split('\n'):
                    if 'ss:' in str(all_node)[0:3]:
                        res_list.append(all_node)
                pass
            else:
                if '<!DOCTYPE html>' in str(soup):
                    codes = soup.find_all('code')
                    for ii, code_ in enumerate(codes):
                        if ii == 1:
                            b64_https_ = code_.text.rstrip()
                            print('soup_646', b64_https_)
                            n2 = 0
                            while True:
                                print(f'使用连接{b64_https_}进行解析！')
                                try:
                                    if n2 > 2:
                                        print('使用AI_all_auto代理88')
                                        proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
                                        soup = requests.get(b64_https_, headers=headers, timeout=8, proxies=proxies).text
                                    else:
                                        print('不使用代理')
                                        soup = requests.get(b64_https_, headers=headers, timeout=8).text
                                    link_url1_successful = f'连接{b64_https_}成功！'
                                    print(link_url1_successful)
                                    break

                                except Exception as err:
                                    print(err)
                                    print(f'连接{b64_https_}错误，2秒后重试！')
                                    time.sleep(2)
                                # print(n)
                                if n2 >= 8:
                                    break
                                n2 += 1
                # print('soup898',soup)
                else:
                    for all_str in soup.text.split('\n'):
                        if 'absslk' in all_str:
                            url2_sub = all_str
                            try:
                                soup = requests.get(url2_sub, headers=headers, timeout=8).text
                            except:
                                traceback.print_exc()
                                soup = requests.get(url2_sub, headers=headers, timeout=8, proxies=proxies).text
                            break
                        if 'mcsslk' in all_str:
                            url2_sub = all_str
                            try:
                                soup = requests.get(url2_sub, headers=headers, timeout=8).text
                            except:
                                traceback.print_exc()
                                soup = requests.get(url2_sub, headers=headers, timeout=8, proxies=proxies).text
                            break


                try:
                    b = bytes(str(soup), encoding='utf-8')
                    b64 = base64.b64decode(b).decode().split('\n')
                    for i,sss in enumerate(b64):
                        if 'ss:' in sss[0:3] :
                            res_list.append(sss)
                except:
                    traceback.print_exc()
                    pass
    for vpn_config in res_list :
        # server = vpn_config.split('#')[0].split('@')[-1].split(':')[0].rstrip() #nn.auozzjs.lol
        # server_port = vpn_config.split('#')[0].split('@')[-1].split(':')[1].rstrip() #40724
        # if '?' in server_port :
        #     server_port = server_port.split('?')[0].rstrip()
        # ss_s = vpn_config.split('ss://')[-1].split('@')[0] + '=='#YWVzLTI1Ni1jZmI6YW1hem9uc2tyMDU
        # # print(server, server_port, password, method, remarks)
        # b = bytes(ss_s, encoding='utf-8')
        # b64 = base64.b64decode(b).decode()
        # password = b64.split(':')[-1].rstrip()
        # method = b64.split(':')[0].rstrip()
        # remarks = vpn_config.split('#')[1].rstrip()
        # # print(server, server_port, password, method,remarks)
        print('vpn_config1137',vpn_config)
        result = parse_ss_url(vpn_config)
        if result:
            method = result['method'].rstrip()
            password = result['password'].rstrip()
            server = result['server'].rstrip()
            server_port = result['port'].rstrip()
            remarks = result['remark'].rstrip()

            print("1146加密方法:", result['method'])
            print("密码:", result['password'])
            print("服务器:", result['server'])
            print("端口:", result['port'])
            print("备注:", result['remark'])
            if 'remark_info' in result:
                print("\n备注解析:")
                if 'prefix' in result['remark_info']:
                    print("前缀:", result['remark_info']['prefix'])
                if 'location' in result['remark_info']:
                    print("位置:", result['remark_info']['location'])
                if 'bandwidth' in result['remark_info']:
                    print("带宽:", result['remark_info']['bandwidth'])
                if 'full_remark' in result['remark_info']:
                    print("完整备注:", result['remark_info']['full_remark'])

            if result['plugin']:
                plugin = result['plugin']
                print("\n插件信息:", result['plugin'])
                plugin_name, plugin_params = extract_and_decode_plugin_params(plugin)
                plugin = f''',
                  "plugin": "{plugin_name}",
                  "plugin_opts": "{plugin_params}",
        '''
            else:
                plugin = ''
            print("-" * 50)
        else:
            method = ''
            password = ''
            server = ''
            server_port = ''
            remarks = ''
            print(f"无法解析URL: {vpn_config}")
            print("-" * 50)
        # print(server, server_port, password, method,remarks)
        if server != '':
            congfig_ = '''
    "server": "{0}",
    "server_port": {1},
    "password": "{2}",
    "method": "{3}",
    "remarks": "{4}",
    "timeout": {5}
    '''.format(server, server_port, password, method,remarks,timeout)
            congfig_list.append('{' + congfig_ + '}')
    print('get_config_informationurl2函数获得的节点SS数目为：', len(congfig_list))
    return congfig_list


def get_config_informationurl3(timeout=2):
    http = urllib3.PoolManager()
    html = ''
    soup = ''
    n = 0
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}
    while True:
        print('使用连接3进行更新！')
        try:
            # html = http.request('GET', url3, timeout=29, headers=headers)
            # link_url1_successful = '连接3成功！'
            # print(link_url1_successful)
            # break
            proxy_port = '88'
            # proxy_port = '10802'
            # url3 = 'https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7'

            # rsp = http.request('GET', url3, timeout=28, headers=headers, proxies=proxies)
            if 2< n <=6:
                print('不走代理')
                reg = requests.get(url3, headers=headers, timeout=8).text
            elif 6<n<=8:
                print('走代理……端口：' + proxy_port)
                proxies = {"http": "socks5h://127.0.0.1:" + str(proxy_port), "https": "socks5h://127.0.0.1:" + str(proxy_port)}
                reg = requests.get(url3, headers=headers, timeout=8, proxies=proxies).text
            else:
                print(f'不走代理{n}')
                reg = requests.get(url8, headers=headers, timeout=8).text
            soup = BeautifulSoup(reg, 'html.parser')
            link_url3_successful = '连接3成功！'
            print(link_url3_successful)
            # print(soup)
            break
        except Exception as err:
            print(err)
            print('连接3错误，2秒后重试！')
            time.sleep(2)
        # print(n)
        if n > 8:
            # os.system('python SS1_ip2.py')
            break
        n += 1

    # data = html.data.decode()
    # code = BeautifulSoup(data, 'html.parser')
    # print(data)
    # time.sleep(99)
    # print('soup479',soup)
    res_list = []
    if '<!DOCTYPE html>' in str(soup):#9
        codes = soup.find_all('code')

        for code in codes:
            # print('code482', code)
            if 'ss:' in str(code)[0:3] :
            # if 'ss:' in code.text.strip()[0:3]:
                # print('code489',code)
                res_list = code.text.strip().split('\n')
                # print('res_list716',res_list)
                break

    else:
        for all_node in str(soup).split('\n'):
            if 'ss:' in str(all_node)[0:3]:
                res_list.append(all_node)
    # time.sleep(188)
    # b = bytes(str(soup), encoding='utf-8')
    # b64 = base64.b64decode(b).decode().split('\n')

    # print(b64)
    # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
    #     f.write('')
    # with open(os.getcwd() + r'\ss1.txt', 'w+', encoding='utf-8') as f:
    #     f.write('')
    # f.close()
    # res_list = []
    ss_txt_list = []

    # for i, sss in enumerate(b64):
    #     # print(i)
    #     # print(sss[0:3])
    #     if 'ss:' in sss[0:3]:
    #         # print(sss)
    #         res_list.append(sss)
    #         ss_txt_list.append('\n' + sss)
            # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
            #     f.write('\n' + sss)
            # with open(os.getcwd() + r'\ss1.txt', 'w+', encoding='utf-8') as f:
            #     f.write('\n' + sss)
            # f.close()
    congfig_list = []
    password = method = remarks = ''
    # print('res_list518',res_list)
    vpn_config_list = []
    plugin = ''
    for i,vpn_config in enumerate(res_list):
        # print('vpn_config518', i,vpn_config)
        # if 'ss://' in str(vpn_config) and 'vless://' not in vpn_config and 'vmess://' not in vpn_config:
        if 'ss:' in str(vpn_config)[0:3] :
            # print('vpn_config520',vpn_config)
            vpn_config_list.append(vpn_config)
            result = parse_ss_url(vpn_config)
            # print('result522',result)
            if result:
                method = result['method'].rstrip()
                password = result['password'].rstrip()
                server = result['server'].rstrip()
                server_port = result['port'].rstrip()
                remarks = result['remark'].rstrip()
                print("加密方法:", result['method'])
                print("密码:", result['password'])
                print("服务器:", result['server'])
                print("端口:", result['port'])
                print("备注:", result['remark'])
                if 'remark_info' in result:
                    print("\n备注解析:")
                    if 'prefix' in result['remark_info']:
                        print("前缀:", result['remark_info']['prefix'])
                    if 'location' in result['remark_info']:
                        print("位置:", result['remark_info']['location'])
                    if 'bandwidth' in result['remark_info']:
                        print("带宽:", result['remark_info']['bandwidth'])
                    if 'full_remark' in result['remark_info']:
                        print("完整备注:", result['remark_info']['full_remark'])

                if result['plugin']:
                    plugin = result['plugin']
                    print("\n插件信息:", result['plugin'])
                    plugin_name, plugin_params = extract_and_decode_plugin_params(plugin)
                    plugin = f''',
                              "plugin": "{plugin_name}",
                              "plugin_opts": "{plugin_params}",
                    '''
                else:
                    plugin = ''
                print("-" * 50)
            else:
                method = ''
                password = ''
                server = ''
                server_port = ''
                remarks = ''
                print(f"无法解析URL: {vpn_config}")
                print("-" * 50)
            # # ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo2NzMyYzRiNC0yZTAwLTQyOGQtYWZjZi1jMzRhODM5NGUxMTY@nn.auozzjs.lol:40724#%E5%89%A9%E4%BD%99%E6%B5%81%E9%87%8F%EF%BC%9A63.68%20GB
            # # if 'type: ss' in vpn_config :
            # #     print(vpn_config)
            # server = vpn_config.split('#')[0].split('@')[-1].split(':')[0]  # nn.auozzjs.lol
            # server_port = vpn_config.split('#')[0].split('@')[-1].split(':')[1]  # 40724
            # if '?' in server_port:
            #     server_port = server_port.split('?')[0]
            # ss_s = vpn_config.split('ss://')[-1].split('@')[0] + '=='  # YWVzLTI1Ni1jZmI6YW1hem9uc2tyMDU
            # # print(server, server_port, password, method, remarks)
            # b = bytes(ss_s, encoding='utf-8')
            # b64 = base64.b64decode(b).decode()
            # password = b64.split(':')[-1]
            # method = b64.split(':')[0]
            # remarks = vpn_config.split('#')[1]
            # print(server, server_port, password, method,remarks)
            if server != '':
                congfig_ = '''
    "server": "{0}",
    "server_port": {1},
    "password": "{2}",
    "method": "{3}",
    "remarks": "{4}",
    "timeout": {5}
        '''.format(server, server_port, password, method, remarks,timeout,plugin)
                congfig_list.append('{' + congfig_ + '}')
            # congfig_list.append(congfig_)
        # configs = ','.join(congfig_list)
        # config = get_config(configs)
        # print(congfig_list)
    # print('vpn_config_list578',vpn_config_list)
    print('get_config_informationurl3函数获得的节点SS数目为：', len(congfig_list))
    return congfig_list


def get_config_informationurl3_old():
    http = urllib3.PoolManager()
    html = ''
    n = 1
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}
    while True:
        print('使用连接3进行更新！')
        try:
            html = http.request('GET', url3, timeout=29, headers=headers)
            link_url3_successful = '连接3成功！'
            print(link_url3_successful)
            break

        except Exception as err:
            print(err)
            print('连接3错误，2秒后重试！')
            time.sleep(2)
        # print(n)
        if n >= 2:
            # os.system('python SS1_ip2.py')
            break
        n += 1

    data = html.data.decode()
    # code = BeautifulSoup(data, 'html.parser')
    print('data365',data)
    # time.sleep(99)
    b = bytes(data, encoding='utf-8')
    b64 = base64.b64decode(b).decode(errors='replace').split('\n')

    # print(b64)
    # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
    #     f.write('')
    # with open(os.getcwd() + r'\ss1.txt', 'w+', encoding='utf-8') as f:
    #     f.write('')
    # f.close()
    res_list = []
    ss_txt_list = []
    for i,sss in enumerate(b64):
        # print(i)
        # print(sss[0:3])
        if 'ss:' in sss[0:3] :
            # print(sss)
            res_list.append(sss)
            ss_txt_list.append('\n' + sss)
            # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
            #     f.write('\n' + sss)
            # with open(os.getcwd() + r'\ss1.txt', 'w+', encoding='utf-8') as f:
            #     f.write('\n' + sss)
            # f.close()
    congfig_list = []
    password= method= remarks = ''
    for vpn_config in res_list :
        #ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo2NzMyYzRiNC0yZTAwLTQyOGQtYWZjZi1jMzRhODM5NGUxMTY@nn.auozzjs.lol:40724#%E5%89%A9%E4%BD%99%E6%B5%81%E9%87%8F%EF%BC%9A63.68%20GB
        # if 'type: ss' in vpn_config :
            server = vpn_config.split('#')[0].split('@')[-1].split(':')[0]#nn.auozzjs.lol
            server_port = vpn_config.split('#')[0].split('@')[-1].split(':')[1]#40724
            ss_s = vpn_config.split('ss://')[-1].split('@')[0] + '=='#YWVzLTI1Ni1jZmI6YW1hem9uc2tyMDU
            # print(server, server_port, password, method, remarks)
            b = bytes(ss_s, encoding='utf-8')
            b64 = base64.b64decode(b).decode()
            password = b64.split(':')[-1]
            method = b64.split(':')[0]
            remarks = vpn_config.split('#')[1].replace('\n','')
            # print(server, server_port, password, method,remarks)
            congfig_ = '''
      "server": "{0}",
      "server_port": {1},
      "password": "{2}",
      "method": "{3}",
      "plugin": "[]",
      "plugin_opts": "[]",
      "plugin_args": "[]",
      "remarks": "{4}",
      "timeout": 5
    '''.format(server, server_port, password, method,remarks)
            congfig_list.append('{' + congfig_ + '}')
            # congfig_list.append(congfig_)
    # configs = ','.join(congfig_list)
    # config = get_config(configs)
    return congfig_list

def get_config_informationurl(local_port=10801):
    congfig_list1 = []
    congfig_list2 = []
    congfig_list3 = []
    try:

        congfig_list1 = get_config_informationurl1()
        pass
    except:
        traceback.print_exc()
    try:
        congfig_list2 = get_config_informationurl2()
    except:
        traceback.print_exc()
    try:
        congfig_list3 = get_config_informationurl3()
    except:
        traceback.print_exc()

    # config, congfig_list_SS2 = get_config_informationurl_SS2()
    congfig_list_SS2 = []

    congfig_list = congfig_list1 + congfig_list2 + congfig_list3 + congfig_list_SS2
    print(f'{type_}总共的列表数目为：{len(congfig_list)}')
    if len(congfig_list) != 0:
        configs = ','.join(list(set(congfig_list)))
        # print('configs722',configs)
        config = get_config(configs,local_port)
        return config



def get_config(configs,local_port=10801):
    config_head = '''
{
    "servers": [
'''

    config_core = f'''

    {configs}

'''
    config_tail = '''
    ],
    "local_port": 88,
    "local_address": "127.0.0.1"
}    
'''
    config = config_head + config_core + config_tail.replace('88',str(local_port))
    return config

def get_config_old(configs,local_port=10801):
    config1 = '''
{
  "version": "4.1.10.0",
  "configs": [
    '''
    config2 = configs
    config3= '''
    
  ],
  "strategy": "com.shadowsocks.strategy.balancing",
  "index": -1,
  "global": false,
  "enabled": false,
  "shareOverLan": false,
  "isDefault": false,
  "isIPv6Enabled": false,
  "localPort": 10801,
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


def main_proxy(local_port=10801):
    download_file(f"http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/{type_}_configs_port{local_port}.json", f"{type_}_configs_port{local_port}.json")
    download_file(f"http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/{type_}_configs_port88.json", f"{type_}_configs_port88.json")
    time.sleep(2)

    # 启动监控进程
    subprocess.Popen([sys.executable, "monitor.py", str(pid), f"{type_}"])
    kill_exe()
    cmd_on_color.printCya(f'++++++++++++++++++++++++++++++++启动{type_}中，请耐心等待............++++++++++++++++++++++++++++++++')
    n=0
    while True:
        try:
            state_ = start_exe(local_port,err_node_number=n+1)
            print('state_1573',state_,n)
            # time.sleep(188)
            # break
            if f'不可以上网' in state_ or f'不可知的异常' in state_:
                if n<=2:
                    show_notification(f"端口 {local_port} 链接错误！准备更新配置", f"不可以上网！【第{n+1}次检测)】", "error")
                print(f'代理错误，疑似代理或IP配置有错误？开始重新获取最新IP配置=={type_}')
                config = get_config_informationurl()
                if config:
                    with open(object_name + fr'\{type_}_configs_port{local_port}.json', 'w+', encoding='utf-8') as f:
                        f.write(config.replace('88',str(local_port)))

                    with open(object_name + fr'\{type_}_configs_port88.json', 'w+', encoding='utf-8') as f:
                        f.write(config.replace(str(local_port),'88'))
                    # time.sleep(2)
                    # upload(f"{type_}_configs_port{local_port}.json")
                    # upload(f"{type_}_configs_port88.json")
                print(f'开始杀死进程{exe_name}')
                kill_exe()#exe_name, exe_name_path, object_name
            if state_ == f'有一个在运行，不能同时运行2个':
                def popup():
                    win32api.MessageBox(None, f'有一个在运行，不能同时运行2个{type_}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)

                threading.Thread(target=popup).start()

                break
            print('1599n============',n)
            if n>18:
                n = 0
                download_file(f"http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/{type_}_configs_port{local_port}.json", f"{type_}_configs_port{local_port}.json")
                download_file(f"http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/{type_}_configs_port88.json", f"{type_}_configs_port88.json")
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
                win32api.MessageBox(None, f'1622严重错误:{err}，程序:{type_}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
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
        except :
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
        state,average_speed = download_files.download_file_state('https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif', os.getcwd() + r"\test_speed.gif", '10801')
        if state == '下载失败':
            print('代理错误，疑似代理或IP配置有错误？开始重新获取最新IP配置')
            # config = get_config_informationurl()
            # config = get_config_informationurl1()
            # config = get_config_informationurl3()
            # with open(object_name + '\gui-config.json', 'w+', encoding='utf-8') as f:
            # with open(object_name + f'\{type_}_configs_port10801.json', 'w+', encoding='utf-8') as f:
            #     f.write(config.replace('88','10801'))
            # with open(object_name + f'\{type_}_configs_port88.json', 'w+', encoding='utf-8') as f:
            #     f.write(config.replace('10801','88'))
            print(f'开始杀死进程{exe_name}')
            kill_exe()#exe_name, exe_name_path, object_name
            print(f'开始启动进程{exe_name}')
            # state = start_exe()#exe_name,exe_name_path,object_name
            # if success == f'启动{exe_name}成功':
            #     cmd_on_color.printGre(f'success642==>>{success}')
        else:
            status = '可以上网'
            # with open(os.getcwd() + r'\ss1.txt', 'r+', encoding='utf-8') as f:
            #     old_data = f.read()
            # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
            #     f.write(old_data)
            # f.close()
            status = cmd_on_color.printGre(status)
            cmd_on_color.printGre('此代理可以上网！端口为===============》》》》》》》》》》》》》》》》》》》：10801【Shadowsocks1】')
            break
        if n >= 2:
            status = '不可以上网'
            status = cmd_on_color.printRed(status)
            cmd_on_color.printRed('10801【Shadowsocks1】此代理最终不可以上网！请更换下一个代理！')
            break
        n += 1
    return status,average_speed


def run_exe_old2(local_port, run_type,cmd):
    state = '未知状态'
    final_state = '手动退出'

    print('CMD:', cmd)

    # 日志文件操作优化（预生成路径）
    log_filename = os.path.join(
        object_name_output_log,
        f"{type_}_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(log_filename, 'a', encoding='utf-8') as log_file:
        # 快速写入初始化信息
        log_file.write(f"执行的命令: {cmd}\n\n")
        log_file.flush()

        try:
            print(f"启动 {exe_name}...")
            log_file.write(f"启动 {exe_name}...\n")

            # 关键优化1：使用无缓冲模式（Windows特殊处理）
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=0,  # 完全无缓冲
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            # 共享状态容器（线程安全）
            # state_container = {'value': None, 'lock': threading.Lock(), 'stop': False}
            state_container = {
                'value': None,
                'code': None,  # 数字错误码
                'message': '',  # 详细描述
                'source': '',  # 错误来源(output/network/process)
                'lock': threading.Lock(),
                'stop': False
            }

            # 修改状态更新方式
            def update_state(code, msg, src):
                with state_container['lock']:
                    state_container.update({
                        'code': code,
                        'message': msg,
                        'source': src
                    })

            def get_final_state():
                with state_container['lock']:
                    if state_container['code'] is not None:
                        return f"错误码:{state_container['code']} ({state_container['message']})"

                    if process.returncode == 0:
                        return "成功"

                    # 进程异常但未捕获的情况
                    return f"未知错误:进程返回{process.returncode}"
            # 预加载频繁访问的文件内容（根据实际情况调整）
            goflyway_status_path = os.path.join(object_name, 'goflyway_status.txt')
            port_coincide_path = os.path.join(object_name, f'{type_}_err.txt')

            # 网络检测标志
            network_status = {'alive': True, 'lock': threading.Lock()}

            # 关键新增1：独立网络检测线程
            def network_checker():
                print('18秒后检测网络状态')
                time.sleep(8)#测试
                # time.sleep(18)
                test_url = "http://www.gstatic.com/generate_204"  # 小米检测地址（快速响应）
                # test_urls = [
                #     "http://connect.rom.miui.com/generate_204",  # 小米
                #     "http://www.gstatic.com/generate_204",  # Google
                #     "http://www.qq.com"  # 腾讯（检测302跳转）
                # ]
                while getattr(threading.current_thread(), "do_run", True):
                    print('循环检测网络状态1314')
                    try:
                        proxies = {'http': f'socks5://127.0.0.1:{local_port}',
                                 'https': f'socks5://127.0.0.1:{local_port}'}
                        # 超时设置为3秒（平衡准确性与速度）
                        n_net = 1
                        while True:
                            try:
                                resp = requests.get(test_url, proxies=proxies, timeout=8)
                                print('resp1318status_code', resp.status_code)
                                log_file.write(f"respstatus_code: {resp.status_code}\n\n")
                                with network_status['lock']:
                                    network_status['alive'] = resp.status_code == 204
                                break
                            except Exception as err:
                                # traceback.print_exc()
                                cmd_on_color.printRed(f'请求出错{n_net}次，错误信息：{err}')
                                log_file.write(f"请求出错{n_net}次，错误信息：{err}\n\n")
                                pass
                            if n_net >= 8:
                            # if n_net >= 2:#测试
                                resp = requests.get(test_url, proxies=proxies, timeout=8)
                                print('resp1330status_code', resp.status_code)
                                log_file.write(f"respstatus_code: {resp.status_code}\n\n")
                                with network_status['lock']:
                                    network_status['alive'] = resp.status_code == 204
                            n_net+=1
                    except requests.exceptions.Timeout:
                        print("网络检测超时")
                        update_state(110, "网络检测超时", "network")
                        with network_status['lock']:
                            network_status['alive'] = False
                    except Exception as e:
                        print(f"网络检测未知错误: {e}")
                        update_state(999, f"网络检测未知错误: {e}", "network")
                        with network_status['lock']:
                            network_status['alive'] = False
                    time.sleep(5)  # 每5秒检测一次

            # 启动网络检测线程
            checker_thread = threading.Thread(target=network_checker)
            checker_thread.daemon = True
            checker_thread.do_run = True
            checker_thread.start()

            # 关键优化2：分离输出处理与业务逻辑
            def output_handler(line):
                """实时输出处理（毫秒级响应）"""
                # 快速打印
                print(f'1272->{type_}==>>{line}')
                # 新增网络状态实时判断
                with network_status['lock']:
                    # if not network_status['alive'] and any(err in line for err in ['积极拒绝', '连接尝试失败', '没有正确答复']):
                    if not network_status['alive'] or (' proxied,' in line and ', error:' in line and any(err in line for err in ['积极拒绝', '连接尝试失败', '没有正确答复'])):
                        update_state(100, "目标服务器拒绝连接", "output")
                        # with network_status['lock']:
                        #     network_status['alive'] = False
                        cmd_on_color.printRed(f"网络不通! 即将切换代理==>>{network_status}")
                        log_file.write(f"网络不通! 即将切换代理==>>{network_status}")
                        return '网络不通'
                # 快速错误检测（使用缓存避免频繁IO）
                # if '系统找不到指定的文件' in line or 'json parse error' in line or 'expected ' in line :
                if '系统找不到指定的文件' in line or 'json parse error' in line :
                    if '.exe' in line:
                        win32api.MessageBox(0, f'缺失文件: {exe_name_path}', '错误', win32con.MB_ICONWARNING)
                        return 'EXE缺失'
                    elif '.json' in line:
                        return '配置缺失'
                    else:
                        return '配置格式错误'
                elif '只允许使用一次' in line:
                    with open(port_coincide_path, 'a') as f:
                        f.write(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}||{line}\n")
                    return '端口冲突' if run_type == '所有' else None
                # elif any(err in line for err in ['积极拒绝', '连接尝试失败', '没有正确答复']):
#                 elif any(err in line for err in ['连接尝试失败', '没有正确答复']):
#                     '''
# 1272->SS1==>>2025-05-16T21:30:49.3145596+08:00 ERROR socks5 tcp client handler error: 由于目标计算机积极拒绝，无法连接。 (os error 10061)
# 1272->SS1==>>2025-05-17T10:28:47.6355198+08:00 ERROR socks5 tcp client handler error: 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。 (os error 10060)
#                     '''
#                     update_state(100, "目标服务器拒绝连接", "output")
#                     cmd_on_color.printRed(f"连接失败")
#                     log_file.write(f"连接失败")
#                     return '连接失败'
                return None

            # 关键优化3：高速输出管道（双缓冲队列）
            output_queue = deque(maxlen=100)

            def output_reader():
                """高速读取线程（仅负责填充队列）"""
                while not state_container['stop']:
                    output = process.stdout.readline()
                    if not output and process.poll() is not None:
                        break
                    if output:
                        output_queue.append(output.strip())

            # 启动高速读取线程
            reader_thread = threading.Thread(target=output_reader)
            reader_thread.daemon = True
            reader_thread.start()

            # 关键优化4：主处理循环（每50ms批量处理）
            process_start_time = time.time()
            process_timeout = 10  # 进程启动超时时间
            last_check = time.time()

            while True:

                # 批量处理队列中的消息
                while output_queue:
                    line = output_queue.popleft()
                    # 写入日志（批量模式）
                    log_file.write(line + '\n')
                    # 快速错误检测
                    error_state = output_handler(line)
                    if error_state:
                        cmd_on_color.printRed(f'不可以上网：{error_state}')
                        log_file.write(f'不可以上网：{error_state}' + '\n')
                        with state_container['lock'] :
                        # with network_status['lock']:
                            # state_container['value'] = f'不可以上网：{error_state}'
                            network_status['alive'] = False
                            state_container['value'] = f'不可以上网'
                        break

                # 新增快速失败检查
                with network_status['lock']:
                    if not network_status['alive']:
                        final_state = '不可上网：网络检测失败'
                        break
                with state_container['lock']:
                    if state_container['code'] is not None:
                        final_state = get_final_state()
                        break

                if process.poll() is not None and process.returncode != 0:
                    update_state(process.returncode, f"进程异常退出", "process")
                # 状态检查（每秒4次，减少CPU消耗）
                if time.time() - last_check > 0.25:
                    last_check = time.time()
                    # 进程存活检查（优化版）
                    process_alive = any(p.name() == exe_name for p in psutil.process_iter(['name']))

                    if not process_alive:
                        if time.time() - process_start_time > process_timeout:
                            print(f'启动失败，尝试重启...')
                            ##中途结束exe  也强制重启！
                            # return run_exe(local_port, run_type,cmd)

                # 退出条件判断
                if process.poll() is not None:
                    print('1433',process.poll())
                    break
                if state_container['value']:
                    print('1436',state_container['value'])
                    break
                time.sleep(0.05)  # 50ms间隔

            # 清理线程
            checker_thread.do_run = False
            checker_thread.join(timeout=1)
            state_container['stop'] = True
            reader_thread.join(timeout=1)

            # 最终状态判定
            final_state = state_container['value'] or ('成功' if process.returncode == 0 else f'错误码:{process.returncode}')
            print('final_state1448',final_state)
            # 异步日志清理（不阻塞主线程）
            def async_log_clean():
                try:
                    logs = sorted(os.listdir(object_name_output_log), key=lambda x: os.path.getmtime(os.path.join(object_name_output_log, x)))
                    while len(logs) > 18:
                        os.remove(os.path.join(object_name_output_log, logs.pop(0)))
                except Exception as e:
                    print(f"日志清理失败: {str(e)}")

            threading.Thread(target=async_log_clean).start()
            log_file.write(f"\n{datetime.now()}进程的最终状态: {final_state}\n")
            return final_state

        except Exception as e:
            traceback.print_exc()
            return f'异常: {str(e)}'
        finally:
            print(f"进程结束，状态: {final_state}")
            log_file.write(f"\n结束时间: {datetime.now()}进程结束，状态: {final_state}\n")
            if '错误码:1' in final_state:
                win32api.MessageBox(0, f'缺失文件: {exe_name_path}', '错误', win32con.MB_ICONWARNING)
            if '错误码' in final_state:
                win32api.MessageBox(0, f'未知错误码：{final_state}，程序：{type_}.py', '错误', win32con.MB_ICONWARNING)
def run_exe_old(local_port,run_type):
    # server_address, port, password = read_config()
    success = ''
    cmd = fr'{exe_name_path} -c {object_name}\{type_}_configs_port{local_port}.json'  #sslocal_SS1.exe -c SS1_configs_port10801.json -v
    print('cmd1082',cmd)
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
                    success = f'启动{exe_name}成功'
                    print(f'启动{exe_name}成功')
                    break
                else:
                    print(f'启动{exe_name}失败！准备开始重启！')
                    # win32api.ShellExecute(0, 'open', open_Shadowsocks1, '', '', 0)
                    # state = run_exe(local_port,run_type,cmd)
                time.sleep(2)
                if n >= 2:
                    break
                n += 1
            # 实时读取输出并写入文件和打印到控制台
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    state = f'不可知的异常{process.poll()}，1 表示子进程已经终止'
                    log_file.write(state)
                    print('state1142',state)
                    break
                if output:
                    # state_url, state_url_list = check_proxy_connection(local_port)
                    # print('output.strip()719',output.strip())#AddrInUse, message: "通常每个套接字地址(协议/网络地址/端口)只允许使用一次。" }
                    print(f'{type_}==>>{output.strip()}')
                    with open(object_name + r'\goflyway_status.txt', 'r+', encoding='utf-8') as f:
                        goflyway_status = f.read()# 可以上网    可以退出当前代理，优先选择 goflyway  goflyway_status == '可以上网'
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
                        if run_type=='所有':
                            state = f'有一个在运行，不能同时运行2个'
                            break
                    if '系统找不到指定的文件' in output.strip() or 'json parse error' in output.strip() or 'expected array, boolean, null, number, object, or string'  in output.strip():
                        #expected boolean, null, or string


                    # if 'shadowsocks' not in output.strip() and 'INFO' not in output.strip() and 'build' not in output.strip():
                        cmd_on_color.printRed('代理格式出错！重新写入格式')
                        state = '不可以上网'
                    # if '由于目标计算机积极拒绝' in output.strip() and state_url != '连接成功':#handler error: 由于目标计算机积极拒绝，无法连接。 (os error 10061)
                    if '由于目标计算机积极拒绝' in output.strip() or '连接尝试失败' in output.strip() or '没有正确答复' in output.strip():#handler error: 由于目标计算机积极拒绝，无法连接。 (os error 10061)
                        ###由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败  #不可以上网
                        # error: 你的主机中的软件中止了一个已建立的连接。 (os error 10053)  #这个是可以上网的
                        state = '不可以上网'
                        cmd_on_color.printRed(f'该代理不可以上网，跳出！更换其它代理')
                        break
                    log_file.write(output)
                    log_file.flush()  # 确保每次写入后立即保存到文件
                # 删除多余的log
                log_list = os.listdir(object_name_output_log)
                for i, log_name in enumerate(log_list):
                    if len(log_list) > 18:
                        if i < 18:  # 删除前29个
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
    return plugin_name,plugin_params

def url22_get_ss_list(headers,url22,url22_source):
    soup = ''
    n22 = 0
    while True:
        print(f'使用连接{url22}进行解析！')
        try:
            if n22 > 2:
                print('使用AI_all_auto代理88')
                proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
                soup = requests.get(url22_source, headers=headers, timeout=8, proxies=proxies).text.rstrip()
            else:
                print('不使用代理')
                soup = requests.get(url22, headers=headers, timeout=8).text.rstrip()
            link_url1_successful = f'连接{url22}成功！'
            print(link_url1_successful)
            break

        except Exception as err:
            print(err)
            print(f'连接{url22}错误，2秒后重试！')
            time.sleep(2)
        # print(n)
        if n22 >= 8:
            break
        n22 += 1
    # print('soup1361',soup)
    ss_list = []
    for ss in soup.split('\n'):
        if 'ss:' in ss[0:3] :
            # print('ss2173',ss)
            ss_list.append(ss)
    # print('ss_list1361',ss_list)
    return ss_list

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
    # os.system("taskkill /F /IM sslocal.exe")
    # main_proxy()

    main_proxy_log()
    # get_yaml('https://v2rayse.com/fs/public/20260304/qxfjgkh.yaml')
    # start_exe()
    #sslocal1.exe -s "195.154.54.171:13355" -k "dongtaiwang.com" -b "127.0.0.1:10801" -m "aes-256-gcm"
    #sslocal1.exe -c configs.json
    #D:\客户端集合代理\SS1\sslocal1.exe -c D:\客户端集合代理\SS1\configs.json

    # get_config_informationurl1()
    # get_ss('https://v2rayse.com/fs/public/20260208/kdfbypk.txt')
    # get_config_informationurl2()
    # get_config_informationurl3()
    # get_config_informationurl()


    # print(extract_and_decode_plugin_params('?plugin=v2ray-plugin%3Bmode%3Dwebsocket%3Bmux%3D8%3Bpath%3D%2Futvbnrzejpmt%3Bhost%3Dhkkh11v1.xpmc.cc%3Btls'))
    # print(extract_and_decode_plugin_params('?plugin=obfs-local%3Bobfs%3Dhttp%3Bobfs-host%3D202505081193439-ADTUVtshPJ.download.microsoft.com'))

    pass