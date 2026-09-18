
#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-

import os
# import colorama
# colorama.init()
# 可以根据自己的需求，把常用的封装起来，用的时候直接调用就可以了
class bcolors:
    cHEADER = '\033[95m'
    cOKBLUE = '\033[94m'
    cOKGREEN = '\033[92m'
    cWARNING = '\033[93m'
    cFAIL = '\033[91m'
    cBOLD = '\033[1m'
    cUNDERLINE = '\033[4m'
    cEND = '\033[0m'


def test1():
    print('\033[0m这是显示方式0')
    print('\033[1m这是显示方式1')
    print('\033[4m这是显示方式4')
    print('\033[5m这是显示方式5')
    print('\033[7m这是显示方式7')
    print('\033[8m这是显示方式8')
    print('\033[30m这是前景色0')
    print('\033[31m这是前景色1')#红色
    print('\033[32m这是前景色2')
    print('\033[33m这是前景色3')
    print('\033[34m这是前景色4')
    print('\033[35m这是前景色5')
    print('\033[36m这是前景色6')
    print('\033[37m这是前景色7')
    print('\033[40m这是背景色0')
    print('\033[41m这是背景色1')
    print('\033[42m这是背景色2')
    print('\033[43m这是背景色3')
    print('\033[44m这是背景色4')
    print('\033[45m这是背景色5')
    print('\033[46m这是背景色6')
    print('\033[47m这是背景色7\033[0m')
    print('\033[2;36;43m这是综合颜色\033[0m\n\n')
        
        
def printRed(state_colour):
    os.system('')
    # state_colour = '\033[3;36m' + state_colour + '\033[0m'
    state_colour = '\033[31m' + state_colour + '\033[0m'
    print(state_colour)
    return state_colour


def printGre(state_colour):
    os.system('')
    # state_colour = '\033[3;36m' + state_colour + '\033[0m'
    state_colour = '\033[1;32m' + state_colour + '\033[0m'
    print(state_colour)
    return state_colour
def printYel(state_colour):
    os.system('')
    # state_colour = '\033[3;36m' + state_colour + '\033[0m'
    state_colour = '\033[1;33m' + state_colour + '\033[0m'
    print(state_colour)
    return state_colour

def printBlu(state_colour):
    os.system('')
    # state_colour = '\033[3;36m' + state_colour + '\033[0m'
    state_colour = '\033[1;34m' + state_colour + '\033[0m'
    print(state_colour)
    return state_colour



def printMag(state_colour):
    os.system('')
    # state_colour = '\033[3;36m' + state_colour + '\033[0m'
    state_colour = '\033[1;35m' + state_colour + '\033[0m'
    print(state_colour)
    return state_colour



def printCya(state_colour):
    os.system('')
    # state_colour = '\033[3;36m' + state_colour + '\033[0m'
    state_colour = '\033[1;36m' + state_colour + '\033[0m'
    print(state_colour)
    return state_colour


def printWhi(state_colour):
    os.system('')
    state_colour = '\033[1;37m' + state_colour + '\033[0m'
    print(state_colour)
    return state_colour


def printCya_Red(state_colour_Cya,state_colour_Red):
    os.system('')
    state_colour_Cya = '\033[1;37m' + state_colour_Cya + '\033[0m'
    state_colour_Red = '\033[31m' + state_colour_Red + '\033[0m'
    state_colour = state_colour_Cya + state_colour_Red
    print(state_colour)
    return state_colour





'''input'''

def printRed_input(state_colour):
    os.system('')
    # state_colour = '\033[3;36m' + state_colour + '\033[0m'
    state_colour = '\033[31m' + state_colour + '\033[0m'
    # print(state_colour)
    return state_colour


def printGre_input(state_colour):
    os.system('')
    # state_colour = '\033[3;36m' + state_colour + '\033[0m'
    state_colour = '\033[1;32m' + state_colour + '\033[0m'
    # print(state_colour)
    return state_colour

def printYel_input(state_colour):
    os.system('')
    # state_colour = '\033[3;36m' + state_colour + '\033[0m'
    state_colour = '\033[1;33m' + state_colour + '\033[0m'
    # print(state_colour)
    return state_colour



def printCya_input(state_colour):
    os.system('')
    # state_colour = '\033[3;36m' + state_colour + '\033[0m'
    state_colour = '\033[1;36m' + state_colour + '\033[0m'
    # print(state_colour)
    return state_colour


def printWhi_input(state_colour):
    os.system('')
    state_colour = '\033[1;37m' + state_colour + '\033[0m'
    # print(state_colour)
    return state_colour





# test2()

if __name__ == '__main__':
    #test
    state_mufu = '发布失败！'
    if state_mufu == '发布失败！' :
        state_mufu = printCya(state_mufu)
    
    
    pass
    os.system('')
    # os.system('clear')
    # print("\n__name__ is "+__name__+"\n")
    # test1()
    test2()
    
    # info = input("Please  Introduce yourself: ")
    # info="hahaha"
    # print("----------")
    # print('\033[1;33mWe asked him to introduce himself first.He said : \033[1;35m\" %s .\"\033[3;31m' %info)
    # print('这行是上一行结尾的颜色输出效果 \n\n')

    # print(bcolors.cHEADER + "警告的颜色字体?" +bcolors.cEND)
    # print(bcolors.cOKBLUE + "警告的颜色字体?" +bcolors.cEND)
    # print(bcolors.cOKGREEN + "警告的颜色字体?\n" +bcolors.cEND)

    # print('This is a \033[1;35m test \033[0m!')
    # print('This is a \033[1;32;41m test \033[0m!')
    # print('\033[1;33;44m  This is a test ! \033[0m\n')