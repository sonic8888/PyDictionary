import datetime
import json
from datetime import datetime
from enum import Enum
from settings import Settings
import PySide6
import requests
from PySide6.QtWidgets import QLabel


class EnumError(Enum):
    ERR_OK = 200
    ERR_KEY_INVALID = 401
    ERR_KEY_BLOCKED = 402
    ERR_DAILY_REQ_LIMIT_EXCEEDED = 403
    ERR_TEXT_TOO_LONG = 413
    ERR_LANG_NOT_SUPPORTED = 501


dict_key_errors = {
    200: 'Операция выполнена успешно.',
    401: 'Ключ API невалиден.',
    402: 'Ключ API заблокирован.',
    403: 'Превышено суточное ограничение на количество запросов.',
    413: 'Превышен максимальный размер текста.',
    501: 'Заданное направление перевода не поддерживается.'
}


class Label(QLabel):
    def __init__(self, word, gen=None, parent=None, color_text='rgba(222, 190, 73, 1)',
                 color_gender='rgba(255, 255, 255, 0.5)', back_color='rgba(222, 190, 73, 0.1)',
                 padding='4', hover_back_color='rgba(222, 190, 73, 0.3)', font_size='12'):
        super().__init__(parent)
        self._word = word
        self._gen = gen
        self._color_gender = color_gender
        self._color_text = color_text
        self._styleSheet = '''Label {background-color: %s; padding: %spx; font-size: %spx }
                              :hover {background-color: %s; padding: %spx;}''' % (
            back_color, padding, font_size, hover_back_color, padding)
        self.setText(self.setHTML())

        self.setStyleSheet(self._styleSheet)

    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        print(self._word)

    def setHTML(self):
        _text = ''
        if self._gen:
            _text = f"<p style='color:{self._color_text}'>{self._word} <span style='color:{self._color_gender}'>" \
                    f"{self._gen}</span></p>"
        else:
            _text = f"<p style='color:{self._color_text}'>{self._word}</p>"
        return _text


def request(word):
    _def = None
    param = {"key": 'dict.1.1.20221117T140505Z.c922e22b66033b98.85efa77b962fdd9f7de016d41321213dcbd4af7d',
             "lang": 'en-ru', 'text': word, 'ui': 'ru', 'flags': 0x0002 | 0x0008}
    response = requests.get('https://dictionary.yandex.net/api/v1/dicservice.json/lookup', params=param)
    _code = response.status_code
    if _code == 200:
        return response
    else:
        return None


def sound_request(word):
    token = 't1.9euelZqel5yPnJmYzZnJy5qVm8bPzu3rnpWampWXl4qXipiPiomUzpCSlInl8_ceJzRi-e8nG2Iv_t3z915VMWL57ycbYi_' \
            '-zef1656VmpGJnJqRx5mbmpqels2Rxp7K7_0.y0olE9ArTdI3scPL00PN64T7d_fsug82GT-fI3humJesXvqjchrZp' \
            '-BuAluPGyLqardGXTbImiWPEaoB_A-fCg'
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    param = {'text': word, 'lang': 'en-EN', 'folderId': 'b1g6omcgou764fnj6h2r', 'format': 'lpcm',
             'sampleRateHertz': 48000}
    response = requests.post(url='https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=headers,
                             params=param)
    _code = response.status_code
    print(_code)


def writeFile(response, pathname):
    s = json.dumps(response.json(), indent=4, sort_keys=True, ensure_ascii=False)
    with open(pathname, "w", encoding='utf-8') as file:
        file.write(s)


def read_json_file(pathname):
    with open(pathname, "r", encoding='utf-8') as file:
        data = json.load(file)
        return data['def']


def read_file_json(pathname, *keys):
    with open(pathname, "r", encoding='utf-8') as file:
        data = json.load(file)
        if keys:
            result = None
            for key in keys:
                if result:
                    result = result.get(key, {})
                else:
                    result = data.get(key, {})
            return result
        else:
            return data


def get_token(oauth_token):
    Uri = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    dic = {'yandexPassportOauthToken': oauth_token}
    response = requests.post(url=Uri, params=dic)
    if response.status_code:
        print("операция обновления 'iamToken' прошла успешно")
        s = json.dumps(response.json(), indent=4, sort_keys=True, ensure_ascii=False)
        settings = Settings()
        with open(settings.path_name_token, "w", encoding='utf-8') as file:
            file.write(s)
    else:
        print(response.status_code)


def check_token(settings):
    datetime_now = datetime.now()
    path_name_iam_token = settings['PATH_NAME_IAM_TOKEN']
    oauth_token = settings['OAUTH_TOKEN']
    date_expires = read_file_json(path_name_iam_token, 'expiresAt').split('.')[0]
    datetime_expire = datetime.fromisoformat(date_expires)
    if datetime_now > datetime_expire:
        get_token(oauth_token)
# def window_set_style(window, **key_style):
#     style_sheet = ''
#     for key, value in key_style.items():

def create_style(**key_style):
    style_sheet = ''
    for key, value in key_style.items():
        style_sheet += key + ' {' + value[0] + ':' + value[1] + '} '
    return style_sheet

