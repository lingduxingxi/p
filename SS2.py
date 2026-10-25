#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# import json
import re
import subprocess
import threading
import urllib.parse

import win32con
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

from download_files import download_file
from notification_simulator import show_notification
# from GoflywayTools import check_proxy_connection
from run_port_exe import run_exe
# from upload_node import upload
# 全局变量记录最后成功循环的时间
last_loop_time = time.time()
# 需要排除的加密方式，在这里添加即可
EXCLUDED_METHODS = {
    'chacha20-poly1305',
    'blake3-aes-256-gcm',
    'xchacha20-ietf-poly1305',
    'chacha20',
    '2022-blake3-aes-128-gcm',
}
def watchdog():
    global last_loop_time  # 添加这一行，声明使用全局变量
    while True:
        time.sleep(30)
        current_time = time.time()
        # 使用局部变量避免重复访问全局变量
        last_time = last_loop_time
        if current_time - last_time > 300:  # 5分钟无进展
            print("看门狗: 主线程可能卡住，打印所有线程堆栈:")
            for thread_id, frame in sys._current_frames().items():
                print(f"线程 {thread_id}:")
                try:
                    traceback.print_stack(frame)
                except Exception as e:
                    print(f"打印堆栈时出错: {e}")
            # 将堆栈写入文件
            try:
                with open("watchdog_stack.log", "w") as f:
                    for thread_id, frame in sys._current_frames().items():
                        f.write(f"线程 {thread_id}:\n")
                        traceback.print_stack(frame, file=f)
            except Exception as e:
                print(f"写入日志文件失败: {e}")
# 启动看门狗线程
threading.Thread(target=watchdog, daemon=True).start()
logging.captureWarnings(True)  # 强制取消证书验证警告

url2_list = [
    "https://ghfile.geekertao.top/https://raw.githubusercontent.com/myominn062-svg/mk-studio-vpn-service/main/ss_configs.txt",
]

url2_source_list = [
    "https://raw.githubusercontent.com/myominn062-svg/mk-studio-vpn-service/main/ss_configs.txt",
]

# url2 = "https://cdn.jsdelivr.net/gh/Alvin9999/pac2@latest/SS-Kcptun/ssconfig.txt"
# url1 = "https://a1.trump2023.org/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"#废弃
# url1 = "https://bku8.xyz/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7/"
url3 = "https://s3.dualstack.us-west-2.amazonaws.com/zhifan2/ss.html"
# url2 = "https://tr3.freeair888.club/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7/"
url1 = "https://gitlab.com/zhifan999/fq/-/wikis/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"  #github.com的镜像
url2 = "https://github.com/Alvin9999-newpac/fanqiang/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"

##https://raw.githubusercontent.com/wenxig/dongtai-sub/refs/heads/main/data/sub.txt  自动抓取 Alvin9999的节点

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
        exe_name = f"sslocal_all.exe"
    else:
        exe_name = f"sslocal_{type_}.exe"
    exe_name_path = fr"{object_name}\{exe_name}"
    print(f'开始启动{exe_name}')
    file_path = object_name + fr'\{type_}_configs_port{local_port}.json'  # 替换为实际文件路径
    state = f'不可以上网'
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            print(f"文件 '{file_path}' 存在")
            # state = run_exe(local_port, run_type)
            cmd = fr'{exe_name_path} -c {object_name}\{type_}_configs_port{local_port}.json'  # sslocal_SS2.exe -c SS2_configs_port10802.json -v
            state = str(run_exe(local_port, run_type, cmd, object_name_output_log, type_, exe_name, object_name, exe_name_path,err_node_number,show_notification_state))
            if '表示子进程已经终止' in state or '端口冲突' in state:
                port88_err_num += 1
                print('port88_err_num196', port88_err_num)
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
    cmd_on_color.printCya(f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}||state216=={state}")
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


