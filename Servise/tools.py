import datetime
import json
import re
import os
import shutil
import sqlite3
import logging
from os import path
from audioplayer import AudioPlayer
from shutil import copy2
from sqlite3 import Error, IntegrityError, InterfaceError, DatabaseError, DataError, InternalError, ProgrammingError, \
    NotSupportedError
from datetime import datetime
from enum import Enum

from PySide6.QtCore import QRect
from PySide6.QtGui import QScreen

# from settings import Settings
import PySide6
import requests
from PySide6.QtWidgets import QLabel, QApplication

logging_tools = logging.getLogger(__name__)
logging_tools.setLevel(logging.INFO)
_handler = logging.FileHandler(f'logs\\{__name__}.log', mode='w')
_formatter = logging.Formatter("%(name)s %(lineno)d %(asctime)s %(levelname)s %(message)s")
_handler.setFormatter(_formatter)
logging_tools.addHandler(_handler)


class Settings(object):
    _instance = None  # Keep instance reference
    _path_name_settings = 'json/settings.json'
    _geometry_window = None
    _settings = None
    _token = None
    _current_theme = None
    _current_theme_name = None
    _iam_token = None
    _folder_id = None
    _path_name_audio_temp = None
    _path_name_audio_storage = None
    _path_name_create_db = None
    _path_name_logs = None
    _name_db = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls._settings = cls.read_file_json(cls._path_name_settings)
            cls._geometry_window = cls.get_geometry()
            cls._token = cls.read_file_json('json/token.json')
            cls._iam_token = cls._token['iamToken']
            cls._folder_id = cls._settings['FOLDER_ID']
            cls._path_name_audio_temp = cls._settings["PATH_NAME"]['AUDIO_TEMP']
            cls._path_name_audio_storage = cls._settings["PATH_NAME"]["AUDIO_STORAGE"]
            cls._path_name_create_db = cls._settings['PATH_NAME']['CREATE_DB']
            cls._name_db = cls._settings['PATH_NAME']['NAME_DB']
            cls._path_name_logs = cls._settings['PATH_NAME']['LOGS']
        return cls._instance

    @classmethod
    def read_file_json(cls, path_name):
        with open(path_name, "r", encoding='utf-8') as file:
            data = json.load(file)
            return data

    @classmethod
    def get_screen_size(cls):
        """
         Возвращает размеры экрана
         """
        screenSize = QScreen.availableGeometry(QApplication.primaryScreen())
        return screenSize.width(), screenSize.height()

    @classmethod
    def get_standard_size_window(cls):
        """
            :return: size window
        """
        dividerWidth = 2.13
        dividerHeight = 2.064
        screenSize = cls.get_screen_size()
        widthStandard = int(screenSize[0] / dividerWidth)
        heightStandard = int(screenSize[1] / dividerHeight)
        return widthStandard, heightStandard

    @classmethod
    def get_geometry(cls):
        """
        start pos. and size window apps
        :return: QRect
        """
        try:
            sizeWindow = cls.get_standard_size_window()
            screenSize = cls.get_screen_size()
            pointWidth = int((screenSize[0] - sizeWindow[0]) / 2)
            pointHeight = int((screenSize[1] - sizeWindow[1]) / 2)
            return QRect(pointWidth, pointHeight, sizeWindow[0], sizeWindow[1])
        except BaseException as bs:
            # display_error(bs)
            # logging_settinds.exception(bs)
            return QRect(509, 268, 901, 503)

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value

    @property
    def token(self):
        return self._token

    @property
    def geometry_window(self):
        return self._geometry_window

    @property
    def current_theme(self):
        return self._current_theme

    @current_theme.setter
    def current_theme(self, value):
        self._current_theme = value

    @property
    def iam_token(self):
        return self._iam_token

    @property
    def folder_id(self):
        return self._folder_id

    @property
    def path_name_audio_temp(self):
        return self._path_name_audio_temp

    @property
    def path_name_create_db(self):
        return self._path_name_create_db

    @property
    def name_db(self):
        return self._name_db

    @property
    def path_name_audio_storage(self):
        return self._path_name_audio_storage

    @property
    def path_name_logs(self):
        return self._path_name_logs


def my_factory_name(cur, res):
    d = {}
    for i, item in enumerate(cur.description):
        d[item[0]] = res[i]
    return d


def my_factory_num(cur, res):
    d = {}
    for i, item in enumerate(cur.description):
        d[i] = res[i]
    return d


