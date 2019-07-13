# -*- coding: UTF-8 -*-
# @LastAuthor: 隠れた人
# @Date: 2019-07-13 19:37:48

#导包
import json
import os
import re
import shutil
import subprocess
import threading
import time
import tkinter
import tkinter.filedialog
from tkinter import ttk

import requests
import pycurl

#初始值
conf = ""
delay = "未测试"
port = "未启用"
httpport = ""
socksport = ""
msg = "-------------------------------------------------------------\n"
status = 0


#函数实现
def Insertlog(log):
    Log.insert(tkinter.END, log + "\n\n")
    Log.update()
    Log.see(tkinter.END)


def UpdateMsg():
    global conf
    global delay
    global port
    global msg
    Msg.config(text=msg + "选中配置文件:  " + conf + "\n端口信息:  " + port +
               "\n打开谷歌网页延迟:  " + delay)
    Msg.update()


def CheckCoreUpdate():
    version = ""
    githubapi = "https://api.github.com/repos/v2ray/v2ray-core/releases/latest"
    githubjson = requests.get(githubapi)
    gj = json.loads(githubjson.text)
    version = gj["tag_name"]
    return version


def CheckClientUpdate():
    version = ""
    githubapi = "https://api.github.com/repos/LovelyFox-koucha/V2py/releases/latest"
    githubjson = requests.get(githubapi)
    gj = json.loads(githubjson.text)
    version = gj["tag_name"]
    return version


def ConfParser():
    global conf
    global port
    global httpport
    global socksport
    with open(r".\\config\\" + conf, "r") as f:
        d = json.load(f)
        f.close()
    for i in d["inbounds"]:
        if i["protocol"] == "socks":
            socksport = str(i["port"])
        if i["protocol"] == "http":
            httpport = str(i["port"])
    if httpport != "" or socksport != "":
        port = "http端口:  " + httpport + "  socks端口:  " + socksport
        UpdateMsg()
    else:
        pass


def CheckDelay():
    global httpport
    global socksport
    global delay
    r = requests.Session()
    while True:
        if socksport != "":
            proxies = {
                "http": "socks5://127.0.0.1:" + str(socksport),
                "https": "socks5://127.0.0.1:" + str(socksport)
            }
            try:
                s = r.get("https://www.google.com/",
                          timeout=3,
                          proxies=proxies)
                delay = str(int(s.elapsed.microseconds / 1000)) + " ms"
            except:
                delay = "超时"
            UpdateMsg()
        elif httpport != "":
            proxies = {
                "http": "http://127.0.0.1:" + str(httpport),
                "https": "http://127.0.0.1:" + str(httpport)
            }
            try:
                s = r.get("https://www.google.com/",
                          timeout=3,
                          proxies=proxies)
                delay = str(int(s.elapsed.microseconds / 1000)) + " ms"
            except:
                delay = "超时"
            UpdateMsg()
        else:
            Insertlog("无法进行延迟测试")
            UpdateMsg()
        time.sleep(5)


def CheckDelay_t():
    timer = threading.Thread(target=CheckDelay)
    timer.setDaemon(True)
    timer.start()


