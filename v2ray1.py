#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import ast
import re
import threading
import traceback
import psutil
import win32con
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage
# import yaml
from bs4 import BeautifulSoup
import win32api, time, urllib3,os
import requests
from tqdm import tqdm
# from numpy import *
import logging
import cmd_on_color
import subprocess
from typing import Dict

import json
import base64
from urllib.parse import urlparse, urlsplit, parse_qs, unquote
from html import unescape as html_unescape

import download_files
from notification_simulator import show_notification
from run_port_exe import run_exe
from upload_node import upload

today = time.strftime('%Y%m%d', time.localtime())
# today = '20250528'
#需要爬取网页的 soup BeautifulSoup
# url11_source = "https://raw.githubusercontent.com/MohammadBahemmat/V2ray-Collector/refs/heads/main/all_servers.txt"  #很多 作为备份
# url11 = 'https://ghfile.geekertao.top/https://raw.githubusercontent.com/MohammadBahemmat/V2ray-Collector/refs/heads/main/all_servers.txt' #很多 作为备份


# url11_source = "https://raw.githubusercontent.com/ProblemTheCode/SylphNet-public/refs/heads/main/sub/sub_plain.txt"  #
# url11 = 'https://ghfile.geekertao.top/https://raw.githubusercontent.com/ProblemTheCode/SylphNet-public/refs/heads/main/sub/sub_plain.txt' #

# url11_source = "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/V2RAY.txt"  #  可以  但100多个
# url11 = 'https://ghfile.geekertao.top/https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/V2RAY.txt' #


# url11_source = "https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/main/configs/vless.txt"  #  可以  但仅仅1个    150多个
# url11 = 'https://ghfile.geekertao.top/https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/main/configs/vless.txt' #

# url11_source = "https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/main/configs/trojan.txt"  #  可以  但仅仅1个    165多个
# url11 = 'https://ghfile.geekertao.top/https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/main/configs/trojan.txt' #




url11_list = [
        'https://ghfile.geekertao.top/https://raw.githubusercontent.com/Romaxa55/MegaV_Public/refs/heads/main/subs/all.txt',
        'https://ghfile.geekertao.top/https://github.com/Idolvpn/Automate-V2ray-Config-Collector/raw/refs/heads/main/configs/mix.txt',
        'https://ghfile.geekertao.top/https://github.com/Barabama/FreeNodes/raw/8356d5838573f9f08dab4682df4ceca00ae77c1c/nodes/clashstair.txt',

         ]
url11_source_list = [
                    "https://raw.githubusercontent.com/Romaxa55/MegaV_Public/refs/heads/main/subs/all.txt",  #  可以  只有9个
                    "https://github.com/Idolvpn/Automate-V2ray-Config-Collector/raw/refs/heads/main/configs/mix.txt",  #  可以  但仅仅2个    66个
                    "https://github.com/Barabama/FreeNodes/raw/8356d5838573f9f08dab4682df4ceca00ae77c1c/nodes/clashstair.txt",  #  可以 但仅仅2个  32个节点

                    ]






url2_list = [
             # "https://ghfile.geekertao.top/https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",# 不用解码  12小时
             "https://ghfile.geekertao.top/https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",# 约38分钟更新一次
             "https://ghfile.geekertao.top/https://raw.githubusercontent.com/hello-world-1989/cn-news/main/end-gfw-together",# 约8分钟更新一次
             "https://ghfile.geekertao.top/https://raw.githubusercontent.com/Au1rxx/free-vpn-subscriptions/main/output/by-country/v2ray-base64-TW.txt",# 约8分钟更新一次
             # "https://ghfile.geekertao.top/https://raw.githubusercontent.com/Huibq/TrojanLinks/refs/heads/master/links/vmess",# 约1小时更新一次  有点小多
             #
             # "https://raw.dgithub.xyz/chengaopan/AutoMergePublicNodes/refs/heads/master/list.txt" #最多  约12分钟更新一次
             ]#备用 可筛选可用的ss   镜像网站
url2_source_list = [
                    # "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt", #不用解码  12小时
                    # "https://raw.githubusercontent.com/ripaojiedian/freenode/refs/heads/main/sub", #8-9 小时更新一次
                    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",# 约38分钟更新一次
                    "https://raw.githubusercontent.com/hello-world-1989/cn-news/main/end-gfw-together",# 约8分钟更新一次
                    "https://raw.githubusercontent.com/Au1rxx/free-vpn-subscriptions/main/output/by-country/v2ray-base64-TW.txt",# 约8分钟更新一次
                    # "https://raw.githubusercontent.com/Huibq/TrojanLinks/refs/heads/master/links/vmess",# 约1小时更新一次  有点小多
                    #
                    # "https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/refs/heads/master/list.txt" #最多 约12分钟更新一次
                    ]#备用 可筛选可用的ss   原生网站


'''
###订阅
#直接解码：如c3M6Ly9ZV1Z6TFRJMU5pMWpabUk2WVhkemNITXdOVEF4QDM0LjIxOS43Mi44
#https://raw.githubusercontent.com/cbusifabcap/daily_free_vpn/refs/heads/main/sub/V2Ray.yml  多

https://betternode.githubrowcontent.com/2025/05/20250525.txt #更新不及时
https://oneclash.githubrowcontent.com/2025/05/20250525.txt #与上一个一样
https://onenode.githubrowcontent.com/2025/05/20250525.txt #与上一个一样
https://nodedog.githubrowcontent.com/2025/05/20250525.txt #与上一个一样
http://wanzhuanmi.cczzuu.top/node/20250525-v2ray.txt
https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub  #8-9 小时更新一次
https://raw.dgithub.xyz/chengaopan/AutoMergePublicNodes/refs/heads/master/list.txt  最多！
https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2  很多  #8-9 小时更新一次
https://ghfile.geekertao.top/https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub    #较多  39 minutes 更新一次
https://raw.githubusercontent.com/hello-world-1989/cn-news/main/end-gfw-together  # 8分钟 1次
https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt   #不用解码  12小时
https://raw.githubusercontent.com/Huibq/TrojanLinks/refs/heads/master/links/vmess  # 1 hour ago  有点小多
#https://github.com/abshare3/abshare3.github.io  #公益流量有限  ss 需要爬取
#https://github.com/mksshare/mksshare.github.io  #公益流量有限  ss 需要爬取
# "https://jiang.netlify.app/",#不理想  有效节点极低
https://jichangtuijian.com/%E5%85%8D%E8%B4%B9ssr%E5%92%8Cv2ray%E6%9C%BA%E5%9C%BA.html  节点池
https://github.com/peasoft/NoMoreWalls/blob/master/list_raw.txt
https://node.freeclashx.com/uploads/2026/03/1-20260309.txt  
https://github.com/shabane/kamaji/blob/master/hub/vless.txt

'''


logging.captureWarnings(True)  # 强制取消证书验证警告




# 固定项目名称：即使此文件临时命名为其他名称，也继续使用原来的 v2ray1.exe/config/log 文件名。
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
# exe_name = f"{type_}.exe"
# exe_name_path = fr"{object_name}\{exe_name}"

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



# 配置区域 ============================================
V2RAY_CONFIG_PATH = r"config.json"  # V2Ray 配置文件路径
V2RAY_EXE_PATH = 'V2Ray'  # V2Ray 主程序路径
NODES = [
    {"name": "节点1", "ip": "114.132.40.118", "port": 30018, "id": "ffc75281-6c9a-4cd7-8af6-aaa12eb7496f"},
    {"name": "节点2", "ip": "195.154.40.247", "port": 39604, "id": "ade83fd4-5fe3-4862-8edf-be9eeb182435"},
]
# SPEED_TEST_URL = "https://example.com/100mb.bin"  # 测速文件URL
# SPEED_TEST_URL = "http://speedtest-sgp1.digitalocean.com/10mb.test"  # 测速文件URL
SPEED_TEST_URL = "https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif"  # 测速文件URL


# ===================================================


import sys


def extract_base64_from_data(data):
    """
    递归遍历数据结构，提取符合特征的Base64编码字符串
    """
    base64_strings = []

    def recursive_search(item):
        # 如果是字符串，检查是否符合Base64特征且是节点链接的编码
        if isinstance(item, str):
            # 节点链接的Base64通常以 vmess://、vless://、ss:// 等开头，编码后有特征
            # 同时长度较长（过滤掉短字符串），且符合Base64字符集
            if len(item) > 100:  # 过滤短字符串
                try:
                    # 尝试解码，验证是否为有效的Base64
                    # 先处理可能的填充问题
                    padding = len(item) % 4
                    if padding != 0:
                        item += '=' * (4 - padding)
                    # 解码验证
                    base64.b64decode(item, validate=True)
                    # 检查解码后是否包含节点协议特征（可选，增强准确性）
                    decoded = base64.b64decode(item).decode('utf-8', errors='ignore')
                    if any(protocol in decoded for protocol in ['vmess://', 'vless://', 'ss://', 'trojan://']):
                        base64_strings.append(item)
                except (base64.binascii.Error, ValueError):
                    # 不是有效的Base64，跳过
                    pass

        # 如果是列表，递归遍历每个元素
        elif isinstance(item, list):
            for sub_item in item:
                recursive_search(sub_item)

        # 如果是字典，递归遍历每个值
        elif isinstance(item, dict):
            for value in item.values():
                recursive_search(value)

    # 开始递归搜索
    recursive_search(data)
    return base64_strings
