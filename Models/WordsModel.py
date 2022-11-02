from PySide6 import QtCore
from PySide6.QtGui import Qt, QFont


class Words(QtCore.QAbstractListModel):
    def __init__(self, words=None, *args, **kwargs):
        super(Words, self).__init__(*args, **kwargs)
        self.words = words or []

    def data(self, index, role):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            _, text = self.words[index.row()]
            return text
        elif role == Qt.FontRole:
            if col == 0:  # change font only for cell(0,0)
                bold_font = QFont()
                bold_font.setPointSize(14)
                return bold_font

    def rowCount(self, index):
        return len(self.words)
