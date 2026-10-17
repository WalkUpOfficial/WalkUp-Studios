from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import os
from tkinter import messagebox
import json
import System32

window_main_title = '总控台'

try:
    with open(os.path.dirname(System32.file.Self())+r'\window_com.json', "r", encoding="utf-8") as f:
        config = json.load(f)
    window_main_title = config['Main']['Title']
except:
    messagebox.showwarning(title='错误', message=f'      无法获取配置文件        \n      将使用默认配置 !      \n        错误代码 : {Exception}     \n如果需要修复，请在 https://github.com/WalkUpOfficial/Release-Warehouse/issues 里报告信息，谢谢您的配合！')

try:
    app = QApplication(sys.argv)
    root = QWidget()
    root.setWindowTitle(window_main_title)

    root.show()

    sys.exit(app.exec())
except Exception:
    messagebox.showwarning(title='')