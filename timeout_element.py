#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import traceback

from func_timeout import func_set_timeout
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import cmd_on_color


# @func_set_timeout(99)
def element_timeout(driver=None, element_attribute=None, element=None, number=None, operation=None, content=None, error=None, timeout=None, interval=None):
    # def element_timeout(driver,element_attribute,element,number,operation,content,error,timeout,interval):
    """说明
    driver：句柄，所有元素，可以自定义局部中的所有元素
    element_attribute：定位的属性，如：ID，CLASS_NAME，XPATH等等
    element：字符串类型，填写需要定位的元素，如"arco-input-tag-input"
    content：字符串类型，填写需要输入的内容，一般用在send_keys函数中
    number：整数类型，定义第几个元素，如1、-1等等
    timeout：元素最大超时，单位为秒，一般用在检查元素是否存在，超出设置时间，提示超时，随后跳过该元素。
    interval：间隔时间，单位为秒，每间隔多久检查一次元素是否存在
    operation：操作的类型，如click()、text、send_keys()等等
    error：打印出错误
    """
    if ' ' in element:
        element = element.replace(' ', '.')
    element_part = ''
    print_element = '定位元素的整行代码为： ' + str(element_attribute) + ' ' + str(element) + '' + str(number) + str(operation) + str(content) + str(error) + str(timeout) + str(interval)
    # print_element = driver,element_attribute,element,number,operation,content,error,timeout,interval
    n = 0
    while True:
        try:
            """CSS_SELECTOR"""

            """CLASS_NAME"""
            """CLASS_NAME""""""click"""
            if element_attribute == 'CLASS_NAME' and operation == 'click' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.CLASS_NAME, element).click()
                break

                # click_text = driver.find_element(By.CLASS_NAME,element).text
                # if click_text != '':
                # element_part =  driver.find_element(By.CLASS_NAME,element).click()
                # break

            """CLASS_NAME""""""text"""

            if element_attribute == 'CLASS_NAME' and operation == 'text' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.CLASS_NAME, element).text

                break

            """CLASS_NAME""""""custom"""
            if element_attribute == 'CLASS_NAME' and operation == 'custom' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.CLASS_NAME, element)
                break

            if element_attribute == 'CLASS_NAME' and operation == 'custom' and number.replace('-', '').isdigit() == True:
                if '-' in number:
                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number)]
                    break
                else:
                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number) - 1]
                    break

            if element_attribute == 'CLASS_NAME' and operation == 'customs' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_elements(By.CLASS_NAME, element)
                if element_part != []:
                    break

            """CLASS_NAME""""""location"""
            """location：获取页面元素的任意坐标。没有找到元素的，要获取任意页面位置坐标，
            需用《py鼠标全自动化.py》获取，再减去115【为固定谷歌浏览器网页栏高度】"""
            if element_attribute == 'CLASS_NAME' and operation == 'location' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.CLASS_NAME, element).location
                break

            """CLASS_NAME""""""size"""
            if element_attribute == 'CLASS_NAME' and operation == 'size' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.CLASS_NAME, element).size
                break

            """CLASS_NAME""""""send_keys"""
            if element_attribute == 'CLASS_NAME' and operation == 'send_keys' and 'Keys.' not in content and number.replace('-', '').isdigit() == False:
                try:
                    element_part = driver.find_element(By.CLASS_NAME, element).send_keys(Keys.CONTROL + 'a')
                    # element_part = driver.find_element(By.CLASS_NAME, element).send_keys(Keys.BACKSPACE)
                except:
                    pass
                element_part = driver.find_element(By.CLASS_NAME, element).send_keys(content)
                break

            if element_attribute == 'CLASS_NAME' and operation == 'send_keys' and 'Keys.' not in content and number.replace('-', '').isdigit() == True:
                try:
                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number)].send_keys(Keys.CONTROL + 'a')
                    # element_part = driver.find_elements(By.CLASS_NAME, element)[int(number)].send_keys(Keys.BACKSPACE)#删除
                except:
                    pass
                if '-' in number:
                    # print(element,int(number),content)
                    # driver.find_elements(By.CLASS_NAME, 'omui-suggestion__value')[-1].send_keys('天文')
                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number)].send_keys(content)
                    break

                else:

                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number) - 1].send_keys(content)
                    break

            if element_attribute == 'CLASS_NAME' and operation == 'send_keys' and 'Keys.' in content and number.replace('-', '').isdigit() == False:
                # element_part = driver.find_element(By.CLASS_NAME,element).send_keys(Keys.ENTER)
                element_part = driver.find_element(By.CLASS_NAME, element).send_keys(eval(content))
                break
            if element_attribute == 'CLASS_NAME' and operation == 'send_keys' and 'Keys.' in content and number.replace('-', '').isdigit() == True:
                if '-' in number:

                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number)].send_keys(eval(content))
                    break

                else:

                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number) - 1].send_keys(eval(content))
                    break


                # try:
                # """此处易报错，报错路径如下："""
                # [D:\Users\fso_lingduxingxi\AppData\Local\Programs\Python\Python39\lib\site-packages\selenium\webdriver\remote\errorhandler.py]第249行

                # element_part = driver.find_element(By.CLASS_NAME,element).send_keys(eval(content))
                # element_part = driver.find_element(By.CLASS_NAME,element).send_keys(Keys.ENTER)
                # break
                # except Exception as err:
                # print(err)
                # if 'no such element' not in str(err):
                # traceback.print_exc()
                # else :
                # pass

                # traceback.print_exc()
                # break
                # pass

            if element_attribute == 'CLASS_NAME' and operation == 'click' and number.replace('-', '').isdigit() == True:
                if '-' in number:
                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number)].click()
                    break
                else:
                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number) - 1].click()
                    break
            """CLASS_NAME""""""get_attribute"""

            if element_attribute == 'CLASS_NAME' and operation == 'get_attribute' and number.replace('-', '').isdigit() == True:
                if '-' in number:
                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number)].get_attribute(content)
                    break
                else:
                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number) - 1].get_attribute(content)
                    break

            if element_attribute == 'CLASS_NAME' and operation == 'get_attribute' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.CLASS_NAME, element).get_attribute(content)
                break

            if element_attribute == 'CLASS_NAME' and operation == 'text' and number.replace('-', '').isdigit() == True:
                if '-' in number:
                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number)].text
                    break
                else:
                    element_part = driver.find_elements(By.CLASS_NAME, element)[int(number) - 1].text
                    break

            """XPATH""""""send_keys"""

            if element_attribute == 'XPATH' and operation == 'send_keys' and 'Keys.' not in content and number.replace('-', '').isdigit() == False:
                try:
                    element_part = driver.find_element(By.XPATH, element).send_keys(Keys.CONTROL + 'a')
                    # element_part = driver.find_element(By.XPATH, element).send_keys(Keys.BACKSPACE)
                except:
                    pass
                element_part = driver.find_element(By.XPATH, element).send_keys(content)
                break

            if element_attribute == 'XPATH' and operation == 'send_keys' and 'Keys.' not in content and number.replace('-', '').isdigit() == True:

                if '-' in number:

                    try:
                        element_part = driver.find_elements(By.XPATH, element)[int(number)].send_keys(Keys.CONTROL + 'a')
                        # element_part = driver.find_elements(By.XPATH, element)[int(number)].send_keys(Keys.BACKSPACE)
                    except:
                        pass
                    element_part = driver.find_elements(By.XPATH, element)[int(number)].send_keys(content)
                    break






                else:
                    try:
                        element_part = driver.find_elements(By.XPATH, element)[int(number) - 1].send_keys(Keys.CONTROL + 'a')
                        # element_part = driver.find_elements(By.XPATH, element)[int(number) - 1].send_keys(Keys.BACKSPACE)
                    except:
                        pass
                    element_part = driver.find_elements(By.XPATH, element)[int(number) - 1].send_keys(content)
                    break

            if element_attribute == 'XPATH' and operation == 'send_keys' and 'Keys.' in content and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.XPATH, element).send_keys(eval(content))
                break

            """XPATH""""""custom"""
            if element_attribute == 'XPATH' and operation == 'custom' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.XPATH, element)
                break

            if element_attribute == 'XPATH' and operation == 'customs' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_elements(By.XPATH, element)
                break

            """XPATH""""""custom""""""有数字"""
            if element_attribute == 'XPATH' and operation == 'custom' and number.replace('-', '').isdigit() == True:
                if '-' in number:
                    element_part = driver.find_elements(By.XPATH, element)[int(number)]
                    break
                else:
                    element_part = driver.find_elements(By.XPATH, element)[int(number) - 1]
                    break

            """XPATH""""""click""""""有数字"""

            if element_attribute == 'XPATH' and operation == 'click' and number.replace('-', '').isdigit() == True:
                if '-' in number:
                    element_part = driver.find_elements(By.XPATH, element)[int(number)].click()
                    break
                else:
                    element_part = driver.find_elements(By.XPATH, element)[int(number) - 1].click()
                    break

            if element_attribute == 'XPATH' and operation == 'click' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.XPATH, element).click()
                break

            if element_attribute == 'XPATH' and operation == 'location' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.CLASS_NAME, element).location
                break

            if element_attribute == 'ActionChains':
                # element_part =  ActionChains(driver).move_by_offset(1173,262).click().perform() # 鼠标左键点击， 200为x坐标， 100为y坐标
                # element_part =  eval(element_attribute) + eval((driver)).move_by_offset(1173,262).click().perform() # 鼠标左键点击， 200为x坐标， 100为y坐标
                break

            """XPATH""""""text"""

            if element_attribute == 'XPATH' and operation == 'text' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.XPATH, element).text

                break
            """XPATH""""""get_attribute"""
            if element_attribute == 'XPATH' and operation == 'get_attribute' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.XPATH, element).get_attribute(content)
                break
            """XPATH""""""get_attribute""""""有数字"""
            if element_attribute == 'XPATH' and operation == 'get_attribute' and number.replace('-', '').isdigit() == True:

                if '-' in number:
                    element_part = driver.find_elements(By.XPATH, element)[int(number)].get_attribute(content)
                    break
                else:
                    element_part = driver.find_elements(By.XPATH, element)[int(number) - 1].get_attribute(content)
                    break

            """NAME"""
            if element_attribute == 'NAME' and operation == 'text' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.NAME, element).text

                break

            if element_attribute == 'NAME' and operation == 'click' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.NAME, element).click()

                break

            if element_attribute == 'NAME' and operation == 'click' and number.replace('-', '').isdigit() == True:
                if '-' in number:
                    element_part = driver.find_elements(By.NAME, element)[int(number)].click()
                    break
                else:
                    element_part = driver.find_elements(By.NAME, element)[int(number) - 1].click()
                    break

            if element_attribute == 'NAME' and operation == 'customs' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_elements(By.NAME, element)
                if element_part != []:
                    break

            if element_attribute == 'NAME' and operation == 'send_keys' and 'Keys.' not in content and number.replace('-', '').isdigit() == False:
                try:
                    element_part = driver.find_element(By.NAME, element).send_keys(Keys.CONTROL + 'a')
                    # element_part = driver.find_element(By.NAME, element).send_keys(Keys.BACKSPACE)
                except:
                    pass
                element_part = driver.find_element(By.NAME, element).send_keys(content)
                break

            """ID"""

            if element_attribute == 'ID' and operation == 'custom' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.ID, element)
                break

            if element_attribute == 'ID' and operation == 'customs' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_elements(By.ID, element)
                break

            if element_attribute == 'ID' and operation == 'click' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.ID, element).click()
                break

            if element_attribute == 'ID' and operation == 'click' and number.replace('-', '').isdigit() == True:
                if '-' in number:
                    element_part = driver.find_elements(By.ID, element)[int(number)].click()
                    break
                else:
                    element_part = driver.find_elements(By.ID, element)[int(number) - 1].click()
                    break

            if element_attribute == 'ID' and operation == 'send_keys' and 'Keys.' not in content and number.replace('-', '').isdigit() == False:
                try:
                    element_part = driver.find_element(By.ID, element).send_keys(Keys.CONTROL + 'a')
                    # element_part = driver.find_element(By.ID, element).send_keys(Keys.BACKSPACE)
                except:
                    pass
                element_part = driver.find_element(By.ID, element).send_keys(content)
                break

            """ID""""""text"""

            if element_attribute == 'ID' and operation == 'text' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.ID, element).text

                break

            """LINK_TEXT"""

            if element_attribute == 'LINK_TEXT' and operation == 'click' and number.replace('-', '').isdigit() == False:
                element_part = driver.find_element(By.LINK_TEXT, element).click()
                break



        except:
            if 'e' in error:
                traceback.print_exc()
                cmd_on_color.printBlu(print_element)
            pass
        timeout_n = int(timeout / interval)
        # timeout_n = 2
        if 'e' in error:
            print(n, timeout_n)
        if n > timeout_n:
            break
        # if n > 9 :
        # kill_chrome_process.kill_process()

        # print('等待' + str(interval) + '秒')
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            traceback.print_exc()
            print("手动退出")
            print('n > timeout_n分别为：' + str(n) + '>' + str(timeout_n))
            print("等待秒数为：" + str(interval))
            exit()

        n += 1
        # s_n = interval
        # print('没有发布过，需要等待' + cmd_on_color.printCya_input(str(s_n) + '秒') + '后再发布下一篇！')
        # for i in range(1,int(s_n)):
        # print(cmd_on_color.printCya_input('第' + str(i) + '秒'),end="")
        # print("\r程序正常运行中，秒数：",end="",flush = True)
        # time.sleep(1)
        # print('\r' + cmd_on_color.printCya_input(str(s_n) + '秒') + '时间到了，开始执行接下来的代码！')

    if element_part == '' and 'e' in error:
        cmd_on_color.printRed('超时！没有【' + element + '】元素')
        cmd_on_color.printBlu(print_element)
        # print()
    return element_part
