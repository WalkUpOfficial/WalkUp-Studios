import sys
import json
from PyQt6.QtWidgets import QApplication, QLabel, QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer
import System32

def show_cake(scale):
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(System32.file.Self_dir() + "\\cake.png"))

    icon_dll_path = System32.file.Self_dir() + "\\icon.dll"
    with open(icon_dll_path, "r", encoding="utf-8") as f:
        icon_cfg = json.load(f)
    img_path = System32.file.Self_dir() + "\\" + icon_cfg["cake"]

    anim_dll_path = System32.file.Self_dir() + "\\animation.dll"
    with open(anim_dll_path, "r", encoding="utf-8") as f:
        anim_cfg = json.load(f)

    overshoot_px = anim_cfg["cake"]["B"]["num"]
    total_dur_ms = int(anim_cfg["after"]["cake"] * 1000)
    main_exit_sec = anim_cfg["main_exit_time"]
    fade_duration_ms = 1000

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
    win_rect = label.frameGeometry()
    win_rect.moveCenter(screen_rect.center())
    target_pos = QPoint(win_rect.topLeft().x(), win_rect.topLeft().y())
    start_pos = QPoint(target_pos.x(), -label.height())

    label.move(start_pos)
    label.show()
    app.processEvents()

    anim = QPropertyAnimation(label, b"pos", parent=label)
    anim.setDuration(total_dur_ms)
    anim.setStartValue(start_pos)
    anim.setEndValue(target_pos)

    ec = QEasingCurve(QEasingCurve.Type.OutBack)
    ec.setAmplitude(overshoot_px / 40)
    anim.setEasingCurve(ec)

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

    def on_anim_finished():
        QTimer.singleShot(int(main_exit_sec * 1000), start_fade)

    anim.finished.connect(on_anim_finished)
    anim.start()

    sys.exit(app.exec())

if __name__ == "__main__":
    show_cake(0.6)