def validate_params(method, password, server, port):
    # chacha20-ietf-poly1305 91a41f4e02dc hkkh11v1.xpmc.cc 54259
    """参数有效性验证"""
    valid_methods = {'aes-256-gcm', 'aes-128-gcm', 'chacha20',
                     'chacha20-ietf', 'xchacha20', 'rc4-md5',
                     'aes-256-cfb', 'aes-128-cfb', 'plain'}

    try:
        # 验证端口有效性
        port = int(port)
        # if not (1 <= port <= 65535):
        #     print('验证端口有效性',False)
        #     return False
    except:
        return False

    # 验证服务器地址格式
    if not re.match(r'^([\w\-]+\.)*[\w\-]+$', server) and not re.match(r'^\[.*\]$', server):
        print('验证服务器地址格式', False)
        return False

    # 验证加密方法有效性
    # print(method.lower())
    # if method.lower() not in valid_methods:
    #     print('验证加密方法有效性', False)
    #     return False

    # 验证密码非空
    if not password.strip():
        print('验证端口有效性', False)
        return False

    return True




def parse_ss_url(ss_url):
    """解析 Shadowsocks 链接。参数无效、格式错误或解析失败时返回 None。"""
    import base64
    import binascii
    import ipaddress
    import json
    import re
    from urllib.parse import unquote, parse_qs

    INVALID_VALUES = {"", "null", "none", "undefined", "nil"}

    def is_valid_value(value):
        """拒绝空字符串和明显的无效占位值。"""
        return (
            isinstance(value, str)
            and bool(value.strip())
            and value.strip().lower() not in INVALID_VALUES
        )

    def decode_b64(text):
        """解码 Base64 包装层，不对已经识别的密码再次解码。"""
        if not isinstance(text, str):
            return None

        text = unquote(text.strip())
        if not text:
            return None

        candidates = [
            text,
            text.replace("-", "+").replace("_", "/"),
        ]

        for candidate in dict.fromkeys(candidates):
            candidate = re.sub(r"\s+", "", candidate)

            if not candidate or len(candidate) % 4 == 1:
                continue

            candidate += "=" * (-len(candidate) % 4)

            try:
                raw = base64.b64decode(
                    candidate.encode("ascii"),
                    validate=True,
                )
                return raw.decode("utf-8")
            except (ValueError, UnicodeError, binascii.Error):
                continue

        return None

    def parse_host_port(endpoint):
        """解析域名、IPv4、[IPv6]:port，并检查端口范围。"""
        if not isinstance(endpoint, str):
            return None, None

        endpoint = endpoint.strip().split("/", 1)[0]
        if not endpoint:
            return None, None

        if endpoint.startswith("["):
            match = re.fullmatch(r"\[([^\]]+)\]:(\d+)", endpoint)
            if not match:
                return None, None

            host, port_text = match.groups()

            try:
                ipaddress.IPv6Address(host)
            except ValueError:
                return None, None
        else:
            if endpoint.count(":") != 1:
                return None, None

            host, port_text = endpoint.rsplit(":", 1)

        if not port_text.isdigit():
            return None, None

        port = int(port_text)
        if not 1 <= port <= 65535:
            return None, None

        host = host.strip()
        if not host or any(c.isspace() for c in host):
            return None, None

        try:
            host = str(ipaddress.ip_address(host))
        except ValueError:
            if any(c in host for c in "/?#@[]"):
                return None, None

            try:
                host = (
                    host.rstrip(".")
                    .encode("idna")
                    .decode("ascii")
                    .lower()
                )
            except UnicodeError:
                return None, None

            if not host or len(host) > 253:
                return None, None

            for label in host.split("."):
                if (
                    not label
                    or len(label) > 63
                    or label.startswith("-")
                    or label.endswith("-")
                    or not re.fullmatch(r"[A-Za-z0-9-]+", label)
                ):
                    return None, None

        return host, port

    def looks_like_non_ss(text):
        """拒绝误装在 SS 链接中的其他协议 JSON。"""
        if not isinstance(text, str):
            return True

        text = text.lstrip("\ufeff \t\r\n")

        if not text.startswith("{"):
            return False

        try:
            obj = json.loads(text)
            if isinstance(obj, dict):
                keys = {
                    "add", "id", "net", "tls", "v",
                    "ps", "scy", "sni", "alpn",
                }
                if keys.intersection(obj):
                    return True
        except (ValueError, TypeError):
            pass

        return bool(re.match(
            r'^\{\s*"(?:add|id|net|tls|v|ps|scy|sni|alpn)"\s*:',
            text,
            re.IGNORECASE,
        ))

    def valid_method(method):
        """只接受当前 Shadowsocks 客户端支持的加密方式。"""
        if not isinstance(method, str):
            return False

        method = method.strip().lower()

        supported_methods = {
            "plain", "none", "table",
            "rc4-md5", "rc4",

            "aes-128-ctr", "aes-192-ctr", "aes-256-ctr",

            "aes-128-cfb", "aes-128-cfb1",
            "aes-128-cfb8", "aes-128-cfb128",
            "aes-192-cfb", "aes-192-cfb1",
            "aes-192-cfb8", "aes-192-cfb128",
            "aes-256-cfb", "aes-256-cfb1",
            "aes-256-cfb8", "aes-256-cfb128",

            "aes-128-ofb", "aes-192-ofb", "aes-256-ofb",

            "camellia-128-ctr", "camellia-192-ctr",
            "camellia-256-ctr",

            "camellia-128-cfb", "camellia-128-cfb1",
            "camellia-128-cfb8", "camellia-128-cfb128",
            "camellia-192-cfb", "camellia-192-cfb1",
            "camellia-192-cfb8", "camellia-192-cfb128",
            "camellia-256-cfb", "camellia-256-cfb1",
            "camellia-256-cfb8", "camellia-256-cfb128",

            "camellia-128-ofb", "camellia-192-ofb",
            "camellia-256-ofb",

            "chacha20-ietf",

            "aes-128-gcm", "aes-256-gcm",
            "chacha20-ietf-poly1305",

            "2022-blake3-aes-128-gcm",
            "2022-blake3-aes-256-gcm",
            "2022-blake3-chacha20-poly1305",
        }

        return method in supported_methods

    def valid_password(password):
        """
        验证密码是否存在。
        不对密码做 Base64 解码，避免改变合法密码。
        """
        if not isinstance(password, str):
            return False

        password = password.strip()

        if not password or password.lower() in INVALID_VALUES:
            return False

        # 防止将其他协议链接或 JSON 当作密码。
        if password.startswith("{"):
            return False

        if password.lower().startswith((
            "ss://", "ssr://", "vless://",
            "vmess://", "trojan://",
        )):
            return False

        return True

    def parse_auth(auth, depth=0):
        """解析认证字段，优先保留已识别的原始密码。"""
        if not isinstance(auth, str) or depth > 4:
            return None, None

        auth = unquote(auth.strip())

        if not auth or looks_like_non_ss(auth):
            return None, None

        # 优先解析原始 method:password。
        # 一旦匹配成功，不再对 password 进行 Base64 解码。
        if ":" in auth:
            method, password = auth.split(":", 1)
            method = method.strip()
            password = password.strip()

            if valid_method(method) and valid_password(password):
                return method, password

        # 原始认证字段不符合格式，才尝试解码其包装层。
        decoded = decode_b64(auth)
        if not decoded:
            return None, None

        decoded = decoded.strip()

        if looks_like_non_ss(decoded):
            return None, None

        # 解码结果是另一层 SS 链接时，继续识别嵌套格式。
        if decoded.lower().startswith("ss://"):
            inner = decoded[5:].strip()

            if "#" in inner:
                inner = inner.split("#", 1)[0]

            if "?" in inner:
                inner = inner.split("?", 1)[0]

            if "@" in inner:
                inner = inner.rsplit("@", 1)[0]

            return parse_auth(inner, depth + 1)

        # 认证字段解码后，若得到合法的 method:password，
        # 直接保留密码文本，不再对密码单独解码。
        if ":" in decoded:
            method, password = decoded.split(":", 1)
            method = method.strip()
            password = password.strip()

            if valid_method(method) and valid_password(password):
                return method, password

        # 仍无法识别时，继续尝试有限层数的包装。
        if depth < 4:
            return parse_auth(decoded, depth + 1)

        return None, None

    def build_result(auth_part, endpoint, remark="", plugin=""):
        """统一校验所有必要字段，任何一项无效都返回 None。"""
        server, port = parse_host_port(endpoint)

        if not server or port is None:
            return None

        method, password = parse_auth(auth_part)

        if not valid_method(method) or not valid_password(password):
            return None

        return {
            "method": method,
            "password": password,
            "server": server,
            "port": port,
            "remark": remark,
            "plugin": plugin,
        }

    def parse_link(link, depth=0):
        """解析完整 SS URL，支持现代格式、旧格式及嵌套包装。"""
        if depth > 4 or not isinstance(link, str):
            return None

        link = link.strip()

        if not link.lower().startswith("ss://"):
            return None

        body = link[5:].strip()
        if not body:
            return None

        remark = ""

        if "#" in body:
            body, fragment = body.split("#", 1)
            remark = unquote(fragment)

        query = ""
        if "?" in body:
            body, query = body.split("?", 1)

        plugin = ""

        if query:
            try:
                params = parse_qs(query, keep_blank_values=True)
                plugin = params.get("plugin", [""])[0]
            except (ValueError, TypeError):
                return None

        body = body.strip()

        if not body:
            return None

        # SIP002 格式：认证字段 @ 服务器地址:端口
        if "@" in body:
            auth_part, endpoint = body.rsplit("@", 1)

            return build_result(
                auth_part,
                endpoint,
                remark,
                plugin,
            )

        # 旧式格式：整个认证字段和服务器地址一起 Base64 编码。
        decoded = decode_b64(body)

        if not decoded:
            return None

        decoded = decoded.strip()

        if looks_like_non_ss(decoded):
            return None

        # 如果整个解码结果仍是 SS URL，递归解析。
        if decoded.lower().startswith("ss://"):
            result = parse_link(decoded, depth + 1)

            if result is None:
                return None

            if remark:
                result["remark"] = remark

            if plugin:
                result["plugin"] = plugin

            return result

        if "@" not in decoded:
            return None

        auth_part, endpoint = decoded.rsplit("@", 1)

        return build_result(
            auth_part,
            endpoint,
            remark,
            plugin,
        )

    try:
        if not isinstance(ss_url, str):
            return None

        result = parse_link(ss_url)

        if result is None:
            return None

        # 最终安全检查，防止无效参数混入返回结果。
        if (
            not valid_method(result.get("method"))
            or not valid_password(result.get("password"))
            or not isinstance(result.get("server"), str)
            or not result["server"].strip()
            or result["server"].strip().lower() in INVALID_VALUES
            or not isinstance(result.get("port"), int)
            or isinstance(result.get("port"), bool)
            or not 1 <= result["port"] <= 65535
        ):
            return None

        return result

    except Exception:
        return None


