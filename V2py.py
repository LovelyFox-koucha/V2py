# -*- coding: UTF-8 -*-
# @LastAuthor: 隠れた人
# @Date: 2019-06-22 00:16:08

#导包
import json
import re
import shutil
import subprocess
import threading
import time
import tkinter
import tkinter.filedialog

import requests
from PIL import Image, ImageTk

import pycurl

#常量变量初始值
delay = "未测试"
port = "未设置"
port1 = "未设置"
status = 0


#函数实现
def StartUP():
    try:
        with open(r".\V2ray-core\config.json", "r") as f:
            try:
                config = json.load(f)
            except:
                config = "error!"
                raise Exception("Invalid Config!", config)
            f.close()
        TextBox.insert(
            tkinter.END, "存在符合json格式的配置\n请不要快速反复启动停止或打开多个实例...\n"
            "右击最小化按钮可最小化到系统托盘\n但是不要直接在托盘操作[会卡死界面]\n配置中的入口顺序应当为socks/http\n")
        TextBox.see(tkinter.END)
    except:
        TextBox.insert(
            tkinter.END, "存在符合json格式的配置\n请不要快速反复启动停止或打开多个实例...\n"
            "右击最小化按钮可最小化到系统托盘\n但是不要直接在托盘操作[会卡死界面]\n配置中的入口顺序应当为socks/http\n")
        TextBox.see(tkinter.END)


def Check():
    global port
    global port1
    global delay
    while True:
        with open(r".\V2ray-core\config.json", "r") as f:
            d = json.load(f)
            f.close()
        port = d["inbounds"][0]["port"]
        port1 = d["inbounds"][1]["port"]
        r = requests.Session()
        proxies = {
            "http": "socks5://127.0.0.1:" + str(port),
            "https": "socks5://127.0.0.1:" + str(port)
        }
        try:
            s = r.get("https://www.google.com/", timeout=3, proxies=proxies)
            delay = int(s.elapsed.microseconds / 1000)
        except:
            delay = "超时"
        Msg.config(text="Socks端口:    " + str(port) + "    Http端口:    " +
                   str(port1) + "\n加载谷歌需要:    " + str(delay) + "  ms")
        Msg.update()
        time.sleep(5)


