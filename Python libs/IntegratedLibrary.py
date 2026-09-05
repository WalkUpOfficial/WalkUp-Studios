import importlib.util
import subprocess
import tkinter as tk
import sys

install_map = {
    "win32api": "pywin32",
    "psutil": "psutil",
    "pygetwindow": "pygetwindow",
    "edge_tts": "edge-tts",
    "playsound": "playsound",
    "vlc": "python-vlc",
    "ollama": "ollama"
}

for import_name, pip_name in install_map.items():
    if importlib.util.find_spec(import_name) is None:
        root = tk.Tk()
        root.title('IntegratedLibrary Installer')
        
        root.geometry()
        for pkg in install_map:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import win32api
import win32con
import win32gui
import ctypes
import time
import math
import random
import os
import shutil
import platform
import psutil
import pygetwindow as gw
import queue
import threading
from ctypes import Structure, c_long, c_ulong, c_ulonglong, c_ushort, POINTER, byref
from datetime import datetime
import edge_tts
import asyncio
import playsound
import vlc
from tkinter import messagebox
import re
import hashlib
import sys
import ollama

voices = {
    '女-普通': 'zh-CN-XiaoxiaoNeural',
    '女-成年': 'zh-CN-XiaoyiNeural',
    '女-故事': 'zh-CN-XiaomoNeural',
    '女-清新': 'zh-CN-XiaoxuanNeural',
    '女-多语言': 'zh-CN-XiaoxiaoMultilingualNeural',
    '女-友好': 'zh-CN-XiaochenNeural',
    '女-友好2': 'zh-CN-XiaochenMultilingualNeural',
    '女-温柔': 'zh-CN-XiaohanNeural',
    '女-甜美': 'zh-CN-XiaomengNeural',
    '女-舒缓': 'zh-CN-XiaoqiuNeural',
    '女-沙哑': 'zh-CN-XiaoruiNeural',
    '女-温暖': 'zh-CN-XiaoyanNeural',
    '女-明亮多语言': 'zh-CN-XiaoyouMultilingualNeural',
    '女-深沉多语言': 'zh-CN-XiaoyuMultilingualNeural',
    '女-冷静': 'zh-CN-XiaozhenNeural',
    '男-普通': 'zh-CN-YunxiNeural',
    '男-深沉': 'zh-CN-YunjianNeural',
    '男-轻松': 'zh-CN-YunxiaNeural',
    '男-播报': 'zh-CN-YunyangNeural',
    '男-多语言': 'zh-CN-YunfanMultilingualNeural',
    '男-自信': 'zh-CN-YunfengNeural',
    '男-随意': 'zh-CN-YunjieNeural',
    '男-温和多语言': 'zh-CN-YunxiaoMultilingualNeural',
    '男-深沉随意': 'zh-CN-YunyeNeural',
    '男-温和多语言2': 'zh-CN-YunyiMultilingualNeural',
    '男-正式': 'zh-CN-YunzeNeural',
    '男-河南方言': 'zh-CN-henan-YundengNeural',
    '女-辽宁方言': 'zh-CN-liaoning-XiaobeiNeural',
    '女-陕西方言': 'zh-CN-shaanxi-XiaoniNeural',
    '男-山东方言': 'zh-CN-shandong-YunxiangNeural',
    '男-四川方言': 'zh-CN-sichuan-YunxiNeural',
}

class MOUSEINPUT(Structure):
    _fields_ = [
        ("dx", c_long),
        ("dy", c_long),
        ("mouseData", c_ulong),
        ("dwFlags", c_ulong),
        ("time", c_ulong),
        ("dwExtraInfo", c_ulonglong)
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]

class INPUT(Structure):
    _fields_ = [
        ("type", c_ulong),
        ("ii", INPUT_UNION)
    ]

System = tk.Tk()
System.title('IntegratedLibrary')
System.withdraw()

def Get_DPI_Power():
    return round(System.winfo_fpixels('1i') / 96) * 100

def Get_DPI_Power_tk():
    return round(System.winfo_fpixels('1i') / 96)

