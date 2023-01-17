import re
import logging
from audioplayer import AudioPlayer
from PySide6 import QtWidgets
from os import path
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from Servise.sound import get_word_sound
from Servise.tools import request, Settings, insert_data, copy_file, display_error, \
    createTextHtmlTranslate, createTextHtmlExamples, play_sound
from Views.Generate.windowtr import Ui_MainWindow

current_word = None
current_audio = ''
audioplayer = None

logging_yandex_translate = logging.getLogger(__name__)
logging_yandex_translate.setLevel(logging.INFO)
_handler = logging.FileHandler(f'logs\\{__name__}.log', mode='w')
_formatter = logging.Formatter("%(name)s %(lineno)d %(asctime)s %(levelname)s %(message)s")
_handler.setFormatter(_formatter)
logging_yandex_translate.addHandler(_handler)


def init_current_audio(path_audio):
    global current_audio
    current_audio = path_audio


def button_action():
    play_sound(current_audio)


class YandexTranslateWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, geometryWindow):
        super(YandexTranslateWindow, self).__init__()
        self.current_response = None
        self.settings = Settings()
        self.setupUi(self)
        self.setGeometry(geometryWindow)
        self.lineEdit.editingFinished.connect(self.edit_finish)
        self.pushButton.clicked.connect(button_action)
        self.pushButton_2.clicked.connect(self.button_click_save_db)
        # self.pushButton_4.clicked.connect(self.update())
        self.lineEdit.setFocus()

    def edit_finish(self):
        global current_word
        text = self.lineEdit.text()
        text = text.strip()
        current_word = text
        self.get_date(text, self.settings.folder_id, self.settings.iam_token)

    def button_click_save_db(self):
        if self.current_response:
            insert_data(self.current_response, self.settings.name_db)
            copy_file(current_audio, self.settings.path_name_audio_storage)

    def get_date(self, word, folder_id, iam_token):
        global current_audio
        response = request(word)
        if response:
            current_audio = get_word_sound(word, folder_id, iam_token)
        if response:
            self.current_response = response
            data = response.json()
            list_data = data['def']
            if list_data:
                dict_html_tra = createTextHtmlTranslate(list_data)
                examples_html = createTextHtmlExamples(list_data)
                self.textEdit_2.setHtml(dict_html_tra['html'])
                self.lineEdit_2.setText(dict_html_tra['tr'])
                self.textEdit.setHtml(examples_html)
        return response