def TopTray():
    try:
        toptray = r".\TopTray.exe"
        subprocess.Popen(toptray,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    except:
        TextBox.insert(tkinter.END, "托盘托管失败,将无法最小化到托盘\n")
        TextBox.update()
        TextBox.see(tkinter.END)


def QuitTopTray():
    try:
        quittop = r".\TopTray.exe --exit"
        subprocess.Popen(quittop,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    except:
        TextBox.insert(tkinter.END, "托盘托管退出失败\n")
        TextBox.update()
        TextBox.see(tkinter.END)


def Test():
    test = r".\V2ray-core\v2ray.exe -test"
    try:
        V2ray_test = subprocess.Popen(test,
                                      shell=True,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
        i = V2ray_test.stdout.read()
        TextBox.insert(tkinter.END, i)
        TextBox.update()
        TextBox.see(tkinter.END)
    except:
        TextBox.insert(tkinter.END, "配置测试失败\n")
        TextBox.update()
        TextBox.see(tkinter.END)


def Start():
    global proc
    TextBox.insert(tkinter.END, "1S之后尝试启动\n")
    TextBox.update()
    TextBox.see(tkinter.END)
    time.sleep(1)
    Test()
    start = r".\V2ray-core\v2ray.exe -config .\V2ray-core\config.json"
    proc = subprocess.Popen(start,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    for i in iter(proc.stdout.readline, "b"):
        TextBox.insert(tkinter.END, i)
        TextBox.update()
        TextBox.see(tkinter.END)


def Start_t():
    global status
    if status == 0:
        V2ray = threading.Thread(target=Start)
        V2ray.setDaemon(True)
        V2ray.start()
        status = 1
    else:
        TextBox.insert(tkinter.END, "已经存在一个实例\n")
        TextBox.update()
        TextBox.see(tkinter.END)


def Stop():
    global proc
    global status
    TextBox.insert(tkinter.END, "1S之后尝试停止\n")
    TextBox.update()
    TextBox.see(tkinter.END)
    time.sleep(1)
    if status == 1:
        subprocess.Popen("taskkill /F /T /PID " + str(proc.pid),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
        TextBox.delete(1.0, tkinter.END)
        TextBox.insert(tkinter.END, "已结束\n")
        TextBox.update()
        TextBox.see(tkinter.END)
        status = 0
    else:
        TextBox.delete(1.0, tkinter.END)
        TextBox.insert(tkinter.END, "没有可结束实例\n")
        TextBox.update()
        TextBox.see(tkinter.END)


def Restart():
    Stop()
    Start_t()


def Upgrade():
    global status
    global port1
    try:
        TextBox.insert(tkinter.END, "[提示]该功能在网络状态差的情况下将无法正常使用\n")
        TextBox.see(tkinter.END)
        githubapi = "https://api.github.com/repos/v2ray/v2ray-core/releases/latest"
        githubjson = requests.get(githubapi)
        gj = json.loads(githubjson.text)
        version = gj["tag_name"]
        url = "https://github.com/v2ray/v2ray-core/releases/download/" + str(
            version) + "/v2ray-windows-64.zip"
        TextBox.insert(tkinter.END, "开始下载核心\nURL:" + url + "\n")
        TextBox.see(tkinter.END)
        with open(r".\v2ray-windows-64.zip", "wb") as f:
            c = pycurl.Curl()
            if status == 1 and port1 != "未设置":
                c.setopt(pycurl.PROXY, "http://127.0.0.1:" + str(port1))
                TextBox.insert(tkinter.END, "已启用http代理\n")
                TextBox.update()
                TextBox.see(tkinter.END)
            else:
                TextBox.insert(tkinter.END, "未启用http代理\n")
                TextBox.update()
                TextBox.see(tkinter.END)
            c.setopt(pycurl.FOLLOWLOCATION, True)
            c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.TIMEOUT, 60)
            c.setopt(c.URL, url)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()
        TextBox.insert(tkinter.END, "下载进程结束\n请查看是否下载成功\n")
        TextBox.update()
        TextBox.see(tkinter.END)
    except:
        TextBox.insert(tkinter.END, "核心下载故障\n可能是下载时间超过60s\n")
        TextBox.update()
        TextBox.see(tkinter.END)


def Upgrade_t():
    global upgrade
    upgrade = threading.Thread(target=Upgrade)
    upgrade.setDaemon(True)
    upgrade.start()


def Import():
    fname = tkinter.filedialog.askopenfilename(filetypes=[("json格式", "json")])
    test = r".\V2ray-core\v2ray.exe -test " + fname
    try:
        shutil.copyfile(fname, r".\V2ray-core\config.json")
        TextBox.insert(tkinter.END, "已替换\n")
        TextBox.update()
        TextBox.see(tkinter.END)
        config_test = subprocess.Popen(test,
                                       shell=True,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
        i = config_test.stdout.read()
        TextBox.insert(tkinter.END, i)
        TextBox.update()
        TextBox.see(tkinter.END)
    except:
        TextBox.insert(tkinter.END, "配置替换/检测失败\n")
        TextBox.update()
        TextBox.see(tkinter.END)


def Quit():
    QuitTopTray()
    Stop()
    root.quit()


#界面与函数绑定

##根窗口
root = tkinter.Tk()
root.geometry("400x310+400+400")
root.resizable(False, False)
root.title("V2py")
root.iconbitmap("V2py.ico")
root.protocol("WM_DELETE_WINDOW", Quit)

##部件
B1 = tkinter.Button(root, text="启动", width=10, command=Start_t)
B2 = tkinter.Button(root, text="重启", width=10, command=Restart)
B3 = tkinter.Button(root, text="停止", width=10, command=Stop)
B4 = tkinter.Button(root, text="更新核心", width=15, command=Upgrade_t)
B5 = tkinter.Button(root, text="导入配置", width=15, command=Import)
Msg = tkinter.Label(root,
                    text="Socks端口:    " + str(port) + "    Http端口:    " +
                    str(port1) + "\n加载谷歌需要:    " + str(delay) + "  ms",
                    width=30,
                    justify="left")
img = Image.open("V2py.png")
Logo = ImageTk.PhotoImage(img)
L1 = tkinter.Label(root, image=Logo)
TextBox = tkinter.Text(root, width=62, height=10, font=("", 9, ""))

##布局
B1.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
B2.grid(row=0, column=2, padx=5, pady=5, columnspan=2)
B3.grid(row=0, column=4, padx=5, pady=5, columnspan=2)
B4.grid(row=1, column=0, padx=5, pady=5, columnspan=3)
B5.grid(row=1, column=3, padx=5, pady=5, columnspan=3)
Msg.grid(row=3, column=0, columnspan=6)
L1.grid(row=0, column=6, rowspan=2, columnspan=2)
TextBox.grid(row=4, column=0, padx=5, pady=5, columnspan=8)

#主循环
if __name__ == "__main__":
    TopTray()
    StartUP()
    timer = threading.Thread(target=Check, args=())
    timer.setDaemon(True)
    timer.start()
    root.mainloop()