infomation = {
    'CPU Infomation': platform.processor(),
    'CPU num': psutil.cpu_count(logical=True),
    'System Infomation': f'{platform.system()} {platform.version()[:platform.version().index(".")]}',
    'Memory': f'{psutil.virtual_memory().total / (1024 ** 3):.1f} GB',
    'screen_w': System.winfo_screenwidth(),
    'screen_h': System.winfo_screenheight(),
    'DPI': {
        'System': Get_DPI_Power(),
        'tkinter': 1
    }
}
System.destroy()

_pressed_modifiers = []
_is_shift_held = False
_last_target_key = None
user32 = ctypes.windll.user32
GWL_STYLE = -16
WS_SYSMENU = 0x00080000
SWP_FRAMECHANGED = 0x0020
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001

MODIFIERS = {
    'ctrl': win32con.VK_CONTROL,
    'alt': win32con.VK_MENU,
    'shift': win32con.VK_SHIFT,
    'win': win32con.VK_LWIN
}

SPECIAL_KEYS = {
    'esc': win32con.VK_ESCAPE,
    'escape': win32con.VK_ESCAPE,
    'enter': win32con.VK_RETURN,
    'return': win32con.VK_RETURN,
    'tab': win32con.VK_TAB,
    'space': win32con.VK_SPACE,
    'backspace': win32con.VK_BACK,
    'delete': win32con.VK_DELETE,
    'up': win32con.VK_UP,
    'down': win32con.VK_DOWN,
    'left': win32con.VK_LEFT,
    'right': win32con.VK_RIGHT,
    'f1': win32con.VK_F1,
    'f2': win32con.VK_F2,
    'f3': win32con.VK_F3,
    'f4': win32con.VK_F4,
    'f5': win32con.VK_F5,
    'f6': win32con.VK_F6,
    'f7': win32con.VK_F7,
    'f8': win32con.VK_F8,
    'f9': win32con.VK_F9,
    'f10': win32con.VK_F10,
    'f11': win32con.VK_F11,
    'f12': win32con.VK_F12,
}

class Hash:
    @staticmethod
    def bit(text, mode=None):
        if mode is None:
            mode = ['32 bit']
        if mode[0] == '32 bit':
            return hashlib.md5(text.encode('utf-8')).hexdigest()
        elif mode[0] == '64 bit':
            return hashlib.sha256(text.encode('utf-8')).hexdigest()
        elif mode[0] == '256 bit':
            return hashlib.sha512(text.encode('utf-8')).hexdigest()

lock = Hash