def TopTray():
    try:
        toptray = r".\\TopTray.exe"
        subprocess.Popen(toptray,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
        Insertlog("托盘托管成功")
    except:
        Insertlog("托盘托管失败,将无法最小化到托盘")


def QuitTopTray():
    try:
        quittop = r".\\TopTray.exe --exit"
        subprocess.Popen(quittop,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
        Insertlog("托盘托管退出成功")
    except:
        Insertlog("托盘托管退出失败")


def ReadConfList():
    global conf
    path = r".\\config"
    try:
        Conf_list['value'] = os.listdir(path)
        Conf_list.update()
        Conf_list.current(0)
        if Conf_list.get() != "":
            conf = Conf_list.get()
        else:
            Insertlog("不存在配置")
    except:
        Insertlog("读取配置文件夹失败")


def Start():
    global proc
    ConfParser()
    start = r".\\V2ray-core\\v2ray.exe -config .\\config\\" + conf
    proc = subprocess.Popen(start,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    Insertlog("V2ray已启动")


def Start_t():
    global status
    if status == 0:
        V2ray = threading.Thread(target=Start)
        V2ray.setDaemon(True)
        V2ray.start()
        status = 1
    else:
        Insertlog("已经存在一个实例")


def Stop():
    global proc
    global status
    if status == 1:
        subprocess.Popen("taskkill /F /T /PID " + str(proc.pid),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
        Insertlog("已结束")
        status = 0
    else:
        Insertlog("没有可结束实例")


def Restart():
    Stop()
    Start_t()


def SwithConf():
    global conf
    conf = Conf_list.get()
    ConfParser()
    Restart()
    Insertlog("已切换到配置:  " + conf)
    UpdateMsg()


def ImportConf():
    path = r".\\config"
    fname = tkinter.filedialog.askopenfilename(filetypes=[("json格式", "json")])
    try:
        shutil.copyfile(fname, r".\\config\\" + os.path.basename(fname))
        Insertlog("已添加")
    except:
        Insertlog("添加失败")
    try:
        Conf_list['value'] = os.listdir(path)
        Conf_list.update()
    except:
        Insertlog("遇到错误")


def CheckConf():
    global conf
    test = r".\\V2ray-core\\v2ray.exe -test .\\config\\" + conf
    try:
        V2ray_test = subprocess.Popen(test,
                                      shell=True,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
        i = V2ray_test.stdout.read()
        Log.insert(tkinter.END, i)
        Log.update()
        Log.see(tkinter.END)
    except:
        Insertlog("配置测试失败")


def DelConf():
    path = r".\\config"
    try:
        os.remove(r".\\config\\" + Conf_list.get())
        Insertlog("已删除")
    except:
        Insertlog("删除失败")
    try:
        Conf_list['value'] = os.listdir(path)
        Conf_list.update()
    except:
        Insertlog("遇到错误")


def UpgradeCore():
    global status
    global httpport
    try:
        Insertlog("该功能在网络状态差的情况下将无法正常使用")
        githubapi = "https://api.github.com/repos/v2ray/v2ray-core/releases/latest"
        githubjson = requests.get(githubapi)
        gj = json.loads(githubjson.text)
        version = gj["tag_name"]
        url = "https://github.com/v2ray/v2ray-core/releases/download/" + str(
            version) + "/v2ray-windows-64.zip"
        Insertlog("开始下载核心\nURL:" + url)
        with open(r".\v2ray-windows-64.zip", "wb") as f:
            c = pycurl.Curl()
            if status == 1 and httpport != "":
                c.setopt(pycurl.PROXY, "http://127.0.0.1:" + str(httpport))
                Insertlog("已启用http代理")
            else:
                Insertlog("未启用http代理")
            c.setopt(pycurl.FOLLOWLOCATION, True)
            c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.TIMEOUT, 60)
            c.setopt(c.URL, url)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()
            Insertlog("下载进程结束\n请查看是否下载成功")
    except:
        Insertlog("核心下载故障\n可能是下载时间超过60s")


def UpgradeClient():
    global status
    global httpport
    try:
        Insertlog("该功能在网络状态差的情况下将无法正常使用")
        githubapi = "https://api.github.com/repos/LovelyFox-koucha/V2py/releases/latest"
        githubjson = requests.get(githubapi)
        gj = json.loads(githubjson.text)
        version = gj["tag_name"]
        url = "https://github.com/LovelyFox-koucha/V2py/releases/download/" + str(
            version) + "/V2py.zip"
        Insertlog("开始下载客户端\nURL:" + url)
        with open(r".\V2py.zip", "wb") as f:
            c = pycurl.Curl()
            if status == 1 and httpport != "":
                c.setopt(pycurl.PROXY, "http://127.0.0.1:" + str(httpport))
                Insertlog("已启用http代理")
            else:
                Insertlog("未启用http代理")
            c.setopt(pycurl.FOLLOWLOCATION, True)
            c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.TIMEOUT, 60)
            c.setopt(c.URL, url)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()
            Insertlog("下载进程结束\n请查看是否下载成功")
    except:
        Insertlog("客户端下载故障\n可能是下载时间超过60s")


def UpgradeCore_t():
    upgrade = threading.Thread(target=UpgradeCore)
    upgrade.setDaemon(True)
    upgrade.start()


def UpgradeClient_t():
    upgrade = threading.Thread(target=UpgradeClient)
    upgrade.setDaemon(True)
    upgrade.start()


def StartUP():
    TopTray()
    ReadConfList()
    update1 = CheckCoreUpdate()
    Insertlog("最新核心版本为:    " + update1)
    update2 = CheckClientUpdate()
    Insertlog("最新客户端版本为:    " + update2)
    Insertlog("软件启动完毕")
    CheckDelay_t()


def Quit():
    Stop()
    QuitTopTray()
    time.sleep(0.5)
    root.quit()


#界面与函数绑定

##根窗口
root = tkinter.Tk()
root.geometry("375x355+300+300")
root.resizable(False, False)
root.title("V2py")
root.iconbitmap("V2py.ico")
root.protocol("WM_DELETE_WINDOW", Quit)

##部件
B_Start = tkinter.Button(root, width=15, text="启动", command=Start_t)
B_Restart = tkinter.Button(root, width=15, text="重启", command=Restart)
B_Stop = tkinter.Button(root, width=15, text="停止", command=Stop)
Conf_list = ttk.Combobox(root, width=30)
B_Conf_Swith = tkinter.Button(root, width=15, text="切换配置", command=SwithConf)
B_Conf_Import = tkinter.Button(root, width=15, text="导入配置", command=ImportConf)
B_Conf_Check = tkinter.Button(root, width=15, text="检查配置", command=CheckConf)
B_Conf_Del = tkinter.Button(root, width=15, text="删除配置", command=DelConf)
B_Upgrade_Core = tkinter.Button(root,
                                width=20,
                                text="更新核心",
                                command=UpgradeCore_t)
B_Upgrade_Client = tkinter.Button(root,
                                  width=20,
                                  text="更新客户端",
                                  command=UpgradeClient_t)
Msg = tkinter.Label(root, width=50, height=4, text=msg, justify="left")
Log = tkinter.Text(root, width=60, height=10, font=("", 9, ""))

##布局
B_Start.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
B_Restart.grid(row=0, column=2, padx=5, pady=5, columnspan=2)
B_Stop.grid(row=0, column=4, padx=5, pady=5, columnspan=2)
Conf_list.grid(row=1, column=0, padx=5, pady=5, columnspan=4)
B_Conf_Swith.grid(row=1, column=4, padx=5, pady=5, columnspan=2)
B_Conf_Import.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
B_Conf_Check.grid(row=2, column=2, padx=5, pady=5, columnspan=2)
B_Conf_Del.grid(row=2, column=4, padx=5, pady=5, columnspan=2)
B_Upgrade_Core.grid(row=3, column=0, padx=5, pady=5, columnspan=3)
B_Upgrade_Client.grid(row=3, column=3, padx=5, pady=5, columnspan=3)
Msg.grid(row=4, column=0, padx=5, pady=5, columnspan=6)
Log.grid(row=5, column=0, padx=5, pady=5, columnspan=6)

#主循环
if __name__ == "__main__":
    startup = threading.Thread(target=StartUP)
    startup.setDaemon(True)
    startup.start()
    root.mainloop()
