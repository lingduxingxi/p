#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import threading
import time
# import datetime
import winreg

import pythoncom
from notifypy import Notify
from win32com.client import gencache

import cmd_on_color
from kill_all_pid_from_filenames_python_name_pid import kill_exe
from upload_node import upload

# 创建一个锁对象
notification_lock = threading.Lock()
# 配置常量
APP_ID = "fso.NotifyApp"
ICON_MAPPING = {
    "fso": os.path.join(os.getcwd(), "fso.ico"),
    "info": os.path.join(os.getcwd(), "info.ico"),
    "warning": os.path.join(os.getcwd(), "warning.ico"),
    "error": os.path.join(os.getcwd(), "error.ico"),
    "success": os.path.join(os.getcwd(), "success.ico"),
}
SOUND_MAPPING = {
    "info": "ms-winsoundevent:Notification.Default",
    "warning": "ms-winsoundevent:Notification.Warning",
    "error": "ms-winsoundevent:Notification.Error",
    "success": "ms-winsoundevent:Notification.SMS",
}


def is_app_id_registered(app_id: str) -> bool:
    """检查 AppID 是否已在注册表中注册"""
    key_path = fr"Software\Classes\AppUserModelId\{app_id}"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ):
            return True
    except FileNotFoundError:
        return False


def register_app_id_if_needed(app_id: str, display_name: str, icon_uri: str):
    """如果未注册 AppUserModelID，则注册"""
    if is_app_id_registered(app_id):
        print(f"AppID '{app_id}' 已存在，无需重复注册。")
        return

    key_path = fr"Software\Classes\AppUserModelId\{app_id}"
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, display_name)
        winreg.SetValueEx(key, "IconUri", 0, winreg.REG_SZ, icon_uri)
        winreg.SetValueEx(key, "ToastActivatorCLSID", 0, winreg.REG_SZ, "{00000000-0000-0000-0000-000000000000}")
        winreg.CloseKey(key)
        print(f"AppID '{app_id}' 已成功注册到注册表。")
    except Exception as e:
        print(f"注册 AppID 时发生错误: {e}")

        pass


def show_notification(title: str, message: str, notification_type: str = "info", duration: int = 6,state_show_notification = True):
    """
    显示自定义通知

    参数:
        title: 通知标题
        message: 通知内容
        notification_type: 通知类型 (info/warning/error/success)
        duration: 通知显示时长（秒）
    """
    # state_show_notification = True #开启通知
    # state_show_notification = False #关闭通知
    # if state_show_notification: #所有端口
    # global show_notification_state
    if not state_show_notification:
        return
    print('state_show_notification72',state_show_notification,title)
    if '成功' in title and '8100' in title:
        upload("goflyway_config.ini")
    if '成功' in title and '10801' in title:
        upload(f"SS1_configs_port10801.json")
        upload(f"SS1_configs_port88.json")
    if '成功' in title and '10801' in title:
        upload(f"SS2_configs_port10802.json")
        upload(f"SS2_configs_port88.json")
    if '成功' in title and '10805' in title:
        upload(f'SSR1_clash_config_port10805.yaml')
        upload(f'SSR1_clash_config_port88.yaml')
    if '成功' in title and '10806' in title:
        upload(f'SSR2_clash_config_port10806.yaml')
        upload(f'SSR2_clash_config_port88.yaml')
    if '成功' in title and '10822' in title:
        upload(fr'v2ray1_configs_port10822.json')
        upload(fr'v2ray1_configs_port88.json')
    if '成功' in title and '10999' in title:
        upload(fr'v2ray2_configs_port10999.json')
        upload(fr'v2ray2_configs_port88.json')

    if state_show_notification and '88' in title:#仅有88端口
        try:
            # 获取锁
            notification_lock.acquire()

            # 显式初始化 COM 库
            pythoncom.CoInitialize()

            # 导入必要的模块
            gencache.EnsureModule('{46EB5926-582E-4017-9FDF-E8998DAA0950}', 0, 1, 0)
            print('即将展示通知，开始导入库winrt')
            import winrt.windows.ui.notifications as notifications
            import winrt.windows.data.xml.dom as dom

            # from winrt.windows.foundation import DateTime
            # 注册 AppID
            default_icon = ICON_MAPPING.get("fso", "")
            print('开始注册通知82')
            register_app_id_if_needed(
                app_id=APP_ID,
                display_name="来自fso的通知",
                icon_uri=default_icon
            )
            print('开始注册通知结束88')
            # 确定通知持续时间（转换为 Windows 支持的值）
            toast_duration = "long" if duration > 7 else "short"

            # 构建通知 XML
            toast_xml_str = f"""
            <toast activationType="foreground" duration="{toast_duration}">
                <visual>
                    <binding template="ToastGeneric">
                        <image placement="appLogoOverride" hint-crop="circle" src="{ICON_MAPPING.get(notification_type, default_icon)}"/>
                        <text>{title}</text>
                        <text>{message}</text>
                    </binding>
                </visual>
                <audio src="{SOUND_MAPPING.get(notification_type, SOUND_MAPPING['info'])}" loop="false"/>
            </toast>
            """
            print('解析 XML105')
            # 解析 XML
            xml_doc = dom.XmlDocument()
            print('导入 XML108')
            xml_doc.load_xml(toast_xml_str)
            print('创建通知109')
            # 创建通知
            notification = notifications.ToastNotification(xml_doc)

            print('设置标签以唯一标识通知113')
            # 设置标签以唯一标识通知
            notification.tag = f"tag_{int(time.time() * 1000)}"

            # 显示通知
            notifier = notifications.ToastNotificationManager.create_toast_notifier(APP_ID)
            print('显示通知119')
            notifier.show(notification)
        except Exception as e:
            print(f"通知显示出错: {str(e)}")
            cmd_on_color.printRed('错误通知，改用备用通知')
            show_notification_backup(title,message,notification_type,duration,state_show_notification)
        finally:
            # 释放 COM 库
            pythoncom.CoUninitialize()

            # 释放锁
            notification_lock.release()
        # print(f"✅ 已发送 {notification_type} 通知: {title}（持续时间: {duration}秒）")
    print('state_show_notification121通知完成', state_show_notification, title)

