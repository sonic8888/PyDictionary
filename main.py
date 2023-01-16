import os
import sys

from PySide6.QtWidgets import QApplication
import qt_material
from qt_material import apply_stylesheet
from Servise.tools import create_structure_project, check_token
from Views import HomeGui
from Servise.tools import read_file_json, Settings

PATH_TOKEN = r'json/path_token.json'


def main():
    data_token = read_file_json(PATH_TOKEN)
    check_token(data_token)
    app = QApplication(sys.argv)
    s = Settings()
    current_theme_name = s.settings.get('CURRENT_THEME_NAME', 'dark_teal.xml')
    geometryWindow = s.geometry_window
    windowHome = HomeGui.HomeWindows(geometryWindow)
    create_structure_project(s)
    apply_stylesheet(app, theme=current_theme_name)
    s.current_theme = qt_material.get_theme(current_theme_name)
    windowHome.show()
    app.exec()


if __name__ == '__main__':
    main()
