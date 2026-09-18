#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from pathlib import Path
import requests
import traceback
import time
import logging
from tqdm import tqdm
import cmd_on_color
from numpy import *
logging.captureWarnings(True)  # 强制取消证书验证警告

#2023年1月6日更新
# import func_timeout;from func_timeout import func_set_timeout
# @func_set_timeout(99)
def download_file(url=None, file_path=None, proxy_port=None, headers=None, data=None):
    state = '下载失败，不可以上网'
    print('下载文件的地址为：' + str(url))
    # print('下载本地的路径为：' + str(file_path))
    if '/' in file_path or '\\' in file_path:
        print('下载本地的路径为：' + str(file_path))
        pass
    else :
        if file_path==None :
            file_path = os.getcwd() + '\\' + url.split('/')[-1]
            print('下载本地的路径为：' + str(file_path))
        else:
            file_path = os.getcwd() + '\\' + file_path
            print('下载本地的路径为：' + str(file_path))
    proxy_port = str(proxy_port)
    if proxy_port.isdigit() and proxy_port != '0':
        print('开始走代理下载')
        proxy_port_list = [88,8100, 10801, 10802, 10805, 10806, 10822, 10999]
        # proxy_port_list = [10805, 10802, 10802, 10805, 10806, 10888, 10822, 10899, 10999]#测试
        for proxy_ports in proxy_port_list:
            # if int(proxy_port) == proxy_ports :#指定代理 测试用
            if proxy_ports != 0:
                np = 0
                while True:
                    state,total_size = d_f(url, file_path, proxy_ports, headers, data)
                    if total_size <= 0 :
                        break
                    if state == '下载成功' :
                        # cmd_on_color.printGre(file_path + '=》下载成功！')
                        break
                    if state == '下载失败，不可以上网' :
                        cmd_on_color.printRed(file_path + '=》下载失败，不可以上网！准备更新该代理：' + str(proxy_ports))
                        # from sys import path
                        # path.append(r'D:\客户端集合代理')  # 添加路径
                        import update_proxy
                        status = update_proxy.update_all_proxy(proxy_ports)
                        if status == '此代理可以上网！' :
                            print(str(proxy_ports) + status)
                            print('继续尝试下载！代理为：' + str(proxy_ports))
                        if status == '此代理最终不可以上网！请更换下一个代理！' :
                            print(status)
                            cmd_on_color.printRed(str(proxy_ports) + '该代理不可上网，准备更换下一个代理，再进行下载')
                            cmd_on_color.printRed(file_path + '=》下载失败，不可以上网！')
                            break
                        
                    if np > 2 :
                    # if np > 0 : #测试
                        cmd_on_color.printRed(str(proxy_ports) + '该代理似乎网速太慢，准备更换下一个代理，再进行下载')
                        cmd_on_color.printRed(file_path + '=》网速太慢，只下了一部分，最下载失败，不可以上网！准备更换下一个代理端口再进行下载！')
                        break
                    np += 1
                if total_size <= 0:
                    cmd_on_color.printRed('最终下载失败，不可以上网！因为请求头长度为0，请检查参数是否错误！')
                    break
                if state == '下载成功' :
                    cmd_on_color.printGre(file_path + '=》下载成功！')
                    break
            if proxy_ports == 0:
                print('开始不走代理下载')
                state, total_size = d_f(url, file_path, proxy_port, headers, data)
                if state == '下载成功':
                    cmd_on_color.printGre(file_path + '=》下载成功！')
                if state == '下载失败，不可以上网':
                    print('80文件下载失败，不可以上网，尝试走代理，再进行下载')
                    cmd_on_color.printRed(file_path + '=》下载失败，不可以上网！')
                    proxy_port_list = [88,8100, 10801, 10802, 10805, 10806, 10822, 10999]
                    # proxy_port_list = [10805, 10802, 10802, 10805, 10806, 10888, 10822, 10899, 10999]#测试
                    for proxy_ports in proxy_port_list:
                        # if int(proxy_port) == proxy_ports :#指定代理 测试用
                        np = 0
                        while True:
                            state, total_size = d_f(url, file_path, proxy_ports, headers, data)
                            if total_size <= 0:
                                break
                            if state == '下载成功':
                                cmd_on_color.printGre(file_path + '=》下载成功！')
                                break
                            if state == '下载失败，不可以上网':
                                cmd_on_color.printRed(file_path + '=》下载失败，不可以上网！准备更新该代理：' + str(proxy_ports))
                                # from sys import path
                                # path.append(r'D:\客户端集合代理')  # 添加路径
                                import update_proxy
                                status = update_proxy.update_all_proxy(proxy_ports)
                                if status == '此代理可以上网！':
                                    print(str(proxy_ports) + status)
                                    print('继续尝试下载！代理为：' + str(proxy_ports))
                                if status == '此代理最终不可以上网！请更换下一个代理！':
                                    print(status)
                                    cmd_on_color.printRed(str(proxy_ports) + '该代理不可上网，准备更换下一个代理，再进行下载')
                                    cmd_on_color.printRed(file_path + '=》下载失败，不可以上网！')
                                    break
                
                            if np > 2:
                                # if np > 0 : #测试
                                cmd_on_color.printRed(str(proxy_ports) + '该代理似乎网速太慢，准备更换下一个代理，再进行下载')
                                cmd_on_color.printRed(file_path + '=》网速太慢，只下了一部分，最下载失败，不可以上网！准备更换下一个代理端口再进行下载！')
                                break
                            np += 1
                        if total_size <= 0:
                            cmd_on_color.printRed('最终下载失败，不可以上网！因为请求头长度为0，请检查参数是否错误！')
                            break
                        if state == '下载成功':
                            cmd_on_color.printGre(file_path + '=》下载成功！')
                            break
    else:
        print('开始不走代理下载')
        state,total_size = d_f(url, file_path, proxy_port, headers, data)
        if state == '下载成功':
            cmd_on_color.printGre(file_path + '=》下载成功！')
        if state == '下载失败，不可以上网':
            print('128文件下载失败，不可以上网，尝试走代理，再进行下载')
            cmd_on_color.printRed(file_path + '=》下载失败，不可以上网！')
            proxy_port_list = [88,8100, 10801, 10802, 10805, 10806, 10822, 10999]
            # proxy_port_list = [10805, 10802, 10802, 10805, 10806, 10888, 10822, 10899, 10999]#测试
            for proxy_ports in proxy_port_list:
                # if int(proxy_port) == proxy_ports :#指定代理 测试用
                    np = 0
                    while True:
                        state,total_size = d_f(url, file_path, proxy_ports, headers, data)
                        if total_size <= 0:
                            break
                        if state == '下载成功':
                            cmd_on_color.printGre(file_path + '=》下载成功！')
                            break
                        if state == '下载失败，不可以上网':
                            cmd_on_color.printRed(file_path + '=》下载失败，不可以上网！准备更新该代理：' + str(proxy_ports))
                            # from sys import path
                            # path.append(r'D:\客户端集合代理')  # 添加路径
                            import update_proxy
                            status = update_proxy.update_all_proxy(proxy_ports)
                            if status == '此代理可以上网！':
                                print(str(proxy_ports) + status)
                                print('继续尝试下载！代理为：' + str(proxy_ports))
                            if status == '此代理最终不可以上网！请更换下一个代理！':
                                print(status)
                                cmd_on_color.printRed(str(proxy_ports) + '该代理不可上网，准备更换下一个代理，再进行下载')
                                cmd_on_color.printRed(file_path + '=》下载失败，不可以上网！')
                                break
            
                        if np > 2:
                            # if np > 0 : #测试
                            cmd_on_color.printRed(str(proxy_ports) + '该代理似乎网速太慢，准备更换下一个代理，再进行下载')
                            cmd_on_color.printRed(file_path + '=》网速太慢，只下了一部分，最下载失败，不可以上网！准备更换下一个代理端口再进行下载！')
                            break
                        np += 1
                    if total_size <= 0:
                        cmd_on_color.printRed('最终下载失败，不可以上网！因为请求头长度为0，请检查参数是否错误！')
                        break
                    if state == '下载成功':
                        cmd_on_color.printGre(file_path + '=》下载成功！')
                        break
    if state == '下载失败，不可以上网' :
        cmd_on_color.printRed(file_path + '=》下载失败，不可以上网！9个代理似乎全部瘫痪！请检查其它原因，或更换其它代理！')
    return state

