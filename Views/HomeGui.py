import sys

from PySide6.QtCore import QRect, QSize
from PySide6.QtGui import QPalette, QColor, QAction, QIcon
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QToolBar

from Servise.Variable import minSizeButton, maxSizeButton, maxSizeWindow, minSizeWindow
from Views.Buttons import Button


class HomeWindows(QMainWindow):
    def __init__(self, sizeWindow):
        super(HomeWindows, self).__init__()
        self.setWindowTitle("Home")
        self.size = QRect(0, 0, sizeWindow[0], sizeWindow[1])
        minSize = QSize(int(sizeWindow[0] * minSizeWindow), int(sizeWindow[1] * minSizeWindow))
        maxSize = QSize(int(sizeWindow[0] * maxSizeWindow), int(sizeWindow[1] * maxSizeWindow))
        self.setMinimumSize(minSize)
        # self.setMaximumSize(maxSize)
        self.setGeometry(self.size)

        #  toolbar
        toolbar = QToolBar("My main toolbar")

        #  button
        self.buttonOne = Button('словарь')
        self.buttonTwo = Button('тренировка')
        self.buttonThree = Button('задание')

        # layout
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()

        # icon
        dicIcon = QIcon('Icons/accessories-dictionary.ico')

        # menu
        menu = self.menuBar()

        # central widget
        widget = QWidget()

        # QAction
        button_action = QAction("Your button", self)

        # layout add widget
        layoutH.addWidget(QWidget())
        layoutH.addWidget(self.buttonOne)
        layoutH.addWidget(self.buttonTwo)
        layoutH.addWidget(self.buttonThree)
        layoutH.addWidget(QWidget())
        layoutH.setSpacing(40)
        layoutV.addWidget(QWidget())
        layoutV.addLayout(layoutH)
        layoutV.addWidget(QWidget())
        layoutV.addWidget(QWidget())

        widget.setLayout(layoutV)

        file_menu = menu.addMenu("&File")
        self.addToolBar(toolbar)
        self.setCentralWidget(widget)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(button_action)
        self.setWindowIcon(dicIcon)
        file_menu.addAction(button_action)

    def onMyToolBarButtonClick(self, s):
        print("click", s)
