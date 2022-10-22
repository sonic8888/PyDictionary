from PySide6.QtWidgets import QMessageBox


def messageBox_critical(parent, exception, title='Error'):
    message = exception.__str__()
    QMessageBox.critical(parent, title, message)
