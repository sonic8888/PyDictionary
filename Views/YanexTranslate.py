import re
import sys
from audioplayer import AudioPlayer
from PySide6 import QtWidgets
from os import path
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import qt_material
from qt_material import apply_stylesheet

from Servise.sound import get_word_sound
from Servise.tools import *
from Views.windowtr import Ui_MainWindow
from settings import Settings

current_word = None
current_audio = ''
audioplayer = None


def wrapperHTML(teg, text, style_color=None, style_margin=None):
    if not text:
        return text
    _html_teg = f'<{teg}>{text}</{teg}>'
    if style_color and style_margin:
        _html_teg = f"<{teg} style='color:{style_color};{style_margin}'>{text}</{teg}>"
    elif style_margin:
        _html_teg = f"<{teg} style='{style_margin}'>{text}</{teg}>"
    elif style_color:
        _html_teg = f"<{teg} style='color:{style_color}'>{text}</{teg}>"
    return _html_teg


def wrapperHTML_recursive(text, list_teg, style=None):
    if len(list_teg) == 1:
        t = list_teg[0]
        return wrapperHTML(t, text, style_color=style)
    else:
        t = list_teg.pop()
        return f'<{t}>{wrapperHTML_recursive(text, list_teg, style)}</{t}>'


def wrapperHTML_dictionary_recursive(dictionary, list_teg, dictLabel):
    settings = Settings()
    current_theme = settings.current_theme
    if len(list_teg) == 1:
        t = list_teg[0]
        _html_teg = ''
        space = ''
        for key in dictLabel:
            color_name = dictLabel[key]
            if not key in dictionary:
                continue
            text = dictionary[key]
            _html = wrapperHTML(t, text, style_color=current_theme[color_name])
            _html_teg += space + _html
            space = " "
        return _html_teg
    else:
        t = list_teg.pop()
        return f'<{t}>{wrapperHTML_dictionary_recursive(dictionary, list_teg, dictLabel)}</{t}>'


def createTextHtmlTranslate(list_article):
    dict_label = {'text': 'secondaryTextColor', 'ts': 'secondaryLightColor', 'pos': 'secondaryTextColor'}
    dict_mean = {'text': 'secondaryTextColor'}
    dict_translate = {'text': 'primaryColor', 'gen': 'secondaryTextColor'}
    result = {'html': '', 'tr': ''}
    html = ''
    result['tr'] = list_article[0]['tr'][0]['text']
    for item in list_article:
        html_block_label = wrapperHTML_dictionary_recursive(item, ['span', 'h3'], dict_label)
        summa_li = ''
        for item_tr in item['tr']:
            html_block_translate = wrapperHTML_dictionary_recursive(item_tr, ['span', 'span'], dict_translate)
            html_syn = ''
            for item_syn in item_tr.get('syn', []):
                html_s = wrapperHTML_dictionary_recursive(item_syn, ['span', 'span'], dict_translate)
                spase = ',   '
                html_syn += spase + html_s
            html_block_translate = wrapperHTML('p', html_block_translate + html_syn)
            html_mean = ''
            spase = ''
            for item_mean in item_tr.get('mean', []):
                html_m = wrapperHTML_dictionary_recursive(item_mean, ['span'], dict_mean)
                html_mean += spase + html_m
                spase = ',   '
            html_mean = wrapperHTML('p', html_mean)
            translate_mean = html_block_translate + html_mean
            translate_mean = wrapperHTML('li', translate_mean)
            summa_li += translate_mean
        html_block_ol = wrapperHTML('ol', summa_li)
        html += html_block_label + html_block_ol
    result['html'] = html
    return result


def createTextHtmlExamples(list_article):
    dict_label = {'text': 'primaryColor', 'pos': 'secondaryLightColor'}
    dict_select = {'text': 'secondaryTextColor', 'select': 'primaryColor'}
    html = ''
    for item in list_article:
        html_block_label = wrapperHTML_dictionary_recursive(item, ['span', 'h3'], dict_label)
        current_text = item['text']
        current_translate_list = []
        html += html_block_label
        for item_tr in item.get('tr', []):
            current_translate_list.append(item_tr['text'])
            for syn in item_tr.get('syn', []):
                current_translate_list.append(syn['text'])
            for item_ex in item_tr.get('ex', []):
                sours_text_example = item_ex['text']
                for item_text_tr in item_ex.get('tr', []):
                    translate_text_example = item_text_tr['text']
                    html_example = wrapperHTML_example(sours_text_example, translate_text_example, current_text,
                                                       current_translate_list, dict_select)
                    html += html_example
    return html


