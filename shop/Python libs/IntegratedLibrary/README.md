# IntegratedLibrary v1.0

> WalkUp Studio 一体化整合总库 | Beta v1.0
> Develop Team : WalkUp

## 📖 项目介绍

IntegratedLibrary 是**一体化全能封装库**，把之前独立的 System32 系统自动化、Terminal自定义curses终端、Ollama本地大模型、Edge-TTS语音、媒体播放、文件工具、键鼠模拟、窗口管理全部打包在同一个文件。
✅ 核心亮点：内置**自动依赖安装器**，导入库的时候自动检测缺少的包，自动调用pip安装；
✅ 内置降级兼容：curses不可用时，终端模块自动切换到普通print/input，不会直接崩溃；
✅ 全部功能使用静态类组织，统一命名空间，**只需要一行 `import IntegratedLibrary`** 就能拿到整套能力，无需分开导入多个py文件。

> ⚠️ 平台限制：**仅支持Windows**；键鼠、关机、DPI适配部分功能需要管理员权限。

✅ 功能清单

1. 自动依赖检测&安装：扫描`ollama`、`pywin32`、`psutil`等包，缺失自动pip安装
2. 系统信息读取：CPU、内存、屏幕分辨率、DPI缩放信息
3. 键鼠自动化：键盘组合键、长按、释放按键；鼠标贝塞尔平滑移动、单击/长按/滚轮
4. 窗口管理：窗口激活/最大化、无边框弹窗、密码校验弹窗（SHA512哈希校验密码，最多3次重试）、高分屏DPI适配
5. 文件工具：文件/文件夹删除、复制、全盘搜索文件、获取用户目录、系统临时目录
6. 时间工具：获取时间戳、时分秒
7. 媒体模块 mpv：Edge-TTS多音色TTS（含普通话+国内方言），自动生成并播放mp3、自动清理临时音频；VLC播放本地mp4视频
8. 哈希加密：MD5 / SHA256 / SHA512
9. 自定义终端 Terminal（内置你之前terminal.py全部能力）
   - output：普通文本定点输出
   - outs：打字机逐字动画输出
   - put：交互式输入
   - clean / cleans：瞬间清行 / 逐字符动画擦除一行
   - move：移动光标坐标
10. AI模块：Ollama本地大模型流式问答，支持指定模型（默认qwen2:latest）
11. 系统操作：一键关机、自动申请管理员权限
12. 调试工具：获取鼠标坐标调试

## 📦 依赖说明

> 库自带自动安装器，首次导入会自动检查并安装缺失包

### 顶层自动安装器

导入时自动执行：检测各个导入包，如果缺失自动执行pip install。

### `System` 系统与键鼠模块

- `System.shutdown()` 一键1秒关机
- `System.Get_Administrtor_permissions()` 自动申请管理员权限
- `System.keys` 键盘：key / start / stop / hold / release / English(切换英文输入法)
- `System.mouse` 鼠标：平滑move、left/right/middle单击、长按long、滚轮num

### `window` 窗口工具

- `window.password()` 密码登录弹窗，密码哈希校验，最多3次机会
- `window.up()` 根据标题查找并激活窗口
- `window.groud()` 最大化窗口
- `window.notwindow()` 无边框简易提示弹窗
- `window.Adaptation_DPI_Hight()` 开启高DPI感知，修复高分屏缩放错位

### `file` 文件操作工具

- `file.startup(path)` 打开文件/文件夹
- `file.delete()` 删除文件/文件夹
- `file.copy()` 复制文件
- `file.listdir()` 递归遍历目录获取全部文件路径
- `file.deletes()` 批量删除多个文件
- `file.user()` 获取用户主目录
- `file.Find()` 全盘搜索指定文件名
- `file.temp()` 获取系统临时目录

### `date` 时间工具

- `date.now()` 返回 `[时:分:秒]` 格式时间戳
- `date.hour()` / `date.minute()` / `date.second()` 获取对应数值

### `mpv` 媒体模块

- `mpv.mp3` Edge-TTS文字转语音，支持超多音色（男女、方言），生成临时音频并自动播放+自动删除
- `mpv.mp4` 使用VLC播放本地视频，tk窗口承载播放器，支持全屏、置顶

### `Hash / lock` 哈希加密

`Hash.bit(text, mode)` 支持32bit(md5),64bit(sha256),256bit(sha512)

### `Terminal` 内置自定义终端（原terminal.py）

> 自动兼容：Windows没有curses时自动降级到普通控制台打印

- `Terminal.output(text, y, x)` 定点输出文字
- `Terminal.outs(text)` 打字机动画
- `Terminal.put(prompt)` 获取用户输入
- `Terminal.clean(line)` 快速清空一行
- `Terminal.cleans(line)` 动画擦除单行
- `Terminal.move(y,x)` 移动光标

### `AI` Ollama本地大模型

`AI.ask(message, AI_Model='qwen2:latest')`
调用本地Ollama模型，流式拼接返回完整回答，**需要本地提前启动ollama服务**

### `debug` 调试工具

`debug.direction()`：等待3秒，获取当前鼠标坐标，用来定位屏幕坐标

## 🚀 最简示例

```python
import IntegratedLibrary as il

# 1. 查看系统硬件信息

print(il.infomation)

# 2. 键盘输入文字

il.System.keys.key("h-e-l-l-o", format=True)

# 3. TTS语音朗读

il.mpv.mp3.take(text="IntegratedLibrary加载成功", voice="男-普通")

# 4. Ollama本地大模型提问（需要ollama后台运行）

res = il.AI.ask("用简单语言解释什么是OpenGL")
print(res)

# 5. 自定义终端输出

il.Terminal.output("Hello custom terminal inside IntegratedLibrary!")
 

📁 整套项目最终结构

plaintext

WalkUp Studio Project Suite/
├─ src/
│  ├─ OpenGL_Base.py        # OpenGL 2D/3D图形绘制库
│  └─ IntegratedLibrary.py # 一体化整合总库（包含System32 + Terminal + AI + TTS +媒体全部功能）
├─ main.py                  # 项目总入口demo
├─ requirements.txt         # 整合全部依赖
├─ README.md                # 项目总README
└─ .gitignore
 

⚠️ Known Issues（已知BUG&注意事项）

1. 启动加载慢根源找到了！
顶层代码在导入阶段直接循环遍历 install_map ，不管包有没有缺失，循环遍历并执行pip安装，哪怕包已经装好了也会走循环，这就是双击运行要等好几秒的元凶！
现在逻辑：只要导入这个文件，for循环遍历所有包，调用pip install。包已经存在也会执行pip检查，pip本身加载非常慢，这就是耗时核心。
2. 拼写错误： Get_Administrtor_permissions  单词Administrator拼写错误（多了r）
4. curses在Windows需要windows-curses，没有会自动降级普通print，但部分终端颜色/坐标失效
5. Ollama调用需要本地电脑启动ollama服务，否则AI.ask直接报错
6. 键鼠、关机功能管理员权限才可以完整生效
7. 顶层创建tk窗口 System = tk.Tk() 然后立刻destroy，每次导入库都会短暂新建销毁tk实例，也会增加一点点加载耗时
8. 多线程同时调用Terminal输出会渲染错乱

📜 License

仅供学习和高级开发使用，请勿用于恶意自动化脚本。
