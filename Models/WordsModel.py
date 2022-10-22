from PySide6 import QtCore
from PySide6.QtGui import Qt


class Words(QtCore.QAbstractListModel):
    def __init__(self, words=None, *args, **kwargs):
        super(Words, self).__init__(*args, **kwargs)
        self.words = words or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.words[index.row()]
            return text

    def rowCount(self, index):
        return len(self.words)
