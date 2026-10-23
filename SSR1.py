#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# import json
import binascii
import re
import subprocess
import threading
import urllib.parse

import win32con
import yaml
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
# from urllib.parse import unquote, parse_qs
# from SS2 import get_config_information as get_config_informationurl_SS2
from datetime import datetime
from urllib.parse import unquote, parse_qsl
from download_files import download_file
from notification_simulator import show_notification
from run_port_exe import run_exe
# from upload_node import upload

# from GoflywayTools import check_proxy_connection

logging.captureWarnings(True)  # 强制取消证书验证警告
url6 = "https://raw.githubusercontent.com/myominn062-svg/mk-studio-vpn-service/main/ssr_configs.txt"


url3 = "https://github.com/aiboboxx/v2rayfree"
url8 = 'https://dgithub.xyz/aiboboxx/v2rayfree'

url1_source = 'https://raw.githubusercontent.com/Huibq/TrojanLinks/master/links/ssr'
url1 = 'https://ghfile.geekertao.top/https://raw.githubusercontent.com/Huibq/TrojanLinks/master/links/ssr'
url2_source = 'https://raw.githubusercontent.com/myominn062-svg/mk-studio-vpn-service/main/ssr_configs.txt'
url2 = 'https://ghfile.geekertao.top/https://raw.githubusercontent.com/myominn062-svg/mk-studio-vpn-service/main/ssr_configs.txt'

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
                print('port88_err_num193', port88_err_num)
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


def parse_ss_url(ss_url, max_retries=8):
    """改进版解析函数，支持多重编码和自动重试"""
    ss_url = ss_url.strip("'\" ")
    # method = password = ''
    for attempt in range(max_retries):
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

            # 尝试两种解析模式
            if '@' in url_part:
                auth_part, server_part = url_part.split('@', 1)
            else:
                # 处理双重编码情况
                decoded = base64.urlsafe_b64decode(url_part + '=' * (4 - len(url_part) % 4)).decode()
                if '@' not in decoded:
                    continue  # 触发重试
                auth_part, server_part = decoded.split('@', 1)
                auth_part = base64.urlsafe_b64encode(auth_part.encode()).decode().rstrip('=')

            # 递归解码多重Base64
            for _ in range(3):  # 最多解码3层
                try:
                    decoded_auth = base64.urlsafe_b64decode(auth_part + '=' * (4 - len(auth_part) % 4)).decode()
                    print('decoded_auth327', decoded_auth)
                    if ':' in decoded_auth and 'ss://' not in decoded_auth:
                        method, password = decoded_auth.split(':', 1)
                        break
                    auth_part = decoded_auth.replace('ss://', '')  # 继续解码
                except:
                    break
            else:
                continue  # 触发重试

            # 解析服务器信息
            server_part = server_part.split('/')[0].split('?')[0]

            # 处理IPv6地址
            if server_part.startswith('['):
                end = server_part.index(']')
                ip = server_part[1:end]
                port = server_part[end + 2:]
            else:
                ip_port = server_part.rsplit(':', 1)
                if len(ip_port) != 2:
                    continue  # 触发重试
                ip, port = ip_port

            # 最终参数验证
            print('validate_params352', method, password, ip, port)
            # print('validate_params355',validate_params(method, password, ip, port))
            if validate_params(method, password, ip, port):
                return {
                    'method': method,
                    'password': password,
                    'server': ip,
                    'port': port,
                    'remark': remark,
                    'plugin': plugin or None
                }

        except Exception as e:
            if attempt == max_retries - 1:
                print(f"最终解析失败: {str(e)}")
                traceback.print_exc()

            # 尝试移除异常字符后重新解析
            ss_url = re.sub(r'[^\w\-@:.#?=/]', '', ss_url)
            continue

    return None

def decode_base64(data):
    # 补齐 base64 字符串
    data += '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data.encode('utf-8')).decode('utf-8')




