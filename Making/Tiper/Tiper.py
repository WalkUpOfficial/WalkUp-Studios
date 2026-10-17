import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

app = QApplication(sys.argv)
window = QWidget()
window.resize(300,150)

font = QFont()
font.setPointSize(18)

label = QLabel("Hello PyQt6", parent=window)
label.setFont(font)
label.setAlignment(Qt.AlignmentFlag.AlignCenter)

window.show()
sys.exit(app.exec())