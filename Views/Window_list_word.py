import json
import logging
from os import path
import PySide6
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Slot
from PySide6.QtGui import Qt

from Servise.tools import Settings, ConnectDb, execute_db, request, display_info, display_error, insert_data, \
    create_con_cur, get_data_general
from Views.Generate.list_words_generate import Ui_MainWindow
from Servise.sound import get_word_sound

logging_list_word = logging.getLogger(__name__)
logging_list_word.setLevel(logging.INFO)
_handler = logging.FileHandler(f'logs\\{__name__}.log', mode='w')
_formatter = logging.Formatter("%(name)s %(lineno)d %(asctime)s %(levelname)s %(message)s")
_handler.setFormatter(_formatter)
logging_list_word.addHandler(_handler)


def add_data_list(list_name, word, word_id, translate):
    s = Settings()
    connectDd = ConnectDb(s.name_db)
    last_id = None
    con = connectDd.get_connect
    cur = con.cursor()
    _tu = list_name,
    res = execute_db(con, cur, "SELECT list_id FROM ListName WHERE list_name = ?",
                     _tu)  # проверяем существует ли такой список
    if not res:
        cur.close()
        con.close()
        return
    res = cur.fetchone()
    if res is None:  # если такого списка не существует, то создаем его и добавляем слово
        res = execute_db(con, cur, "INSERT INTO ListName (list_name) VALUES (?)", _tu)
        if not res:
            cur.close()
            con.close()
            return
        list_id = cur.lastrowid
        _tu = word_id, list_name, word, list_id, translate
        execute_db(con, cur, "INSERT INTO ListWords (word_id, list_name, word, list_id, translate) "
                             "VALUES (?, ?, ?, ?, ?)", _tu)
        last_word_id = cur.lastrowid
    else:  # если список уже существует, то добавляем в него слово
        list_id = res[0]
        _tu = word_id, list_name, word, list_id, translate
        execute_db(con, cur, "INSERT INTO ListWords (word_id, list_name, word, list_id, translate) VALUES (?, ?, ?, "
                             "?, ?)", _tu)
        list_id = cur.lastrowid
    con.commit()
    cur.close()
    con.close()
    return list_id


def find_word_in_db(word):
    s = Settings()
    connectDd = ConnectDb(s.name_db)
    con = connectDd.get_connect
    cur = con.cursor()
    _tu = word,
    if not execute_db(con, cur, "SELECT word_id, translate FROM Words WHERE word = ? ", _tu):
        cur.close()
        con.close()
        return None
    else:
        res = cur.fetchone()
        if not res:
            return None
        cur.close()
        con.close()
        return res


# def add_data_in_db(list_name, word, word_id):
#     s = Settings()
#     add_data_list(list_name, word, word_id)
#     get_word_sound(word, s.folder_id, s.iam_token, s.path_name_audio_storage)
#     display_info(f"слово:'{word}' сохранено в списке: '{list_name}'")
#     logging_list_word.info(f"слово:'{word}' сохранено в списке: '{list_name}'")
#     return word


def search_in_net(word):
    if response := request(word):
        data = response.json()
        list_data = data['def']
        if list_data:
            return response
        else:
            display_info("слово не найдено")
            logging_list_word.info("слово не найдено")
            return None
    else:
        display_info("ошибка соединения с сервером")
        logging_list_word.info("ошибка соединения с сервером")
        return None


def select_from_db(sql_query, **kwargs):
    pass


def add_data_to_model(model, sql, params_sql, editable=False, **kwargs):
    res = get_data_general(sql, params_sql)
    si_w = QtGui.QStandardItem(res[0])
    si_w.setEditable(editable)
    si_t = QtGui.QStandardItem(res[1])
    si_t.setEditable(editable)
    si_w.list_words_i = params_sql[0]
    model.appendRow((si_w, si_t))
    return model


