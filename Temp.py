# from PyQt6.QtWidgets import QApplication, QWidget
# from PyQt6.QtGui import QPainter, QColor, QPen, QConicalGradient
# from PyQt6.QtCore import Qt, QTimer, QRectF
# import sys

def run_spinner():
    app = QApplication(sys.argv)
    rot_angle = 0

    def paint_func(widget, event):
        nonlocal rot_angle
        p = QPainter(widget)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = widget.width()
        h = widget.height()
        cx, cy = w / 2, h / 2
        r = min(w, h) / 2 - 24

        p.fillRect(widget.rect(), QColor(15,15,18))
        grad = QConicalGradient(cx, cy, rot_angle)
        grad.setColorAt(0.0, QColor(255,255,255,0))
        grad.setColorAt(0.18, QColor(255,255,255,255))
        grad.setColorAt(0.36, QColor(255,255,255,0))
        pen = QPen()
        pen.setBrush(grad)
        pen.setWidth(8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        rect = QRectF(cx - r, cy - r, r*2, r*2)
        p.drawArc(rect, int(rot_angle*16), int(120*16))

    win = QWidget()
    win.setWindowTitle("Steam 原版启动转圈")
    win.resize(420, 420)

    timer = QTimer()
    def animate():
        nonlocal rot_angle
        rot_angle += 1.0
        if rot_angle >= 360:
            rot_angle = 0
        win.update()
    timer.timeout.connect(animate)
    timer.start(0)

    # 重写paintEvent
    old_paint = win.paintEvent
    def new_paint(event):
        paint_func(win, event)
    win.paintEvent = new_paint

    win.show()
    sys.exit(app.exec())

# if __name__ == "__main__":
#     run_spinner()

import tkinter as tk
import math
import OpenGL_Base


if __name__ == "__main__":
    run_spinner()