def parse_ssr(ssr_url):
    """
    解析 SSR 分享链接，转换为代理配置字典。

    支持：
    - 标准 Base64 / URL-safe Base64
    - 自动补齐 Base64 末尾填充符
    - password 字段的独立 Base64 解码
    - obfsparam、protoparam、remarks、group 参数解析
    - rc4、rc4-md5 等加密方法保留原值，不在解析阶段拒绝
    - 单个节点解析失败时返回 error，不影响其他节点
    """

    if not isinstance(ssr_url, str):
        return {
            "error": "SSR 链接必须是字符串",
            "original": str(ssr_url)
        }

    ssr_url = ssr_url.strip()

    if not ssr_url.lower().startswith("ssr://"):
        return {
            "error": "不是有效的 ssr:// 链接",
            "original": ssr_url
        }

    def b64_decode_bytes(value):
        """严格解码 Base64 字节，兼容 URL-safe 格式和缺失的填充符。"""
        if isinstance(value, bytes):
            raw_value = value
        else:
            raw_value = str(value).strip()
            raw_value = re.sub(r"\s+", "", raw_value)

            if not raw_value:
                return b""

            # 标准 SSR Base64 通常使用 + /，URL-safe 格式可能使用 - _。
            raw_value = raw_value.replace("-", "+").replace("_", "/")

            # Base64 长度余数为 1 时，不可能仅靠补 = 修复。
            remainder = len(raw_value) % 4
            if remainder == 1:
                raise ValueError(
                    "Base64 字符串长度无效，长度余数为 1"
                )

            if remainder:
                raw_value += "=" * (4 - remainder)

            raw_value = raw_value.encode("ascii")

        return base64.b64decode(raw_value, validate=True)

    def b64_decode_text(value):
        """Base64 解码为文本。"""
        return b64_decode_bytes(value).decode("utf-8-sig")

    def decode_password(value):
        """
        解码 SSR 密码字段。

        SSR 主体中的密码一般是 Base64 编码。
        如果解码后不是 UTF-8，返回明确错误，避免生成错误密码。
        """
        value = value.strip()

        if not value:
            return ""

        return b64_decode_text(value).strip()

    def decode_parameter(value):
        """
        解析 SSR 查询参数值。

        SSR 参数常见形式：
        - obfsparam=...
        - protoparam=...
        - remarks=...
        - group=...

        参数值先经过 URL 解码。
        对 remarks/group，通常是 URL 编码后的文本；
        对 obfsparam/protoparam，部分订阅源会额外使用 Base64。
        """
        if value is None:
            return ""

        value = unquote(str(value)).strip()

        if not value:
            return ""

        # 参数值中有中文、空格、标点等时，优先按普通文本保留。
        # 对纯 Base64 字符串，尝试解码并验证结果。
        if not re.fullmatch(r"[A-Za-z0-9+/=_-]+", value):
            return value

        try:
            decoded = b64_decode_text(value)

            # 只接受可打印文本，防止将普通参数误判为 Base64。
            if decoded and all(
                ch.isprintable() or ch in "\r\n\t"
                for ch in decoded
            ):
                return decoded
        except (
            ValueError,
            UnicodeDecodeError,
            binascii.Error
        ):
            pass

        return value

    try:
        # 1. 解码外层 SSR Base64。
        encoded = ssr_url[6:].strip()

        # 外层分享链接中不应包含空格，但有些复制过程会插入换行。
        encoded = re.sub(r"\s+", "", encoded)

        decoded = b64_decode_text(encoded).strip()

        if not decoded:
            raise ValueError("外层 Base64 解码结果为空")

        # 2. 分离主体和查询参数。
        if "/?" in decoded:
            server_part, query_part = decoded.split("/?", 1)
        else:
            server_part, query_part = decoded, ""

        server_part = server_part.strip()

        # SSR 标准格式：
        # server:port:protocol:method:obfs:password
        #
        # 不要在这里先对整个主体调用 unquote，
        # 否则可能把编码后的分隔符变成真实分隔符。
        fields = server_part.split(":")

        if len(fields) < 6:
            raise ValueError(
                "SSR 主体字段不足："
                f"预期至少 6 段，实际得到 {len(fields)} 段"
            )

        server = fields[0].strip()
        port_text = fields[1].strip()
        protocol = fields[2].strip()
        method = fields[3].strip()
        obfs = fields[4].strip()

        # 标准 IPv4/域名 SSR 链接中，密码是第 6 段。
        # 合并剩余字段，避免非标准数据中的额外冒号被直接丢弃。
        password_encoded = ":".join(fields[5:]).strip()

        if not server:
            raise ValueError("服务器地址为空")

        if not port_text.isdigit():
            raise ValueError(f"端口号无效：{port_text!r}")

        port = int(port_text)

        if not 1 <= port <= 65535:
            raise ValueError(f"端口号超出有效范围：{port}")

        if not protocol:
            raise ValueError("SSR protocol 字段为空")

        if not method:
            raise ValueError("SSR method 字段为空")

        if not obfs:
            raise ValueError("SSR obfs 字段为空")

        # 3. 解码密码。
        password = decode_password(password_encoded)

        # 4. 解析查询参数。
        # parse_qsl 可正确处理参数中的多个等号和空值。
        raw_params = {}

        if query_part:
            for key, value in parse_qsl(
                query_part,
                keep_blank_values=True
            ):
                raw_params[key.strip().lower()] = value

        def get_param(*names):
            """按多个兼容名称获取参数。"""
            for name in names:
                key = name.lower()

                if key in raw_params:
                    return decode_parameter(raw_params[key])

            return ""

        obfs_param = get_param(
            "obfsparam",
            "obfs-param",
            "obfs_param"
        )

        protocol_param = get_param(
            "protoparam",
            "protocol-param",
            "protocol_param"
        )

        remarks = get_param(
            "remarks",
            "remark",
            "name"
        )

        group = get_param("group")

        # 5. 构造配置。
        # 不在解析阶段拒绝 rc4、rc4-md5。
        # 后续内核不支持时，应由启动或连接阶段报告。
        result = {
            "name": f"{server}:{port}",
            "type": "ssr",
            "server": server,
            "port": port,
            "password": password,
            "cipher": method,
            "obfs": obfs,
            "protocol": protocol,
            "obfs-param": obfs_param,
            "protocol-param": protocol_param
        }

        if remarks:
            result["remarks"] = remarks

        if group:
            result["group"] = group

        return result

    except Exception as e:
        return {
            "error": f"{type(e).__name__}: {e}",
            "original": ssr_url
        }




