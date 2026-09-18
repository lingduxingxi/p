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
from upload_node import upload
# 全局变量记录最后成功循环的时间
last_loop_time = time.time()

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



# url2 = "https://cdn.jsdelivr.net/gh/Alvin9999/pac2@latest/SS-Kcptun/ssconfig.txt"
# url1 = "https://a1.trump2023.org/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"#废弃
# url1 = "https://bku8.xyz/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7/"
url3 = "https://s3.dualstack.us-west-2.amazonaws.com/zhifan2/ss.html"
# url2 = "https://tr3.freeair888.club/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7/"
url1 = "https://gitlab.com/zhifan999/fq/-/wikis/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"  #github.com的镜像
url2 = "https://github.com/Alvin9999-newpac/fanqiang/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"



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


def validate_params(method, password, ip, port):
    """参数验证函数（补充缺失的依赖函数）"""
    if not all([method, password, ip, port]):
        return False
    # 简单的端口合法性校验
    try:
        port_int = int(port)
        return 1 <= port_int <= 65535
    except:
        return False


def parse_ss_url(ss_url, max_retries=8):
    """改进版解析函数，支持多重编码、IPv6和自动重试"""
    # 初始清理：移除首尾的引号、空格
    ss_url = ss_url.strip("'\" ")
    # 记录原始URL，避免多次清理导致数据丢失
    original_url = ss_url

    for attempt in range(max_retries):
        try:
            # 每次重试使用原始URL的副本，避免累积修改
            current_url = original_url if attempt > 0 else ss_url

            # 1. 分离基本部分和备注（兼容多#号场景，只切分第一个）
            parts = current_url.split('#', 1)
            url_part = parts[0].strip()
            remark = unquote(parts[1].strip()) if len(parts) > 1 else ""

            # 2. 处理插件参数（兼容?plugin=在#前面的情况）
            plugin = ""
            if '?plugin=' in url_part:
                url_part, plugin_part = url_part.split('?plugin=', 1)
                plugin = f'?plugin={plugin_part.strip()}'

            # 3. 移除ss://前缀
            if url_part.lower().startswith('ss://'):
                url_part = url_part[5:]

            # 4. 提取认证信息和服务器信息（核心修复：兼容两种模式）
            auth_part = ""
            server_part = ""
            if '@' in url_part:
                # 模式1：直接包含@分隔符（你的目标链接属于这种）
                auth_part, server_part = url_part.split('@', 1)
            else:
                # 模式2：无@分隔符，先解码整体
                try:
                    padding = 4 - len(url_part) % 4
                    decoded_full = base64.urlsafe_b64decode(url_part + '=' * padding).decode('utf-8').strip()
                    if '@' in decoded_full:
                        auth_part, server_part = decoded_full.split('@', 1)
                    else:
                        continue  # 无@则重试
                except:
                    continue  # 解码失败则重试

            # 5. 递归解码多重Base64（修复终止条件，兼容单层编码）
            method = ""
            password = ""
            decoded_auth = auth_part
            # 最多解码3层，确保单层编码也能正确解析
            for decode_layer in range(3):
                try:
                    # 补全Base64填充符
                    padding = 4 - len(decoded_auth) % 4
                    if padding != 4:
                        decoded_auth += '=' * padding
                    # 尝试解码
                    temp_decoded = base64.urlsafe_b64decode(decoded_auth).decode('utf-8').strip()
                    # 核心判断：解码后包含:且不是ss://开头，说明是加密方式:密码
                    if ':' in temp_decoded and not temp_decoded.lower().startswith('ss://'):
                        method, password = temp_decoded.split(':', 1)
                        break
                    # 否则继续解码下一层
                    decoded_auth = temp_decoded
                except:
                    # 解码失败时，检查当前字符串是否已是 加密方式:密码 格式
                    if ':' in decoded_auth and not decoded_auth.lower().startswith('ss://'):
                        method, password = decoded_auth.split(':', 1)
                        break
                    break  # 彻底解码失败，退出循环

            # 6. 解析服务器信息（重点修复IPv6解析逻辑）
            ip = ""
            port = ""
            # 清理server_part中的无关字符
            server_part = server_part.split('/')[0].split('?')[0].strip()

            # 处理IPv6地址（[xxxx:xxxx]:port 格式）
            if server_part.startswith('[') and ']:' in server_part:
                # 精准拆分IPv6和端口
                ipv6_end_idx = server_part.index(']')
                ip = server_part[1:ipv6_end_idx].strip()  # 提取[]内的IPv6地址
                port_part = server_part[ipv6_end_idx + 1:].strip()
                if port_part.startswith(':'):
                    port = port_part[1:].strip()  # 提取端口
            else:
                # 处理IPv4或无[]的IPv6（兼容常规格式）
                ip_port = server_part.rsplit(':', 1)
                if len(ip_port) == 2:
                    ip, port = ip_port
                    ip = ip.strip()
                    port = port.strip()
                else:
                    continue  # 端口格式错误，触发重试

            # 7. 最终参数验证
            print(f'解析结果(第{attempt + 1}次尝试)：', method, password, ip, port)
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
            # 最后一次重试时打印详细错误
            if attempt == max_retries - 1:
                print(f"最终解析失败: {str(e)}")
                traceback.print_exc()
            # 清理异常字符（保留IPv6必需的[]和:）
            ss_url = re.sub(r'[^\w\-@:.#?=/\[\]]', '', ss_url)
            continue

    return None


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
    print('res_list565',res_list)
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
        if result:
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