class ConnectDb:
    instance = None
    _path_name = None
    _timeout = None
    _detect_types = None
    _isolation_level = None
    _check_same_thread = None
    _factory = None
    _cached_statements = None
    _uri = None

    def __new__(cls, path_name_db, timeout=5.0, detect_types=0, isolation_level='DEFERRED',
                check_same_thread=True, factory=sqlite3.Connection, cached_statements=128, uri=False):
        if not cls.instance:
            cls.instance = object.__new__(cls)
        cls._path_name = path_name_db
        cls._timeout = timeout
        cls._detect_types = detect_types
        cls._isolation_level = isolation_level
        cls._check_same_thread = check_same_thread
        cls._factory = factory
        cls._cached_statements = cached_statements
        cls._uri = uri
        return cls.instance

    @property
    def get_connect(self, row_factory=None):
        '''
        Возвращает объект Connection.
        если row_factory = my_factory_name -> 'имя столбца' - 'значение',
        row_factory = my+factory_num -> 'номер столбца' - 'значение',
        row_factory = sqlite3.Row -> res[номер строки][номер столбца]
        :param row_factory: function
        :return:Connection
        '''
        _con = None
        if row_factory:
            try:
                _con = sqlite3.connect(self._path_name, self._timeout, self._detect_types, self._isolation_level,
                                       self._check_same_thread, self._factory, self._cached_statements, self._uri)
                _con.row_factory = row_factory
            except Error:
                display_error(Error, 'ошибка создания соединения БД')
                logging_tools.exception('Error create connection Db')
                return None
        else:
            try:
                _con = sqlite3.connect(self._path_name, self._timeout, self._detect_types, self._isolation_level,
                                       self._check_same_thread, self._factory, self._cached_statements, self._uri)
            except Error:
                display_error(Error, 'ошибка создания соединения БД')
                logging_tools.exception('Error create connection Db')
                return None

        return _con


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


def get_token(oauth_token, path_iam_token):
    Uri = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    dic = {'yandexPassportOauthToken': oauth_token}
    response = requests.post(url=Uri, params=dic)

    if response.status_code:
        s = json.dumps(response.json(), indent=4, sort_keys=True, ensure_ascii=False)
        with open(path_iam_token, "w", encoding='utf-8') as file:
            file.write(s)
        display_info("операция обновления 'iamToken' прошла успешно")
        logging_tools.info("'iamToken' update operation succeeded")
    else:
        display_info("не удалось обновить 'iamToken'", response.status_code)
        logging_tools.warning("не удалось обновить 'iamToken'", f"response.status_code: {response.status_code}")


def check_token(data_token):
    path_token = data_token["PATH_TOKEN_FILE"]
    oauth_token = data_token["OAUTH_TOKEN"]
    path_iam_token = data_token["path_name_iam_token"]
    datetime_now = datetime.now()
    date_expires = read_file_json(path_token, 'expiresAt').split('.')[0]
    datetime_expire = datetime.fromisoformat(date_expires)
    if datetime_now > datetime_expire:
        get_token(oauth_token, path_iam_token)


def create_style(**key_style):
    style_sheet = ''
    for key, value in key_style.items():
        style_sheet += key + ' {' + value[0] + ':' + value[1] + '} '
    return style_sheet


def create_structure_project(settings):
    _file_create_db = settings.path_name_create_db
    _name_db = settings.name_db
    create_table(path_db=_name_db, path_create_db=_file_create_db)


def create_table(path_db, path_create_db):
    if path.exists(path_db):
        return
    connection_db = ConnectDb(path_db)
    con = connection_db.get_connect
    if not con:
        return
    cur = con.cursor()
    dict_json = read_file_json(path_create_db)
    sql_script = ""
    for value in dict_json.values():
        sql_script += value
    try:
        cur.executescript(sql_script)
    except sqlite3.DatabaseError as err:
        display_error(err, 'ошибка создания таблиц БД')
        logging_tools.exception('Error create table Db')
        con.close()
        return
    con.commit()
    cur.close()
    con.close()
    display_info(f'создание пустой БД: {path_db}')
    logging_tools.info(f"Create empty Db: {path_db}")


