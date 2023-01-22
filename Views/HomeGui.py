import PySide6
import logging
from PySide6.QtCore import QSize, SIGNAL
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QToolBar, QPushButton

from Views.YanexTranslate import YandexTranslateWindow
from Servise.tools import create_style, clear_folder_temp, Settings, display_error
from Views.Window_show_db import WindowDb
from Views.Window_list_word import WindowList

logging_home = logging.getLogger(__name__)
logging_home.setLevel(logging.INFO)
_handler = logging.FileHandler(f'logs\\{__name__}.log', mode='w')
_formatter = logging.Formatter("%(name)s %(lineno)d %(asctime)s %(levelname)s %(message)s")
_handler.setFormatter(_formatter)
logging_home.addHandler(_handler)


class HomeWindows(QMainWindow):
    """
    Начальное окно приложения
    """

    def __init__(self, geometryWindow):
        super(HomeWindows, self).__init__()
        self.geometryWindow = geometryWindow
        self.window_db = None
        self.window_list_word = None
        self.yandex_translate_window = None
        self.setWindowTitle("Home")
        self.name = 'HomeWindows'
        self.setGeometry(self.geometryWindow)
        self.settings = Settings()

        #  toolbar
        toolbar = QToolBar("My main toolbar")

        #  button
        self.buttonOne = QPushButton('словарь')
        self.buttonOne.clicked.connect(self.open_window_list_word)
        self.buttonTwo = QPushButton('тренировка')
        self.buttonTwo.clicked.connect(self.open_window_show_db)
        self.buttonThree = QPushButton('задание')
        self.buttonThree.clicked.connect(self.open_window_yandex_translate)

        # layout
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()

        # icon
        dicIcon = QIcon('Icons/accessories-dictionary.ico')

        # menu
        menu = self.menuBar()

        # central widget
        widget = QWidget()

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

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def open_window_dictionary(self, s):
        pass

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent):
        clear_folder_temp(self.settings.path_name_audio_temp)
        print("closeEvent")

    # def open_window_show_db(self):
    #     if self.window_db:
    #         self.window_db.show()
    #         self.hide()
    #     else:
    #         self.window_db = WindowDb(self.geometryWindow)
    #         s = Settings()
    #
    #         try:
    #             font_line = s.settings['FONT_SIZE']['QLineEdit']
    #             font_text = s.settings['FONT_SIZE']['QTextEdit']
    #             font_label = s.settings['FONT_SIZE']['QLabel']
    #         except KeyError as k:
    #             display_error('не удалось установить размер шрифта')
    #             logging_home.exception('не удалось установить размер шрифта', k)
    #             font_line = '9px'
    #             font_text = '9px'
    #             font_label = '9px'
    #         style = create_style(QLineEdit=('font-size', font_line), QTextEdit=('font-size', font_text),
    #                              QLabel=('font-size', font_label))
    #         self.window_db.setStyleSheet(style)
    #         self.window_db.show()
    #         self.hide()

    def open_window_yandex_translate(self):
        s = Settings()

        try:
            font_line = s.settings['FONT_SIZE']['QLineEdit']
            font_text = s.settings['FONT_SIZE']['QTextEdit']
        except KeyError as k:
            display_error('не удалось установить размер шрифта')
            logging_home.exception('не удалось установить размер шрифта', k)
            font_line = '9px'
            font_text = '9px'
        style = create_style(QLineEdit=('font-size', font_line), QTextEdit=('font-size', font_text))
        self.open_window(self.yandex_translate_window, 'window_yandex_translate', style)

    def open_window_list_word(self):
        self.open_window(self.window_list_word, 'window_list_word')

    def create_windows(self, name_window_class):
        match name_window_class:
            case 'window_show_db':
                return WindowDb(self.geometryWindow, self)
            case 'window_yandex_translate':
                return YandexTranslateWindow(self.geometryWindow, self)
            case 'window_list_word':
                return WindowList(self.geometryWindow, self)
            case _:
                return None

    def open_window(self, window_variable, name_window_class, style_window=None):
        if window_variable:
            window_variable.show()
            self.hide()
        else:
            window_variable = self.create_windows(name_window_class)
            window_variable.setStyleSheet(style_window)
            window_variable.show()
            self.hide()

    def open_window_show_db(self):
        s = Settings()
        try:
            font_line = s.settings['FONT_SIZE']['QLineEdit']
            font_text = s.settings['FONT_SIZE']['QTextEdit']
        except KeyError as k:
            display_error('не удалось установить размер шрифта')
            logging_home.exception('не удалось установить размер шрифта', k)
            font_line = '9px'
            font_text = '9px'
        style = create_style(QLineEdit=('font-size', font_line), QTextEdit=('font-size', font_text))
        self.open_window(self.window_db, 'window_show_db', style)

    def mousePressEvent(self, e):
        print("ggggg")

    def delete(self):
        pass
