import sys

from PySide6.QtWidgets import QApplication
import qt_material
from qt_material import apply_stylesheet
from Servise.tools import check_token
from Views import HomeGui
from settings import Settings

if __name__ == '__main__':
    # set_current_themas(Themas.LIGHT)
    app = QApplication(sys.argv)
    s = Settings()
    current_theme_name = s.settings.get('CURRENT_THEME_NAME', 'dark_teal.xml')
    check_token(s.settings)
    geometryWindow = s.geometry_window
    windowHome = HomeGui.HomeWindows(geometryWindow)

    apply_stylesheet(app, theme=current_theme_name )
    s.current_theme = qt_material.get_theme(current_theme_name)
    windowHome.show()
    app.exec()
