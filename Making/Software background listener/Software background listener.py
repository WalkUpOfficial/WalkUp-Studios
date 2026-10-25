from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import QTimer, Qt
import sys
import os
import json
import System32

window_main_title = '总控台'
window_main_resize = [1000, 600]
error_title = '错误'

def GetConfig():
    global window_main_title, window_main_resize
    try:
        cfg_path = os.path.dirname(System32.file.Self()) + r'\window_com.json'
        with open(cfg_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        window_main_title = config['Main']['Title']
        window_main_resize = [config['Main']['resize_x'], config['Main']['resize_y']]
    except Exception as e:
        QMessageBox.critical(None, error_title,
            f'无法获取配置文件\n将使用默认配置 !\n错误代码 : {e}\n'
            '如果需要修复，请在 https://github.com/WalkUpOfficial/Release-Warehouse/issues 里报告信息，谢谢您的配合！')

GetConfig()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        root = QWidget()
        root.setWindowTitle(window_main_title)
        root.resize(window_main_resize[0], window_main_resize[1])

        root.setCursor(QCursor(QPixmap(r"E:\文件\图片\自用\退出.png")))

        root.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        err_info = traceback.format_exc()
        QMessageBox.critical(None, error_title, f"异常：{e}\n\n堆栈  : \n{err_info}")