def get_config_informationurl1(local_port):
    import base64
    import binascii
    import re
    import time
    import requests

    reg_list = []
    res_list = []
    config_list = []
    config_err_list = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36 "
            "Edg/107.0.1418.26"
        )
    }

    # 保留原有代理设置。
    proxy_port = 88
    proxies_dict = {
        "http": f"socks5h://127.0.0.1:{proxy_port}",
        "https": f"socks5h://127.0.0.1:{proxy_port}",
    }

    def fetch_subscription(url_candidates, label):
        """
        获取订阅内容。
        前两次直接连接，后续尝试通过本地 SOCKS5 代理连接。
        每次请求失败后尝试备用 URL，避免重复使用旧响应。
        """
        url_candidates = [
            url for url in url_candidates
            if isinstance(url, str) and url.strip()
        ]

        if not url_candidates:
            print(f"{label}：没有可用的订阅 URL")
            return None

        # 最多尝试 9 轮。
        for attempt in range(9):
            use_proxy = attempt >= 2

            if use_proxy:
                print(f"{label}：使用 AI_all_auto 代理 {proxy_port}")
            else:
                print(f"{label}：不使用代理")

            for url in url_candidates:
                try:
                    request_kwargs = {
                        "headers": headers,
                        "timeout": 12,
                    }

                    if use_proxy:
                        request_kwargs["proxies"] = proxies_dict

                    response = requests.get(url, **request_kwargs)

                    # HTTP 404、403、500 等不应被误认为订阅成功。
                    response.raise_for_status()

                    text = response.text

                    if not text or not text.strip():
                        print(f"{label}：订阅响应为空，尝试下一个地址")
                        continue

                    print(f"{label}：获取响应成功")
                    return text

                except requests.RequestException as err:
                    print(f"{label} 请求失败：{err}")

                except Exception as err:
                    print(f"{label} 发生异常：{err}")

            if attempt < 8:
                print(f"{label}：本轮失败，2 秒后重试")
                time.sleep(2)

        print(f"{label}：已达到最大重试次数，跳过该订阅")
        return None

    def extract_ssr_links(content, label):
        """
        解析订阅响应。

        支持：
        1. 响应直接包含 ssr:// 链接。
        2. 响应为 Base64 编码的订阅内容。
        3. Base64 使用 URL-safe 字符集。
        4. Base64 缺少结尾 padding。
        5. 订阅内容含空行、BOM 和多条链接。

        非法数据只跳过当前订阅，不让整个函数崩溃。
        """
        if not isinstance(content, str) or not content.strip():
            print(f"{label}：响应内容为空")
            return []

        content = content.strip().lstrip("\ufeff")

        def find_links(text):
            # 按行提取，允许链接前后存在空白。
            links = []

            for line in text.splitlines():
                line = line.strip().lstrip("\ufeff")

                if not line:
                    continue

                # 只提取 SSR 链接，避免将其他协议误传给 parse_ssr。
                match = re.search(r"ssr://[A-Za-z0-9_\-+/=%]+", line)

                if match:
                    links.append(match.group(0))

            return links

        # 情况一：响应本身已经包含 SSR 链接。
        direct_links = find_links(content)

        if direct_links:
            print(f"{label}：直接提取到 {len(direct_links)} 条 SSR 链接")
            return direct_links

        # 情况二：尝试将响应视为 Base64 订阅。
        # 移除空白字符，但不对普通网页内容进行强制 UTF-8 解码。
        compact = re.sub(r"\s+", "", content)

        if not compact:
            print(f"{label}：去除空白后没有有效内容")
            return []

        # Base64 长度余数为 1 时，无法通过补 padding 修复。
        if len(compact) % 4 == 1:
            print(
                f"{label}：内容不是有效的 Base64，"
                f"长度余数为 1，疑似网页错误响应或数据损坏"
            )
            return []

        # 同时尝试标准 Base64 和 URL-safe Base64。
        candidates = [
            compact,
            compact.replace("-", "+").replace("_", "/"),
        ]

        decoded_text = None
        seen = set()

        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)

            if len(candidate) % 4 == 1:
                continue

            padded = candidate + ("=" * ((-len(candidate)) % 4))

            try:
                decoded_bytes = base64.b64decode(
                    padded.encode("ascii"),
                    validate=True
                )

            except (ValueError, UnicodeError, binascii.Error):
                continue

            try:
                # utf-8-sig 同时兼容带 BOM 的 UTF-8 文本。
                decoded_text = decoded_bytes.decode("utf-8-sig")
                break

            except UnicodeDecodeError as err:
                print(
                    f"{label}：Base64 解码后的内容不是有效 UTF-8 文本，"
                    f"错误位置 {err.start}，跳过该响应"
                )

        if decoded_text is None:
            print(
                f"{label}：无法将响应解析为有效的 Base64 UTF-8 订阅"
            )
            print(f"{label}：响应前 100 个字符：{content[:100]!r}")
            return []

        # 解码后再次提取 SSR 链接。
        links = find_links(decoded_text)

        if links:
            print(f"{label}：Base64 解码后提取到 {len(links)} 条 SSR 链接")
        else:
            print(
                f"{label}：Base64 解码成功，但内容中没有找到 SSR 链接"
            )
            print(f"{label}：解码内容前 100 个字符：{decoded_text[:100]!r}")

        return links

    # ---------------------------------------------------------
    # 第一组订阅：优先 url1，失败时尝试 url1_source。
    # ---------------------------------------------------------
    print("使用连接1进行更新！")

    content1 = fetch_subscription(
        [url1, url1_source],
        "连接1"
    )

    if content1 is not None:
        reg_list.append(content1)
        print("连接1获取成功！")
    else:
        print("连接1获取失败，继续尝试其他订阅。")

    # ---------------------------------------------------------
    # 第二组订阅：获取 url6。
    # ---------------------------------------------------------
    print("使用连接2进行更新！")

    content2 = fetch_subscription(
        [url6],
        "连接2"
    )

    if content2 is not None:
        reg_list.append(content2)
        print("连接2获取成功！")
    else:
        print("连接2获取失败，继续处理已取得的订阅。")

    # ---------------------------------------------------------
    # 解析订阅响应，避免对错误页面强制 Base64 解码。
    # ---------------------------------------------------------
    for index, reg in enumerate(reg_list, start=1):
        links = extract_ssr_links(reg, f"订阅响应 {index}")
        res_list.extend(links)

    # 去重，同时保持原有顺序。
    ssr_links = list(dict.fromkeys(res_list))

    print("get_config_informationurl1_ssr_links626 节点", len(ssr_links))

    # ---------------------------------------------------------
    # 解析所有 SSR 链接。
    # 保留外部 parse_ssr(link) 函数的调用方式。
    # ---------------------------------------------------------
    for index, link in enumerate(ssr_links, start=1):
        try:
            node = parse_ssr(link)

            if node:
                config_list.append(node)
            else:
                config_err_list.append(link)
                print(f"SSR 节点解析失败，第 {index} 条：{link[:80]}")

        except Exception as err:
            config_err_list.append(link)
            print(f"SSR 节点解析异常，第 {index} 条：{err}")

    print(
        f"get_config_informationurl1："
        f"成功解析 {len(config_list)}/{len(ssr_links)} 个 SSR 节点"
    )

    if config_err_list:
        print(f"无法解析的 SSR 节点数量：{len(config_err_list)}")

    return config_list



