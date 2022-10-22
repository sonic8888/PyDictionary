import sys
from PySide6.QtCore import QRect
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from Views import HomeGui
from Servise.Db.Sqlite.SqliteApplication import create_empty_tables
from test import displey


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    geometryWindow = get_geometry()
    windowHome = HomeGui.HomeWindows(geometryWindow)
    windowHome.show()
    apply_stylesheet(app, theme='dark_teal.xml')
    app.exec()
    # create_empty_tables()
    # displey()
