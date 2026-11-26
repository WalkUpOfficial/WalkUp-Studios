import sys
import math
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QColor, QBrush, QPen, QPainter
from PyQt6.QtCore import Qt, QTimer, QPoint
import System32


def heart_points(count, scale):
    pts = []
    for i in range(count):
        t = (i / count) * 2 * math.pi
        x = 16 * (math.sin(t) ** 3)
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        x *= scale
        y *= scale
        pts.append((x, y))
    return pts


class BlessWindow(QWidget):
    def __init__(self, text, pos):
        super().__init__()
        self.text = text
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)

        self.resize(180, 42)
        self.move(pos)

        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            color: #c84268;
            font-size: 14px;
            background-color: transparent;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor(255, 182, 193)))
        painter.setPen(QPen(QColor(255, 105, 135), 2))
        painter.drawRoundedRect(rect, 10, 10)
        inner_rect = rect.adjusted(2, 2, -2, -2)
        painter.setBrush(QBrush(QColor(255, 240, 245)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(inner_rect, 8, 8)


def show_love_heart():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)

    anim_cfg_path = System32.file.Self_dir() + "\\animation.dll"
    with open(anim_cfg_path, "r", encoding="utf-8") as f:
        anim_cfg = json.load(f)
    bless_cfg = anim_cfg["blesses"]
    zoom = bless_cfg["zoom"]
    spawn_delay = bless_cfg["during time"]
    point_count = bless_cfg["num"]
    exit_wait = bless_cfg["wait time of the exit"]

    bless_path = System32.file.Self_dir() + "\\blesses.dll"
    with open(bless_path, "r", encoding="utf-8") as f:
        bless_list = [line.strip() for line in f.readlines() if line.strip()]

    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    cx = rect.center().x()
    cy = rect.center().y()

    point_list = heart_points(point_count, zoom)
    win_list = []

    def spawn_one(idx=0):
        if idx >= len(point_list):
            # 全部窗口生成完毕，开始倒计时退出
            QTimer.singleShot(int(exit_wait * 1000), on_all_exit)
            return
        dx, dy = point_list[idx]
        px = int(cx + dx)
        py = int(cy + dy)
        txt = bless_list[idx % len(bless_list)]
        w = BlessWindow(txt, QPoint(px, py))
        win_list.append(w)
        QTimer.singleShot(int(spawn_delay * 1000), lambda: spawn_one(idx + 1))

    def on_all_exit():
        for w in win_list: w.close();System32.time.sleep(0.01)
        app.quit()

    QTimer.singleShot(100, spawn_one)
    sys.exit(app.exec())


if __name__ == "__main__":
    show_love_heart()
