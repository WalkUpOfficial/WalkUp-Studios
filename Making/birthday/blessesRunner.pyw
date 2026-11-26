import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import System32
import json

class BlessSingleWindow(QWidget):
    def __init__(self, text, x, y, cfg):
        super().__init__()
        self.resize(cfg["window_width"], cfg["window_height"])
        self.setWindowTitle("Blesses")
        self.move(x, y)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.label = QLabel(text, self)
        self.label.setFont(QFont("Microsoft YaHei", cfg["font_size"]))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.resize(self.size())

def main():
    app = QApplication(sys.argv)
    animation_cfg_path = System32.file.Self_dir() + "\\animation.dll"
    with open(animation_cfg_path, "r", encoding="utf-8") as f:
        animation_data = json.load(f)
    cfg = animation_data["blesseser"]
    wait_seconds = cfg["wait_for_exit"]

    bless_text_path = System32.file.Self_dir() + "\\blesses.dll"
    with open(bless_text_path, "r", encoding="utf-8") as f:
        line_list = [line.strip() for line in f.read().split("\n") if line.strip()]

    used_texts = []
    window_list = []
    screen = app.primaryScreen()
    scr_w, scr_h = screen.geometry().width(), screen.geometry().height()

    spawn_timer = QTimer()
    destroy_timer = QTimer()
    destroy_timer.setSingleShot(True)

    def spawn_one():
        if len(used_texts) >= len(line_list) or len(window_list) >= cfg["max_count"]:
            spawn_timer.stop()
            destroy_timer.start(int(wait_seconds * 1000))
            return
        available = [txt for txt in line_list if txt not in used_texts]
        selected = random.choice(available)
        used_texts.append(selected)

        max_x = scr_w - cfg["window_width"] * 1.5
        max_y = scr_h - cfg["window_height"] * 1.5
        rand_x = random.randint(0, int(max_x))
        rand_y = random.randint(0, int(max_y))

        win = BlessSingleWindow(selected, rand_x, rand_y, cfg,)
        win.show()
        win.raise_()
        window_list.append(win)

    def destroy_all():
        for w in window_list:
            w.close()

    spawn_timer.timeout.connect(spawn_one)
    spawn_timer.start(cfg["interval_ms"])
    destroy_timer.timeout.connect(destroy_all)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()