class System:
    @staticmethod
    def shutdown():
        os.system("shutdown /s /t 1")

    @staticmethod
    def Get_Administrtor_permissions():
        if not ctypes.windll.shell32.IsUserAnAdmin():
            if sys.argv[0].endswith('.pyw'):
                exe = sys.executable.replace("python.exe", "pythonw.exe")
            else:
                exe = sys.executable
            params = " ".join(f'"{arg}"' for arg in sys.argv)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, params, None, 1)
            sys.exit(0)

    class keys:
        @staticmethod
        def key(key_string: str, format=False, wait=0):
            time.sleep(0.02)
            global _is_shift_held, _last_target_key
            if format:
                keys = list(key_string)
            else:
                keys = [x for x in key_string.split('-') if x]
            for idx, k_raw in enumerate(keys):
                is_last_key = (idx == len(keys) - 1)
                if k_raw.lower() in MODIFIERS:
                    vk = MODIFIERS[k_raw.lower()]
                    win32api.keybd_event(vk, 0, 0, 0)
                    _pressed_modifiers.append(vk)
                    continue
                vk_to_press = None
                need_shift = False
                if k_raw.lower() in SPECIAL_KEYS:
                    vk_to_press = SPECIAL_KEYS[k_raw.lower()]
                else:
                    scan_result = user32.VkKeyScanW(ord(k_raw))
                    if scan_result == -1:
                        raise ValueError(f"No key : {k_raw}")
                    vk_to_press = scan_result & 0xFF
                    shift_state = (scan_result >> 8) & 0xFF
                    if shift_state & 1:
                        need_shift = True
                if need_shift:
                    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
                win32api.keybd_event(vk_to_press, 0, 0, 0)
                time.sleep(wait)
                win32api.keybd_event(vk_to_press, 0, win32con.KEYEVENTF_KEYUP, 0)
                if need_shift:
                    win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            System.keys.release()

        @staticmethod
        def start(key_string: str, format=False, wait=0):
            global _is_shift_held, _last_target_key
            if format:
                keys = [char for char in key_string.lower()]
            else:
                keys = [x for x in key_string.lower().split('-') if x]
            for idx, k in enumerate(keys):
                is_last_key = (idx == len(keys) - 1)
                if k in MODIFIERS:
                    vk = MODIFIERS[k]
                    win32api.keybd_event(vk, 0, 0, 0)
                    _pressed_modifiers.append(vk)
                    if is_last_key:
                        _last_target_key = None
                elif k in SPECIAL_KEYS:
                    vk = SPECIAL_KEYS[k]
                    win32api.keybd_event(vk, 0, 0, 0)
                    if is_last_key:
                        _last_target_key = vk
                else:
                    scan_result = user32.VkKeyScanW(ord(k))
                    if scan_result == -1:
                        raise ValueError(f"无法识别的按键: {k}")
                    virtual_key = scan_result & 0xFF
                    shift_state = (scan_result >> 8) & 0xFF
                    if shift_state & 1:
                        win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
                        _is_shift_held = True
                    win32api.keybd_event(virtual_key, 0, 0, 0)
                    if is_last_key:
                        _last_target_key = virtual_key
                if format and not is_last_key:
                    time.sleep(wait)

        @staticmethod
        def stop(key_string: str = None):
            System.keys.release()

        @staticmethod
        def hold(key_string: str, format=False, wait=0, long=0):
            time.sleep(0.5)
            System.keys.start(key_string, format=format, wait=wait)
            time.sleep(long)
            System.keys.release()

        @staticmethod
        def release():
            global _is_shift_held, _last_target_key
            if _last_target_key is not None:
                win32api.keybd_event(_last_target_key, 0, win32con.KEYEVENTF_KEYUP, 0)
                _last_target_key = None
            if _is_shift_held:
                win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
                _is_shift_held = False
            while _pressed_modifiers:
                mod_key = _pressed_modifiers.pop()
                win32api.keybd_event(mod_key, 0, win32con.KEYEVENTF_KEYUP, 0)

        @staticmethod
        def English():
            time.sleep(0.08)
            System.keys.key('ctrl-space')
            time.sleep(0.08)

    class mouse:
        @staticmethod
        def mouse(dx=0, dy=0):
            inp = INPUT()
            inp.type = 0
            inp.ii.mi.dx = dx
            inp.ii.mi.dy = dy
            inp.ii.mi.dwFlags = 0x0001
            inp.ii.mi.mouseData = 0
            inp.ii.mi.time = 0
            inp.ii.mi.dwExtraInfo = 0
            result = ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))
            if result == 0:
                print(f"[警告] SendInput 失败！请确保以 Administrtor 运行 Python ! ")
            return result

        @staticmethod
        def move(x=None, y=None, duration=0.5):
            if x is None:
                x = infomation['screen_w'] // 2
            if y is None:
                y = infomation['screen_h'] // 2
            start_x, start_y = win32api.GetCursorPos()
            distance = math.hypot(x - start_x, y - start_y)
            if distance < 10:
                win32api.SetCursorPos((x, y))
                return
            steps = max(int(distance / 5), 20)
            step_delay = duration / steps
            offset_scale = distance * 0.3
            ctrl_x = (start_x + x) / 2 + random.uniform(-offset_scale, offset_scale)
            ctrl_y = (start_y + y) / 2 + random.uniform(-offset_scale, offset_scale)
            for step in range(steps + 1):
                t = step / steps
                ease_t = 1 - (1 - t) ** 3
                inv_t = 1 - ease_t
                current_x = int(inv_t ** 2 * start_x + 2 * inv_t * ease_t * ctrl_x + ease_t ** 2 * x)
                current_y = int(inv_t ** 2 * start_y + 2 * inv_t * ease_t * ctrl_y + ease_t ** 2 * y)
                win32api.SetCursorPos((current_x, current_y))
                time.sleep(step_delay)

        @staticmethod
        def left(num=1, wait=0.1):
            for _ in range(num):
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                if wait > 0:
                    time.sleep(wait)

        @staticmethod
        def long(mouse='left', long=1):
            time.sleep(0.02)
            if mouse == 'left':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                time.sleep(long)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            elif mouse == 'right':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                time.sleep(long)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

        @staticmethod
        def right(num=1, wait=0.1):
            for _ in range(num):
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                if wait > 0:
                    time.sleep(wait)

        @staticmethod
        def middle():
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

        @staticmethod
        def num(direction='down', lines=3, wait=0):
            delta = 120 if direction.lower() == 'up' else -120
            for _ in range(lines):
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, delta, 0)
                time.sleep(wait)

