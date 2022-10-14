import sys

from PySide6.QtCore import QRect
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QMainWindow


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class HomeWindows(QMainWindow):
    def __init__(self, sizeWindow):
        super(HomeWindows, self).__init__()
        self.setWindowTitle("Home")
        self.size = QRect(0, 0, sizeWindow[0], sizeWindow[1])
        self.setGeometry(self.size)
        widget = QWidget()
        self.setCentralWidget(widget)