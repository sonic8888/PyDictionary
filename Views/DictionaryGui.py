import os
import re
from datetime import date
from typing import Any
import PySide6
from PySide6 import QtGui
from PySide6.QtCore import QSize, Qt, Slot, QItemSelection, QUrl
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem, QFont
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QToolBar, QListView, \
    QLineEdit, QTreeView, QPushButton, QLabel, QGridLayout
from DataSettings import create_icon, list_resources, window_title, SelectData
from Models.WordsModel import Words
from Servise.Db.Sqlite.SqliteApplication import select_data, delete_data, update_data, insert_data, load, \
    select_data_like
from Servise.Variable import minSizeWindow
from Views.MessageBoxess import *

regx_pattern = r'\w+\s?\(\w+\)'
regx_split_pattern = r'\s?\('


class CustomItem(QStandardItem):

    def __init__(self, window, name, key_word, parent=None, *args, **kwargs):
        super(CustomItem, self).__init__(*args, **kwargs)
        self.key_word = key_word
        self.window = window
        self.name = name
        self.parent = parent

    def data(self, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if self.name == 'Translate':
                text = '{} ({})'.format(self.key_word['Translate'], self.key_word['PartOfSpeach'])
                return text
            else:
                text = self.key_word['Example']
                return text
        if role == Qt.FontRole:
            if self.name == 'Translate':
                font = QFont()
                font.setPointSize(15)
                return font
            else:
                font = QFont()
                font.setPointSize(12)
                font.setItalic(True)
                return font

    def setData(self, value: Any, role: int = ...) -> None:
        if role == Qt.EditRole:
            if self.name == 'Translate':
                try:
                    if re.fullmatch(regx_pattern, value):
                        _list_val = re.split(regx_split_pattern, value)
                        _list_val[1] = _list_val[1][:-1]
                        self.key_word['Translate'] = _list_val[0]
                        _list_val[1] = self.window.convert_part_of_speach(_list_val[1])
                        self.key_word['PartOfSpeach'] = _list_val[1]
                    else:
                        message_critical_(self.window, 'укажите "перевод слова" и "часть речи" в скобках')
                        self.window.buttonAdd.setChecked(False)
                        return
                except BaseException as ex:
                    message_critical_(self.window, str(ex))
                    return
            else:
                self.key_word['Example'] = value
        if not self.window.button_save_db.isVisible():
            self.window.button_save_db.setVisible(True)

    def type(self) -> int:
        return 134567

    @property
    def get_key_word(self):
        return self.key_word


class DictionaryWindow(QMainWindow):

    def __init__(self, geometryWindow, widowParent):
        super(DictionaryWindow, self).__init__()
        self.text_lineEdit = ''
        self._standard_model = None
        self._current_sound_file = ''
        self._current_word_id = 0
        self._current_translate_id = None
        self._current_select_data = SelectData.ALL
        self._current_standard_item = None
        self._current_selected_index_list_view = None
        self._player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self._player.setAudioOutput(self.audioOutput)
        self.setWindowTitle(window_title)
        self.geometryWindow = geometryWindow
        self.setGeometry(self.geometryWindow)
        self.windowParent = widowParent
        self.name = 'DictionaryWindow'
        minSize = QSize(int(geometryWindow.width() * minSizeWindow), int(geometryWindow.height() * minSizeWindow))
        self.setMinimumSize(minSize)
        self.toolbar = QToolBar("toolbar")
        self.addToolBar(self.toolbar)
        _icon_home = create_icon('home')
        button_action = QAction(_icon_home, "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        self.toolbar.addAction(button_action)

        self.layoutH = QHBoxLayout()
        self.layoutH_V = QVBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.textChanged.connect(self.textChanged)
        self.layoutH_V.addWidget(self.lineEdit)

        self.listW = QListView(self)
        self.model = Words()
        self.load()
        self.listW.doubleClicked.connect(self.getSelectIndex)

        self.listW.setModel(self.model)
        self.layoutH_V.addWidget(self.listW)
        self.leftWidget = QWidget()
        self.leftWidget.setLayout(self.layoutH_V)
        self.layoutH.addWidget(self.leftWidget, stretch=1)
        self.treeview = QTreeView()
        self.widget_bottom_right = QWidget()
        self.layout_grid_bottom_right = QGridLayout()
        self._label_word = QLabel('слово:')
        self._label_transcription = QLabel('транскрипция:')
        self._label_part_of_speach = QLabel('часть речи:')
        self._label_translate = QLabel('перевод:')
        self._label_example = QLabel('пример:')
        self._line_part_of_speach = QLineEdit()
        self._line_word = QLineEdit()
        self._line_transcription = QLineEdit()
        self._line_translate = QLineEdit()
        self._line_example = QLineEdit()
        self.layout_grid_bottom_right.addWidget(self._label_word, 0, 0)
        self.layout_grid_bottom_right.addWidget(self._label_transcription, 1, 0)
        self.layout_grid_bottom_right.addWidget(self._label_translate, 2, 0)
        self.layout_grid_bottom_right.addWidget(self._label_part_of_speach, 3, 0)
        self.layout_grid_bottom_right.addWidget(self._label_example, 4, 0)
        self.layout_grid_bottom_right.addWidget(self._line_word, 0, 1)
        self.layout_grid_bottom_right.addWidget(self._line_transcription, 1, 1)
        self.layout_grid_bottom_right.addWidget(self._line_translate, 2, 1)
        self.layout_grid_bottom_right.addWidget(self._line_part_of_speach, 3, 1)
        self.layout_grid_bottom_right.addWidget(self._line_example, 4, 1)
        self.widget_bottom_right.setLayout(self.layout_grid_bottom_right)
        self.widget_bottom_right.setHidden(True)
        self._label_word.setHidden(True)
        self._label_transcription.setHidden(True)
        self._label_part_of_speach.setHidden(True)
        self._label_translate.setHidden(True)
        self._label_example.setHidden(True)
        self._line_part_of_speach.setHidden(True)
        self._line_word.setHidden(True)
        self._line_transcription.setHidden(True)
        self._line_translate.setHidden(True)
        self._line_example.setHidden(True)
        self.treeview.setHeaderHidden(True)

        self.widgetRight = QWidget()
        self.layoutVWidgetRight = QVBoxLayout()  # правый вертикальный макет
        self.widgetTopRight = QWidget()
        self.layoutVWidgetRight.addWidget(self.widgetTopRight)
        self.widgetRight.setLayout(self.layoutVWidgetRight)
        self.iconSound = create_icon('sound')
        self.buttonSound = QPushButton(self.iconSound, '')
        self.buttonSound.clicked.connect(self.playSound)
        self.labelWord = QLabel('')
        self.labelWord.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelWord.setStyleSheet("font: 17pt")
        _icon_delete = create_icon('delete')
        _icon_clear = create_icon('broom')
        self.button_clear = QPushButton(_icon_clear, '')
        self.labelTranscription = QLabel('')
        self.labelTranscription.setStyleSheet('font: 15pt Georgia; color: DarkGrey')
        _icon_plus = create_icon('plus')
        _icon_save_db = create_icon('save_db')
        self.buttonAdd = QPushButton(_icon_plus, '')
        self.buttonAdd.setCheckable(True)
        self.button_delete = QPushButton(_icon_delete, '')
        self.button_delete.clicked.connect(self.delete)
        self.button_clear.clicked.connect(self.clear_treeview)
        self.buttonAdd.clicked.connect(self.add_data)
        self.button_save_db = QPushButton(_icon_save_db, '')
        self.button_save_db.clicked.connect(self.update_data_db)
        self.button_save_db.setVisible(False)
        self.layoutHWidgetTopRight = QHBoxLayout()
        self.layoutHWidgetTopRight.addWidget(self.buttonSound)
        self.layoutHWidgetTopRight.addWidget(self.labelWord, stretch=3)
        self.layoutHWidgetTopRight.addWidget(self.labelTranscription, stretch=3)
        self.layoutHWidgetTopRight.addWidget(self.buttonAdd)
        self.layoutHWidgetTopRight.addWidget(self.button_clear)
        self.layoutHWidgetTopRight.addWidget(self.button_save_db)
        self.layoutHWidgetTopRight.addWidget(self.button_delete)
        self.widgetTopRight.setLayout(self.layoutHWidgetTopRight)
        self.widgetForTree = QWidget()
        self.layoutForTree = QHBoxLayout()
        self.layoutForTree.addWidget(self.treeview)
        self.widgetForTree.setLayout(self.layoutForTree)
        self.layoutForTree.setContentsMargins(10, 0, 0, 0)
        self.layoutVWidgetRight.addWidget(self.widgetForTree, stretch=9)
        self.layoutVWidgetRight.addWidget(self.widget_bottom_right)
        self.layoutH.addWidget(self.widgetRight, stretch=2)

        widget = QWidget()
        widget.setLayout(self.layoutH)
        self.setCentralWidget(widget)

    def set_add_visible_all(self, is_visible):
        """
                    Устанавливает видимость поля "слово","транскрипция" "перевод", "пример", "часть речи"
                    :param is_visible: bool
                    :return:
                    """
        self.widget_bottom_right.setHidden(is_visible)
        self._label_word.setHidden(is_visible)
        self._label_transcription.setHidden(is_visible)
        self._label_part_of_speach.setHidden(is_visible)
        self._label_translate.setHidden(is_visible)
        self._label_example.setHidden(is_visible)
        self._line_part_of_speach.setHidden(is_visible)
        self._line_word.setHidden(is_visible)
        self._line_transcription.setHidden(is_visible)
        self._line_translate.setHidden(is_visible)
        self._line_example.setHidden(is_visible)

    def set_add_visible_translate(self, is_visible):
        """
              Устанавливает видимость поля "перевод", "пример", "часть речи"
              :param is_visible: bool
              :return:
              """
        self.widget_bottom_right.setHidden(is_visible)
        self._label_translate.setHidden(is_visible)
        self._label_part_of_speach.setHidden(is_visible)
        self._label_example.setHidden(is_visible)
        self._line_translate.setHidden(is_visible)
        self._line_part_of_speach.setHidden(is_visible)
        self._line_example.setHidden(is_visible)
        self._current_select_data = SelectData.TRANSLATE

    def set_add_visible_example(self, is_visible):
        """
        Устанавливает видимость поля "пример"
        :param is_visible: bool
        :return:
        """
        self.widget_bottom_right.setHidden(is_visible)
        self._label_example.setHidden(is_visible)
        self._line_example.setHidden(is_visible)
        self._current_select_data = SelectData.EXAMPLE

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent):
        """
        Действия при закрытии окна
        :param event:
        :return:
        """
        if not self.windowParent.isVisible():
            self.windowParent.show()
            self.windowParent.delete()

    @Slot()
    def onMyToolBarButtonClick(self):
        """
        Скрывает текущие окно и
        открывает родительское окно
        :param s:
        :return:
        """
        self.windowParent.show()
        self.hide()

    def add_data(self):
        """
        Открывает поля для данных
        и добавляет данные в TreeView
        :return: Any
        """
        if self.buttonAdd.isChecked():
            _indexes = self.treeview.selectedIndexes()
            if not _indexes:
                if self._current_word_id:
                    self.set_add_visible_translate(False)
                else:
                    self.set_add_visible_all(False)
            else:
                _item = self._standard_model.itemFromIndex(_indexes[0])
                self._current_standard_item = _item
                if type(_item) == QStandardItem:
                    self.set_add_visible_translate(False)
                if type(_item) == CustomItem and _item.name == 'Translate':
                    self._current_translate_id = _item.key_word['id']
                    self.set_add_visible_example(False)
                if type(_item) == CustomItem and _item.name == 'Example':
                    return

        else:
            self.set_add_visible_all(True)
            if self._current_select_data == SelectData.EXAMPLE:  # add example in model and db
                self.add_example()
            if self._current_select_data == SelectData.TRANSLATE:  # add translate, example, in model and db
                self.add_translate_example()

            if self._current_select_data == SelectData.ALL:  # add word, translate, example, in model and db
                self.add_word_translate_example()

    def add_example(self):
        """
        Добавляет пример в модель данных
        и сохраняет его в БД
        :return: Any
        """
        self.set_add_visible_all(True)
        if self._current_select_data == SelectData.EXAMPLE:  # add example in model and db
            _text_example = self._line_example.text().strip()
            if _text_example:
                _id = insert_data(self._current_translate_id, _text_example, index=10, window=self)

                _key_word_example = {'id': _id, 'TranslateId': self._current_translate_id, 'Example': _text_example}

                example_item = self.create_customItem(name='Example', key_word=_key_word_example,
                                                      parent=self._current_standard_item)
                count_row = self._current_standard_item.rowCount()
                self._current_standard_item.setChild(count_row, 0, example_item)
                self._standard_model.layoutChanged.emit()

    def add_translate_example(self):
        """
        Добавляет перевод и пример в модель данных
        и сохраняет в БД
        :return: Any
        """
        _text_translate = self._line_translate.text().strip()
        if not _text_translate:
            return
        _text_part_of_speach = self._line_part_of_speach.text().strip()
        _text_translate = self.convert_part_of_speach(_text_part_of_speach)
        _text_example = self._line_example.text().strip()
        _id = insert_data(self._current_word_id, _text_translate, _text_part_of_speach, index=11,
                          window=self)
        # _list_key_translate = ['Translate', 'PartOfSpeach']
        _key_word_translate = {'id': _id, 'WordId': self._current_word_id,
                               'Translate': _text_translate,
                               'PartOfSpeach': _text_part_of_speach}

        translate_item = self.create_customItem(name='Translate', key_word=_key_word_translate,
                                                parent=self._current_standard_item)

        if _text_example:
            id_ex = insert_data(_id, _text_example, index=10, window=self)
            _key_word_example = {'id': id_ex, 'TranslateId': _id,
                                 'Example': _text_example}
            example_item = self.create_customItem(name='Example', key_word=_key_word_example, parent=translate_item)
            count_row = translate_item.rowCount()
            translate_item.setChild(count_row, 0, example_item)
        count_row = self._current_standard_item.rowCount()
        self._current_standard_item.setChild(count_row, 0, translate_item)
        self._standard_model.layoutChanged.emit()

    def add_word_translate_example(self):
        """
        Добавляет слово, перевод, пример в модель данных TreeView
        и сохраняет в БД
        :return:
        """
        _text_word = self._line_word.text().strip()
        if not _text_word:
            return
        _sound_name = _text_word + '.wav'
        _text_transcription = self._line_transcription.text().strip()
        _text_translate = self._line_translate.text().strip()
        if not _text_translate:
            return
        _text_part_of_speach = self._line_part_of_speach.text().strip()
        _text_part_of_speach = self.convert_part_of_speach(_text_part_of_speach)
        _text_example = self._line_example.text().strip()
        _current_data = date.today()
        _word_id = insert_data(_text_word, _sound_name, _text_transcription, 1, _current_data, _current_data,
                               index=12,
                               window=self)
        _word_item = QStandardItem(_text_word)
        _word_item.setEditable(False)
        font_word = _word_item.font()
        font_word.setPointSize(16)
        _word_item.setFont(font_word)

        if _text_translate:
            _translate_id = insert_data(_word_id, _text_translate, _text_part_of_speach, index=11,
                                        window=self)
            _key_word_translate = {'id': _translate_id, 'WordId': _word_id,
                                   'Translate': _text_translate,
                                   'PartOfSpeach': _text_part_of_speach}
            translate_item = self.create_customItem(name='Translate', key_word=_key_word_translate, parent=_word_item)

            if _text_example:
                id_ex = insert_data(_translate_id, _text_example, index=10, window=self)
                _key_word_example = {'id': id_ex, 'TranslateId': _translate_id,
                                     'Example': _text_example}
                _example_item = self.create_customItem(name='Example', key_word=_key_word_example,
                                                       parent=translate_item)
                count_row = translate_item.rowCount()
                translate_item.setChild(count_row, 0, _example_item)
            count_row = _word_item.rowCount()
            _word_item.setChild(count_row, 0, translate_item)
            self._standard_model = QStandardItemModel(self)
            root_node = self._standard_model.invisibleRootItem()
            root_node.appendRow(_word_item)
            self.treeview.setModel(self._standard_model)
            self._standard_model.layoutChanged.emit()

    def load(self):
        """
        Загружает список слов из БД
        в ListView
        :return:
        """
        if load(self):
            self.model.words = select_data(self, 0)

    @Slot(str)
    def textChanged(self, s):
        """
        Фильтрует слова по начальным буквам
        :param s: строка
        :return: Any
        """
        self.text_lineEdit = s
        self.model.words = select_data_like(self, 1, s)
        self.model.layoutChanged.emit()

    def getSelectIndex(self):
        """
        Получаем индекс выделенного слова в ListView
        и добавляем элемент в модель TreeView
        :return:
        """
        listSelectedIndex = self.listW.selectedIndexes()
        index = listSelectedIndex[0]
        self._current_selected_index_list_view = index
        listData = self.model.words[index.row()]
        _word_id = listData[0]
        _word = listData[1]
        _sound_name = listData[2]
        self.setData(_word_id, _word)
        _path_audio = list_resources[0]
        self._current_sound_file = os.path.join(os.path.abspath(_path_audio), _sound_name)

    def setData(self, idWord, word):
        """
        Создает элемент (word, translate,example)
        и добавляет его в модель TreeView
        :param idWord: id
        :param word: word
        :return: Any
        """
        self._current_word_id = idWord
        self._standard_model = QStandardItemModel(self)
        root_node = self._standard_model.invisibleRootItem()
        word_item = QStandardItem(word)
        word_item.setEditable(False)
        font_word = word_item.font()
        font_word.setPointSize(16)
        word_item.setFont(font_word)
        list_data = select_data(self, 2, idWord)
        _tuple = list_data[0]
        self.labelTranscription.setText(_tuple[1])
        self.labelWord.setText(word)
        list_data = select_data(self, 3, idWord)
        for i in range(len(list_data)):
            m_tuple = list_data[i]
            _key_word_translate = {'id': m_tuple[0], 'WordId': m_tuple[1], 'Translate': m_tuple[2],
                                   'PartOfSpeach': m_tuple[3]}
            translate_item = self.create_customItem(name='Translate', key_word=_key_word_translate, parent=word_item)
            list_ex = select_data(self, 4, m_tuple[0])
            for k in range(len(list_ex)):
                tuple_ex = list_ex[k]
                _key_word_example = {'id': tuple_ex[0], 'TranslateId': tuple_ex[1], 'Example': tuple_ex[2]}
                example_item = self.create_customItem(name='Example', key_word=_key_word_example, parent=translate_item)
                translate_item.setChild(k, 0, example_item)
            word_item.setChild(i, 0, translate_item)
        root_node.appendRow(word_item)
        self.treeview.setModel(self._standard_model)
        self._standard_model.layoutChanged.emit()

    @Slot()
    def playSound(self):
        """
        Проигрывает звук
        :return:
        """
        _file = QUrl.fromLocalFile(self._current_sound_file)
        self._player.setSource(_file)
        self._player.play()

    @Slot()
    def delete(self):
        """
        Удаляет (слово, перевод, пример) в зависимости от
        выбора из модели TreeView
        :return:
        """
        _indexes = self.treeview.selectedIndexes()
        item_parent = None
        if _indexes:
            _item = self._standard_model.itemFromIndex(_indexes[0])
            button = messageBox_question(self, "Вы точно хотите удалить '{:s}'?".format(_item.text()))
            if button == QMessageBox.Yes:
                if type(_item) == CustomItem:
                    if _item.name == 'Translate':
                        delete_data(self, 6, _item.key_word['id'])  # delete translate
                        item_parent = _item.parent
                    else:
                        delete_data(self, 5, _item.key_word['id'])  # delete example
                        item_parent = _item.parent
                else:
                    delete_data(self, 7, self._current_word_id)  # delete word
                    del self.listW.model().words[self._current_selected_index_list_view.row()]
                    self.listW.model().layoutChanged.emit()
                    item_parent = self._standard_model.invisibleRootItem()
                    self.clear_treeview()
            item_parent.removeRow(_indexes[0].row())
            self._standard_model.layoutChanged.emit()
        else:
            messageBox_warning(self, 'ничего не выбрано')

    @Slot()
    def update_data_db(self):
        """
        Вносит в БД отредактированные значения
        перевода или примера:return:
        """
        root_node = self._standard_model.invisibleRootItem()
        _word_item = root_node.child(0, 0)
        for i in range(_word_item.rowCount()):
            _custom_item = _word_item.child(i)
            _translate_id = _custom_item.get_key_word['id']
            update_data(index=8, name=_custom_item.name, translate_id=_translate_id, window=self,
                        translate=_custom_item.get_key_word['Translate'],
                        part_of_speach=_custom_item.get_key_word['PartOfSpeach'])
            for k in range(_custom_item.rowCount()):
                _example_item = _custom_item.child(k)
                _id = _example_item.get_key_word['id']
                update_data(index=9, name=_example_item.name, translate_id=_id, window=self,
                            example=_example_item.get_key_word['Example'])
        if self.button_save_db.isVisible():
            self.button_save_db.setVisible(False)

    @Slot()
    def clear_treeview(self):
        """
        Удаляет текст из 'меток',
        и заменяет модель TreeView на пустую.
        :return:
        """
        self.labelWord.setText('')
        self.labelTranscription.setText('')
        self._current_word_id = None
        self._current_sound_file = ''
        self._standard_model = QStandardItemModel(self)
        self.treeview.setModel(self._standard_model)
        self._current_select_data = SelectData.ALL

    def create_customItem(self, name, key_word, parent) -> CustomItem:
        """
        Создает CustomItem
        :param name: Имя элемента
        :param key_word: словарь
        :param parent: родитель
        :return: CustomItem
        """
        return CustomItem(window=self, name=name, key_word=key_word, parent=parent)

    def convert_part_of_speach(self, s):
        _str = ''
        if s.startswith('сущ'):
            _str = 'сущ'
        if s.startswith('прил'):
            _str = 'прил'
        if s.startswith('гл'):
            _str = 'гл'
        if s.startswith('мест'):
            _str = 'мест'
        if s.startswith('нар'):
            _str = 'наречие'
        if s.startswith('числ'):
            _str = 'числительное'
        if s.startswith('союз'):
            _str = 'союз'
        if s.startswith('пред'):
            _str = 'предлог'
        if s.startswith('час'):
            _str = 'частица'
        if s.startswith('воск'):
            _str = 'восклицание'
        if s.startswith('арт'):
            _str = 'артикул'
        return _str
