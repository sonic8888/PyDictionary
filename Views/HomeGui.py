import sys

from PySide6.QtCore import QRect, QSize
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton

minSizeButton = QSize(100, 40)
maxSizeButton = QSize(200, 40)
maxSizeWindow = 1.4
minSizeWindow = 0.8


class Button(QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()
        self.setMaximumSize(minSizeButton)
        self.setMaximumSize(maxSizeButton)
        self.setText(text)


class HomeWindows(QMainWindow):
    def __init__(self, sizeWindow):
        super(HomeWindows, self).__init__()
        self.setWindowTitle("Home")
        self.size = QRect(0, 0, sizeWindow[0], sizeWindow[1])
        minSize = QSize(int(sizeWindow[0] * minSizeWindow), int(sizeWindow[1] * minSizeWindow))
        maxSize = QSize(int(sizeWindow[0] * maxSizeWindow), int(sizeWindow[1] * maxSizeWindow))
        self.setMinimumSize(minSize)
        self.setMaximumSize(maxSize)
        self.setGeometry(self.size)
        buttonOne = Button('One')
        buttonTwo = Button('Two')
        buttonThree = Button('Three')

        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()

        layoutH.addWidget(QWidget())
        layoutH.addWidget(buttonOne)
        layoutH.addWidget(buttonTwo)
        layoutH.addWidget(buttonThree)
        layoutH.addWidget(QWidget())
        # layoutH.setContentsMargins(40, 10, 40, 10)
        layoutH.setSpacing(40)
        layoutV.addWidget(QWidget())
        layoutV.addLayout(layoutH)
        layoutV.addWidget(QWidget())
        layoutV.addWidget(QWidget())
        widget = QWidget()
        widget.setLayout(layoutV)
        self.setCentralWidget(widget)
