from PySide6.QtWidgets import QMessageBox


def messageBox_critical(parent, exception, title='Error'):
    message = exception.__str__()
    QMessageBox.critical(parent, title, message)


def message_critical_(parent, message, title='Error'):
    QMessageBox.critical(parent, title, message)