def d_f(url=None, file_path=None, proxy_port=None, headers=None, data=None):
    total_size = -1
    n = 0
    while True:
        try:
            # 用流stream的方式获取url的数据
            proxy_port = str(proxy_port)
            if headers == None:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26", 'Accept-Language': 'zh-CN,zh;q=0.9,ko;q=0.8', "Accept-Encoding": "identity"}
            if proxy_port.isdigit() and proxy_port != '0':
                print('走代理下载中……端口：', proxy_port)
                # import os
                # os.environ["http_proxy"] = "http://127.0.0.1:" + proxy_port
                # os.environ["https_proxy"] = "http://127.0.0.1:" + proxy_port
                # proxies = {'http': 'socks5://127.0.0.1:' + str(proxy_port),'https': 'socks5://127.0.0.1:' + str(proxy_port)}
                proxies = {"http": "socks5h://127.0.0.1:" + str(proxy_port), "https": "socks5h://127.0.0.1:" + str(proxy_port)}
            else:
                print('不走代理，直接下载中……1')
                proxies = 0
            resp = requests.get(url, stream=True, timeout=8, headers=headers, proxies=proxies, verify=False)
            # 拿到文件的长度，并把total初始化为0
            if 'X-TTDB-L' in str(resp.headers):
                total_size = int(resp.headers.get('X-TTDB-L', 0))
            else :
                total_size = int(resp.headers.get('content-length', 0))
            # total_size = int(resp.headers.get('X-TTDB-L', 0))
            # total_size = int(resp.headers['Content-Length'])
            print(resp.headers)
            # 打开当前目录的file_path文件(名字你来传入)
            # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
            with open(file_path, 'wb') as file, tqdm(
                    desc=file_path,
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
            ) as bar:
                for data in resp.iter_content(chunk_size=1024):  # chunk_size=8192#chunk_size=1024
                    size = file.write(data)
                    bar.update(size)
                    # print(data)
            break
        except Exception as e:
            print(e)
            # traceback.print_exc()
            err = '下载错误！2秒后重试！'
            print(err)
            n += 1
            pass
        if n > 2:
            print('循环大于9，跳出！')
            break
        time.sleep(2)
    print('开始检查是否下载成功？225')
    print('需要下载的文件大小为：', total_size)
    file_size_path = ''
    try:
        file_size_path = os.path.getsize(file_path)
    except :
        pass
    print('下载到本地文件大小为：', file_size_path)
    my_file = Path(file_path)
    # if my_file.is_file() and total_size == file_size_path and file_size_path != 0 :
    if my_file.is_file() and total_size == file_size_path and file_size_path > 0 :
        state = '下载成功'
        
        # print(file_path,'=》下载成功！')
    else:
        state = '下载失败，不可以上网'

        # print(file_path,'=》下载失败，不可以上网！')
    return state,total_size


