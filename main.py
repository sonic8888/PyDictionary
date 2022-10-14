import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QScreen
from Views import HomeGui


def get_screen_size():
    """
     Возвращает размеры экрана
     """
    screenSize = QScreen.availableGeometry(QApplication.primaryScreen())
    return screenSize.width(), screenSize.height()


def get_standard_size_window():
    """
        :return: размер окна
    """
    dividerWidth = 2.13
    dividerHeight = 2.064
    screenSize = get_screen_size()
    widthStandard = int(screenSize[0] / dividerWidth)
    heightStandard = int(screenSize[1] / dividerHeight)
    return widthStandard, heightStandard


def move_to_centre(widget):
    """
    Перемещает виджет(окно)
    по центру экрана
    :param widget:
    :return:
    """
    screenSize = get_screen_size()
    sizeWidget = widget.geometry()
    pointWidth = int((screenSize[0] - sizeWidget.width()) / 2)
    pointHeight = int((screenSize[1] - sizeWidget.height()) / 2)
    widget.move(pointWidth, pointHeight)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sizeWindow = get_standard_size_window()
    windowHome = HomeGui.HomeWindows(sizeWindow)
    move_to_centre(windowHome)
    windowHome.show()
    app.exec()
