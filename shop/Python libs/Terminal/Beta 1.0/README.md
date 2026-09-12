# terminal v1.0

> Python curses 简易自定义终端渲染库 | Beta v1.0
> Develop Team : WalkUp

## 📖 项目介绍

terminal 是基于Python内置`curses`封装的轻量控制台渲染库，专门用来打造自定义命令行界面。
支持定点输出文字、逐字打字机效果、单行擦除、光标移动、交互式输入。

> ⚠️ Windows提示：Windows原生cmd需要开启VT支持，代码内置`os.system('')`来启用虚拟终端；curses在Windows依赖windows-curses包。

✅ 功能清单：

1. output：普通文本输出，支持指定坐标(y,x)，自动清行末尾
2. outs：打字机动画效果逐字输出文本，可控制坐标
3. put：交互式输入框，自定义提示符，读取用户输入字符串
4. line：空行换行
5. clean：快速清空指定一行文字
6. cleans：动画擦除一行文字（逐个空格覆盖，带延时）
7. move：直接移动光标到指定(y,x)控制台坐标

> ⚠️ 警告：curses终端库运行时会接管控制台，程序异常退出可能导致控制台乱码；代码已经使用`atexit`自动恢复终端。

## 📦 依赖安装

```bash
pip install windows-curses
```




✨ 内置模块

output 普通输出

 output(text, y=None, x=0, end=True) 

- text：输出文本
- y,x：控制台坐标，不填默认当前光标位置
- end=True：输出后自动换行

outs 打字机动画输出

 outs(text, y=None, x=0, end=True) 
逐字符缓慢打印文字，带有动画效果，适合做终端UI。

put 交互式输入

 put(prompt='', y=None, x=0, max_len=50) 

- prompt：输入前面的提示文字
- 返回用户输入的utf-8字符串

line 空行

 line(y=None, x=0) ，插入空白行。

clean 快速清行

 clean(line=行号) ，瞬间清空指定一行。

cleans 动画擦除行

 cleans(line=行号) ，用空格逐个覆盖文字，实现擦除动画。

move 光标移动

 move(y, x) ，移动控制台光标到目标坐标。

🚀 最简示例

python

import terminal

# 普通文字输出

terminal.output("Hello custom terminal!")

# 打字机动画

terminal.outs("This is typewriter text effect.")

# 输入提示

res = terminal.put("请输入内容 > ")
terminal.output(f"你输入的是：{res}")
 

📁 整套项目结构更新

plaintext

WalkUp Studio Project Suite/
├─ src/
│  ├─ OpenGL_Base.py    # OpenGL图形绘制库
│  ├─ System32.py       # Windows底层自动化库
│  ├─ terminal.py       # curses自定义终端UI库
│  └─ library.py        # 通用工具库（等你贴代码）
├─ main.py              # 项目总入口demo
├─ requirements.txt     # 整合全部依赖
├─ README.md            # 项目总文档
└─ .gitignore
 

⚠️ Known Issues

1. Windows下必须安装 windows-curses ，Linux/Mac自带curses无需额外安装
2. 窗口大小改变会破坏布局，当前版本不支持动态resize监听
3.  clean 类内部代码存在索引bug，直接运行会报错，需要微调
4. 多线程同时调用输出函数会造成控制台渲染错乱，不支持并发打印
5. 中文显示受终端编码限制，部分旧cmd中文容易乱码，推荐使用Windows Terminal

📜 License

仅供学习和高级开发使用。
