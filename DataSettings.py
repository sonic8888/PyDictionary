import json
from enum import Enum

from PySide6.QtCore import QRect
from PySide6.QtGui import QScreen, QIcon
from PySide6.QtWidgets import QApplication

list_resources = ['Audio']
window_title = 'Dictionary'


class Themas(Enum):
    LIGHT = 1
    DARK = 2


class SelectData(Enum):
    ALL = 1
    TRANSLATE = 2
    EXAMPLE = 3


current_themas = Themas.LIGHT


def get_screen_size():
    """
     Возвращает размеры экрана
     """
    screenSize = QScreen.availableGeometry(QApplication.primaryScreen())
    return screenSize.width(), screenSize.height()


def get_standard_size_window():
    """
        :return: size window
    """
    dividerWidth = 2.13
    dividerHeight = 2.064
    screenSize = get_screen_size()
    widthStandard = int(screenSize[0] / dividerWidth)
    heightStandard = int(screenSize[1] / dividerHeight)
    return widthStandard, heightStandard


def get_geometry():
    """
    start pos. and size window apps
    :return: QRect
    """
    sizeWindow = get_standard_size_window()
    screenSize = get_screen_size()
    pointWidth = int((screenSize[0] - sizeWindow[0]) / 2)
    pointHeight = int((screenSize[1] - sizeWindow[1]) / 2)
    return QRect(pointWidth, pointHeight, sizeWindow[0], sizeWindow[1])


def get_current_themas():
    with open("current_themas.json", "r") as read_file:
        _data = json.load(read_file)
        return _data["current_themas"]


def set_current_themas(themas=Themas.LIGHT):
    with open("current_themas.json", "w") as write_file:
        json.dump({"current_themas": str(themas)}, write_file)


def get_path_icon(name_icon):
    _current_themas = get_current_themas()
    with open("icon_names.json", "r") as read_file:
        _data = json.load(read_file)
        path_name = _data[name_icon][_current_themas]
        print(_data[name_icon][_current_themas])
        return path_name


def create_icon(name_icon, dir_icon='Icons'):
    _current_themas = get_current_themas()
    with open("icon_names.json", "r") as read_file:
        _data = json.load(read_file)
        _path_name = _data[name_icon][_current_themas]
        _path = dir_icon + '/' + _path_name
        return QIcon(_path)


def get_color_from_themas(color_name):
    _current_themas = get_current_themas()
    with open("icon_names.json", "r") as read_file:
        _data = json.load(read_file)
        return _data[color_name][_current_themas]