class debug:
    @staticmethod
    def direction():
        time.sleep(3)
        start_x, start_y = win32api.GetCursorPos()
        return [start_x, start_y]

    @staticmethod
    def end():
        time.sleep(0.02)

class window:
    @staticmethod
    def Adaptation_DPI_Hight():
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()

    @staticmethod
    def password(one=True, Error=None, bind='Enter', cnt=0, title='Enter the password', show="·", sure="Next",
                 font=('Arial', 14), width=10, text="Please enter the password :", geometry="350x150", password='123',
                 yes=None, no=None):
        if Error is None:
            Error = ['Error', 'Warning to much.\n   Try Faild.']
        if yes is None:
            yes = ['Success', '     Correct password ! 😊      ']
        if no is None:
            no = ['Error', 'Incorrect password. Please try again!']
        result = None

        def check_password(event=None):
            nonlocal cnt, password_entry, result
            user_input = lock.Hash.bit(text=password_entry.get(), mode=['256 bit'])
            correct_password = lock.Hash.bit(text=password, mode=['256 bit'])
            if user_input == correct_password:
                root.destroy()
                messagebox.showinfo(yes[0], yes[1])
                result = True
            else:
                cnt += 1
                if cnt < 3:
                    messagebox.showwarning(no[0], no[1])
                    password_entry.delete(0, tk.END)
                else:
                    root.destroy()
                    messagebox.showerror(Error[0], Error[1])
                    result = False

        root = tk.Tk()
        try:
            real_width = user32.GetSystemMetrics(0)
            logical_width = root.winfo_screenwidth()
            dpi_scale = real_width / logical_width
        except Exception:
            dpi_scale = 1.0
        root.attributes('-topmost', one)
        root.title(title)
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        geo_w = round(int(geometry.split('x')[0]) * dpi_scale)
        geo_h = round(int(geometry.split('x')[1]) * dpi_scale)
        root.geometry(f"{geo_w}x{geo_h}+{(screen_w - geo_w) // 2}+{(screen_h - geo_h) // 2}")
        root.resizable(False, False)
        label = tk.Label(root, text=text, font=("Arial", int(12 * dpi_scale)))
        label.pack(pady=10)
        password_entry = tk.Entry(root, show=show, font=(font[0], int(font[1] * dpi_scale)), width=20)
        password_entry.pack(pady=5)
        button = tk.Button(root, text=sure, command=check_password,
                           font=(font[0], int((font[1] - 2) * dpi_scale)), width=int(width * dpi_scale))
        button.pack(pady=10)
        if bind == 'Enter':
            bind = 'Return'
        root.bind(f'<{bind}>', lambda e: check_password())
        root.mainloop()
        return result

    @staticmethod
    def up(Window=''):
        windows_list = gw.getWindowsWithTitle(Window)
        if not windows_list:
            raise SyntaxWarning(f"No Window named '{Window}'.")
        win = windows_list[0]
        if win.isMinimized:
            win.restore()
        win.activate()
        return True

    @staticmethod
    def groud(Window):
        hwnd = win32gui.FindWindow(None, Window)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        time.sleep(0.1)
        window.up(Window=Window)

    @staticmethod
    def notwindow(title="Windows", text="Tips", do=None, x=500, y=200):
        if do is None:
            do = lambda: print('hello word.')
        root = tk.Tk()
        root.title(title)
        root.geometry(f"{x}x{y}+{infomation['screen_w'] // 2 - x // 2}+{infomation['screen_h'] // 2 - y // 2}")
        root.update_idletasks()
        Hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongPtrW(Hwnd, GWL_STYLE)
        new_style = style & ~WS_SYSMENU
        ctypes.windll.user32.SetWindowLongPtrW(Hwnd, GWL_STYLE, new_style)
        ctypes.windll.user32.SetWindowPos(Hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_FRAMECHANGED)
        tk.Label(root, text=text, font=("Microsoft YaHei", 12)).pack(pady=50)
        do()
        root.after(500, root.destroy)
        root.mainloop()