def download_file_state(url=None, file_path=None, proxy_port=None, headers=None, data=None):
    print('测速下载图片的地址为：' + str(url))
    print('测速下载本地的路径为：' + str(file_path))
    n = 0
    average_speed = '-1'
    total_size = -1
    while True:
        try:
            # 用流stream的方式获取url的数据
            proxy_port = str(proxy_port)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26", 'Accept-Language': 'zh-CN,zh;q=0.9,ko;q=0.8',
                       "Accept-Encoding": "identity"}
            print('走代理下载中……端口：' + proxy_port)
            proxies = {"http": "socks5h://127.0.0.1:" + str(proxy_port), "https": "socks5h://127.0.0.1:" + str(proxy_port)}
            resp = requests.get(url, stream=True, timeout=29, headers=headers, proxies=proxies, verify=False)
            # 拿到文件的长度，并把total初始化为0
            total_size = int(resp.headers.get('content-length', 0))
            # total_size = int(resp.headers.get('X-TTDB-L', 0))
            # 打开当前目录的fname文件(名字你来传入)
            # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
            bar_list = []
            with open(file_path, 'wb') as file, tqdm(
                    desc=file_path,
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
            ) as bar:
                for i, data in enumerate(resp.iter_content(chunk_size=1024)):  # chunk_size=8192#chunk_size=1024
                    size = file.write(data)
                    bar.update(size)
            # print('速度为',bar.update(size))
            print('开始检查是否下载成功？')
            print('需要下载的文件大小为：', total_size)
            file_size_path = ''
            try:
                file_size_path = os.path.getsize(file_path)
            except:
                pass
            print('下载到本地文件大小为：', file_size_path)
            my_file = Path(file_path)
            if my_file.is_file() and total_size == file_size_path:
                state = '下载成功'
                cmd_on_color.printGre(file_path + '=》下载成功！')
                print('====================开始测试平均速度！===================')
                average_speed = test_speed(url, file_path, proxy_port)
                break
                # print(file_path,'=》下载成功！')
            else:
                state = '下载失败'
                cmd_on_color.printRed(file_path + '=》下载失败！')
                # print(file_path,'=》下载失败！')
        except Exception as e:
            print(e)  # timed out  #port=443
            # traceback.print_exc()
            print('下载错误！2秒后重试！')

            pass

        if n >= 2:
            # if n > 2:#测试
            cmd_on_color.printRed('循环大于9，跳出！该代理最终不可用！download_files代理为：' + str(proxy_port))
            state = '下载失败'
            break
        time.sleep(2)
        n += 1
    return state, average_speed