def url22_get_ss_list(headers,url22,url22_source,day):
    soup = ''
    n22 = 0
    while True:
        print(f'使用连接{url22}进行解析！')
        try:
            if n22 > 2:
                print('使用AI_all_auto代理88')
                proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
                soup = requests.get(url22_source, headers=headers, timeout=8, proxies=proxies).text.rstrip().replace("<br/>","\n")
            else:
                print('2563不使用代理')
                soup = requests.get(url22, headers=headers, timeout=8).text.rstrip().replace("<br/>","\n")
            with open(fr'{type_}_soup.txt', 'w+', encoding='utf-8') as f:
                f.write(str(soup))
            if 'DOCTYPE html' in  soup:
                pass
            else:
                link_url1_successful = f'912连接{url22}成功！'
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
    if 'kamaji' in url22:

        for ss in soup.split('\n'):
            if 'ss:' in ss[0:3] :
                # if yesterday.strftime("[%Y-%m-%d]") in ss or today.strftime("[%Y-%m-%d]") in ss:
                if day in ss:
                    # print('ss2173',ss)
                    ss_list.append(ss)
    else:
        for ss in soup.split('\n'):
            if 'ss:' in ss[0:3] :
                # print('ss2173',ss)
                ss_list.append(ss)
    # print('ss_list1361',ss_list)
    return ss_list

