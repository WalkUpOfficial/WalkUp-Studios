import sys
import json
from PyQt6.QtWidgets import QApplication, QLabel, QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap, QIcon
import System32
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QSequentialAnimationGroup, QPauseAnimation, QTimer

def show_image_no_window(scale):
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(System32.file.Self_dir() + "\\plate.png"))

    icon_dll_path = System32.file.Self_dir() + "\\icon.dll"
    with open(icon_dll_path, "r", encoding="utf-8") as f:
        icon_cfg = json.load(f)
    img_path = System32.file.Self_dir() + "\\" + icon_cfg["plate"]

    anim_dll_path = System32.file.Self_dir() + "\\animation.dll"
    with open(anim_dll_path, "r", encoding="utf-8") as f:
        anim_cfg = json.load(f)

    overshoot_px = anim_cfg["plate"]["B"]["num"]
    total_dur_ms = int(anim_cfg["after"]["plate"] * 1000)
    shake_amp_start = anim_cfg["plate"]["D"]["num"]
    shake_amp_end = anim_cfg["plate"]["D"]["end"]
    shake_dur_ms = int(anim_cfg["plate"]["D"]["end during time"] * 1000)
    wait_before_step2_ms = int(anim_cfg["plate"]["wait times"]["2"] * 1000)
    main_exit_sec = anim_cfg["main_exit_time"]
    fade_duration_ms = 1000

    xy_cfg = anim_cfg["plate"]["total xy"]
    pix = QPixmap(img_path)
    if pix.isNull():
        print(f"❌ 图片加载失败！路径：{img_path}")
        return
    new_w = int(pix.width() * scale)
    new_h = int(pix.height() * scale)
    pix_scaled = pix.scaled(
        new_w,
        new_h,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )

    label = QLabel()
    label.setPixmap(pix_scaled)
    label.resize(pix_scaled.size())

    label.setWindowFlags(
        Qt.WindowType.Window
        | Qt.WindowType.FramelessWindowHint
        | Qt.WindowType.WindowStaysOnTopHint
    )
    label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    # 保留 QGraphicsOpacityEffect
    opacity_effect = QGraphicsOpacityEffect(label)
    opacity_effect.setOpacity(1.0)
    label.setGraphicsEffect(opacity_effect)

    screen_rect = app.primaryScreen().availableGeometry()
    base_x = screen_rect.center().x() - new_w // 2
    base_y = screen_rect.center().y() - new_h // 2

    x_raw = xy_cfg["x"]
    if x_raw == "Auto":
        target_x = base_x
    elif isinstance(x_raw, str) and ("+" in x_raw or "-" in x_raw):
        op = "+" if "+" in x_raw else "-"
        val = int(x_raw.split(op)[-1])
        target_x = base_x + val if op == "+" else base_x - val
    else:
        target_x = int(x_raw)

    y_raw = xy_cfg["y"]
    if y_raw == "Auto":
        target_y = base_y
    elif isinstance(y_raw, str) and ("+" in y_raw or "-" in y_raw):
        op = "+" if "+" in y_raw else "-"
        val = int(y_raw.split(op)[-1])
        target_y = base_y + val if op == "+" else base_y - val
    else:
        target_y = int(y_raw)

    target_pos = QPoint(target_x, target_y)
    start_pos = QPoint(-label.width(), target_pos.y())

    label.move(start_pos)
    label.show()
    app.processEvents()

    anim_main = QPropertyAnimation(label, b"pos", parent=label)
    anim_main.setDuration(total_dur_ms)
    anim_main.setStartValue(start_pos)
    anim_main.setEndValue(target_pos)
    ec = QEasingCurve(QEasingCurve.Type.OutBack)
    ec.setAmplitude(overshoot_px / 40)
    anim_main.setEasingCurve(ec)

    anim_shake = QPropertyAnimation(label, b"pos", parent=label)
    anim_shake.setDuration(shake_dur_ms)
    anim_shake.setKeyValueAt(0.0, QPoint(target_pos.x(), target_pos.y()))
    anim_shake.setKeyValueAt(0.4, QPoint(target_pos.x(), target_pos.y() + int(shake_amp_start)))
    anim_shake.setKeyValueAt(1.0, QPoint(target_pos.x(), target_pos.y() + int(shake_amp_end)))
    anim_shake.setEasingCurve(QEasingCurve.Type.OutQuad)

    seq_group = QSequentialAnimationGroup(parent=label)
    seq_group.addAnimation(anim_main)
    seq_group.addPause(wait_before_step2_ms)
    seq_group.addAnimation(anim_shake)

    def start_fade():
        fade_anim = QPropertyAnimation(opacity_effect, b"opacity", parent=label)
        fade_anim.setDuration(fade_duration_ms)
        fade_anim.setStartValue(1.0)
        fade_anim.setEndValue(0.0)
        def fade_done():
            label.close()
            app.quit()
        fade_anim.finished.connect(fade_done)
        fade_anim.start()

    def on_seq_finished():
        QTimer.singleShot(int(main_exit_sec * 1000), start_fade)

    seq_group.finished.connect(on_seq_finished)
    seq_group.start()

    sys.exit(app.exec())

if __name__ == "__main__":
    show_image_no_window(0.6)
