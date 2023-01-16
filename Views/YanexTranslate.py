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


# def wrapperHTML(teg, text, style_color=None, style_margin=None):
#     if not text:
#         return text
#     _html_teg = f'<{teg}>{text}</{teg}>'
#     if style_color and style_margin:
#         _html_teg = f"<{teg} style='color:{style_color};{style_margin}'>{text}</{teg}>"
#     elif style_margin:
#         _html_teg = f"<{teg} style='{style_margin}'>{text}</{teg}>"
#     elif style_color:
#         _html_teg = f"<{teg} style='color:{style_color}'>{text}</{teg}>"
#     return _html_teg
#
#
# def wrapperHTML_recursive(text, list_teg, style=None):
#     if len(list_teg) == 1:
#         t = list_teg[0]
#         return wrapperHTML(t, text, style_color=style)
#     else:
#         t = list_teg.pop()
#         return f'<{t}>{wrapperHTML_recursive(text, list_teg, style)}</{t}>'
#
#
# def wrapperHTML_dictionary_recursive(dictionary, list_teg, dictLabel):
#     settings = Settings()
#     current_theme = settings.current_theme
#     if len(list_teg) == 1:
#         t = list_teg[0]
#         _html_teg = ''
#         space = ''
#         for key in dictLabel:
#             color_name = dictLabel[key]
#             if not key in dictionary:
#                 continue
#             text = dictionary[key]
#             _html = wrapperHTML(t, text, style_color=current_theme[color_name])
#             _html_teg += space + _html
#             space = " "
#         return _html_teg
#     else:
#         t = list_teg.pop()
#         return f'<{t}>{wrapperHTML_dictionary_recursive(dictionary, list_teg, dictLabel)}</{t}>'
#
#
# def createTextHtmlTranslate(list_article):
#     dict_label = {'text': 'secondaryTextColor', 'ts': 'secondaryLightColor', 'pos': 'secondaryTextColor'}
#     dict_mean = {'text': 'secondaryTextColor'}
#     dict_translate = {'text': 'primaryColor', 'gen': 'secondaryTextColor'}
#     result = {'html': '', 'tr': ''}
#     html = ''
#     result['tr'] = list_article[0]['tr'][0]['text']
#     for item in list_article:
#         html_block_label = wrapperHTML_dictionary_recursive(item, ['span', 'h3'], dict_label)
#         summa_li = ''
#         for item_tr in item['tr']:
#             html_block_translate = wrapperHTML_dictionary_recursive(item_tr, ['span', 'span'], dict_translate)
#             html_syn = ''
#             for item_syn in item_tr.get('syn', []):
#                 html_s = wrapperHTML_dictionary_recursive(item_syn, ['span', 'span'], dict_translate)
#                 spase = ',   '
#                 html_syn += spase + html_s
#             html_block_translate = wrapperHTML('p', html_block_translate + html_syn)
#             html_mean = ''
#             spase = ''
#             for item_mean in item_tr.get('mean', []):
#                 html_m = wrapperHTML_dictionary_recursive(item_mean, ['span'], dict_mean)
#                 html_mean += spase + html_m
#                 spase = ',   '
#             html_mean = wrapperHTML('p', html_mean)
#             translate_mean = html_block_translate + html_mean
#             translate_mean = wrapperHTML('li', translate_mean)
#             summa_li += translate_mean
#         html_block_ol = wrapperHTML('ol', summa_li)
#         html += html_block_label + html_block_ol
#     result['html'] = html
#     return result
#
#
# def createTextHtmlExamples(list_article):
#     dict_label = {'text': 'primaryColor', 'pos': 'secondaryLightColor'}
#     dict_select = {'text': 'secondaryTextColor', 'select': 'primaryColor'}
#     html = ''
#     for item in list_article:
#         html_block_label = wrapperHTML_dictionary_recursive(item, ['span', 'h3'], dict_label)
#         current_text = item['text']
#         current_translate_list = []
#         html += html_block_label
#         for item_tr in item.get('tr', []):
#             current_translate_list.append(item_tr['text'])
#             for syn in item_tr.get('syn', []):
#                 current_translate_list.append(syn['text'])
#             for item_ex in item_tr.get('ex', []):
#                 sours_text_example = item_ex['text']
#                 for item_text_tr in item_ex.get('tr', []):
#                     translate_text_example = item_text_tr['text']
#                     html_example = wrapperHTML_example(sours_text_example, translate_text_example, current_text,
#                                                        current_translate_list, dict_select)
#                     html += html_example
#     return html
#
#
# def wrapperHTML_example(source_example, translate_example, source_word, list_translates, dictionary_color):
#     match_ex = None
#     settings = Settings()
#     current_theme = settings.current_theme
#     for item in list_translates:
#         match_ex = isMath(translate_example, item)
#         if match_ex:
#             translate_html = wrapperHTML('span', match_ex[0], style_color=current_theme[dictionary_color['select']])
#
#             translate_example = translate_example.replace(match_ex[0], translate_html)
#
#             break
#     match_word = isMath(source_example, source_word)
#     if match_word:
#         source_word = match_word[0]
#     source_word_html = wrapperHTML('span', source_word, style_color=current_theme[dictionary_color['select']])
#     source_example = source_example.replace(source_word, source_word_html)
#     text_example = source_example + ' — ' + translate_example
#     return wrapperHTML('p', text_example,
#                        style_color=current_theme[dictionary_color['text']],
#                        style_margin="margin-left:20px")
#
#
# def isMath(text, word):
#     count = 0
#     if len(word) > 4:
#         count = 1
#     if len(word) > 7:
#         count = 2
#     pattern = '\\b' + word[:len(word) - count] + '?\\S*\\b'
#     if len(word) <= 2:
#         pattern = '\\b' + word + '\\b'
#     return re.search(pattern, text)


def init_current_audio(path_audio):
    global current_audio
    current_audio = path_audio


# def create_audioplayer():
#     global audioplayer
#     audioplayer = QMediaPlayer()
#     audioOutput = QAudioOutput()
#     audioplayer.setAudioOutput(audioOutput)


class YandexTranslateWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, geometryWindow):
        super(YandexTranslateWindow, self).__init__()
        self.current_response = None
        self.settings = Settings()
        self.setupUi(self)
        self.setGeometry(geometryWindow)
        self.lineEdit.editingFinished.connect(self.edit_finish)
        self.pushButton.clicked.connect(self.button_action)
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

    def button_action(self):
        play_sound(current_audio)

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
