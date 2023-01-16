import PySide6
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QTableView

from Servise.tools import get_data


class MyTable(QTableView):
    def __init__(self, parent):
        super(MyTable, self).__init__(parent=parent)
        self.window_show_db = None

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        _width = event.size().width()
        self.setColumnWidth(0, _width * 0.5)
        self.setColumnWidth(1, _width * 0.5)

    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        model = self.model()
        model_index = self.selectionModel().selectedIndexes()
        data = model.item(model_index[0].row(), 0)
        word = data.text()
        res = get_data(word)
        self.window_show_db.insert_data_textEdit(res)
        self.window_show_db.current_word = word