# 测试解析你的目标链接

def get_config_informationurl1(timeout=2):
    # http = urllib3.PoolManager()
    webpage = ''
    n = 0
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}

    while True:
        print('使用连接1进行更新！')
        try:
            proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
            if 2 < n <= 6:
                print('使用AI_all_auto代理88')
                try:
                    webpage = requests.get(url1, headers=headers, timeout=8, proxies=proxies)
                except:
                    print('不走代理')
                    webpage = requests.get(url2, headers=headers, timeout=8).text
            elif 6 < n < 8:
                print('使用AI_all_auto代理88')
                try:
                    webpage = requests.get(url2, headers=headers, timeout=8, proxies=proxies).text
                except:
                    print('不走代理810')
                    webpage = requests.get(url3, headers=headers, timeout=8).text
            else:
                print('不使用代理517')
                webpage = requests.get(url1, headers=headers, timeout=8)
            link_url1_successful = '连接1成功！'
            print(link_url1_successful)
            break

        except Exception as err:
            print(err)
            print('连接1错误，2秒后重试！')
            time.sleep(2)
        # print(n)
        if n >= 8:
            # os.system('python SS2_ip2.py')

            break
        n += 1
    data = webpage.content
    # data = html.data.decode()
    # code = BeautifulSoup(data, 'html.parser')
    links = re.findall(r'ss://[^\s`"]+', str(data))
    congfig_list = []
    # print(res_list)
    plugin = ''
    # 去掉末尾空白和 \r\n
    res_list = [item.rstrip('\\\\r\\\\n') for item in links]
    # print('res_list565',res_list)
    res_list = list(dict.fromkeys(res_list))
    for vpn_config in res_list:  # ss://YWVzLTI1Ni1jZmI6YW1hem9uc2tyMDU=@35.90.10.174:443#%F0%9F%87%BA%F0%9F%87%B8_US_%E7%BE%8E%E5%9B%BD
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
        if result and not any(
    method in result['method'].lower()
    for method in EXCLUDED_METHODS
):
            method = result['method']
            password = result['password']
            server = result['server']
            server_port = result['port']
            remarks = result['remark']
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
        # print(server, server_port, password, method,remarks)
        congfig_ = '''
    "server": "{0}",
    "server_port": {1},
    "password": "{2}",
    "method": "{3}",
    "remarks": "{4}",
    "timeout": {5}
    {6}
    '''.format(server, server_port, password, method, remarks, timeout, plugin)
        congfig_list.append('{' + congfig_ + '}')
        # congfig_list.append(congfig_)
    # configs = ','.join(congfig_list)
    # config = get_config(configs)
    return congfig_list



