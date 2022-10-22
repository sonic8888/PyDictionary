import PySide6
from PySide6 import QtCore
from PySide6.QtCore import QSize, QRect, Qt
from PySide6.QtGui import QPalette, QColor, QAction, QIcon
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QToolBar, QListWidget, QListView, \
    QLineEdit
from Models.WordsModel import Words
from Servise.Db.Sqlite.SqliteApplication import select_data

import main
from Servise.Variable import minSizeWindow, maxSizeWindow


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


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

        self.layoutH = QHBoxLayout()
        self.layoutH_V = QVBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.textChanged.connect(self.textChanged)
        self.layoutH_V.addWidget(self.lineEdit)

        self.listW = QListView()
        self.model = Words()
        self.load()

        self.listW.setModel(self.model)
        self.layoutH_V.addWidget(self.listW)
        # self.listW.addItems(["One", "Two", "Three"])
        self.leftWidget = QWidget()
        self.leftWidget.setLayout(self.layoutH_V)
        self.layoutH.addWidget(self.leftWidget, stretch=1)
        self.layoutH.addWidget(Color('green'), stretch=2)

        widget = QWidget()
        widget.setLayout(self.layoutH)
        self.setCentralWidget(widget)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent):
        if not self.windowParent.isVisible():
            self.windowParent.show()

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def load(self):
        self.model.words = select_data(self)

    def textChanged(self, s):
        self.model.words = select_data(self, 1, s)
        self.model.layoutChanged.emit()
