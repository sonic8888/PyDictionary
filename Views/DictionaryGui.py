import PySide6
from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QPalette, QColor, QAction, QIcon
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QToolBar

import main
from Servise.Variable import minSizeWindow, maxSizeWindow


class DictionaryWindow(QMainWindow):
    def __init__(self, geometryWindow, widowParent):
        super(DictionaryWindow, self).__init__()
        self.setWindowTitle("Dictionary")
        self.geometryWindow = geometryWindow
        self.setGeometry(self.geometryWindow)
        self.windowParent = widowParent
        self.name = 'DictionaryWindow'
        minSize = QSize(int(geometryWindow.width() * minSizeWindow), int(geometryWindow.height() * minSizeWindow))
        self.setMinimumSize(minSize)
        self.toolbar = QToolBar("toolbar")
        self.addToolBar(self.toolbar)
        # QAction
        button_action = QAction(QIcon('Icons/home_white.png'), "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        self.toolbar.addAction(button_action)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent):
        if not self.windowParent.isVisible():
            self.windowParent.show()

    def onMyToolBarButtonClick(self, s):
        print("click", s)