def get_config_informationurl2(timeout=2,day="[2026-10-22]"):
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
    for i,url22 in enumerate(url2_list):
        if 'hello-world-1989' in url22 or 'kamaji' in url22 or 'myominn062' in url22:
            res_list+= url22_get_ss_list(headers,url22,url2_source_list[i],day)
        else:
            while True:
                print(f'使用连接2:{url22}进行更新！')
                try:
                    if n > 2:
                        print('使用AI_all_auto代理88')

                        try:
                            reg = requests.get(url2_source_list[i], headers=headers, timeout=8, proxies=proxies).text
                        except:
                            traceback.print_exc()
                            reg = requests.get(url22, headers=headers, timeout=8, proxies=proxies).text

                    else:
                        print('不使用代理')
                        try:
                            reg = requests.get(url22, headers=headers, timeout=8).text
                        except:
                            traceback.print_exc()
                            reg = requests.get(url2_source_list[i], headers=headers, timeout=8).text
                    if 'DOCTYPE html' in reg:
                        pass
                    else:
                        link_url2_successful = '连接2成功！'
                        print(link_url2_successful)
                        # print('1102reg',reg)
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
            soup = BeautifulSoup(reg, 'html.parser').text
            print('soup1117',soup)
            for sss in soup.split():
                if sss[:3] == 'ss:':
                    res_list.append(sss)
            print('1121res_list',res_list)
    res_list = list(dict.fromkeys(res_list))
    with open(fr'{type_}_result.txt', 'w+', encoding='utf-8') as f:
        f.write("")
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
        # print('vpn_config1137',vpn_config)
        result = parse_ss_url(vpn_config)
        with open(fr'{type_}_result.txt', 'a+', encoding='utf-8') as f:
            f.write(f"{vpn_config}\n{result}\n--------------------------------------------------\n\n\n")
        if result and not any(
    method in result['method'].lower()
    for method in EXCLUDED_METHODS
):
            method = result['method'].rstrip()
            password = result['password'].rstrip()
            server = result['server'].rstrip()
            server_port = result['port']
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
            if 2 < n <= 6:
                print('不走代理')
                reg = requests.get(url3, headers=headers, timeout=8).text
            elif 6 < n <= 8:
                print('走代理……端口：' + proxy_port)
                proxies = {"http": "socks5h://127.0.0.1:" + str(proxy_port), "https": "socks5h://127.0.0.1:" + str(proxy_port)}
                reg = requests.get(url3, headers=headers, timeout=8, proxies=proxies).text
            else:
                print('不走代理')
                reg = requests.get(url3, headers=headers, timeout=8).text
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
        if n >= 8:
            # os.system('python SS2_ip2.py')
            break
        n += 1

    # data = html.data.decode()
    # code = BeautifulSoup(data, 'html.parser')
    # print(data)
    # time.sleep(99)
    # print('soup479',soup)
    codes = soup.find_all('code')
    res_list = []
    for code in codes:
        # print('code482', code)
        if 'ss://' in str(code) or 'trojan' in str(code):
            # print('code489',code)
            res_list = code.text.strip().split()
    # b = bytes(str(soup), encoding='utf-8')
    # b64 = base64.b64decode(b).decode().split('\n')

    # print(b64)
    # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
    #     f.write('')
    # with open(os.getcwd() + r'\ss2.txt', 'w+', encoding='utf-8') as f:
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
    # with open(os.getcwd() + r'\ss2.txt', 'w+', encoding='utf-8') as f:
    #     f.write('\n' + sss)
    # f.close()
    congfig_list = []
    password = method = remarks = ''
    # print('res_list518',res_list)
    vpn_config_list = []
    plugin = ''
    res_list = list(dict.fromkeys(res_list))
    for i, vpn_config in enumerate(res_list):
        # print('vpn_config518', i,vpn_config)
        if 'ss://' in str(vpn_config) and 'vless://' not in vpn_config and 'vmess://' not in vpn_config:
            print('vpn_config520', vpn_config)
            vpn_config_list.append(vpn_config)
            result = parse_ss_url(vpn_config)
            # print('result522',result)
            if result and not any(
    method in result['method'].lower()
    for method in EXCLUDED_METHODS
):
                method = result['method']
                password = result['password']
                server = result['server']
                server_port = result['port']
                remarks = result['remark']
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
            congfig_ = '''
    "server": "{0}",
    "server_port": {1},
    "password": "{2}",
    "method": "{3}",
    "remarks": "{4}",
    "timeout": {5}
    '''.format(server, server_port, password, method, remarks, timeout, plugin)
            congfig_list.append('{' + congfig_ + '}')
            # congfig_list.append(congfig_)
        # configs = ','.join(congfig_list)
        # config = get_config(configs)
        # print(congfig_list)
    # print('vpn_config_list578',vpn_config_list)
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
            # os.system('python SS2_ip2.py')
            break
        n += 1

    data = html.data.decode()
    # code = BeautifulSoup(data, 'html.parser')
    print('data365', data)
    # time.sleep(99)
    b = bytes(data, encoding='utf-8')
    b64 = base64.b64decode(b).decode(errors='replace').split('\n')

    # print(b64)
    # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
    #     f.write('')
    # with open(os.getcwd() + r'\ss2.txt', 'w+', encoding='utf-8') as f:
    #     f.write('')
    # f.close()
    res_list = []
    ss_txt_list = []
    for i, sss in enumerate(b64):
        # print(i)
        # print(sss[0:3])
        if 'ss:' in sss[0:3]:
            # print(sss)
            res_list.append(sss)
            ss_txt_list.append('\n' + sss)
            # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
            #     f.write('\n' + sss)
            # with open(os.getcwd() + r'\ss2.txt', 'w+', encoding='utf-8') as f:
            #     f.write('\n' + sss)
            # f.close()
    congfig_list = []
    password = method = remarks = ''
    for vpn_config in res_list:
        # ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo2NzMyYzRiNC0yZTAwLTQyOGQtYWZjZi1jMzRhODM5NGUxMTY@nn.auozzjs.lol:40724#%E5%89%A9%E4%BD%99%E6%B5%81%E9%87%8F%EF%BC%9A63.68%20GB
        # if 'type: ss' in vpn_config :
        server = vpn_config.split('#')[0].split('@')[-1].split(':')[0]  # nn.auozzjs.lol
        server_port = vpn_config.split('#')[0].split('@')[-1].split(':')[1]  # 40724
        ss_s = vpn_config.split('ss://')[-1].split('@')[0] + '=='  # YWVzLTI1Ni1jZmI6YW1hem9uc2tyMDU
        # print(server, server_port, password, method, remarks)
        b = bytes(ss_s, encoding='utf-8')
        b64 = base64.b64decode(b).decode()
        password = b64.split(':')[-1]
        method = b64.split(':')[0]
        remarks = vpn_config.split('#')[1].replace('\n', '')
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
    '''.format(server, server_port, password, method, remarks)
        congfig_list.append('{' + congfig_ + '}')
        # congfig_list.append(congfig_)
    # configs = ','.join(congfig_list)
    # config = get_config(configs)
    return congfig_list


def get_config_informationurl(local_port=10802):
    congfig_list1 = []
    congfig_list2 = []
    congfig_list3 = []
    try:
        congfig_list1 = get_config_informationurl1()
    except:
        traceback.print_exc()
    # try:
    #     congfig_list2 = get_config_informationurl2()
    # except:
    #     traceback.print_exc()
    # try:
    #     congfig_list3 = get_config_informationurl3()
    # except:
    #     traceback.print_exc()

    # config, congfig_list_SS2 = get_config_informationurl_SS2()
    congfig_list_SS2 = []

    # congfig_list = congfig_list1 + congfig_list2 + congfig_list3 + congfig_list_SS2
    congfig_list = congfig_list1
    if len(congfig_list)!=0:
        configs = ','.join(list(set(congfig_list)))
        # print('configs722',configs)
        config = get_config(configs, local_port)
        return config


def get_config(configs, local_port=10802):
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
    config = config_head + config_core + config_tail.replace('88', str(local_port))
    return config


def get_config_old(configs, local_port=10802):
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
  "localPort": 10802,
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


def main_proxy(local_port=10802):
    download_file(f"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_configs_port{local_port}.json", f"{type_}_configs_port{local_port}.json")
    download_file(f"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_configs_port88.json", f"{type_}_configs_port88.json")
    time.sleep(2)

    # 启动监控进程
    subprocess.Popen([sys.executable, "monitor.py", str(pid), f"{type_}"])
    kill_exe()
    cmd_on_color.printCya(f'++++++++++++++++++++++++++++++++启动{type_}中，请耐心等待............++++++++++++++++++++++++++++++++')
    n=0
    config = ''
    while True:
        try:
            last_loop_time = time.time()
            state_ = start_exe(local_port,err_node_number=n+1)
            if f'不可以上网' in state_ or f'不可知的异常' in state_:
                if n <=2:
                    show_notification(f"端口 {local_port} 链接错误！准备更新配置", f"不可以上网！【第{n+1}次检测)】", "error")
                print(f'{n}==代理错误，疑似代理或IP配置有错误？开始重新获取最新IP配置=={type_}')
                if n < 8:
                # if n >= 8:
                    config = get_config_informationurl()
                else:
                    congfig_list2 = []
                    try:
                        congfig_list2 = get_config_informationurl2()
                    except:
                        traceback.print_exc()
                    # try:
                    #     congfig_list3 = get_config_informationurl3()
                    # except:
                    #     traceback.print_exc()

                    # config, congfig_list_SS2 = get_config_informationurl_SS2()
                    congfig_list_SS2 = []

                    # congfig_list = congfig_list1 + congfig_list2 + congfig_list3 + congfig_list_SS2
                    congfig_list = congfig_list2
                    if len(congfig_list) != 0:
                        configs = ','.join(list(set(congfig_list)))
                        # print('configs722',configs)
                        config = get_config(configs, local_port)
                if config:
                    with open(object_name + fr'\{type_}_configs_port{local_port}.json', 'w+', encoding='utf-8') as f:
                        f.write(config.replace('88', str(local_port)))

                    with open(object_name + fr'\{type_}_configs_port88.json', 'w+', encoding='utf-8') as f:
                        f.write(config.replace(str(local_port), '88'))
                    # time.sleep(2)
                    # upload(f"{type_}_configs_port{local_port}.json")
                    # upload(f"{type_}_configs_port88.json")
                print(f'开始杀死进程{exe_name}')
                kill_exe()  # exe_name, exe_name_path, object_name
            if state_ == f'有一个在运行，不能同时运行2个':
                def popup():
                    win32api.MessageBox(None, f'有一个在运行，不能同时运行2个{type_}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)

                threading.Thread(target=popup).start()

                break

            if n>18:
                n = 0
                download_file(f"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_configs_port{local_port}.json", f"{type_}_configs_port{local_port}.json")
                download_file(f"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_configs_port88.json", f"{type_}_configs_port88.json")
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
    # os.system("taskkill /F /IM sslocal.exe")
    # main_proxy()

    main_proxy_log()
    # start_exe()
    # sslocal1.exe -s "195.154.54.171:13355" -k "dongtaiwang.com" -b "127.0.0.1:10802" -m "aes-256-gcm"
    # sslocal1.exe -c configs.json
    # D:\客户端集合代理\SS2\sslocal1.exe -c D:\客户端集合代理\SS2\configs.json

    # get_config_informationurl1()
    # get_config_informationurl2()
    # get_config_informationurl3()
    # get_config_informationurl()

    # print(parse_ss_url('ss://eyJhZGQiOiI5My4xMTQuOTguNzkiLCJhaWQiOiIwIiwiYWxwbiI6ImgyLGh0dHAvMS4xIiwiZnAiOiJjaHJvbWUiLCJob3N0IjoiIiwiaWQiOiI2YTM4MjgzOS1kNGQ0LTRlNWEtYTA2MS0zMjhiNzRlZTlhZGEiLCJpbnNlY3VyZSI6IjAiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicGNzIjoiIiwicG9ydCI6IjIwODMiLCJwcyI6InQubWUvbXRtdnBuIiwic2N5IjoiYXV0byIsInNuaSI6ImFkc2xuZGlmNjNmNC5kb3A2NjYuY29tIiwidGxzIjoidGxzIiwidHlwZSI6Im5vbmUiLCJ2IjoiMiIsInZjbiI6IiJ9bix1fXU-Nt62NXc@fast.jkerm.com:443#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%20-%20Unknown%20%7C%20fast.jkerm.com%3A443%202'))

    # print(extract_and_decode_plugin_params('?plugin=v2ray-plugin%3Bmode%3Dwebsocket%3Bmux%3D8%3Bpath%3D%2Futvbnrzejpmt%3Bhost%3Dhkkh11v1.xpmc.cc%3Btls'))
    # print(extract_and_decode_plugin_params('?plugin=obfs-local%3Bobfs%3Dhttp%3Bobfs-host%3D202505081193439-ADTUVtshPJ.download.microsoft.com'))

    pass