class file:
    @staticmethod
    def startup(path):
        os.startfile(path)

    @staticmethod
    def delete(path):
        try:
            shutil.rmtree(path)
        except NotADirectoryError:
            os.remove(path)
        except Exception:
            raise FileNotFoundError()

    @staticmethod
    def copy(file_path, dir_path):
        shutil.copy2(file_path, dir_path)

    @staticmethod
    def listdir(path=r'C:\\'):
        result = []
        for root, dirs, files in os.walk(path):
            for f in files:
                result.append(os.path.join(root, f))
        return result

    @staticmethod
    def deletes(paths=None):
        if paths is None:
            return
        for i in paths:
            if isinstance(i, list):
                for j in i:
                    file.delete(path=j)
            else:
                file.delete(path=i)

    @staticmethod
    def user():
        return os.path.expanduser('~')

    @staticmethod
    def Find(filename=None, findpath=None, filesnumer=None):
        numer = 0
        returnpath = None
        if filename is None:
            raise SyntaxWarning('Please provide the \'filename\' for WalkUp Studios')
        if filesnumer is None:
            filesnumer = 10000000

        def _is_safe_name(name):
            if len(name) > 150:
                return False
            if not re.match(r'^[\w\u4e00-\u9fa5\s.\-]+$', name):
                return False
            return True

        def _search_in_path(path):
            nonlocal numer, returnpath
            try:
                for root, dirs, files in os.walk(path):
                    if numer >= filesnumer:
                        break
                    dirs[:] = [d for d in dirs if _is_safe_name(d)]
                    if filename in dirs:
                        returnpath = os.path.join(root, filename)
                        return True
                    if filename in files:
                        returnpath = os.path.join(root, filename)
                        return True
                    numer += 1
            except PermissionError:
                pass
            return False

        if findpath is None:
            if hasattr(os, 'listdrives'):
                drives = os.listdrives()
            else:
                drives = [f"{chr(d)}:\\" for d in range(65, 91) if os.path.exists(f"{chr(d)}:\\")]
            for drive in drives:
                if _search_in_path(drive):
                    break
        else:
            _search_in_path(findpath)
        return returnpath

    @staticmethod
    def temp():
        return os.environ.get('TEMP')

class date:
    @staticmethod
    def now():
        s = datetime.now()
        when = f'[{s.hour}:{s.minute}:{s.second}]'
        return when

    @staticmethod
    def hour():
        return datetime.now().hour

    @staticmethod
    def minute():
        return datetime.now().minute

    @staticmethod
    def second():
        return datetime.now().second

