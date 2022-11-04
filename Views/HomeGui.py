import PySide6
from PySide6.QtCore import QSize, SIGNAL
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QToolBar, QMessageBox
from Servise.Variable import minSizeWindow
from Views.Buttons import Button
from Views.DictionaryGui import DictionaryWindow
from main import create_icon


class HomeWindows(QMainWindow):
    """
    Начальное окно приложения
    """

    def __init__(self, geometryWindow):
        super(HomeWindows, self).__init__()
        self.geometryWindow = geometryWindow
        self.windowDictionary = None
        self.setWindowTitle("Home")
        self.name = 'HomeWindows'
        self.setGeometry(self.geometryWindow)
        minSize = QSize(int(geometryWindow.width() * minSizeWindow), int(geometryWindow.height() * minSizeWindow))

        self.setMinimumSize(minSize)

        #  toolbar
        toolbar = QToolBar("My main toolbar")

        #  button
        self.buttonOne = Button('словарь')
        self.buttonOne.clicked.connect(self.open_window_dictionary)
        self.buttonTwo = Button('тренировка')
        self.buttonTwo.clicked.connect(self.buttonTwo_clicked)
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
        _icon_settings = create_icon('settings')
        # QAction
        button_action = QAction(_icon_settings, "Your button", self)

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

    def open_window_dictionary(self, s):
        if self.windowDictionary:
            self.windowDictionary.show()
            self.hide()
        else:
            self.windowDictionary = DictionaryWindow(self.geometryWindow, self)
            self.windowDictionary.show()
            self.hide()

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent):
        print("closeEvent")

    def buttonTwo_clicked(self):
        pass

    def mousePressEvent(self, e):
        print("ggggg")

    def delete(self):
        self.windowDictionary = None