def show_notification_backup(title: str, message: str, notification_type: str = "info", duration: int = 6, state_show_notification=True):
    """
    显示自定义通知

    参数:
        title: 通知标题
        message: 通知内容
        notification_type: 通知类型 (info/warning/error/success)
        duration: 通知显示时长（秒）
    """
    if state_show_notification and '88' in title:  # 仅有88端口
        # 注册 AppID（notifypy不需要注册表项，但保留原有功能）
        default_icon = ICON_MAPPING.get("info", "")
        register_app_id_if_needed(
            app_id=APP_ID,
            display_name="来自fso的通知",
            icon_uri=default_icon
        )

        try:
            # 创建通知对象
            notification = Notify()
            notification.title = title
            notification.message = message
            notification.application_name = "来自fso的通知"

            # 设置图标
            icon_path = ICON_MAPPING.get(notification_type, default_icon)
            if os.path.exists(icon_path):
                notification.icon = icon_path

            # 设置声音（notifypy使用系统声音或自定义WAV文件）
            sound_name = SOUND_MAPPING.get(notification_type)
            if sound_name:
                # 注意：notifypy需要实际文件路径，而不是WinRT的ms-winsoundevent格式
                # 这里简化处理，使用系统默认声音
                pass

            # 显示通知
            notification.send()

            # print(f"✅ 已发送 {notification_type} 通知: {title}（持续时间: {duration}秒）")
        except Exception as e:
            # print(f"❌ 发送通知时出错: {e}")
            pass

# 示例调用
if __name__ == "__main__":
    # kill_exe('sslocal_all.exe')
    kill_exe('CASiLab.exe')
    # show_notification(f"端口 88 链接错误！\n准备更换端口为 10801", "不可以上网！", "error")
    # show_notification_backup(f"端口 88 链接错误！\n准备更换端口为 10801", "不可以上网！", "error")
    # # 发送不同类型的通知，使用不同的持续时间
    # show_notification("系统消息", "程序已成功启动并运行", "info", 5)
    # time.sleep(2)
    # show_notification("更新提醒", "新版本可用，点击此处下载更新", "warning", 5)
    # time.sleep(2)
    # show_notification("错误报告", "无法连接到服务器，请检查网络连接", "error", 5)
    # time.sleep(2)
    # show_notification("操作成功", "文件已成功保存到指定位置", "success", 5)

# 在上述代码的基础上修改下，需求为：获取通知中心的所有通知数量，如果检测到通知数量超过8个就将通知中心清除所有通知，类似鼠标点击了清除所有通知