def test_speed_old(url='http://ipv4.download.thinkbroadband.com/20MB.zip', file_path="test_speed.gif", proxy_port=None, headers=None, interval=0.2):
    def MB(byte):
        return byte / 1024 / 1024

    average_speed_str = '-1.000'
    print_params = ''
    print('测速下载图片的地址为：' + str(url))
    print('测速下载本地的路径为：' + str(file_path))
    n = 0
    nn = 0
    while True:
        try:
            # 用流stream的方式获取url的数据
            proxy_port = str(proxy_port)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}
            if proxy_port.isdigit() or n > 2:
                print('走代理下载中……端口：' + proxy_port)
                # import os
                # os.environ["http_proxy"] = "http://127.0.0.1:" + proxy_port
                # os.environ["https_proxy"] = "http://127.0.0.1:" + proxy_port
                # resp = requests.get(url, stream=True,timeout=8,headers = headers)
                proxies = {"http": "socks5h://127.0.0.1:" + str(proxy_port), "https": "socks5h://127.0.0.1:" + str(proxy_port)}
                # proxies = {'http': 'socks5://127.0.0.1:' + str(proxy_port),'https': 'socks5://127.0.0.1:' + str(proxy_port)}
                # proxies = {'http': '127.0.0.1:8100'}
                # proxies = {"https://127.0.0.1:8100": "https://i.gifer.com",}
                # session = requests.session()
                resp = requests.get(url, stream=True, timeout=2, headers=headers, proxies=proxies, verify=False)
            else:
                print('不走代理，直接下载中……2')
                resp = requests.get(url, stream=True, timeout=2, headers=headers)
            # print(resp.headers)
            # resp = requests.get(url, stream=True, headers=headers)
            # file_size = int(resp.headers['content-length'])  # 文件大小 Byte
            file_size = int(url.split('bytes=')[-1])
            f = open(file_path, 'wb')
            down_size = 0  # 已下载字节数
            old_down_size = 0  # 上一次已下载字节数
            time_ = time.time()
            speed_list = []
            for i, chunk in enumerate(resp.iter_content(chunk_size=512)):
                if chunk:
                    f.write(chunk)
                    down_size += len(chunk)
                    if time.time() - time_ > interval:
                        # rate = down_size / file_size * 100  # 进度  0.01%
                        speed = (down_size - old_down_size) / interval  # 速率 0.01B/s
                        # print(nn)
                        old_down_size = down_size
                        time_ = time.time()
                        # if nn > 2:
                        if 2< nn <= 18:
                            speed_list.append(MB(speed))
                        if nn==18:
                            average_speed = mean(speed_list)

                            # print('\r下载平均速度：' + str(average_speed))
                            # average_speed = str(average_speed)[0:6]
                            average_speed_str = f"{average_speed:.3f}"

                            if average_speed < 2.000:
                                cmd_on_color.printRed(f"下载平均速度小于2M，跳出循环，视为不可以上网")
                                average_speed_str = str(average_speed)
                                # average_speed_str = '-2.000'
                                break
                            else:
                                cmd_on_color.printGre('\r下载平均速度：' + average_speed_str + f' MB/s，速度列表：{speed_list}')
                        print_params = [MB(speed), MB(down_size), MB(file_size), (file_size - down_size) / speed]
                        print('\r{:.1f}MB/s - {:.1f}MB，共 {:.1f}MB，还剩 {:.0f} 秒   '.format(*print_params), end='')
                        nn += 1
                # if nn > 22:  # 测试99次，跳出！
                #     print('\r测速18次，跳出！')
                #     break
            f.close()
            print('\r{:.1f}MB/s - {:.1f}MB，共 {:.1f}MB，还剩 {:.0f} 秒   '.format(*print_params))

            print('开始检查是否下载成功？418')
            print('需要下载的文件大小为：', file_size)
            file_size_path = ''
            try:
                file_size_path = os.path.getsize(file_path)
            except:
                pass
            print('下载到本地文件大小为：', file_size_path)
            my_file = Path(file_path)
            if my_file.is_file() and file_size == file_size_path:
                state = '下载成功'
                cmd_on_color.printGre(file_path + '=》下载成功！')
                # print('====================开始测试平均速度！===================')
                # average_speed = test_speed(url, file_path, proxy_port)
                # print(file_path,'=》下载成功！')
            else:
                state = '下载失败，不可以上网'
                # average_speed_str = '-1.000'
                cmd_on_color.printRed(file_path + '=》408下载失败，文件大小不一致，但【可以上网！】')
                # print(file_path,'=》下载失败，不可以上网！')


            # print('\r下载速度列表：',speed_list)
            # if len(speed_list) == 0:
            #     average_speed = -1
            #     cmd_on_color.printRed('\r下载平均速度：' + str(average_speed))
            # else:
                # average_speed = mean(speed_list)
                # # print('\r下载平均速度：' + str(average_speed))
                # # average_speed = str(average_speed)[0:6]
                # average_speed = f"{average_speed:.3f}"
                # cmd_on_color.printGre('\r下载平均速度：' + str(average_speed)  + 'MB/s')
                # print('\r速度完成！' + ' ' * 29)
                # pass

            break
        except Exception as e:
            traceback.print_exc()
            print(e)
            print('下载错误！2秒后重试！')
            n += 1
            pass
        if n >= 2:
            state = '下载失败，不可以上网'
            average_speed_str = '-1.000'
            cmd_on_color.printRed(file_path + '=》435下载失败，不可以上网！')
            break

        time.sleep(2)
    return average_speed_str


