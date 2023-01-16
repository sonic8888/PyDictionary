from PySide6.QtWidgets import QMessageBox


def messageBox_critical(parent, exception, title='Error'):
    message = exception.__str__()
    QMessageBox.critical(parent, title, message)


def message_critical_(parent, message, title='Error'):
    QMessageBox.critical(parent, title, message)


def messageBox_warning(parent, message, title='Warning'):
    QMessageBox.warning(parent, title, message)


def messageBox_question(parent, message, title='Question'):
    return QMessageBox.question(parent, title, message)
