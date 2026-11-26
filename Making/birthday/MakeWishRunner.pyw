import sys
import json
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtGui import QFont, QFontMetrics, QTransform, QPainter, QColor
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, pyqtProperty, QParallelAnimationGroup
import System32


class ScaleLabel(QLabel):
    def __init__(self, text, text_color="#ffffff", parent=None):
        super().__init__(text, parent)
        self._scale = 1.0
        self.text_color = text_color
        self.edge_color = self._darker_color(text_color)

    def _darker_color(self, color_hex):
        c = QColor(color_hex)
        h, s, l, a = c.getHsl()
        l = max(0, l - 25)
        return QColor.fromHsl(h, s, l, a)

    @pyqtProperty(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val):
        self._scale = val
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        t = QTransform()
        t.translate(self.width() / 2, self.height() / 2)
        t.scale(self._scale, self._scale)
        t.translate(-self.width() / 2, -self.height() / 2)
        painter.setTransform(t)

        font = self.font()
        metrics = QFontMetrics(font)
        text = self.text()
        rect = metrics.boundingRect(text)

        x = (self.width() - rect.width()) / 2 - rect.left()
        y = (self.height() - rect.height()) / 2 - rect.top()

        painter.setFont(font)
        painter.setPen(self.edge_color)
        offset = max(1, int(self._scale * 1.2))
        for dx in (-offset, 0, offset):
            for dy in (-offset, 0, offset):
                if dx != 0 or dy != 0:
                    # 转int，解决float报错
                    painter.drawText(int(x + dx), int(y + dy), text)

        painter.setPen(QColor(self.text_color))
        painter.drawText(int(x), int(y), text)