def get_config_informationurl2(local_port):
    rsp = ''
    reg = ''
    html = ''
    link_url2_successful = ''
    link_url2_successful = ''
    link_url3_successful = ''
    reg_list = []

    n = 0
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}
    while True:
        print('使用连接2进行更新！')
        try:
            # req = urllib.request.Request(url2)
            # webpage = urllib.request.urlopen(req)

            if n >= 2:
                print('使用AI_all_auto代理88')
                proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
                try:
                    reg = requests.get(url2_source, headers=headers,proxies=proxies, timeout=8).text
                except:
                    reg = requests.get(url2, headers=headers,proxies=proxies, timeout=8).text
            else:
                print('不使用代理')
                try:
                    reg = requests.get(url2, headers=headers, timeout=8).text
                except:
                    reg = requests.get(url2_source, headers=headers, timeout=8).text
            # print(reg)
            # soup = BeautifulSoup(reg, 'html.parser')
            # reg_list.append(reg)
            if 'DOCTYPE html' in reg:
                pass
            else:
                reg_list = reg.split()
                link_url2_successful = '连接2成功！'
                print(link_url2_successful)
                break

        except Exception as err:
            print(err)
            print('连接2错误，2秒后重试！')
            time.sleep(2)
        # print(n)
        if n >= 8:
            break
        n += 1
    res_list = []
    for reg in reg_list:
            # print(sss[0:3])
            # if 'ssr:' in sss[0:3] :
        if 'ssr://' in reg:
            # print('767ssr',reg)
            res_list.append(reg)
    ssr_links = list(dict.fromkeys(res_list))
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
    proxies = [parse_ssr(link) for link in ssr_links]


    print('get_config_informationurl2_ssr_links802节点', len(proxies))
    #get_config_informationurl2_ssr_links626节点 20
    # cmd_on_color.printGre("配置文件已生成：clash_config_{type_}.yaml")
    return proxies