def insert_data(response, path_name_db):
    data = response.json()
    list_data = data['def']
    word = ''
    connect_db = ConnectDb(path_name_db)
    con = connect_db.get_connect
    if not con:
        return
    cur = con.cursor()
    last_word_id = 0
    for item in list_data:
        if not last_word_id:
            word = item.get('text', '')
            ts = item.get('ts', '')
            translate = item.get('tr', [])[0].get('text', '')
            _list_words_data = [word, ts, translate]
            if not execute_db(con, cur, "INSERT INTO Words (word, ts, translate) VALUES (?, ?, ?)", _list_words_data):
                return
            last_word_id = cur.lastrowid
            _list_response_data = [last_word_id, response.text]
            if not execute_db(con, cur, "INSERT INTO DataResponse (res_id, response) VALUES (?, ?)",
                              _list_response_data):
                return
        for item_tr in item.get('tr', []):
            translate = item_tr.get('text', '')
            pos = item_tr.get('pos', '')
            gen = item_tr.get('gen', '')
            fr = item_tr.get('fr', '')
            list_translate_data = [last_word_id, translate, pos, gen, fr]
            if not execute_db(con, cur,
                              "INSERT INTO Translates (word_id, translate, pos, gen, fr) VALUES (?, ?, ?, ?, ?)",
                              list_translate_data):
                return
            last_translate_id = cur.lastrowid
            _list_syn_id = []
            for item_syn in item_tr.get('syn', []):
                text_syn = item_syn.get('text', '')
                pos = item_syn.get('pos', '')
                gen = item_syn.get('gen', '')
                fr = item_syn.get('fr', '')
                list_syn_data = [last_translate_id, text_syn, pos, gen, fr]
                if not execute_db(con, cur, "INSERT INTO Syn (translate_id, syn, pos, gen, fr) VALUES(?, ?, ?, ?, ?)",
                                  list_syn_data):
                    return
                last_syn_id = cur.lastrowid
                _list_syn_id.append(last_syn_id)
            for item_mean in item_tr.get('mean', []):
                text_mean = item_mean.get('text', '')
                list_mean_data = [last_translate_id, text_mean]
                if not execute_db(con, cur, "INSERT INTO Mean (translate_id, mean) VALUES (?, ?)", list_mean_data):
                    return
            index = 0
            for item_example in item_tr.get('ex', []):
                text_en = item_example.get('text', '')
                _list_text_ru = item_example.get('tr', [])
                text_ru = ''
                if _list_text_ru:
                    text_ru = _list_text_ru[0].get('text', '')
                _list_examples = []
                if not index:
                    _list_examples = [last_translate_id, text_en, text_ru]
                    if not execute_db(con, cur,
                                      "INSERT INTO Examples (translate_id, examp_en, examp_ru) VALUES (?, ?, ?)",
                                      _list_examples):
                        return
                    index += 1
                    continue
                else:
                    if (index - 1) in range(len(_list_syn_id)):
                        _list_examples = [_list_syn_id[index - 1], text_en, text_ru]
                        if not execute_db(con, cur,
                                          "INSERT INTO SynExample (syn_id, examp_en, examp_ru) VALUES (?, ?, ?)",
                                          _list_examples):
                            return
                    index += 1
    con.commit()
    cur.close()
    con.close()
    display_error(f"'{word}' - успешно сохранено в БД")


def execute_db(connect, cursor, sql_query, sequence_data=None):
    try:
        cursor.execute(sql_query, sequence_data)
        return connect
    except IntegrityError as ei:
        cursor.close()
        connect.close()
        display_error(ei)
        logging_tools.exception(ei)
        return None
    except NotSupportedError as nse:
        cursor.close()
        connect.close()
        display_error(nse)
        logging_tools.exception(nse)
        return None
    except ProgrammingError as pe:
        cursor.close()
        connect.close()
        display_error(pe)
        logging_tools.exception(pe)
        return None
    except InternalError as ier:
        cursor.close()
        connect.close()
        display_error(ier)
        logging_tools.exception(ier)
        return None
    except DataError as de:
        cursor.close()
        connect.close()
        display_error(de)
        logging_tools.exception(de)
        return None
    except DatabaseError as dbe:
        cursor.close()
        connect.close()
        display_error(dbe)
        logging_tools.exception(dbe)
        return None
    except InterfaceError as ier:
        cursor.close()
        connect.close()
        display_error(ier)
        logging_tools.exception(ier)
        return None
    except Error as error:
        cursor.close()
        connect.close()
        display_error(error)
        logging_tools.exception(error)
        return None


def copy_file(path_file, directory_target):
    _base_name = path.basename(path_file)
    file_target = path.join(directory_target, _base_name)
    if not path.exists(file_target):
        shutil.copy2(path_file, directory_target)
        # print('файл скопирован')


def clear_folder_temp(path_direct):
    _path = ''
    for item in os.scandir(path_direct):
        _path = item.path
        try:
            os.remove(_path)
        except OSError:
            display_error(OSError, f"ошибка удаления файлов из папки: {path_direct}")
            logging_tools.exception(f"Error deleting files from folder: {path_direct}")


def display_error(*args):
    for item in args:
        print(str(item))


def display_info(*args):
    for item in args:
        print(str(item))


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
    match_word = isMath(source_example, source_word)
    if match_word:
        source_word = match_word[0]
    source_word_html = wrapperHTML('span', source_word, style_color=current_theme[dictionary_color['select']])
    source_example = source_example.replace(source_word, source_word_html)
    text_example = source_example + ' — ' + translate_example
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


def play_sound(path_sound):
    try:
        path_file = path.abspath(path_sound)
        player = AudioPlayer(path_file).play(block=True)
    except BaseException as bs:
        display_error(f'Не возможно воспроизвести файл: {path_sound}')
        logging_tools.exception(f"File cannot be played: {path_sound}")


def get_data(word):
    s = Settings()
    connection_db = ConnectDb(s.name_db)
    con = connection_db.get_connect
    cur = con.cursor()
    _tu = word,
    execute_db(con, cur,
               "SELECT response FROM DataResponse WHERE res_id IN (SELECT word_id FROM Words WHERE word = "
               "?)", _tu)
    res = cur.fetchone()
    cur.close()
    con.close()
    return res