class CharWindow(QWidget):
    def __init__(self, char, target_pos, anim_type, speed, start_zoom, end_zoom, font_size, text_color="#ffffff"):
        super().__init__()
        self.anim_type = anim_type
        self.speed = speed
        self.start_zoom = start_zoom
        self.end_zoom = end_zoom
        self.target_pos = target_pos
        self.anim_in = None
        self.anim_out = None
        self.exit_anim_type = None

        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)

        self.label = ScaleLabel(char, text_color=text_color, parent=self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("background: transparent;")

        self.op_effect = QGraphicsOpacityEffect()
        self.op_effect.setOpacity(1.0)
        self.label.setGraphicsEffect(self.op_effect)

        f = QFont()
        f.setPointSize(font_size)
        f.setBold(True)
        self.label.setFont(f)

        metrics = QFontMetrics(f)
        rect = metrics.boundingRect(char)
        text_w = rect.width()
        text_h = rect.height()

        self.orig_w = max(text_w, text_h) + 20
        self.orig_h = self.orig_w
        self.resize(self.orig_w, self.orig_h)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        self.scr = self.screen().availableGeometry()
        tx, ty = self.target_pos.x(), self.target_pos.y()
        if self.anim_type == "up_to_down_with_shake":
            self.start_center = QPoint(tx, -80)
        elif self.anim_type == "down_to_up_with_zoom":
            self.start_center = QPoint(tx, self.scr.height() + 80)
        elif self.anim_type == "left_to_right":
            self.start_center = QPoint(-80, ty)
        elif self.anim_type == "right_to_down":
            self.start_center = QPoint(self.scr.width() + 80, -80)
        else:
            self.start_center = self.target_pos

        self.moveCenter(self.start_center)
        self.hide()

        self._win_scale = 1.0

    @pyqtProperty(float)
    def win_scale(self):
        return self._win_scale

    @win_scale.setter
    def win_scale(self, val):
        self._win_scale = val
        center = self.frameGeometry().center()
        new_w = int(self.orig_w * val)
        new_h = int(self.orig_h * val)
        self.resize(new_w, new_h)
        self.moveCenter(center)
        self.label.scale = val

    def moveCenter(self, pos):
        geo = self.frameGeometry()
        geo.moveCenter(pos)
        self.move(geo.topLeft())

    def start_anim(self):
        self.show()
        dur = int(self.speed * 1000)
        self.anim_in = QPropertyAnimation(self, b"pos")
        self.anim_in.setStartValue(self.pos())
        self.moveCenter(self.target_pos)
        self.anim_in.setEndValue(self.pos())
        self.anim_in.setDuration(dur)
        self.anim_in.setEasingCurve(QEasingCurve.Type.OutBack)

        self.anim_op_in = QPropertyAnimation(self.op_effect, b"opacity")
        self.anim_op_in.setStartValue(self.start_zoom)
        self.anim_op_in.setEndValue(self.end_zoom)
        self.anim_op_in.setDuration(dur)

        self.anim_in.start()
        self.anim_op_in.start()

    def get_exit_center(self, anim_t):
        tx, ty = self.target_pos.x(), self.target_pos.y()
        if anim_t == "up_to_down_with_shake":
            return QPoint(tx, -80)
        elif anim_t == "down_to_up_with_zoom":
            return QPoint(tx, self.scr.height() + 80)
        elif anim_t == "left_to_right":
            return QPoint(-80, ty)
        elif anim_t == "right_to_down":
            return QPoint(self.scr.width() + 80, -80)
        return self.target_pos

    def start_exit_anim(self, exit_mode, all_anim_list):
        if exit_mode == "Auto":
            self.exit_anim_type = self.anim_type
        elif exit_mode == "random":
            self.exit_anim_type = random.choice(all_anim_list)
        elif exit_mode == "exit":
            dur = int(self.speed * 1000)
            self.anim_out_op = QPropertyAnimation(self.op_effect, b"opacity")
            self.anim_out_op.setStartValue(1.0)
            self.anim_out_op.setEndValue(0.0)
            self.anim_out_op.setDuration(dur)

            self.anim_out_scale = QPropertyAnimation(self, b"win_scale")
            self.anim_out_scale.setStartValue(1.0)
            self.anim_out_scale.setEndValue(2.0)
            self.anim_out_scale.setDuration(dur)
            self.anim_out_scale.setEasingCurve(QEasingCurve.Type.OutCubic)

            self.anim_out_group = QParallelAnimationGroup()
            self.anim_out_group.addAnimation(self.anim_out_op)
            self.anim_out_group.addAnimation(self.anim_out_scale)
            self.anim_out_group.finished.connect(self.close)
            self.anim_out_group.start()
            return

        exit_center = self.get_exit_center(self.exit_anim_type)
        self.anim_out = QPropertyAnimation(self, b"pos")
        self.anim_out.setStartValue(self.pos())
        self.moveCenter(exit_center)
        self.anim_out.setEndValue(self.pos())
        self.anim_out.setDuration(int(self.speed * 1000))
        self.anim_out.setEasingCurve(QEasingCurve.Type.InBack)

        self.anim_op_out = QPropertyAnimation(self.op_effect, b"opacity")
        self.anim_op_out.setStartValue(1.0)
        self.anim_op_out.setEndValue(0.0)
        self.anim_op_out.setDuration(int(self.speed * 1000))

        self.anim_out_group = QParallelAnimationGroup()
        self.anim_out_group.addAnimation(self.anim_out)
        self.anim_out_group.addAnimation(self.anim_op_out)
        self.anim_out_group.finished.connect(self.close)
        self.anim_out_group.start()


def show_make_wish():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    cfg_path = System32.file.Self_dir() + "\\animation.dll"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    wish_cfg = cfg["MakeWish"]
    text = wish_cfg["text"]
    font_size = wish_cfg["text_zoom"]
    display_mode = wish_cfg["display"]
    display_time = wish_cfg["display_time"]
    distance = wish_cfg["distance"]
    exit_time = wish_cfg["exit_time"]
    exit_displays = wish_cfg["exit_displays"]
    disp_cfg = wish_cfg["displays"]
    anim_keys = list(disp_cfg.keys())
    text_color_raw = wish_cfg.get("text_color", "#ffffff")
    color_map = {
        "pink": "#ff88bb",
        "red": "#ff4444",
        "white": "#ffffff",
        "yellow": "#ffdd44",
        "green": "#44dd66",
        "blue": "#4499ff"
    }
    text_color = color_map.get(text_color_raw.lower(), text_color_raw)

    scr_rect = app.primaryScreen().availableGeometry()
    cx = scr_rect.center().x()
    cy = scr_rect.center().y()

    char_list = list(text)
    count = len(char_list)

    if count <= 1:
        spacing = 0
    else:
        if str(distance).lower() == "auto":
            spacing = scr_rect.width() * 0.4 / (count - 1)
        else:
            spacing = float(distance)

    total_width = spacing * (count - 1)
    start_x = cx - total_width / 2

    char_win_list = []
    for i, ch in enumerate(char_list):
        anim_name = random.choice(anim_keys)
        p = disp_cfg[anim_name]

        target_x = int(start_x + i * spacing)
        target_y = int(cy)

        w = CharWindow(
            char=ch,
            target_pos=QPoint(target_x, target_y),
            anim_type=anim_name,
            speed=p.get("speed", 1),
            start_zoom=p.get("start_zoom", 0.2),
            end_zoom=p.get("zoom", 1),
            font_size=font_size,
            text_color=text_color
        )
        char_win_list.append(w)

    if display_mode == "and":
        for w in char_win_list:
            w.start_anim()
        QTimer.singleShot(int(exit_time * 1000), lambda: [w.start_exit_anim(exit_displays, anim_keys) for w in char_win_list])
    elif display_mode == "one":
        interval_ms = int(display_time * 1000)
        for idx, w in enumerate(char_win_list):
            QTimer.singleShot(idx * interval_ms, w.start_anim)
        last_delay = int(((count - 1) * display_time + exit_time) * 1000)
        QTimer.singleShot(last_delay, lambda: [w.start_exit_anim(exit_displays, anim_keys) for w in char_win_list])

    sys.exit(app.exec())


if __name__ == "__main__":
    show_make_wish()