class mpv:
    class mp3:
        @staticmethod
        async def generate_audio(path=file.user(), name='temp', text='此音频由 edge‑tts 库生成', voice='女-普通',
                                speed='+0%', volumed='+0%'):
            using_voice = voices.get(voice, 'zh‑CN‑YunxiNeural')
            out_file = os.path.join(path, f'{name}.mp3')
            await edge_tts.Communicate(text, using_voice, rate=speed, volume=volumed).save(out_file)
            return out_file

        @staticmethod
        def casting(path=file.user(), name='temp', text='此音频由 edge‑tts 库生成', voice='女-普通', speed='+0%',
                    volumed='+0%'):
            def _run_async():
                asyncio.run(mpv.mp3.generate_audio(path, name, text, voice, speed, volumed))

            t = threading.Thread(target=_run_async)
            t.start()

        @staticmethod
        def music(MusicPath):
            def _play():
                try:
                    playsound.playsound(MusicPath)
                except Exception as e:
                    print(f"播放出错: {e}")

            t = threading.Thread(target=_play)
            t.daemon = True
            t.start()

        @staticmethod
        def take(paths=file.user(), names='temp', texts='此音频由 edge‑tts 库生成', voices='女-普通', speeds='+0%',
                 volumeds='+0%'):
            def _task():
                asyncio.run(mpv.mp3.generate_audio(paths, names, texts, voices, speeds, volumeds))
                full_path = os.path.join(paths, f'{names}.mp3')
                mpv.mp3.music(full_path)
                if os.path.exists(full_path):
                    os.remove(full_path)

            t = threading.Thread(target=_task)
            t.start()

        @staticmethod
        def temp(paths=file.user(), name='temp', text='此音频由 edge‑tts 库生成', voice='女-普通', speed='+0%',
                 volumed='+0%'):
            def _task():
                asyncio.run(mpv.mp3.generate_audio(path=paths, name=name, text=text, voice=voice, speed=speed,
                                                   volumed=volumed))
                full_path = os.path.join(paths, f'{name}.mp3')
                try:
                    playsound.playsound(full_path)
                except Exception as e:
                    print(f"播放出错: {e}")
                if os.path.exists(full_path):
                    os.remove(full_path)

            t = threading.Thread(target=_task)
            t.start()

    class mp4:
        @staticmethod
        def show(path=None, title='mp4', arrow='none', bgcolor='black', one=False, first=False, maximization=True,
                 width=750, hight=440):
            if path:
                root = tk.Tk()
                root.bind('<Escape>', lambda event: root.destroy())
                root.geometry(f"{width}x{hight}+{root.winfo_screenwidth() // 2 - width // 2}+{root.winfo_screenheight() // 2 - hight // 2}")
                root.update()
                time.sleep(0.3)
                root.title(title)
                root.config(cursor=arrow)

                def ones():
                    root.state('zoomed')
                    root.update()
                    root.attributes('-fullscreen', one)

                if one:
                    ones()
                root.attributes('-topmost', first)
                root.resizable(maximization, maximization)
                frame = tk.Frame(root, bg=bgcolor)
                frame.config(cursor=arrow)
                frame.pack(fill=tk.BOTH, expand=True)
                instance = vlc.Instance('--avcodec‑hw=any')
                player = instance.media_player_new()
                player.set_hwnd(frame.winfo_id())
                player.set_media(instance.media_new(path))
                player.play()
                root.mainloop()
            else:
                for _ in range(3):
                    messagebox.showwarning('<<!cnm!>>', '             喂！              ')
                for _ in range(5):
                    messagebox.showwarning('<<!cnm!>>', '🤬老子的视频呢？？？🤬')

