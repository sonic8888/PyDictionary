import sys
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from DataSettings import set_current_themas, get_geometry, Themas
from Views import HomeGui

if __name__ == '__main__':
    set_current_themas(Themas.LIGHT)
    set_current_themas(Themas.DARK)
    app = QApplication(sys.argv)
    geometryWindow = get_geometry()
    windowHome = HomeGui.HomeWindows(geometryWindow)
    windowHome.show()
    apply_stylesheet(app, theme='dark_teal.xml')
    app.exec()