def test_speed(url='http://ipv4.download.thinkbroadband.com/20MB.zip', file_path="test_speed.gif", proxy_port=None, headers=None, interval=0.2):
    def MB(byte):
        return byte / 1024 / 1024

    average_speed_str = '-1.000'
    print('测速下载图片的地址为：' + str(url))
    print('测速下载本地的路径为：' + str(file_path))
    n = 0
    nn = 0  # 初始化nn
    while True:
        try:
            # 设置默认headers
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"}

            # 代理判断
            if proxy_port and str(proxy_port).isdigit():
                print('走代理下载中……端口：' + str(proxy_port))
                proxies = {"http": "socks5h://127.0.0.1:" + str(proxy_port), "https": "socks5h://127.0.0.1:" + str(proxy_port)}
                resp = requests.get(url, stream=True, timeout=8, headers=headers, proxies=proxies, verify=False)
            else:
                print('不走代理，直接下载中……2')
                resp = requests.get(url, stream=True, timeout=2, headers=headers)

            # 获取文件大小
            try:
                file_size = int(resp.headers.get('content-length', 0))
            except (TypeError, ValueError):
                file_size = 0

            if file_size == 0:
                print("警告：无法获取文件大小，进度和平均速度可能不准确。")

            f = open(file_path, 'wb')
            down_size = 0
            old_down_size = 0
            time_ = time.time()
            speed_list = []
            for i, chunk in enumerate(resp.iter_content(chunk_size=512)):
                if chunk:
                    f.write(chunk)
                    down_size += len(chunk)
                    if time.time() - time_ > interval:
                        speed = (down_size - old_down_size) / interval
                        old_down_size = down_size
                        time_ = time.time()
                        if 2 < nn <= 18:
                            speed_list.append(MB(speed))
                        if nn == 18:
                            average_speed = mean(speed_list)
                            average_speed_str = f"{average_speed:.3f}"
                            if average_speed < 2.000:
                                print("下载平均速度小于2M，跳出循环，视为不可以上网")  # 用普通print替换彩色
                                average_speed_str = str(average_speed)
                                break
                            else:
                                print('\r下载平均速度：' + average_speed_str + f' MB/s，速度列表：{speed_list}')
                        print_params = [MB(speed), MB(down_size), MB(file_size), (file_size - down_size) / speed]
                        print('\r{:.1f}MB/s - {:.1f}MB，共 {:.1f}MB，还剩 {:.0f} 秒   '.format(*print_params), end='')
                        nn += 1
            f.close()
            print()  # 换行

            # 检查下载完整性
            file_size_path = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            if file_size == file_size_path:
                print(file_path + ' => 下载成功！')
            else:
                print(file_path + ' => 下载失败，文件大小不一致，但【可以上网！】')

            break
        except Exception as e:
            traceback.print_exc()
            print(e)
            print('下载错误！2秒后重试！')
            n += 1
            time.sleep(2)
            if n >= 2:
                average_speed_str = '-1.000'
                print(file_path + ' => 435下载失败，不可以上网！')
                break

    return average_speed_str
