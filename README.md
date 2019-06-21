# V2py

![screenshot](https://github.com/LovelyFox-koucha/V2py/blob/master/readme/screenshot.png)


## 声明
本项目使用GPLv3许可
本项目不带任何代理功能
仅供为GUI练习项目使用,请勿用于违法用途

## 特性
- 支持启动/重启/停止
- 支持更新核心文件
- 支持从别的地方导入config.json文件配置
- 显示socks端口
- 间隔5s测试一次通过代理打开谷歌所需的时间
- 右击最小化按钮可最小化到系统托盘

## 使用方式
1. 将文件放在同一文件夹下并在建立名为"V2ray-core"的文件夹
2. 将核心文件解压到该文件夹下
3. 导入/编辑配置文件
4. 启动主程序V2py.py或V2py.exe

## 待更新
- 重启时似乎存在偶尔会进程管理异常的情况
- 下载核心文件走http代理[如果有的话]
- 显示http代理端口
- 优化延迟测试部分
- 界面自适应化设计[防止系统缩放导致的显示异常]

## 致谢
- 文件下载[wget项目](https://github.com/mirror/wget)
- 系统托盘[TopTray项目](https://github.com/RanFeng/TopTray)
