import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
import System32

exit_time = 16  # 等待时长(秒)
fade_duration = 1000  # 渐变1秒完成

class BlackWindow(QWidget):
    def __init__(self, state_file):
        super().__init__()
        self.state_file = state_file
        self.is_exiting = False

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: #000000;")
        screen = QApplication.primaryScreen()
        self.setGeometry(screen.geometry())
        self.setWindowOpacity(1.0)

        # 淡出动画，1秒结束
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(fade_duration)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.on_anim_end)

        # 等待倒计时，到点自动开始淡出
        self.wait_timer = QTimer()
        self.wait_timer.setInterval(exit_time * 1000)
        self.wait_timer.setSingleShot(True)
        self.wait_timer.timeout.connect(self.start_exit_gradient)
        self.wait_timer.start()

    def start_exit_gradient(self):
        if self.is_exiting:
            return
        self.is_exiting = True
        with open(self.state_file, "w", encoding="utf-8") as f:
            f.write("exit")
        self.anim.start()

    def on_anim_end(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            f.write("false")
        self.hide()

def show_black_screen():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(System32.file.Self_dir() + "plate.png"))
    state_file = System32.file.Self_dir() + "state.dll"
    w = BlackWindow(state_file)
    w.show()
    w.raise_()
    sys.exit(app.exec())

if __name__ == "__main__":
    show_black_screen()