def get_config_informationurl2(timeout=2):
    http = urllib3.PoolManager()
    reg = ''
    soup = ''
    n = 1
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}
    while True:
        print('使用连接2进行更新！')
        try:
            # html = http.request('GET', url2, timeout=29, headers=headers)
            # link_url1_successful = '连接2成功！'
            # print(link_url1_successful)
            # break
            if n > 2:
                print('使用AI_all_auto代理88')
                proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
                reg = requests.get(url2, headers=headers, timeout=8, proxies=proxies)
            else:
                print('不使用代理')
                reg = requests.get(url2, headers=headers, timeout=8)

            link_url2_successful = '连接2成功！'
            print(link_url2_successful)
            # print(soup)
            break
        except Exception as err:
            print(err)
            print('连接2错误，2秒后重试！')
            time.sleep(2)
        # print(n)
        if n >= 2:
            # os.system('python SS2_ip2.py')
            break
        n += 1
    soup = BeautifulSoup(reg, 'html.parser')
    # data = html.data.decode()
    # code = BeautifulSoup(data, 'html.parser')
    # print(data)
    # time.sleep(99)
    b = bytes(str(soup), encoding='utf-8')
    b64 = base64.b64decode(b).decode().split('\n')

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
            print('sss716',sss)
            res_list.append(sss)
            ss_txt_list.append('\n' + sss)
            # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
            #     f.write('\n' + sss)
            # with open(os.getcwd() + r'\ss2.txt', 'w+', encoding='utf-8') as f:
            #     f.write('\n' + sss)
            # f.close()
    congfig_list = []
    password = method = remarks = ''
    plugin = '"[]"'
    for vpn_config in res_list:
        # ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo2NzMyYzRiNC0yZTAwLTQyOGQtYWZjZi1jMzRhODM5NGUxMTY@nn.auozzjs.lol:40724#%E5%89%A9%E4%BD%99%E6%B5%81%E9%87%8F%EF%BC%9A63.68%20GB
        # if 'type: ss' in vpn_config :
        #     print(vpn_config)
        server = vpn_config.split('#')[0].split('@')[-1].split(':')[0]  # nn.auozzjs.lol
        server_port = vpn_config.split('#')[0].split('@')[-1].split(':')[1]  # 40724
        if '?' in server_port:
            server_port = server_port.split('?')[0]
        ss_s = vpn_config.split('ss://')[-1].split('@')[0] + '=='  # YWVzLTI1Ni1jZmI6YW1hem9uc2tyMDU
        # print(server, server_port, password, method, remarks)
        b = bytes(ss_s, encoding='utf-8')
        b64 = base64.b64decode(b).decode()
        password = b64.split(':')[-1]
        method = b64.split(':')[0]
        remarks = vpn_config.split('#')[1]
        # print(server, server_port, password, method,remarks)
        congfig_ = '''
    "server": "{0}",
    "server_port": {1},
    "password": "{2}",
    "method": "{3}",
    "remarks": "{4}",
    "timeout": {5}
    '''.format(server, server_port, password, method, remarks, timeout)
        congfig_list.append('{' + congfig_ + '}')
        # congfig_list.append(congfig_)
    # configs = ','.join(congfig_list)
    # config = get_config(configs)
    # print(congfig_list)
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
    for i, vpn_config in enumerate(res_list):
        # print('vpn_config518', i,vpn_config)
        if 'ss://' in str(vpn_config) and 'vless://' not in vpn_config and 'vmess://' not in vpn_config:
            print('vpn_config520', vpn_config)
            vpn_config_list.append(vpn_config)
            result = parse_ss_url(vpn_config)
            # print('result522',result)
            if result:
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
            last_loop_time = time.time()
            state_ = start_exe(local_port,err_node_number=n+1)
            if f'不可以上网' in state_ or f'不可知的异常' in state_:
                if n <=2:
                    show_notification(f"端口 {local_port} 链接错误！准备更新配置", f"不可以上网！【第{n+1}次检测)】", "error")
                print(f'代理错误，疑似代理或IP配置有错误？开始重新获取最新IP配置=={type_}')
                config = get_config_informationurl()
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
                win32api.MessageBox(None, f'严重错误:{err}，程序:{type_}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)
        n += 1
def SS2_old():
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
        state, average_speed = download_files.download_file_state('https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif', os.getcwd() + r"\test_speed.gif", '10802')
        if state == '下载失败':
            print('代理错误，疑似代理或IP配置有错误？开始重新获取最新IP配置')
            # config = get_config_informationurl()
            # config = get_config_informationurl1()
            # config = get_config_informationurl3()
            # with open(object_name + '\gui-config.json', 'w+', encoding='utf-8') as f:
            # with open(object_name + f'\{type_}_configs_port10802.json', 'w+', encoding='utf-8') as f:
            #     f.write(config.replace('88', '10802'))
            # with open(object_name + f'\{type_}_configs_port88.json', 'w+', encoding='utf-8') as f:
            #     f.write(config.replace('10802', '88'))
            print(f'开始杀死进程{exe_name}')
            kill_exe()  # exe_name, exe_name_path, object_name
            print(f'开始启动进程{exe_name}')
            # state = start_exe()  # exe_name,exe_name_path,object_name
            # if success == f'启动{exe_name}成功':
            #     cmd_on_color.printGre(f'success642==>>{success}')
        else:
            status = '可以上网'
            # with open(os.getcwd() + r'\ss2.txt', 'r+', encoding='utf-8') as f:
            #     old_data = f.read()
            # with open(os.getcwd() + r'\ss.txt', 'w+', encoding='utf-8') as f:
            #     f.write(old_data)
            # f.close()
            status = cmd_on_color.printGre(status)
            cmd_on_color.printGre('此代理可以上网！端口为===============》》》》》》》》》》》》》》》》》》》：10802【Shadowsocks1】')
            break
        if n >= 2:
            status = '不可上网'
            status = cmd_on_color.printRed(status)
            cmd_on_color.printRed('10802【Shadowsocks1】此代理最终不可以上网！请更换下一个代理！')
            break
        n += 1
    return status, average_speed


def run_exe_old(local_port, run_type):
    # server_address, port, password = read_config()
    success = ''
    cmd = fr'{exe_name_path} -c {object_name}\{type_}_configs_port{local_port}.json'  # sslocal_SS2.exe -c SS2_configs_port10802.json -v
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

            # 实时读取输出并写入文件和打印到控制台
            while True:
                output = process.stdout.readline()
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
                            success = f'启动{exe_name}成功'
                            print(success)
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
                        with open(object_name + r'\ss2_err.txt', 'a+', encoding='utf-8') as f:
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
                        # with open(object_name + f'\{type_}_configs_port10802.json', 'w+', encoding='utf-8') as f:
                        #     f.write(config.replace('88', '10802'))
                        # with open(object_name + f'\{type_}_configs_port88.json', 'w+', encoding='utf-8') as f:
                        #     f.write(config.replace('10802', '88'))

                    # if '由于目标计算机积极拒绝' in output.strip() and state_url != '连接成功':#handler error: 由于目标计算机积极拒绝，无法连接。 (os error 10061)
                    if '由于目标计算机积极拒绝' in output.strip() or '连接尝试失败' in output.strip() or '没有正确答复' in output.strip():  # handler error: 由于目标计算机积极拒绝，无法连接。 (os error 10061)
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

    # print(parse_ss_url('ss://c3M6Ly9ZV1Z6TFRJMU5pMWpabUk2WVhkemNITXdOVEF4@18.236.149.239:443#14%7Ctg%E9%A2%91%E9%81%93%3A%40ripaojiedian%20%231'))

    # print(extract_and_decode_plugin_params('?plugin=v2ray-plugin%3Bmode%3Dwebsocket%3Bmux%3D8%3Bpath%3D%2Futvbnrzejpmt%3Bhost%3Dhkkh11v1.xpmc.cc%3Btls'))
    # print(extract_and_decode_plugin_params('?plugin=obfs-local%3Bobfs%3Dhttp%3Bobfs-host%3D202505081193439-ADTUVtshPJ.download.microsoft.com'))

    pass