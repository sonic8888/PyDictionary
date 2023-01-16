import json
import PySide6
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Slot
from PySide6.QtGui import Qt
from Views.Generate.window_data_generate import Ui_MainWindow
from Servise.tools import ConnectDb, Settings, execute_db, createTextHtmlTranslate, createTextHtmlExamples, get_data


class WindowDb(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, geometryWindow):
        super(WindowDb, self).__init__()
        self._sti = None
        self.setupUi(self)
        self.tableView.setSortingEnabled(True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.window_show_db = self
        self.setGeometry(geometryWindow)
        self.get_data_for_table()
        self.lineEdit.textChanged.connect(self.sort_model)
        self.pushButton_4.clicked.connect(self.update)
        self.lineEdit.editingFinished.connect(self.get_data_for_textedit)
        self.checkBox.stateChanged.connect(self.hide_table_num)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        # print("hello")
        # self.get_data_from_db()
        pass

    def get_data_for_table(self, text=''):
        self._sti = QtGui.QStandardItemModel(parent=self)
        self._sti.setHorizontalHeaderLabels(['Слово', 'Перевод'])
        s = Settings()
        connect_db = ConnectDb(s.name_db)
        con = connect_db.get_connect
        cur = con.cursor()
        res = None
        list_tuple = []
        if text:
            res = cur.execute(
                "SELECT word, translate FROM Words,"
                f" Translates WHERE Words.word_id = Translates.word_id and Translates.fr = 10 and Words.word LIKE '{text}%'")
            list_tuple = res.fetchall()
        else:
            res = cur.execute(
                "SELECT word, translate FROM Words,"
                " Translates WHERE Words.word_id = Translates.word_id and Translates.fr = 10")
            list_tuple = res.fetchall()
        for item in list_tuple:
            st_1 = QtGui.QStandardItem(item[0])
            st_1.setEditable(False)
            st_2 = QtGui.QStandardItem(item[1])
            st_2.setEditable(False)
            _tu = st_1, st_2
            self._sti.appendRow(_tu)
        self.tableView.setModel(self._sti)
        self._sti.layoutChanged.emit()
        cur.close()
        con.close()

    @Slot()
    def sort_model(self, text):
        self.get_data_for_table(text)

    @Slot()
    def update(self):
        self.lineEdit.setText('')

    @Slot()
    def get_data_for_textedit(self):
        text = self.lineEdit.text()
        res = get_data(text)
        self.insert_data_textEdit(res)

    def hide_table_num(self):
        if self.checkBox.checkState() == Qt.CheckState.Checked:
            self.tableView.verticalHeader().setVisible(True)
        else:
            self.tableView.verticalHeader().setVisible(False)

    def insert_data_textEdit(self, data):
        if data:
            _data = json.loads(data[0])
            list_data = _data['def']
            if list_data:
                dict_html_tra = createTextHtmlTranslate(list_data)
                examples_html = createTextHtmlExamples(list_data)
                self.textEdit.setHtml(dict_html_tra['html'])
                self.textEdit_2.setHtml(examples_html)