if __name__ == "__main__":
    # update_proxy('8100')
    pass
    # download_file("https://i0.wp.com/whenthecurveslineup.com/wp-content/uploads/2022/12/lune_gvit_230113-t.png?w=599&ssl=1", "test.jpg")
    # download_file("http://sprite.phys.ncku.edu.tw/astrolab/mirrors/apod/image/2211/Lunar-Eclipse-South-Pole_1024.jpg", "test.jpg",'10802')
    # download_file_state("https://i.gifer.com/embedded/download/RtpG.gif", r"D:/天文在线的天文大数据/天文酷图/test.gif",10802)
    # download_file("https://64.media.tumblr.com/3988e7b4c0766b52eba9cd34d639a2c7/tumblr_ofajxrHN4p1u3mqgso1_500.gifv", "test.gif",'8100')
    # download_file()
    # download_file_state("https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif","test.gif",'0')
    # download_file("https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif", "test.gif",'8100')
    # test_speed("https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif","test.gif",'10999')
    # download_file("https://www.heavens-above.com/skychart.ashx?cometID=C%2f2022+E3&size=400&FOV=5&MaxMag=10&RA=-8.1196035266563&DEC=31.6256285182429&mjd=59946.2254398148&cn=1&cl=1&cul=zh", "test.jpg", '8100')
    # download_file("https://in-the-sky.org/widgets/custom_finder_chart.php?id=2020V2&mag_min=11&width=26&&color=0&duration=7&format=jpg", "test.jpg", '8100')
    # try:
    # download_file("https://cdn1219.savetube.me/media/CdVuHDBDYbA/som-et-59-mars-curiosity-sol-929-video-1-shorts-3840-ytshorts.savetube.me.mp4", "test.mp4",'8100',**kwargs)
    # except func_timeout.exceptions.FunctionTimedOut as e:
    # traceback.print_exc()
    # print(e)
    # print("超时29秒，准备重试!!!")
    print(test_speed('http://ipv4.download.thinkbroadband.com/20MB.zip', os.getcwd() + r"\test_speed.zip", 88))
    # print(test_speed('https://www.thinkbroadband.com/download?file=18MB', os.getcwd() + r"\test_speed.gif", 10801))
    # print(test_speed('https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif', os.getcwd() + r"\test_speed.gif", 88))
    # download_file_state('https://i.pinimg.com/originals/cd/55/08/cd5508e5c2e50e38e4227ac630741f5d.gif', os.getcwd() + r"\test_speed.gif", '88')
    # download_file_state('http://ipv4.download.thinkbroadband.com/20MB.zip', os.getcwd() + r"\test_speed.zip", '88')
    # download_file_state('http://speed.cloudflare.com/__down?bytes=18000000', os.getcwd() + r"\test_speed.gif", '88')