def get_config_informationurl3(local_port):
    http = urllib3.PoolManager()
    html = ''
    soup = ''
    n = 0
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}
    while True:
        print('使用连接3进行更新！')
        try:

            proxy_port = '88'
            # proxy_port = '10802'
            # url3 = 'https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7'

            # rsp = http.request('GET', url3, timeout=28, headers=headers, proxies=proxies)
            if 2 < n <= 6:
                print('不走代理')
                reg = requests.get(url8, headers=headers, timeout=8).text
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
            # os.system('python SS1_ip2.py')
            break
        n += 1

    # data = html.data.decode()
    # code = BeautifulSoup(data, 'html.parser')
    # print(data)
    # time.sleep(99)
    # print('soup479',soup)
    res_list = []
    if '<!DOCTYPE html>' in str(soup):
        codes = soup.find_all('code')

        for code in codes:
            # print('code482', code)
            if 'ssr://' in str(code) :
                print('code489',code)
                res_list = code.text.strip().split('\n')
                # print('res_list716',res_list)
                break
    else:
        for code in soup.text.strip().split('\n'):
            # print('code482', code)
            if 'ssr://' in str(code) :
                print('code489',code)
                res_list.append(code)
    # b = bytes(str(soup), encoding='utf-8')
    # b64 = base64.b64decode(b).decode().split('\n')

    # print(b64)
    # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
    #     f.write('')
    # with open(os.getcwd() + r'\ssr1.txt', 'w+', encoding='utf-8') as f:
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
    # with open(os.getcwd() + r'\ssr1.txt', 'w+', encoding='utf-8') as f:
    #     f.write('\n' + sss)
    # f.close()
    congfig_list = []
    password = method = remarks = ''
    # print('res_list518',res_list)
    vpn_config_list = []
    ssr_links = []
    plugin = ''
    res_list = list(dict.fromkeys(res_list))
    for i, vpn_config in enumerate(res_list):
        # print('vpn_config518', i,vpn_config)
        if 'ssr://' in str(vpn_config) :
            # 解析所有 SSR 链接
            ssr_links.append(vpn_config)
    proxies = [parse_ssr(link) for link in ssr_links]
    print('get_config_informationurl3_ssr_links843节点', len(proxies))
    return proxies