def wrapperHTML_example(source_example, translate_example, source_word, list_translates, dictionary_color):
    match_ex = None
    settings = Settings()
    current_theme = settings.current_theme
    for item in list_translates:
        match_ex = isMath(translate_example, item)
        if match_ex:
            translate_html = wrapperHTML('span', match_ex[0], style_color=current_theme[dictionary_color['select']])

            translate_example = translate_example.replace(match_ex[0], translate_html)

            break
    # print(source_example, '--', translate_example, ' ', source_word, ' ', match_ex[0])
    match_word = isMath(source_example, source_word)
    if match_word:
        source_word = match_word[0]
    source_word_html = wrapperHTML('span', source_word, style_color=current_theme[dictionary_color['select']])
    source_example = source_example.replace(source_word, source_word_html)
    text_example = source_example + ' — ' + translate_example
    # print(source_example, '--', translate_example, ' ', source_word, ' ', match_ex[0])
    return wrapperHTML('p', text_example,
                       style_color=current_theme[dictionary_color['text']],
                       style_margin="margin-left:20px")


def isMath(text, word):
    count = 0
    if len(word) > 4:
        count = 1
    if len(word) > 7:
        count = 2
    pattern = '\\b' + word[:len(word) - count] + '?\\S*\\b'
    if len(word) <= 2:
        pattern = '\\b' + word + '\\b'
    return re.search(pattern, text)


def init_current_audio(path_audio):
    global current_audio
    current_audio = path_audio


def create_audioplayer():
    global audioplayer
    audioplayer = QMediaPlayer()
    audioOutput = QAudioOutput()
    audioplayer.setAudioOutput(audioOutput)


class YandexTranslateWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, geometryWindow):
        super(YandexTranslateWindow, self).__init__()
        self.settings = Settings()
        self.setupUi(self)
        self.setGeometry(geometryWindow)
        self.lineEdit.editingFinished.connect(self.edit_finish)
        self.pushButton.clicked.connect(self.button_action)
        self.pushButton_2.clicked.connect(self.button_test)
        self.lineEdit.setFocus()



    def edit_finish(self):
        global current_word
        text = self.lineEdit.text()
        text = text.strip()
        current_word = text
        self.get_date(text, self.settings.folder_id, self.settings.iam_token)
        # get_word_sound(text, FOLDER_ID, OAUTH_TOKEN)

    def button_test(self):
        pass

    def button_action(self):
        path_file = path.abspath(current_audio)
        player = AudioPlayer(path_file).play(block=True)

    def get_date(self, word, folder_id, iam_token):
        global current_audio
        response = request(word)
        if response:
            current_audio = get_word_sound(word, folder_id, iam_token)
        if response:
            data = response.json()
            list_data = data['def']
            if list_data:
                dict_html_tra = createTextHtmlTranslate(list_data)
                examples_html = createTextHtmlExamples(list_data)
                self.textEdit_2.setHtml(dict_html_tra['html'])
                self.lineEdit_2.setText(dict_html_tra['tr'])
                self.textEdit.setHtml(examples_html)
        return response

    # player = QMediaPlayer()

# audioOutput = QAudioOutput()
# player.setAudioOutput(audioOutput)
# sours = QUrl.fromLocalFile(r'D:\Documents\PythonProjects\TestListWidget\file.mp3')
# print(sours)
# player.setSource(sours)
# audioOutput.setVolume(90)
# player.play()


# def main():
#     global FOLDER_ID, OAUTH_TOKEN, IAM_TOKEN
#
#
#
#     data_settings = read_file_json(PATH_SETTINGS)
#     font_size = data_settings.get("FONT_SIZE", {})
#     FOLDER_ID = data_settings.get("FOLDER_ID", None)
#     OAUTH_TOKEN = data_settings.get("OAUTH_TOKEN", None)
#     path_iam_token = data_settings.get('PATH_NAME_IAM_TOKEN', '')
#     IAM_TOKEN = read_file_json(path_iam_token, 'iamToken')
#     # current_audio = get_word_sound('addition', FOLDER_ID, OAUTH_TOKEN)
#     app = QtWidgets.QApplication(sys.argv)
#     window = YandexTranslateWindow()
#     apply_stylesheet(app, theme=current_theme_name)
#     window.setStyleSheet(f"QLineEdit {{ font-size: {font_size.get('QLineEdit', '9')}px }} QTextEdit {{font-size:"
#                          f" {font_size.get('QTextEdit', '9')}px}}")
#     window.show()
#     app.exec()
#
#
# if __name__ == '__main__':
#     current_theme = qt_material.get_theme(current_theme_name)
#     if current_theme:
#         main()
