# System32 v1.0

> Windows系统自动化工具库，Python Windows底层控制封装库 | Beta v1.0
> Develop Team : WalkUp

## 📖 项目介绍

System32 是一套面向Windows平台的Python底层工具封装库，基于`win32api`、`ctypes`、tkinter等封装。
提供**键鼠模拟、窗口管理、文件操作、系统信息读取、TTS语音合成、视频播放、密码弹窗、哈希加密**等功能。

> ⚠️ 重要提示：仅支持 Windows，部分功能需要管理员权限。

✅ 功能清单：

1. 系统信息读取：CPU、内存、屏幕分辨率、DPI适配
2. 键鼠自动化：按键模拟、组合键、鼠标移动/点击/滚轮，带贝塞尔曲线平滑移动
3. Windows窗口控制：激活窗口、最大化、置顶无边框弹窗
4. 文件工具：遍历搜索、复制、删除、获取用户目录、临时目录
5. TTS语音：Edge-TTS微软多音色语音合成（支持普通话、多地方言）
6. 媒体播放：mp3音频播放、VLC播放mp4视频
7. 加密工具：MD5、SHA256、SHA512哈希
8. 弹窗组件：密码验证登录窗口、提示弹窗
9. 系统控制：DPI适配、获取管理员权限、一键关机

> ⚠️ 警告：键鼠模拟、关机等高危操作，请仅在自己电脑、可控环境内测试，不要用于恶意自动化。

## 📦 依赖安装

```bash
pip install pywin32 psutil pygetwindow edge-tts playsound vlc
```

```
✨ 内置模块

keys 键盘模块

-  keys.key() ：按下完整按键序列，支持组合键（ctrl/alt/shift/win）
-  keys.start() ：按下按键不松开
-  keys.stop() ：停止按键
-  keys.hold() ：长按指定按键一段时间
-  keys.release() ：释放所有按住的修饰键
-  keys.English() ：快速切换英文输入法（ctrl+空格）

mouse 鼠标模块

-  mouse.move() ：平滑曲线移动鼠标到坐标
-  mouse.left() ：左键单击
-  mouse.right() ：右键单击
-  mouse.long() ：长按左键/右键
-  mouse.middle() ：中键点击
-  mouse.num() ：鼠标滚轮上下滚动

window 窗口管理

-  window.password() ：弹出密码验证窗口，密码使用哈希校验，最多3次重试
-  window.up() ：查找并激活指定标题窗口，最小化窗口自动恢复
-  window.groud() ：最大化目标窗口
-  window.notwindow() ：无边框简易提示弹窗

file 文件工具

-  file.startup() ：打开文件/文件夹
-  file.delete() ：删除文件/文件夹
-  file.copy() ：复制文件
-  file.listdir() ：递归遍历目录获取全部文件路径
-  file.deletes() ：批量删除多个文件
-  file.user() ：获取用户主目录
-  file.Find() ：全盘搜索指定文件名
-  file.temp() ：获取系统临时文件夹路径

date 时间工具

-  date.now()  返回带时分秒时间戳
-  date.hour()  /  date.minute()  /  date.second()  获取时分秒

mpv 媒体模块

-  mpv.mp3  Edge-TTS文字转语音，生成临时mp3并自动播放、自动清理
-  mpv.mp4  使用VLC播放本地视频，tk窗口承载播放器，支持全屏、置顶

lock 加密哈希

-  lock.Hash.bit() ：MD5 / SHA256 / SHA512 哈希计算

debug 调试工具

-  debug.direction() ：获取当前鼠标坐标（延时3秒，方便定位）

系统功能

-  shutdown() ：一键关机（1秒后关机）
-  Get_Administrtor_permissions() ：自动申请管理员权限
-  Adaptation_DPI_Hight() ：开启高DPI适配，修复高分屏窗口缩放问题
-  infomation  字典：预读取硬件、屏幕、DPI信息

🚀 最简示例

python

import System32

# 1. 获取系统信息

print(System32.infomation)

# 2. 模拟键盘输入 hello

System32.keys.key("h-e-l-l-o", format=True)

# 3. 鼠标平滑移动到屏幕中心，左键单击

System32.mouse.move()
System32.mouse.left()

# 4. TTS语音朗读文字

System32.mpv.mp3.take(text="你好，System32库加载成功", voice="男-普通")

# 5. 弹出密码窗口

System32.window.password(password="123456")
 

📁 项目结构示例

plaintext

OpenGL_Base/
├─ src/
│  ├─ OpenGL_Base.py    # OpenGL绘图核心库
│  └─ System32.py       # Windows系统自动化库
├─ main.py              # 项目测试demo
├─ requirements.txt     # 全部依赖
├─ README.md
└─ .gitignore
 

⚠️ Known Issues

1. VLC需要本机安装VLC播放器，仅安装python vlc库会播放失败
2. 键鼠模拟、关机部分功能需要管理员权限才能正常执行
3. 仅支持Windows系统，Linux/macOS完全不可用
4. edge-tts需要联网，离线环境无法生成语音
5.  window.password 窗口DPI缩放在部分老系统可能出现窗口尺寸偏移

📜 License

仅供学习和开发高级操作使用。请勿用于恶意脚本。
```