class WindowList(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, geometryWindow, parent):
        super(WindowList, self).__init__(parent=parent)
        self.setupUi(self)
        self.setGeometry(geometryWindow)
        self._list_data = None
        self.current_list_name = None
        self.lineEdit_2.editingFinished.connect(self.transition_next_line_edit)  # list_name
        self.lineEdit.editingFinished.connect(self.test)  # word
        self.pushButton_3.clicked.connect(self.create_name_list)  # создать список
        self.pushButton_3.setText("создать")
        self.pushButton_4.setText("удалить")
        self.pushButton.clicked.connect(self.add)  # добавить
        self.pushButton_2.clicked.connect(self.select_word)
        self.lineEdit.setReadOnly(True)
        # self.lineEdit.setMinimumWidth(150)
        self.lineEdit.setReadOnly(False)
        self.checkBox.stateChanged.connect(self.hide_table_num)
        self.checkBox.setChecked(True)
        self.gridLayout.setContentsMargins(40, 40, 40, 40)
        self.comboBox.currentTextChanged.connect(self.select_current_list)
        self._sti = None
        # self.init()
        self.init_list()
        self.init_table()

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        super().parent().show()

    def create_name_list(self):
        print("test")
        self._sti = None
        self.lineEdit.setReadOnly(False)
        self.lineEdit_2.setReadOnly(False)
        self.lineEdit_2.setText('')
        self.lineEdit_2.setFocus()

    def transition_next_line_edit(self):
        if self.lineEdit_2.text():
            self.lineEdit.setText('')
            self.lineEdit.setFocus()

    def add_new_word_to_db(self):
        word = self.lineEdit.text()
        list_name = self.lineEdit_2.text()
        word_id = None
        last_id = None
        if not list_name:
            display_info("не указано название списка.")
            return None
        if not word:
            # display_info("не указано слово списка.")
            return None
        word_id_translate = find_word_in_db(word)  # ищем слово в БД
        if word_id_translate:
            last_id = add_data_list(list_name, word, word_id_translate[0],
                                    word_id_translate[1])  # сохраняем в другой таблице (ListName, ListWords)
        else:
            if response := search_in_net(word):  # если не найдено в БД ищем в интернете
                s = Settings()
                word_id = insert_data(response, s.name_db)
                get_word_sound(word, s.folder_id, s.iam_token, s.path_name_audio_storage)
                word_id_translate = find_word_in_db(word)  # ищем слово в БД
                # add_data_in_db(list_name, word, word_id)
                last_id = add_data_list(list_name, word, word_id_translate[0],
                                        word_id_translate[1])  # сохраняем в другой таблице (ListName, ListWords)
        return word_id, word, list_name, last_id, word_id_translate[1]

    def create_model(self):
        self._sti = QtGui.QStandardItemModel(parent=self)
        self._sti.setHorizontalHeaderLabels(['Слово', 'Перевод'])
        self._sti.setColumnCount(2)
        return self._sti

    def add_words_to_model(self, word_id):
        if self._sti is None:
            self._sti = self.create_model()
        self._sti = add_data_to_model(self._sti, "SELECT word, translate "
                                                 "FROM ListWords WHERE list_words_id = ?",
                                      (word_id,))
        self.tableView.setModel(self._sti)

    def add(self):
        res = self.add_new_word_to_db()
        if res:
            self.add_words_to_model(res[0])
        self.lineEdit.setText('')

    def hide_table_num(self):
        if self.checkBox.checkState() == Qt.CheckState.Checked:
            self.tableView.verticalHeader().setVisible(False)
        else:
            self.tableView.verticalHeader().setVisible(True)

    def load_list(self):
        """Загружаем в combobox списки"""
        res = get_data_general(sql="SELECT * FROM ListName ORDER BY current_list DESC", params_sql=(),
                               operation_cur='fetchall')
        self._list_data = list(res)
        self.current_list_name = self._list_data[0][1]
        self.lineEdit_2.setText(self.current_list_name)
        for item in self._list_data:
            self.comboBox.addItem(item[1])

    def select_current_list(self, text):
        print(text)

    def init_current_list_data(self):
        if text := self.current_list_name:
            res = get_data_general("SELECT list_words_id FROM ListWords WHERE list_name = ?", (text,),
                                   operation_cur='fetchall')
            list_word_id = [item[0] for item in res]
            for word_id in list_word_id:
                self.add_words_to_model(word_id)

    def select_word(self):
        if self._sti:
            model_index = self.tableView.selectionModel().selectedIndexes()
            if model_index:
                _l_i = self._sti.item(model_index[0].row(), 0).list_words_i
                self._sti.removeRows(model_index[0].row(), 1)
                self._sti.layoutChanged.emit()
                res = get_data_general("DELETE FROM ListWords WHERE list_words_id = ?", (_l_i,), commit='rowcount')
                print(res)

    def test(self):
        print('test finish')

    def init_list(self):
        self.load_list()

    def init_table(self):
        self.init_current_list_data()