# 全局异常捕获
def exception_hook(exctype, value, tb):
    from datetime import datetime
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


def run_command(cmd: str) -> str:
    """执行命令行并返回输出"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def tcping(ip: str, port: int, count=3) -> float:
    """TCPing 测试延迟 (ms)"""
    cmd = f'tcping -n {count} {ip} {port}'
    output = run_command(cmd)

    # 解析平均延迟（示例输出："Average = 120ms"）
    for line in output.split('\n'):
        # print('line98',line)
        if "Average" in line:# Minimum = 38.560ms, Maximum = 64.959ms, Average = 52.615ms
            return float(line.split('=')[-1].strip().replace('ms', ''))
    return float('inf')  # 如果失败返回无限大


def speed_test(url: str, timeout=5) -> float:
    """CURL 下载测速 (MB/s)"""
    cmd = f'curl -o NUL -w "%{{speed_download}}" --max-time {timeout} {url}'
    print('cmd109',cmd)
    try:
        speed_bytes = float(run_command(cmd))
        return speed_bytes / (1024 * 1024)  # 转换为MB/s
    except:
        return 0


def evaluate_node(node: Dict) -> Dict:
    """评估节点质量（延迟 + 速度）"""
    print(f"正在测试节点 [{node['name']}]...")
    latency = tcping(node["ip"], node["port"])
    speed = speed_test(SPEED_TEST_URL)
    score = (1 / latency) * 0.7 + speed * 0.3  # 加权评分（延迟权重70%，速度30%）

    return {
        **node,
        "latency": latency,
        "speed": speed,
        "score": score
    }


def update_v2ray_config(best_node: Dict):
    """修改V2Ray配置文件"""
    with open(V2RAY_CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 更新outbound配置
    for outbound in config["outbounds"]:
        if outbound["tag"] == "proxy":
            outbound["settings"]["vnext"][0]["address"] = best_node["ip"]
            outbound["settings"]["vnext"][0]["port"] = best_node["port"]
            outbound["settings"]["vnext"][0]["users"][0]["id"] = best_node["id"]

    with open(V2RAY_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)


def restart_v2ray():
    """重启V2Ray服务"""
    run_command(f'taskkill /f /im v2ray.exe')
    time.sleep(2)
    subprocess.Popen([V2RAY_EXE_PATH, '-config', V2RAY_CONFIG_PATH], shell=True)

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
    # print('nuxt_script306',nuxt_script)
    if not nuxt_script:
        print("未找到__NUXT_DATA__脚本标签")
    else:
        # 3. 提取脚本内的JSON数据
        nuxt_data_str = nuxt_script.string.strip()
        try:
            # 解析JSON数组（__NUXT_DATA__是数组格式）
            # nuxt_data = json.loads(nuxt_data_str)
            # nuxt_data = nuxt_data_str
            for i,nuxt_data in enumerate(json.loads(nuxt_data_str)):
                # print('nuxt_data315',nuxt_data)
                if "'url': 392" in str(nuxt_data):
                    base64_str = json.loads(nuxt_data_str)[i+1]
                    # print('base64_str362',base64_str)
                    return base64_str
        except Exception as e:
            print(f"JSON解析失败：{e}")

    # 备用方案：如果上述方法失效，直接用正则全局匹配Base64串
    def extract_base64_by_regex(html_str):
        # 匹配以dmxlc3M6Ly8开头的Base64串（长度很长）
        pattern = re.compile(r'dmxlc3M6Ly8[A-Za-z0-9+/=]+')
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


def get_config_informationurl1(local_port):
    reg_list = []
    for i,url11_source in enumerate(url11_source_list):
        n = 0
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}
        while True:
            print(f'使用连接{url11_source}进行更新！')
            try:


                if n >= 8:
                    print('使用AI_all_auto代理88')
                    proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
                    try:
                        reg = requests.get(url11_source, headers=headers,proxies=proxies, timeout=8).text
                    except:
                        reg = requests.get(url11_list[i], headers=headers,proxies=proxies, timeout=8).text
                else:
                    print('不使用代理')
                    try:
                        reg = requests.get(url11_list[i], headers=headers, timeout=8).text
                    except:
                        reg = requests.get(url11_source, headers=headers, timeout=8).text
                # print(reg)
                # soup = BeautifulSoup(reg, 'html.parser')
                # reg_list.append(reg)
                if 'DOCTYPE html' in reg:
                    pass
                else:
                    reg_list += reg.split()
                    link_url2_successful = f'连接url11_source成功！'
                    print(link_url2_successful)
                    break

            except Exception as err:
                print(err)
                print(f'连接{url11_source}错误，2秒后重试！')
                time.sleep(2)
            # print(n)
            if n >= 18:
                break
            n += 1



    node_links = []
    for i,sss in enumerate(reg_list):
        # print(i)
        # print(sss[0:3])
        # if 'ss:' not in sss[0:3] and 'ssr:' not in sss[0:3]:
        if is_candidate_node_link(sss):
            print('识别到节点链接:', sss[:100])
            node_links.append(normalize_node_link(sss))
    node_links = list(dict.fromkeys(node_links))
    # print(node_links)
    print(f'541get_config_informationurl1共有节点数目为：{len(node_links)}')
    return node_links



def get_config_informationurl(local_port):

    node_links1 = []
    node_links2 = []
    try:
        node_links1 = get_config_informationurl1(local_port)
        pass
    except:
        traceback.print_exc()
    if not node_links1:
        node_links1 = []
    try:
        node_links2 = get_config_informationurl2(local_port)
        pass
    except:
        traceback.print_exc()
    node_link_list = node_links1 + node_links2
    # 解析所有节点
    backup_average_speed_list = []
    backup_valid_node_list = []
    valid_node_list = []
    average_speed_list = []
    link_err_list = []
    skipped_node_list = []
    node_link_list2 = []
    # print('\n'.join(node_link_list+node_link_list2))
    # while True:
    for i,link in enumerate(node_link_list+node_link_list2):

        # if i==3 :break #测试
        cmd_on_color.printMag(f"++++++++++++++++++++++++++处理节点进度{i+1}/{len(node_link_list)}++++++++++++++++++++++++++")
        # cmd_on_color.printCya(f"开始处理的第{i+1}个节点b64全部信息为：{link}")
        node = parse_node(link)
        if node:
            # 根据协议生成 Xray 或 sing-box 原生配置
            try:
                config, selected_core = generate_node_config(link, node, local_port)
            except Exception as config_error:
                print(f"生成节点配置失败 [{get_node_scheme(link)}]: {config_error}")
                link_err_list.append(link)
                continue

            if config and config != -1:
                # 保存到文件
                with open(object_name + fr'\{type_}_configs_port{local_port}.json', "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)

                with open(object_name + fr'\{type_}_configs_port88.json', "w", encoding='utf-8') as f:
                    config88 = json.loads(json.dumps(config, ensure_ascii=False))
                    set_config_inbound_port(config88, 88)
                    json.dump(config88, f, indent=2, ensure_ascii=False)
                # time.sleep(2)
                # upload(fr'{type_}_configs_port{local_port}.json')
                # upload(fr'{type_}_configs_port88.json')
            print(fr"配置文件已生成: \{type_}_configs_port{local_port}.json，开始对该节点{link}进行测速")
            # state_ = start_exe(local_port)
            # print('state_246', state_)#可以上网
            # # 第一层检测
            # if state_ == '可以上网':
            kill_all_proxy_cores()
            if selected_core == "sing-box":
                exe_name = SING_BOX_EXE_NAME
                exe_name_path = SING_BOX_EXE_PATH
                cmd = [exe_name_path, "run", "-c", os.path.join(object_name, f"{type_}_configs_port{local_port}.json")]
            else:
                exe_name = f"{type_}.exe"
                exe_name_path = os.path.join(object_name, exe_name)
                cmd = [exe_name_path, "run", "-config", os.path.join(object_name, f"{type_}_configs_port{local_port}.json")]
            print("启动核心命令:", subprocess.list2cmdline(cmd))
            if not os.path.isfile(exe_name_path):
                message = f"缺少核心程序 {exe_name}，该节点暂时跳过。请将核心放到程序目录：{exe_name_path}"
                cmd_on_color.printRed(message)
                link_err_list.append(link)
                continue
            process = subprocess.Popen(
                cmd,
                cwd=object_name,
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )

            # state, average_speed = download_files.download_file_state('https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif', os.getcwd() + r"\test_speed.gif", local_port)
            average_speed = download_files.test_speed(proxy_port=local_port)
            kill_all_proxy_cores()
            # 第二层检测
            if average_speed == '-1.000':
                cmd_on_color.printRed(f"{link[:18]}该节点不可以上网，准备换下一个节点！252")
            elif float(average_speed) < 2.000:
                cmd_on_color.printBlu(f'{link[:18]}该节点速度小于【2M】，不过【可以上网】，其平均速度为{average_speed}MB/s')
                backup_valid_node_list.append(link)
                backup_average_speed_list.append(average_speed)
            else:
                cmd_on_color.printGre(f'{link[:18]}该节点可以上网，其平均速度为{average_speed}MB/s')
                valid_node_list.append(link)
                average_speed_list.append(average_speed)
            # else:
            #     cmd_on_color.printRed(f"{link[:8]}该节点不可以上网，准备换下一个节点！258")
        else:
            scheme = get_node_scheme(link)
            if scheme and get_node_core(link) == "unsupported":
                skipped_node_list.append(link)
                cmd_on_color.printBlu(
                    f"已识别 {scheme}，但当前 Xray + sing-box 双核心配置暂不支持，跳过：{link[:100]}"
                )
            elif not scheme:
                # 网站地址、Website= 元信息、公告文字等不是节点，不计入解析错误
                skipped_node_list.append(link)
                print(f"跳过非节点订阅内容：{link[:100]}")
            else:
                cmd_on_color.printRed(f"{link}，该节点解析错误！")
                link_err_list.append(link)
        # sys.exit()
        # if '该节点解析错误' not in link_err_list:
        #     break

    kill_all_proxy_cores()
    cmd_on_color.printRed(
        f"真正解析失败的节点数目：{len(link_err_list)}个，具体如下：\n{link_err_list}"
    )
    cmd_on_color.printBlu(
        f"跳过的非节点/暂不支持节点数目：{len(skipped_node_list)}个"
    )
    cmd_on_color.printCya(f"总共需要处理的节点数目：{len(node_link_list)}")
    cmd_on_color.printMag(f'测速完成！{len(average_speed_list)}个有效节点的速度列表：{average_speed_list}')
    if len(average_speed_list) == 0:#如果节点为0个  就切换备用节点
        average_speed_list = backup_average_speed_list
        valid_node_list = backup_valid_node_list
        cmd_on_color.printMag(f'改用【小于2M】的备用节点数目！{len(average_speed_list)}个【备用】有效节点的速度列表：{average_speed_list}')
    # 步骤1: 生成带原始序号的元组列表
    indexed_data = list(enumerate(average_speed_list))  # [(0, '1.423'), (1, '1.213'), ...]

    # 步骤2: 按值排序（升序）
    valid_node_list_sorted_data = sorted(indexed_data, key=lambda x: float(x[1]), reverse=True)
    with open(fr'{object_name_output_log}/{type_}_valid_node_list_sorted_data.txt', 'w+', encoding='utf-8') as f:
        f.write(f'{valid_node_list_sorted_data}')
    with open(fr'{object_name_output_log}/{type_}_valid_node_list.txt', 'w+', encoding='utf-8') as f:
        f.write(f'{valid_node_list}')

    # 步骤3: 输出排序后的序号和对应值
    # print("排序后序号\t原始序号\t值")
    for new_idx, (old_idx, value) in enumerate(valid_node_list_sorted_data, start=1):
        if new_idx == 1:
            # print(f"{new_idx}\t\t{max_index}\t\t{max_value}")
            # max_index = average_speed_list.index(max_value)
            max_value = value
            max_index = old_idx
            very_good_node = valid_node_list[max_index]
            cmd_on_color.printBlu(f"速度最快的节点: {very_good_node}, 其速度为: {max_value}MB/s，开始将其写入配置文件，并运行！")
            node = parse_node(very_good_node)
            if node:
                very_good_config, _best_core = generate_node_config(very_good_node, node, local_port)
                return very_good_config
            return -1


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
            resp = requests.get(url, stream=True, timeout=8, headers=headers, proxies=proxies, verify=False)
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
        # if n > 0 :#test
            break
        time.sleep(2)
    return err


def kill_v2rayN_Alvin10899_exe():
    print('开始终止v2rayN_Alvin10899.exe')
    n = 0
    p = 0
    while True:
        os.system("taskkill /F /IM v2rayN_Alvin10899.exe")
        not_kill_list = []
        pids = psutil.pids()
        for pid in pids:
            try:
                p = psutil.Process(pid)
                if 'v2rayN_Alvin10899' in p.name():
                    not_kill_list.append('未杀死！')
                    #os.system("taskkill /PID " + str(p.pid))
                    #os.system('taskkill /pid ' + str(p.pid) + ' /f')
                else:
                    pass
            except:
                pass
        
        if len(not_kill_list) != 0:
            print('终止v2rayN_Alvin10899失败！准备开始重新终止！')
            try:
                #os.system("taskkill /PID " + str(p.pid))
                #os.system('taskkill /pid ' + str(p.pid) + ' /f')
                os.system("taskkill /F /IM v2rayN_Alvin10899.exe")
            except:
                traceback.print_exc()
                pass
        else:
            print('终止v2rayN_Alvin10899成功！')
            break
        
        time.sleep(2)
        if n >= 2:
            break
        n += 1



def kill_exe(exe_name = f"{type_}.exe"):
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
port88_err_num = 1
def start_exe(local_port, run_type='单独', err_node_number=1,show_notification_state = True):
    global port88_err_num
    file_path = object_name + fr'\{type_}_configs_port{local_port}.json'
    if run_type == '所有':
        exe_name = "v2ray_all.exe"
        core_kind = "xray"
    else:
        core_kind = detect_config_core(file_path) if os.path.exists(file_path) else "xray"
        exe_name = SING_BOX_EXE_NAME if core_kind == "sing-box" else f"{type_}.exe"
    exe_name_path = os.path.join(object_name, exe_name)
    print(f'开始启动{exe_name}')
    # if '表示子进程已经终止' in state:
    #     today_num = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    #     cmd_on_color.printRed(f"{today_num} 程序被杀死，准备重启！105")
    #     state = start_exe(local_port,run_type)
    # print(f'开始启动{exe_name}')
    file_path = object_name + fr'\{type_}_configs_port{local_port}.json'  # 替换为实际文件路径
    state = f'不可以上网'
    # node_int = 8
    try:
        with open(fr'{object_name_output_log}/{type_}_valid_node_list.txt', 'r+', encoding='utf-8') as f:
            valid_node_list = eval(f.read())
        node_int = len(valid_node_list)
    except:
        node_int = 0
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            print(f"文件 '{file_path}' 存在")
            for i in range(node_int):
                # cmd = f'"{exe_name_path}" -c "{object_name}\\{type_}_configs_port{local_port}.json" -vvv'
                config_arg = os.path.join(object_name, f"{type_}_configs_port{local_port}.json")
                if core_kind == "sing-box":
                    cmd = subprocess.list2cmdline([exe_name_path, "run", "-c", config_arg])
                else:
                    cmd = subprocess.list2cmdline([exe_name_path, "run", "-config", config_arg])
                state = str(run_exe(local_port, run_type, cmd, object_name_output_log, type_, exe_name, object_name, exe_name_path,err_node_number,show_notification_state))
                if '表示子进程已经终止' in state or '端口冲突' in state:
                    port88_err_num+=1
                    print('port88_err_num565',port88_err_num)
                    if port88_err_num<8:
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
                if run_type=='单独':
                    break
                    pass
                else:#全部  所有  D:\客户端集合代理\AI_all_auto.py
                    if f'不可以上网' in state or f'不可知的异常' in state:
                        cmd_on_color.printRed(f'{exe_name}第{i+1}个节点无法上网，准备切换第{i+2}个节点')
                        if run_type == '所有':
                            exe_name = f"v2ray_all.exe"
                            kill_exe(exe_name)
                        else:
                            kill_exe(exe_name)
                        try:
                            with open(fr'{object_name_output_log}/{type_}_valid_node_list_sorted_data.txt', 'r+', encoding='utf-8') as f:
                                valid_node_list_sorted_data = eval(f.read())
                            with open(fr'{object_name_output_log}/{type_}_valid_node_list.txt', 'r+', encoding='utf-8') as f:
                                valid_node_list = eval(f.read())

                            for new_idx, (old_idx, value) in enumerate(valid_node_list_sorted_data, start=1):
                                if new_idx == i+2:
                                    # print(f"{new_idx}\t\t{max_index}\t\t{max_value}")
                                    # max_index = average_speed_list.index(max_value)
                                    max_value = value
                                    max_index = old_idx
                                    very_good_node = valid_node_list[max_index]
                                    cmd_on_color.printBlu(f"节点: {very_good_node}, 其速度为: {max_value}MB/s，开始将其写入配置文件，并运行！")
                                    node = parse_node(very_good_node)
                                    very_good_config, core_kind = generate_node_config(very_good_node, node, local_port)
                                    exe_name = SING_BOX_EXE_NAME if core_kind == "sing-box" else f"{type_}.exe"
                                    exe_name_path = os.path.join(object_name, exe_name)
                                    if very_good_config and very_good_config != -1:
                                        # 保存到文件
                                        with open(object_name + fr'\{type_}_configs_port{local_port}.json', "w", encoding='utf-8') as f:
                                            json.dump(very_good_config, f, indent=2, ensure_ascii=False)

                                        with open(object_name + fr'\{type_}_configs_port88.json', "w", encoding='utf-8') as f:
                                            config88 = json.loads(json.dumps(very_good_config, ensure_ascii=False))
                                            set_config_inbound_port(config88, 88)
                                            json.dump(config88, f, indent=2, ensure_ascii=False)
                                        # time.sleep(2)
                                        # upload(fr'{type_}_configs_port{local_port}.json')
                                        # upload(fr'{type_}_configs_port88.json')
                                    print(f'开始杀死进程{exe_name}')
                                    kill_all_proxy_cores()  # 停止 Xray 和 sing-box
                        except:
                            state = f'不可以上网，配置文件不存在'
        else:
            print(f"'{file_path}' 存在，但不是文件")
    else:
        print(f"文件 '{file_path}' 不存在")
        state = f'不可以上网，配置文件不存在'
    if f'不可以上网' in state or f'不可知的异常' in state:
        if run_type=='单独':
            pass
        else:
            cmd_on_color.printRed(f'{exe_name}前{node_int}个速度最快的都不能上网！准备更换端口！')
        # os.system(f"taskkill /F /IM {exe_name}")
        pass
    return state



def main_proxy(local_port=10822):
    download_files.download_file(fr"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_configs_port{local_port}.json",
                                 f"{type_}_configs_port{local_port}.json")
    download_files.download_file(fr"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_configs_port88.json", f"{type_}_configs_port88.json")
    time.sleep(2)

    # 启动监控进程
    subprocess.Popen([sys.executable, "monitor.py", str(pid), f"{type_}"])
    kill_all_proxy_cores()



    exe_name = f"{type_}.exe"
    exe_name_path = fr"{object_name}\{exe_name}"
    cmd_on_color.printCya(f'++++++++++++++++++++++++++++++++启动{type_}中，请耐心等待............++++++++++++++++++++++++++++++++')
    very_good_config = -1
    n=0

    try:
        with open(fr'{object_name_output_log}/{type_}_valid_node_list.txt', 'r+', encoding='utf-8') as f:
            valid_node_list = eval(f.read())
        node_index = len(valid_node_list)
    except:
        node_index = 0
    if node_index == 0:#无有效节点  需要更新
        very_good_config = get_config_informationurl(local_port)
        if very_good_config and very_good_config != -1:
            # 保存到文件
            with open(object_name + fr'\{type_}_configs_port{local_port}.json', "w", encoding='utf-8') as f:
                json.dump(very_good_config, f, indent=2, ensure_ascii=False)

            with open(object_name + fr'\{type_}_configs_port88.json', "w", encoding='utf-8') as f:
                config88 = json.loads(json.dumps(very_good_config, ensure_ascii=False))
                set_config_inbound_port(config88, 88)
                json.dump(config88, f, indent=2, ensure_ascii=False)
            # time.sleep(2)
            # upload(fr'{type_}_configs_port{local_port}.json')
            # upload(fr'{type_}_configs_port88.json')
        print(f'575开始杀死进程{exe_name}')
        kill_all_proxy_cores()  # exe_name, exe_name_path, object_name
        try:
            with open(fr'{object_name_output_log}/{type_}_valid_node_list.txt', 'r+', encoding='utf-8') as f:
                valid_node_list = eval(f.read())
            node_index = len(valid_node_list)
        except:
            node_index = 0
    else:
        kill_all_proxy_cores()
        while True:
            try:
                with open(fr'{object_name_output_log}/{type_}_valid_node_list_sorted_data.txt', 'r+', encoding='utf-8') as f:
                    valid_node_list_sorted_data = eval(f.read())
                with open(fr'{object_name_output_log}/{type_}_valid_node_list.txt', 'r+', encoding='utf-8') as f:
                    valid_node_list = eval(f.read())
                break
            except:
                very_good_config = get_config_informationurl(local_port)
        for new_idx, (old_idx, value) in enumerate(valid_node_list_sorted_data, start=1):
            # if new_idx == i + 2:
                # print(f"{new_idx}\t\t{max_index}\t\t{max_value}")
                # max_index = average_speed_list.index(max_value)
                max_value = value
                max_index = old_idx
                very_good_node = valid_node_list[max_index]
                cmd_on_color.printBlu(f"节点: {very_good_node}, 其速度为: {max_value}MB/s，开始将其写入配置文件，并运行！")
                node = parse_node(very_good_node)
                very_good_config, _selected_core = generate_node_config(very_good_node, node, local_port)

        if very_good_config and very_good_config != -1:
            # 保存到文件
            with open(object_name + fr'\{type_}_configs_port{local_port}.json', "w", encoding='utf-8') as f:
                json.dump(very_good_config, f, indent=2, ensure_ascii=False)

            with open(object_name + fr'\{type_}_configs_port88.json', "w", encoding='utf-8') as f:
                config88 = json.loads(json.dumps(very_good_config, ensure_ascii=False))
                set_config_inbound_port(config88, 88)
                json.dump(config88, f, indent=2, ensure_ascii=False)
            # time.sleep(2)
            # # upload(fr'{type_}_configs_port{local_port}.json')
            # # upload(fr'{type_}_configs_port88.json')

    while True:
        try:
            cmd_on_color.printMag(fr'需要运行并【可以上网】的节点数目为：{node_index}个')
            for i in range(node_index):
                state_ = start_exe(local_port,err_node_number=n+1)
                print('state_412',state_)
                # time.sleep(188)
                # break
                if f'不可以上网' in state_ or f'不可知的异常' in state_:
                    if n <= 2:
                        show_notification(f"端口 {local_port} 链接错误！准备更新配置", f"{state_}【第{i+1}次检测)】", "error")
                    if '配置文件不存在' in state_ or '配置缺失' in state_:

                        print(f'代理错误，IP配置有错误？开始重新获取最新IP配置=={type_}')
                        very_good_config = get_config_informationurl(local_port)
                        # i-=1
                        # config = get_config_informationurl1()
                        # config = get_config_informationurl3()
                    else:##  只是 不可以上网
                        cmd_on_color.printRed(f'{exe_name}第{i + 1}个节点无法上网，准备切换第{i + 2}个节点')
                        kill_all_proxy_cores()
                        while True:
                            try:
                                with open(fr'{object_name_output_log}/{type_}_valid_node_list_sorted_data.txt', 'r+', encoding='utf-8') as f:
                                    valid_node_list_sorted_data = eval(f.read())
                                with open(fr'{object_name_output_log}/{type_}_valid_node_list.txt', 'r+', encoding='utf-8') as f:
                                    valid_node_list = eval(f.read())
                                break
                            except:
                                very_good_config = get_config_informationurl(local_port)
                        for new_idx, (old_idx, value) in enumerate(valid_node_list_sorted_data, start=1):
                            if new_idx == i + 2:
                                # print(f"{new_idx}\t\t{max_index}\t\t{max_value}")
                                # max_index = average_speed_list.index(max_value)
                                max_value = value
                                max_index = old_idx
                                very_good_node = valid_node_list[max_index]
                                cmd_on_color.printBlu(f"节点: {very_good_node}, 其速度为: {max_value}MB/s，开始将其写入配置文件，并运行！")
                                node = parse_node(very_good_node)
                                very_good_config, _selected_core = generate_node_config(very_good_node, node, local_port)
                    # print('very_good_config596',very_good_config)
                    if very_good_config and very_good_config!=-1:
                        # 保存到文件
                        with open(object_name + fr'\{type_}_configs_port{local_port}.json', "w", encoding='utf-8') as f:
                            json.dump(very_good_config, f, indent=2, ensure_ascii=False)

                        with open(object_name + fr'\{type_}_configs_port88.json', "w", encoding='utf-8') as f:
                            config88 = json.loads(json.dumps(very_good_config, ensure_ascii=False))
                            set_config_inbound_port(config88, 88)
                            json.dump(config88, f, indent=2, ensure_ascii=False)
                        # time.sleep(2)
                        # # upload(fr'{type_}_configs_port{local_port}.json')
                        # # upload(fr'{type_}_configs_port88.json')

                    print(f'开始杀死进程{exe_name}')
                    kill_all_proxy_cores()  # exe_name, exe_name_path, object_name
                if state_ == f'有一个在运行，不能同时运行2个':
                    def popup():
                        win32api.MessageBox(None, f'有一个在运行，不能同时运行2个{type_}', '来自FSO的警告', win32con.MB_ICONWARNING + win32con.MB_SERVICE_NOTIFICATION)

                    threading.Thread(target=popup).start()

                    break
            cmd_on_color.printRed(f'{exe_name}前{node_index}个速度最快的都不能上网！准备重新获取最新IP配置！')
            very_good_config = get_config_informationurl(local_port)
            if very_good_config and very_good_config != -1:
                # 保存到文件
                with open(object_name + fr'\{type_}_configs_port{local_port}.json', "w", encoding='utf-8') as f:
                    json.dump(very_good_config, f, indent=2, ensure_ascii=False)

                with open(object_name + fr'\{type_}_configs_port88.json', "w", encoding='utf-8') as f:
                    config88 = json.loads(json.dumps(very_good_config, ensure_ascii=False))
                    set_config_inbound_port(config88, 88)
                    json.dump(config88, f, indent=2, ensure_ascii=False)
                # time.sleep(2)
                # upload(fr'{type_}_configs_port{local_port}.json')
                # upload(fr'{type_}_configs_port88.json')
            print(f'开始杀死进程{exe_name}')
            kill_all_proxy_cores()  # exe_name, exe_name_path, object_name
            if n>18:
                n = 0
                download_files.download_file(fr"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_configs_port{local_port}.json",
                                             f"{type_}_configs_port{local_port}.json")
                download_files.download_file(fr"https://nvst-video-tio.oss-cn-chengdu.aliyuncs.com/20260909/9/9/{type_}_configs_port88.json", f"{type_}_configs_port88.json")
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


def parse_vmess(vmess_link):
    """
    解析 VMess 节点。

    支持：
    1. 标准 vmess://Base64(JSON)#备注
    2. URL-safe Base64 和缺少填充的 Base64
    3. UUID@服务器:端口?参数#备注 形式

    注意：
    第3种形式并非传统 VMess JSON 格式。
    其结构属于 VLESS 风格，因此按 VLESS 出站生成。
    """
    try:
        if not isinstance(vmess_link, str):
            return None

        vmess_link = vmess_link.strip()
        if not vmess_link.lower().startswith("vmess://"):
            return None

        # 去除协议头
        content = vmess_link[8:].strip()

        if not content:
            return None

        # -------------------------------------------------
        # 第一种：UUID@服务器:端口 URI 风格
        # -------------------------------------------------
        if "@" in content.split("#", 1)[0]:

            # 把备注、查询参数和服务器信息分开
            parsed = urlsplit("vless://" + content)

            address = parsed.hostname
            port = parsed.port
            user_id = unquote(parsed.username or "")
            query = parse_qs(parsed.query)

            if not address or not port or not user_id:
                print("VMess URI风格节点缺少服务器地址、端口或UUID")
                return None

            network = query.get("type", ["tcp"])[0].lower()
            security = query.get("security", ["none"])[0].lower()
            host = query.get("host", [""])[0]
            path = query.get("path", [""])[0]
            sni = query.get("sni", [""])[0]
            fingerprint = query.get("fp", [""])[0]

            stream_settings = {
                "network": network,
                "security": security
            }

            if security == "tls":
                stream_settings["tlsSettings"] = {
                    "serverName": sni or host or address,
                    "fingerprint": fingerprint,
                    "allowInsecure": query.get(
                        "allowInsecure", ["0"]
                    )[0] == "1"
                }
            elif security == "reality":
                stream_settings["realitySettings"] = {
                    "serverName": sni or host or address,
                    "fingerprint": fingerprint or "chrome",
                    "publicKey": query.get("pbk", [""])[0],
                    "shortId": query.get("sid", [""])[0],
                    "spiderX": query.get("spx", ["/"])[0]
                }

            if network == "ws":
                stream_settings["wsSettings"] = {
                    "path": path or "/",
                    "headers": {"Host": host} if host else {}
                }

            elif network == "httpupgrade":
                stream_settings["httpupgradeSettings"] = {
                    "path": path or "/",
                    "host": host or address
                }

            elif network == "grpc":
                stream_settings["grpcSettings"] = {
                    "serviceName": query.get(
                        "serviceName", [path.lstrip("/")]
                    )[0]
                }

            elif network in ("tcp", "raw"):
                stream_settings["network"] = "tcp"
                stream_settings["tcpSettings"] = {
                    "header": {
                        "type": query.get("headerType", ["none"])[0]
                    }
                }

            return {
                "protocol": "vless",
                "settings": {
                    "vnext": [{
                        "address": address,
                        "port": int(port),
                        "users": [{
                            "id": user_id,
                            "encryption": "none",
                            "flow": query.get("flow", [""])[0]
                        }]
                    }]
                },
                "streamSettings": stream_settings,
                "tag": unquote(parsed.fragment or "vless_uri_node")
            }

        # -------------------------------------------------
        # 第二种：标准 VMess Base64 JSON
        # -------------------------------------------------

        # 必须先去掉 #备注，不能把备注一起进行 Base64 解码
        b64_part = content.split("#", 1)[0].strip()

        # 某些订阅使用 URL-safe Base64
        b64_part = b64_part.replace("-", "+").replace("_", "/")

        # 清除可能出现的空白字符
        b64_part = "".join(b64_part.split())

        # 补齐 Base64
        b64_part += "=" * (-len(b64_part) % 4)

        # 解码
        decoded_bytes = base64.b64decode(b64_part)

        # UTF-8 解码
        vmess_json = decoded_bytes.decode("utf-8-sig")

        vmess = json.loads(vmess_json)

        if not isinstance(vmess, dict):
            print("VMess JSON格式错误")
            return None

        # 必要字段检查
        address = vmess.get("add") or vmess.get("address")
        port = vmess.get("port")
        user_id = vmess.get("id")

        if not address or not port or not user_id:
            print("VMess节点缺少 add、port 或 id")
            return None

        # alterId
        try:
            alter_id = int(vmess.get("aid", 0))
        except (ValueError, TypeError):
            alter_id = 0

        # 端口
        port = int(port)

        # 网络类型
        network = str(vmess.get("net", "tcp")).lower()

        # TLS
        tls_value = str(vmess.get("tls", "")).lower()
        security = "tls" if tls_value in ("tls", "true") else "none"

        host = vmess.get("host", "")
        path = vmess.get("path", "")

        stream_settings = {
            "network": network,
            "security": security
        }

        if security == "tls":
            stream_settings["tlsSettings"] = {
                "serverName": vmess.get("sni") or host or address,
                "allowInsecure": str(
                    vmess.get("allowInsecure", "0")
                ).lower() in ("1", "true")
            }

        if network == "ws":
            stream_settings["wsSettings"] = {
                "path": path or "/",
                "headers": {"Host": host} if host else {}
            }

        elif network == "httpupgrade":
            stream_settings["httpupgradeSettings"] = {
                "path": path or "/",
                "host": host or address
            }

        elif network == "grpc":
            stream_settings["grpcSettings"] = {
                "serviceName": vmess.get("serviceName", "")
            }

        elif network in ("tcp", "raw"):
            stream_settings["network"] = "tcp"
            stream_settings["tcpSettings"] = {
                "header": {
                    "type": vmess.get("type", "none")
                }
            }

        return {
            "protocol": "vmess",
            "settings": {
                "vnext": [{
                    "address": address,
                    "port": port,
                    "users": [{
                        "id": user_id,
                        "alterId": alter_id,
                        "security": vmess.get("scy", "auto")
                    }]
                }]
            },
            "streamSettings": stream_settings,
            "tag": unquote(vmess.get("ps", "vmess_node"))
        }

    except Exception as e:
        print(f"VMess 解析失败: {type(e).__name__}: {str(e)}")
        return None

def parse_trojan(trojan_link):
    """解析 Trojan 链接"""
    parsed = urlparse(trojan_link)
    query = parse_qs(parsed.query)

    stream_settings = {
        "network": query.get("type", ["tcp"])[0],
        "security": query.get("security", ["tls"])[0],
        "tlsSettings": {
            "serverName": query.get("sni", [""])[0],
            "allowInsecure": query.get("allowInsecure", ["0"])[0] == "1"
        },
        "wsSettings": {
            "path": query.get("path", [""])[0],
            "headers": {"Host": query.get("host", [query.get("sni", [""])[0]])[0]}
        } if query.get("type", [""])[0] == "ws" else None
    }

    # 清理空值
    stream_settings = {k: v for k, v in stream_settings.items() if v is not None}

    return {
        "protocol": "trojan",
        "settings": {
            "servers": [{
                "address": parsed.hostname,
                "port": parsed.port,
                "password": parsed.username,
                # "flow": query.get("flow", [""])[0],
                "level": 0
            }]
        },
        "streamSettings": stream_settings,
        "tag": unquote(parsed.fragment or "trojan_node")
    }


def parse_vless(vless_link):
    """解析 VLESS 链接"""
    parsed = urlparse(vless_link)
    query = parse_qs(parsed.query)

    stream_settings = {
        "network": query.get("type", ["tcp"])[0],
        "security": query.get("security", ["none"])[0],
        "tlsSettings": {
            "serverName": query.get("sni", [""])[0],
            "fingerprint": query.get("fp", [""])[0],
            "allowInsecure": query.get("allowInsecure", ["0"])[0] == "1"
        },
        "wsSettings": {
            "path": query.get("path", [""])[0],
            "headers": {"Host": query.get("host", [""])[0]}
        } if query.get("type", [""])[0] == "ws" else None,
        "grpcSettings": {
            "serviceName": query.get("serviceName", [""])[0]
        } if query.get("type", [""])[0] == "grpc" else None
    }

    # 清理空值
    stream_settings = {k: v for k, v in stream_settings.items() if v is not None}

    return {
        "protocol": "vless",
        "settings": {
            "vnext": [{
                "address": parsed.hostname,
                "port": parsed.port,
                "users": [{
                    "id": parsed.username,
                    # "flow": query.get("flow", [""])[0],
                    "encryption": "none"
                }]
            }]
        },
        "streamSettings": stream_settings,
        "tag": unquote(parsed.fragment or "vless_node")
    }

def parse_hysteria(hysteria_link):
    """解析 hysteria 链接"""
    parsed = urlparse(hysteria_link)
    query = parse_qs(parsed.query)

    # 提取基础信息
    auth_part = parsed.netloc.split('@')
    if len(auth_part) == 2:
        password = auth_part[0]
        server_info = auth_part[1]
    else:
        password = ""
        server_info = auth_part[0]

    server_parts = server_info.split(':')
    address = server_parts[0]
    port = int(server_parts[1]) if len(server_parts) > 1 else 443

    return {
        "protocol": "hysteria",
        "settings": {
            "servers": [
                {
                    "address": address,
                    "port": port,
                    "password": password,
                    "insecure": query.get("insecure", ["0"])[0] == "1",
                    "sni": query.get("sni", [""])[0]
                }
            ]
        },
        "streamSettings": {
            "network": "udp",
            "security": "tls",
            "tlsSettings": {
                "serverName": query.get("sni", [""])[0],
                "allowInsecure": query.get("insecure", ["0"])[0] == "1"
            }
        },
        "tag": unquote(parsed.fragment or "hysteria_node")
    }


def parse_hysteria2(hysteria2_link):
    """解析 Hysteria2 链接"""
    parsed = urlparse(hysteria2_link)
    query = parse_qs(parsed.query)

    # 提取基础信息
    auth_part = parsed.netloc.split('@')
    if len(auth_part) == 2:
        password = auth_part[0]
        server_info = auth_part[1]
    else:
        password = ""
        server_info = auth_part[0]

    server_parts = server_info.split(':')
    address = server_parts[0]
    port = int(server_parts[1]) if len(server_parts) > 1 else 443

    return {
        "protocol": "hysteria2",
        "settings": {
            "servers": [
                {
                    "address": address,
                    "port": port,
                    "password": password,
                    "insecure": query.get("insecure", ["0"])[0] == "1",
                    "sni": query.get("sni", [""])[0]
                }
            ]
        },
        "streamSettings": {
            "network": "udp",
            "security": "tls",
            "tlsSettings": {
                "serverName": query.get("sni", [""])[0],
                "allowInsecure": query.get("insecure", ["0"])[0] == "1"
            }
        },
        "tag": unquote(parsed.fragment or "hysteria2_node")
    }


def parse_shadowsocks(ss_link):
    """
    解析 Shadowsocks 节点。

    支持：
    1. SIP002:
       ss://BASE64(method:password)@host:port#name

    2. 旧式:
       ss://BASE64(method:password@host:port)#name

    3. 明文形式:
       ss://method:password@host:port#name

    同时支持 URL-safe Base64 和缺失填充。
    """

    def decode_base64_text(value):
        """兼容标准 Base64、URL-safe Base64 和缺失填充。"""
        value = "".join(str(value).split())
        value = value.replace("-", "+").replace("_", "/")
        value += "=" * (-len(value) % 4)

        decoded = base64.b64decode(value)
        return decoded.decode("utf-8-sig")

    try:
        if not isinstance(ss_link, str):
            return None

        ss_link = ss_link.strip()

        if not ss_link.lower().startswith("ss://"):
            return None

        parsed = urlsplit(ss_link)

        # 节点备注
        tag = unquote(parsed.fragment or "ss_node")

        # -------------------------------------------------
        # 第一种：SIP002 格式
        # ss://BASE64(method:password)@host:port
        # -------------------------------------------------

        if parsed.hostname and parsed.port:

            host = parsed.hostname
            port = int(parsed.port)

            # 取出 @ 前面的认证部分
            user_info = parsed.netloc.rsplit("@", 1)[0]

            # 去除可能存在的用户信息百分号编码
            user_info = unquote(user_info)

            if ":" in user_info and not user_info.startswith(
                ("ey",)
            ):
                # 明文 method:password
                auth = user_info
            else:
                # Base64 method:password
                auth = decode_base64_text(user_info)

            if ":" not in auth:
                print("SS认证信息缺少 method:password")
                return None

            method, password = auth.split(":", 1)

        else:
            # -------------------------------------------------
            # 第二种：旧式完整 Base64 格式
            # ss://BASE64(method:password@host:port)
            # -------------------------------------------------

            b64_part = ss_link[5:].split("#", 1)[0]
            b64_part = b64_part.split("?", 1)[0]

            decoded = decode_base64_text(b64_part)

            if "@" not in decoded:
                print("SS旧式链接缺少 @ 分隔符")
                return None

            auth, server = decoded.rsplit("@", 1)

            if ":" not in auth:
                print("SS旧式链接缺少 method:password")
                return None

            method, password = auth.split(":", 1)

            # 服务器地址和端口
            server_parsed = urlsplit("//" + server)

            host = server_parsed.hostname
            port = server_parsed.port

            if not host or not port:
                print("SS旧式链接服务器地址或端口无效")
                return None

        # -------------------------------------------------
        # 最终检查
        # -------------------------------------------------

        method = method.strip()
        password = password.strip()

        if not method or not password or not host or not port:
            print("SS节点信息不完整")
            return None

        return {
            "protocol": "shadowsocks",
            "settings": {
                "servers": [{
                    "address": host,
                    "port": int(port),
                    "method": method,
                    "password": password,
                    "level": 0
                }]
            },
            "tag": tag
        }

    except Exception as e:
        print(f"SS 解析失败: {type(e).__name__}: {str(e)}")
        return None


def parse_shadowsocksr(ssr_link):
    """解析 ShadowsocksR (SSR) 链接"""
    if not ssr_link.startswith('ssr://'):
        return None

    try:
        # 处理 SSR 的 base64 编码
        b64_part = ssr_link[6:].split('/')[0]
        b64_part += '=' * (-len(b64_part) % 4)
        decoded = base64.b64decode(b64_part).decode('utf-8')

        # SSR 格式：server:port:protocol:method:obfs:password_base64/?params
        parts = decoded.split(':')
        if len(parts) < 6:
            return None

        server = parts[0]
        port = parts[1]
        protocol = parts[2]
        method = parts[3]
        obfs = parts[4]
        password = base64.b64decode(parts[5] + '=' * (-len(parts[5]) % 4)).decode('utf-8')

        return {
            "protocol": "shadowsocksr",
            "settings": {
                "servers": [{
                    "address": server,
                    "port": int(port),
                    "method": method,
                    "password": password,
                    "protocol": protocol,
                    "protocol_param": "",
                    "obfs": obfs,
                    "obfs_param": ""
                }]
            },
            "tag": "ssr_node"
        }
    except Exception as e:
        print(f"SSR 解析失败: {str(e)}")
        return None


def parse_socks(socks_link):
    """解析 SOCKS4/SOCKS5/SOCKS5H 链接。"""
    parsed = urlsplit(socks_link)
    if parsed.scheme.lower() not in ("socks", "socks4", "socks5", "socks5h"):
        return None

    host = parsed.hostname
    port = parsed.port
    if not host or port is None:
        return None

    username = unquote(parsed.username) if parsed.username else None
    password = unquote(parsed.password) if parsed.password else None

    users = []
    if username is not None:
        users.append({
            "user": username,
            "pass": password or "",
            "level": 0
        })

    return {
        "protocol": "socks",
        "settings": {
            "servers": [{
                "address": host,
                "port": int(port),
                "users": users
            }]
        },
        "tag": unquote(parsed.fragment) if parsed.fragment else "socks_node"
    }


def parse_http(http_link):
    """解析 HTTP/HTTPS 代理分享链接；普通网页 URL 不会被当成代理。"""
    parsed = urlsplit(http_link)
    if parsed.scheme.lower() not in ("http", "https"):
        return None

    host = parsed.hostname
    port = parsed.port
    if not host or port is None:
        return None

    username = unquote(parsed.username) if parsed.username else None
    password = unquote(parsed.password) if parsed.password else None

    users = []
    if username is not None:
        users.append({"user": username, "pass": password or ""})

    return {
        "protocol": "http",
        "settings": {
            "servers": [{
                "address": host,
                "port": int(port),
                "users": users
            }]
        },
        "tag": unquote(parsed.fragment) if parsed.fragment else "http_node"
    }


def parse_mtproto(mtproto_link):
    """解析 MTProto 链接 (Telegram)"""
    if not mtproto_link.startswith('tg://'):
        return None

    # tg://proxy?server=host&port=443&secret=ee...
    query = parse_qs(urlparse(mtproto_link).query)

    return {
        "protocol": "mtproto",
        "settings": {
            "servers": [{
                "address": query.get('server', [''])[0],
                "port": int(query.get('port', ['443'])[0]),
                "secret": query.get('secret', [''])[0]
            }]
        },
        "tag": "mtproto_node"
    }



# 支持的分享链接协议。AnyTLS 单独识别，但当前由 Xray 核心运行时不支持。
NODE_SCHEMES = {
    "vmess", "trojan", "vless", "hysteria", "hysteria2", "tuic",
    "ss", "ssr", "socks", "socks4", "socks5", "socks5h",
    "http", "https", "tg", "anytls"
}

# Xray 负责传统 V2Ray 协议；sing-box 负责 Xray 不支持但 sing-box 支持的协议。
SING_BOX_SCHEMES = {"anytls", "hysteria", "hysteria2", "tuic"}
SING_BOX_EXE_NAME = "sing-box.exe"
SING_BOX_EXE_PATH = os.path.join(object_name, SING_BOX_EXE_NAME)


def get_node_core(link):
    """根据分享链接协议选择核心。返回 xray / sing-box / unsupported。"""
    scheme = get_node_scheme(link)
    if scheme in SING_BOX_SCHEMES:
        return "sing-box"
    if scheme in {"ssr", "tg"}:
        # 当前 sing-box 稳定版的官方出站类型列表不包含 SSR / MTProto。
        return "unsupported"
    if scheme in NODE_SCHEMES:
        return "xray"
    return "unsupported"


def _query_bool(query, *keys, default=False):
    for key in keys:
        if key in query and query[key]:
            return str(query[key][0]).strip().lower() in ("1", "true", "yes", "on")
    return default


def _tls_config(query, default_server_name=""):
    tls = {"enabled": True}
    server_name = query.get("sni", query.get("peer", [default_server_name]))[0]
    if server_name:
        tls["server_name"] = server_name
    if _query_bool(query, "insecure", "allowInsecure", "allow_insecure"):
        tls["insecure"] = True
    alpn = query.get("alpn", [""])[0]
    if alpn:
        tls["alpn"] = [x.strip() for x in alpn.split(",") if x.strip()]
    return tls


def generate_singbox_config(link, local_port):
    """将 AnyTLS/Hysteria/Hysteria2/TUIC 分享链接转换为 sing-box 1.14.x 配置。"""
    link = normalize_node_link(link)
    parsed = urlparse(link)
    scheme = parsed.scheme.lower()
    query = parse_qs(parsed.query, keep_blank_values=True)
    host = parsed.hostname
    port = parsed.port
    if not host or not port:
        raise ValueError(f"节点缺少服务器地址或端口: {link[:100]}")

    outbound = {"tag": "proxy"}
    if scheme == "anytls":
        # anytls://password@server:port?security=tls&sni=...
        outbound.update({
            "type": "anytls",
            "server": host,
            "server_port": port,
            "password": unquote(parsed.username or ""),
            "tls": _tls_config(query, host),
        })
    elif scheme == "hysteria2":
        outbound.update({
            "type": "hysteria2",
            "server": host,
            "server_port": port,
            "password": unquote(parsed.username or ""),
            "tls": _tls_config(query, host),
        })
        obfs_type = query.get("obfs", [""])[0]
        obfs_password = query.get("obfs-password", query.get("obfs_password", [""]))[0]
        if obfs_type and obfs_password:
            outbound["obfs"] = {"type": obfs_type, "password": obfs_password}
        up = query.get("upmbps", query.get("up_mbps", [""]))[0]
        down = query.get("downmbps", query.get("down_mbps", [""]))[0]
        if up.isdigit():
            outbound["up_mbps"] = int(up)
        if down.isdigit():
            outbound["down_mbps"] = int(down)
    elif scheme == "hysteria":
        # 常见 hysteria://auth@host:port?auth=...&obfs=...&sni=...
        auth = query.get("auth", [unquote(parsed.username or "")])[0]
        outbound.update({
            "type": "hysteria",
            "server": host,
            "server_port": port,
            "auth_str": auth,
            "tls": _tls_config(query, host),
        })
        obfs = query.get("obfs", [""])[0]
        if obfs:
            outbound["obfs"] = obfs
        up = query.get("upmbps", query.get("up_mbps", ["100"]))[0]
        down = query.get("downmbps", query.get("down_mbps", ["100"]))[0]
        outbound["up_mbps"] = int(up) if str(up).isdigit() else 100
        outbound["down_mbps"] = int(down) if str(down).isdigit() else 100
    elif scheme == "tuic":
        # tuic://uuid:password@host:port?congestion_control=bbr&udp_relay_mode=native&sni=...
        outbound.update({
            "type": "tuic",
            "server": host,
            "server_port": port,
            "uuid": unquote(parsed.username or ""),
            "password": unquote(parsed.password or ""),
            "congestion_control": query.get("congestion_control", ["bbr"])[0],
            "udp_relay_mode": query.get("udp_relay_mode", ["native"])[0],
            "tls": _tls_config(query, host),
        })
    else:
        raise ValueError(f"sing-box 暂不处理该协议: {scheme}")

    tag = unquote(parsed.fragment or f"{scheme}_node")
    outbound["tag"] = "proxy"
    return {
        "log": {"level": "warn"},
        "inbounds": [{
            "type": "socks",
            "tag": "socks-in",
            "listen": "127.0.0.1",
            "listen_port": int(local_port)
        }],
        "outbounds": [
            outbound,
            {"type": "direct", "tag": "direct"}
        ],
        "route": {"final": "proxy"}
    }


def generate_node_config(link, parsed_node, local_port):
    """统一配置入口，按协议选择 Xray 或 sing-box。"""
    core = get_node_core(link)
    if core == "sing-box":
        return generate_singbox_config(link, local_port), core
    if core == "xray":
        return generate_config([parsed_node], local_port), core
    raise ValueError(f"当前没有可用核心支持该协议: {get_node_scheme(link)}")


def set_config_inbound_port(config, port):
    """同时兼容 Xray 的 inbound.port 与 sing-box 的 inbound.listen_port。"""
    inbound = config["inbounds"][0]
    if "listen_port" in inbound:
        inbound["listen_port"] = int(port)
    else:
        inbound["port"] = int(port)


def detect_config_core(config_path):
    """通过配置结构判断配置属于 sing-box 还是 Xray。"""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        inbound = (cfg.get("inbounds") or [{}])[0]
        return "sing-box" if "type" in inbound and "listen_port" in inbound else "xray"
    except Exception:
        return "xray"


def kill_all_proxy_cores():
    """停止本程序可能启动的两个核心，避免旧核心占用测速端口。"""
    for name in (f"{type_}.exe", SING_BOX_EXE_NAME):
        try:
            kill_exe(name)
        except Exception:
            traceback.print_exc()



def normalize_node_link(link):
    """清理订阅中的链接文本，不改动节点参数本身。"""
    if not isinstance(link, str):
        return ""
    link = html_unescape(link).strip().lstrip("\ufeff")
    # 兼容日志/订阅中出现的转义形式 https\\://
    link = re.sub(r"\\+://", "://", link)
    # 有些订阅将节点写成 markdown 链接，先不尝试猜测/改写其参数
    return link.strip().strip('"').strip("'")


def get_node_scheme(link):
    """返回明确的协议名；普通网址说明、公告等返回空字符串。"""
    link = normalize_node_link(link)
    if not link or "://" not in link:
        return ""
    scheme = link.split("://", 1)[0].lower()
    return scheme if scheme in NODE_SCHEMES else ""


def is_candidate_node_link(link):
    """订阅抓取阶段只保留明确的节点协议，避免把 Website= 等文本送去解析。"""
    scheme = get_node_scheme(link)
    if not scheme:
        return False
    if scheme in ("http", "https"):
        try:
            parsed = urlsplit(normalize_node_link(link))
            return bool(parsed.hostname and parsed.port is not None)
        except ValueError:
            return False
    return True


def extract_subscription_links(raw_text):
    """
    兼容明文节点订阅和 Base64 节点订阅。
    不再对普通 HTML/说明文字盲目 Base64 解码。
    """
    if not isinstance(raw_text, str):
        return []

    raw_text = html_unescape(raw_text).strip().lstrip("\ufeff")
    candidates = []

    def collect(text):
        found = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            # 订阅文件有时一行包含多个空格分隔节点
            for token in re.split(r"\s+", line):
                token = normalize_node_link(token)
                if is_candidate_node_link(token):
                    found.append(token)
        return found

    candidates = collect(raw_text)
    if candidates:
        return list(dict.fromkeys(candidates))

    # 明文没有节点时，再尝试 Base64（标准及 URL-safe）
    compact = re.sub(r"\s+", "", raw_text)
    if not compact:
        return []

    try:
        padded = compact + "=" * (-len(compact) % 4)
        decoded_bytes = base64.urlsafe_b64decode(padded.encode("ascii"))
        decoded_text = decoded_bytes.decode("utf-8-sig", errors="strict")
    except Exception:
        return []

    candidates = collect(decoded_text)
    return list(dict.fromkeys(candidates))


def parse_node(link):
    """自动识别节点；sing-box 协议返回核心标记，Xray 协议返回原有出站字典。"""
    link = normalize_node_link(link)
    if not link:
        return None

    lower_link = link.lower()
    if lower_link.startswith(("#", ";", "//", "website=", "website:",
                              "update=", "更新时间", "订阅地址", "剩余流量",
                              "过期时间", "套餐到期", "流量信息")):
        print(f"跳过订阅说明/元信息: {link[:80]}")
        return None

    scheme = get_node_scheme(link)
    if not scheme:
        print(f"跳过非节点订阅内容: {link[:80]}")
        return None

    core = get_node_core(link)
    if core == "sing-box":
        # 保留原始分享链接，稍后按 sing-box 原生 JSON 格式生成配置。
        return {"_core": "sing-box", "_link": link, "protocol": scheme,
                "tag": unquote(urlparse(link).fragment or f"{scheme}_node")}
    if core == "unsupported":
        print(f"当前双核心组合暂不支持 {scheme} 协议，跳过: {link[:100]}")
        return None

    parsers = {
        "vmess": parse_vmess,
        "trojan": parse_trojan,
        "vless": parse_vless,
        "ss": parse_shadowsocks,
        "socks": parse_socks,
        "socks4": parse_socks,
        "socks5": parse_socks,
        "socks5h": parse_socks,
        "http": parse_http,
        "https": parse_http,
    }
    if scheme in ("http", "https"):
        try:
            parsed_url = urlsplit(link)
            if not parsed_url.hostname or parsed_url.port is None:
                print(f"跳过普通网页（不是 HTTP 代理节点）: {link[:80]}")
                return None
        except ValueError as exc:
            print(f"HTTP代理链接格式错误: {exc}")
            return None

    parser = parsers.get(scheme)
    if parser is None:
        print(f"暂不支持的节点协议: {scheme}")
        return None
    try:
        node = parser(link)
        if not node:
            print(f"{scheme} 节点内容不完整或解析失败: {link}")
        return node
    except Exception as exc:
        print(f"解析链接失败 [{link}]: {type(exc).__name__}: {exc}")
        return None


def generate_config(nodes, local_port,template=None):
    """生成完整 config.json"""
    if template is None:
        template = {
            "log": {
                "loglevel": "warning"
            },
            "inbounds": [
                {
                    "port": local_port,
                    "listen": "127.0.0.1",
                    "protocol": "socks",
                    "settings": {
                        "auth": "noauth",
                        # "udp": False,
                        "udp": True,
                        "ip": "127.0.0.1"
                    },
                    "sniffing": {
                        "enabled": True,
                        "destOverride": ["http", "tls"]
                    },
                    "tag": "socks-inbound"
                }
            ],
            "dns": {
                "hosts": {
                    "domain:v2fly.org": "www.vicemc.net",
                    "domain:github.io": "pages.github.com",
                    "domain:wikipedia.org": "www.wikimedia.org",
                    "domain:shadowsocks.org": "electronicsrealm.com"
                },
                "servers": [
                    "localhost"
                ]

            },
            "policy": {
                "levels": {
                    "0": {
                        "uplinkOnly": 0,
                        "downlinkOnly": 0
                    }
                },
                "system": {
                    "statsInboundUplink": False,
                    "statsInboundDownlink": False,
                    "statsOutboundUplink": False,
                    "statsOutboundDownlink": False
                }
            }
        }

    # 添加节点出站配置
    template["outbounds"] = nodes + [
        {
            "protocol": "freedom",
            "settings": {},
            "tag": "direct"
        },
        {
            "protocol": "blackhole",
            "settings": {},
            "tag": "blocked"
        }
    ]

    # 添加路由规则
    template["routing"] = {
        "domainStrategy": "AsIs",
        "rules": [
            {
                "type": "field",
                "ip": ["geoip:private"],
                "outboundTag": "direct"
            },
            {
                "type": "field",
                "domain": ["geosite:category-ads"],
                "outboundTag": "blocked"
            }
        ]
    }

    return template


def url22_get_v2ray1_list(headers,url22,url22_source):
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
            link_url1_succev2ray1ful = f'连接{url22}成功！'
            print(link_url1_succev2ray1ful)
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
    v2ray1_list = soup.split('\n')
    # print('v2ray1_list1361',v2ray1_list)
    # time.sleep(188)
    url_v2ray1_list = []
    for not_ss in v2ray1_list:
        if 'ss:' not in str(not_ss)[0:3] and str(not_ss) != '' and 'ssr://' not in str(not_ss):
            url_v2ray1_list.append(not_ss)
    return url_v2ray1_list

def get_config_informationurl2(local_port):
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
    # url2_list = ["https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub", "https://github.com/abshare3/abshare3.github.io", "https://github.com/mksshare/mksshare.github.io"]  # 备用 可筛选可用的ss   B64 解码
    congfig_list = []
    node_links = []
    for i, url2 in enumerate(url2_list):
        if 'ermaozi' in url2:  #不用解码
            pass
            node_links += url22_get_v2ray1_list(headers, url2, url2_source_list[i])
        else:
            n = 0
            while True:
                print(f'使用连接2:{url2}进行更新！')
                try:
                    # html = http.request('GET', url2, timeout=29, headers=headers)
                    # link_url1_successful = '连接2成功！'
                    # print(link_url1_successful)
                    # break
                    if n > 2:
                        print('使用AI_all_auto代理88')
                        proxies = {"http": "socks5h://127.0.0.1:" + str(88), "https": "socks5h://127.0.0.1:" + str(88)}
                        try:
                            reg = requests.get(url2_source_list[i], headers=headers, timeout=8, proxies=proxies).text
                            # if 'abshare3.github.io' in url2:
                            #     reg = requests.get('https://github.com/abshare3/abshare3.github.io', headers=headers, timeout=8, proxies=proxies).text
                            # elif 'mksshare.github.io' in url2:
                            #     reg = requests.get('https://github.com/mksshare/mksshare.github.io', headers=headers, timeout=8, proxies=proxies).text
                            # else:
                            #     reg = requests.get('https://raw.githubusercontent.com/ripaojiedian/freenode/refs/heads/main/sub', headers=headers, timeout=8, proxies=proxies).text
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
                            # if 'abshare3.github.io' in url2:
                            #     reg = requests.get('https://github.com/abshare3/abshare3.github.io', headers=headers, timeout=8).text
                            # elif 'mksshare.github.io' in url2:
                            #     reg = requests.get('https://github.com/mksshare/mksshare.github.io', headers=headers, timeout=8).text
                            # else:
                            #     reg = requests.get('https://raw.githubusercontent.com/ripaojiedian/freenode/refs/heads/main/sub', headers=headers, timeout=8).text
                    link_url2_successful = '连接2成功！'
                    print(link_url2_successful)
                    # print('reg631',reg)
                    soup = BeautifulSoup(reg, 'html.parser')
                    # print('soup1192',soup)

                    if '404 Not Found' not in str(soup):
                        # continue
                        # print('soup1197', soup)
                        # time.sleep(188)
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
                        # print('soup672',soup)
                        # 同时支持明文订阅与 Base64 订阅；不再错误排除 ss://、ssr://
                        extracted_links = extract_subscription_links(str(soup))
                        node_links.extend(extracted_links)
                    else:
                        cmd_on_color.printRed(f"暂时没有节点，跳过该链接{url2}，错误信息：{soup[:18]}")
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
    node_links = list(dict.fromkeys(node_links))
    print(f'get_config_informationurl2共有节点数目为：{len(node_links)}')
    return node_links

def main_proxy_log():
    # 确保目录存在
    os.makedirs(object_name_output_log, exist_ok=True)
    from datetime import datetime
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
    # get_config_informationurl1(10822)
    # get_config_informationurl2(10822)