class Terminal:
    try:
        import curses
        _stdscr = curses.initscr()
        import atexit
        atexit.register(curses.endwin)
    except Exception:
        curses = None
        _stdscr = None
    _line_lengths = {}
    lines = 0
    cleanf = {}

    class output:
        def __init__(self, text, y=None, x=0, end=True):
            if Terminal._stdscr is None:
                print(text)
                return
            Terminal.lines += 1
            Terminal.cleanf[Terminal.lines] = len(text)
            max_y, max_x = Terminal._stdscr.getmaxyx()
            if y is None:
                y, _ = Terminal._stdscr.getyx()
            y = max(0, min(y, max_y - 1))
            x = max(0, min(x, max_x - 1))
            Terminal._stdscr.move(y, x)
            Terminal._stdscr.addstr(str(text))
            Terminal._stdscr.clrtoeol()
            if end:
                Terminal._stdscr.addstr('\n')
            Terminal._stdscr.refresh()
            Terminal._line_lengths[y] = len(str(text))
            final_y, _ = Terminal._stdscr.getyx()
            if final_y >= max_y - 1:
                Terminal._stdscr.move(max_y - 1, 0)
                Terminal._stdscr.refresh()

    class line:
        def __init__(self, y=None, x=0):
            if Terminal._stdscr is None:
                return
            if y is None:
                y, _ = Terminal._stdscr.getyx()
            Terminal._stdscr.move(y, x)
            Terminal._stdscr.clrtoeol()
            Terminal._stdscr.addstr('\n')
            Terminal._stdscr.refresh()

    class clean:
        def __init__(self, line=None):
            if Terminal._stdscr is None:
                return
            sy, _ = Terminal._stdscr.getyx()
            y = line if line is not None else sy
            y -= 1
            max_y, _ = Terminal._stdscr.getmaxyx()
            y = min(max(y, 0), max_y - 1)
            Terminal._stdscr.move(y, 0)
            Terminal._stdscr.clrtoeol()
            Terminal._stdscr.refresh()
            Terminal.cleanf[line] = 0

    @staticmethod
    def put(prompt='', y=None, x=0, max_len=50):
        if Terminal._stdscr is None:
            return input(prompt)
        Terminal.lines += 1
        Terminal.cleanf[Terminal.lines] = len(prompt)
        if y is None:
            y, _ = Terminal._stdscr.getyx()
        Terminal._stdscr.move(y, x)
        Terminal._stdscr.addstr(prompt)
        Terminal._stdscr.refresh()
        Terminal.curses.echo()
        result = Terminal._stdscr.getstr(y, x + len(prompt), max_len)
        Terminal.curses.noecho()
        return result.decode('utf‑8')

    class outs:
        def __init__(self, text, y=None, x=0, end=True):
            if Terminal._stdscr is None:
                print(text)
                return
            max_y, max_x = Terminal._stdscr.getmaxyx()
            Terminal.lines += 1
            Terminal.cleanf[Terminal.lines] = len(text)
            if y is None:
                y, _ = Terminal._stdscr.getyx()
            y = max(0, min(y, max_y - 1))
            x = max(0, min(x, max_x - 1))
            Terminal._stdscr.move(y, x)
            text_str = str(text)
            for i in text_str:
                cur_y, cur_x = Terminal._stdscr.getyx()
                if cur_x >= max_x - 1:
                    if cur_y < max_y - 1:
                        Terminal._stdscr.move(cur_y + 1, 0)
                    else:
                        break
                Terminal._stdscr.addstr(i)
                if end:
                    Terminal._stdscr.addstr('\n')
                Terminal._stdscr.refresh()
                time.sleep(0.02)
            final_y, _ = Terminal._stdscr.getyx()
            if final_y < max_y - 1:
                Terminal._stdscr.move(final_y + 1, 0)
            Terminal._stdscr.clrtoeol()
            Terminal._stdscr.refresh()

    class cleans:
        def __init__(self, line=None):
            if Terminal._stdscr is None:
                return
            sy, _ = Terminal._stdscr.getyx()
            y = line if line is not None else sy
            y -= 1
            max_y, max_x = Terminal._stdscr.getmaxyx()
            y = min(max(y, 0), max_y - 1)
            n = Terminal._line_lengths.get(y, max_x - 1)
            Terminal._stdscr.move(y, 0)
            Terminal._stdscr.refresh()
            for x in range(n):
                Terminal._stdscr.move(y, x)
                Terminal._stdscr.addstr(' ')
                Terminal._stdscr.refresh()
                time.sleep(0.05)
            Terminal._stdscr.move(y, 0)
            Terminal._stdscr.clrtoeol()
            Terminal._stdscr.refresh()

    class move:
        def __init__(self, y, x=None):
            if Terminal._stdscr is None:
                return
            max_y, max_x = Terminal._stdscr.getmaxyx()
            y = min(max(y, 0), max_y - 1) - 1
            if x is None:
                x = 0
            x = min(max(x, 0), max_x - 1)
            Terminal._stdscr.move(y, x)
            Terminal._stdscr.refresh()

class AI:
    @staticmethod
    def ask(message, AI_Model='qwen2:latest'):
        result = ''
        for chunk in ollama.chat(model=AI_Model, messages=[{'role': 'user', 'content': message}], stream=True):
            result += str(chunk['message']['content'])
        return result