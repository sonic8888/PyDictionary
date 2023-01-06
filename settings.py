import os
import json

from PySide6.QtCore import QRect
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QApplication


class Settings(object):
    _instance = None  # Keep instance reference
    _path_name_settings = 'json/settings.json'
    _path_name_token = 'json/token.json'
    _geometry_window = None
    _settings = None
    _token = None
    _current_theme = None
    _current_theme_name = None
    _iamToken = None
    _folder_id = None
    _path_name_audio_temp = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls._settings = cls.read_file_json(cls._path_name_settings)
            cls._token = cls.read_file_json(cls._path_name_token)
            cls._geometry_window = cls.get_geometry()
            cls._iamToken = cls._token['iamToken']
            cls._folder_id = cls._settings['FOLDER_ID']
            cls._path_name_audio_temp = cls.read_file_json(cls._path_name_settings)["PATH_NAME"]['AUDIO_TEMP']
            cls._path_name_token = cls.read_file_json(cls._path_name_settings)['PATH_NAME']['IAM_TOKEN']
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
        sizeWindow = cls.get_standard_size_window()
        screenSize = cls.get_screen_size()
        pointWidth = int((screenSize[0] - sizeWindow[0]) / 2)
        pointHeight = int((screenSize[1] - sizeWindow[1]) / 2)
        return QRect(pointWidth, pointHeight, sizeWindow[0], sizeWindow[1])

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
    def path_name_token(self):
        return self._path_name_token

    @property
    def iam_token(self):
        return self._iamToken

    @property
    def folder_id(self):
        return self._folder_id

    @property
    def path_name_audio_temp(self):
        return self._path_name_audio_temp