def get_config_informationurl(local_port):
    congfig_list1 = []
    congfig_list2 = []
    congfig_list3 = []
    try:
        congfig_list1 = get_config_informationurl1(local_port)
        pass
    except:
        traceback.print_exc()
    try:
        congfig_list2 = get_config_informationurl2(local_port)
        pass
    except:
        traceback.print_exc()
    try:
        congfig_list3 = get_config_informationurl3(local_port)
        pass
    except:
        traceback.print_exc()

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
    # print('\n'.join(list(congfig_list1) + list(congfig_list2) + list(congfig_list3)))
    if len(congfig_list1 + congfig_list2 + congfig_list3) != 0:
        for proxy in congfig_list1 + congfig_list2 + congfig_list3:
            # 将字典转换为可哈希的元组表示
            proxy_tuple = tuple(sorted(proxy.items()))
            if proxy_tuple not in seen:
                seen.add(proxy_tuple)
                unique_proxies.append(proxy)

        proxies = unique_proxies
        # for p in proxies:
        #     print('1266p',p)
            # name_p = p["name"]

        # print('1265unique_proxies',unique_proxies)
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


def get_config(configs, local_port=10805):
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


def get_config_old(configs, local_port=10805):
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
  "localPort": 10805,
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


def main_proxy(local_port=10805):
    download_file(f"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_clash_config_port{local_port}.yaml", f"{type_}_clash_config_port{local_port}.yaml")
    download_file(f"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_clash_config_port88.yaml", f"{type_}_clash_config_port88.yaml")
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
                download_file(f"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_clash_config_port{local_port}.yaml", f"{type_}_clash_config_port{local_port}.yaml")
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
        state, average_speed = download_files.download_file_state('https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif', os.getcwd() + r"\test_speed.gif", '10805')
        if state == '下载失败':
            print('代理错误，疑似代理或IP配置有错误？开始重新获取最新IP配置')
            # config = get_config_informationurl(10805)
            # config = get_config_informationurl1()
            # config = get_config_informationurl3()


            # with open(object_name + f'\{type_}_configs_port10805.json', 'w+', encoding='utf-8') as f:
            #     f.write(config.replace('88', '10805'))
            # with open(object_name + f'\{type_}_configs_port88.json', 'w+', encoding='utf-8') as f:
            #     f.write(config.replace('10805', '88'))
            print(f'开始杀死进程{exe_name}')
            kill_exe()  # exe_name, exe_name_path, object_name
            print(f'开始启动进程{exe_name}')
            # state = start_exe()  # exe_name,exe_name_path,object_name
            # if success == f'启动{exe_name}成功':
            #     cmd_on_color.printGre(f'success642==>>{success}')
        else:
            status = '可以上网'
            # with open(os.getcwd() + r'\ssr1.txt', 'r+', encoding='utf-8') as f:
            #     old_data = f.read()
            # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
            #     f.write(old_data)
            # f.close()
            status = cmd_on_color.printGre(status)
            cmd_on_color.printGre('此代理可以上网！端口为===============》》》》》》》》》》》》》》》》》》》：10805【Shadowsocks1】')
            break
        if n >= 2:
            status = '不可上网'
            status = cmd_on_color.printRed(status)
            cmd_on_color.printRed('10805【Shadowsocks1】此代理最终不可以上网！请更换下一个代理！')
            break
        n += 1
    return status, average_speed




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

    # main_proxy_log()
    # start_exe()
    # sslocal1.exe -s "195.154.54.171:13355" -k "dongtaiwang.com" -b "127.0.0.1:10805" -m "aes-256-gcm"
    # sslocal1.exe -c configs.json
    # D:\客户端集合代理\SSR1\sslocal1.exe -c D:\客户端集合代理\SSR1\configs.json

    # get_config_informationurl1(10805)
    get_config_informationurl2(10805)
    # get_config_informationurl3(10805)
    # get_config_informationurl(10805)
