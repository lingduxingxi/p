#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import subprocess
import time

import run_all_node
from AI_all_auto import run_all

today_date = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
print('开始更新，日期为：', today_date)
# run_all('每天')
# os.system("taskkill /F /IM goflyway.exe")
# os.system("taskkill /F /IM sslocal_SS1.exe")
# os.system("taskkill /F /IM sslocal_SS2.exe")
# os.system(r'D:\客户端集合代理\GoflywayTools.vbs')
# run_all_node.vpn_all()
# run_all_node.operate_move_mouse()#移动鼠标让图标消失
print(today_date,'更新完毕！！！')
if __name__ == "__main__":
    pass