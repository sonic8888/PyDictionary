import re
import os
from typing import Any
import PySide6
from PySide6.QtCore import QSize, Qt, Slot, QItemSelection, QUrl
from PySide6.QtGui import QPalette, QAction, QStandardItemModel, QStandardItem, QFont
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QToolBar, QListView, \
    QLineEdit, QTreeView, QPushButton, QLabel, QGridLayout

from DataSettings import create_icon, list_resources, window_title
from Models.WordsModel import Words
from Servise.Db.Sqlite.SqliteApplication import select_data
from Servise.Variable import minSizeWindow
from Views.MessageBoxess import *

regx_pattern = r'\w+\s?\(\w+\)'
regx_split_pattern = r'\s?\('


class TreeView(QTreeView):
    def __init__(self):
        super(TreeView, self).__init__()

    def mousePressEvent(self, e):
        super(TreeView, self).mousePressEvent(e)
        if e.button() == Qt.MouseButton.RightButton:
            index = self.selectedIndexes()
            index = index[0]
            item = self.model().item(index.row(), 0)
            item.removeRow(0)
            self.model().layoutChanged.emit()
            # del item
            # model.layoutChanged.emit()
            # root = self.model().invisibleRootItem()
            # print(root.hasChildren())


class TranslateItem(QStandardItem):
    def __init__(self, window, words=None, *args, **kwargs):
        super(TranslateItem, self).__init__(*args, **kwargs)
        self.words = words or []
        self.window = window

    def data(self, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            text = '{} ({})'.format(self.words[0], self.words[1])
            return text
        if role == Qt.FontRole:
            font = QFont()
            font.setPointSize(15)
            return font

    def setData(self, value: Any, role: int = ...) -> None:
        if role == Qt.EditRole:
            if re.fullmatch(regx_pattern, value):
                _list_val = re.split(regx_split_pattern, value)
                _list_val[1] = _list_val[1][:-1]
                self.words = _list_val
            else:
                print()
                message_critical_(self.window, 'укажите "перевод слова" и "часть речи" в скобках')

    def type(self) -> int:
        return 13456794


class DictionaryWindow(QMainWindow):
    def __init__(self, geometryWindow, widowParent):
        super(DictionaryWindow, self).__init__()
        self.text_lineEdit = ''
        self._standard_model = None
        self._current_sound_file = ''
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
        self.current_word_id = 0
        # QAction
        _icon_home = create_icon('home')
        button_action = QAction(_icon_home, "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        self.toolbar.addAction(button_action)

        # self.set_data()

        self.layoutH = QHBoxLayout()
        self.layoutH_V = QVBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.textChanged.connect(self.textChanged)
        self.lineEdit.returnPressed.connect(self.get_data)
        self.layoutH_V.addWidget(self.lineEdit)

        self.listW = QListView(self)
        self.model = Words()
        self.load()
        self.listW.doubleClicked.connect(self.getSelectIndex)
        # self.listW.clicked.connect(self.getSelectIndex)

        self.listW.setModel(self.model)
        self.layoutH_V.addWidget(self.listW)
        # self.listW.addItems(["One", "Two", "Three"])
        self.leftWidget = QWidget()
        self.leftWidget.setLayout(self.layoutH_V)
        self.layoutH.addWidget(self.leftWidget, stretch=1)
        self.treeview = QTreeView()
        self.widget_bottom_right = QWidget()
        self.layout_grid_bottom_right = QGridLayout()
        _label_part_of_speach = QLabel('часть речи:')
        _label_translate = QLabel('перевод:')
        _label_example = QLabel('пример:')
        self._line_part_of_speach = QLineEdit()
        self._line_translate = QLineEdit()
        self._line_example = QLineEdit()
        self.layout_grid_bottom_right.addWidget(_label_part_of_speach, 0, 0)
        self.layout_grid_bottom_right.addWidget(_label_translate, 1, 0)
        self.layout_grid_bottom_right.addWidget(_label_example, 2, 0)
        self.layout_grid_bottom_right.addWidget(self._line_part_of_speach, 0, 1)
        self.layout_grid_bottom_right.addWidget(self._line_translate, 1, 1)
        self.layout_grid_bottom_right.addWidget(self._line_example, 2, 1)
        self.widget_bottom_right.setLayout(self.layout_grid_bottom_right)
        self.widget_bottom_right.setHidden(True)
        # self.treeview.setModel(self._standard_model)
        self.treeview.setHeaderHidden(True)

        # self.treeview.expandAll()
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
        # self.action_delete = QAction(_icon_delete, 'delete', self)
        # self.action_delete.setStatusTip('delete selected item')
        # self.action_delete.triggered.connect(self.delete)

        self.labelTranscription = QLabel('')
        self.labelTranscription.setStyleSheet('font: 15pt Georgia; color: DarkGrey')
        # self.iconAdd = QIcon('Icons/plus-5-64.png')
        # self.iconTest = QIcon.fromTheme('edit-undo')
        _icon_plus = create_icon('plus')
        _icon_save_db = create_icon('save_db')
        self.buttonAdd = QPushButton(_icon_plus, '')
        self.button_delete = QPushButton(_icon_delete, '')
        self.button_delete.clicked.connect(self.delete)

        self.buttonAdd.clicked.connect(self.add_translate)
        self.button_save_db = QPushButton(_icon_save_db, '')
        self.button_save_db.clicked.connect(self.save_to_db)
        self.button_save_db.setVisible(False)
        self.layoutHWidgetTopRight = QHBoxLayout()
        self.layoutHWidgetTopRight.addWidget(self.buttonSound)
        self.layoutHWidgetTopRight.addWidget(self.labelWord, stretch=3)
        self.layoutHWidgetTopRight.addWidget(self.labelTranscription, stretch=3)
        self.layoutHWidgetTopRight.addWidget(self.buttonAdd)
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

        self.current_sound = ''
        # self.setData(1, 'addition')
        widget = QWidget()
        widget.setLayout(self.layoutH)
        self.setCentralWidget(widget)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent):
        if not self.windowParent.isVisible():
            self.windowParent.show()
            self.windowParent.delete()

    def onMyToolBarButtonClick(self, s):
        self.windowParent.show()
        self.hide()

    def add_translate(self):
        if not self.button_save_db.isVisible():
            self.button_save_db.setVisible(True)
        if self.widget_bottom_right.isHidden():
            self.widget_bottom_right.setHidden(False)
        else:
            self.widget_bottom_right.setHidden(True)

    def save_to_db(self):
        if self.button_save_db.isVisible():
            self.button_save_db.setVisible(False)

    def load(self):
        self.model.words = select_data(self)

    def textChanged(self, s):
        self.text_lineEdit = s
        self.model.words = select_data(self, 1, s)
        self.model.layoutChanged.emit()

    def get_data(self):
        print(self.text_lineEdit)

    def getSelectIndex(self):
        listSelectedIndex = self.listW.selectedIndexes()
        index = listSelectedIndex[0]
        listData = self.model.words[index.row()]
        _word_id = listData[0]
        _word = listData[1]
        _sound_name = listData[2]
        self.setData(_word_id, _word)
        _path_audio = list_resources[0]
        self._current_sound_file = os.path.join(os.path.abspath(_path_audio), _sound_name)

    def setData(self, idWord, word):
        self.current_word_id = idWord
        self._standard_model = QStandardItemModel(self)
        root_node = self._standard_model.invisibleRootItem()

        word_item = QStandardItem(word)
        font_word = word_item.font()
        font_word.setPointSize(16)
        word_item.setFont(font_word)

        list_data = select_data(self, 2, idWord)
        _tuple = list_data[0]
        self.current_sound = _tuple[2]
        self.labelTranscription.setText(_tuple[1])
        self.labelWord.setText(word)

        list_data = select_data(self, 3, idWord)
        for i in range(len(list_data)):
            m_tuple = list_data[i]
            list_translate_speach = [m_tuple[1], m_tuple[2]]
            translate_item = TranslateItem(self, list_translate_speach)
            list_ex = select_data(self, 4, m_tuple[0])
            for k in range(len(list_ex)):
                tuple_ex = list_ex[k]
                example_item = QStandardItem(tuple_ex[0])
                font_ex = example_item.font()
                font_ex.setPointSize(12)
                example_item.setFont(font_ex)
                translate_item.setChild(k, 0, example_item)
            word_item.setChild(i, 0, translate_item)
        root_node.appendRow(word_item)
        self.treeview.setModel(self._standard_model)
        self._standard_model.layoutChanged.emit()
        # selection_model = self.treeview.selectionModel()
        # selection_model.selectionChanged.connect(self.selection_changed_slot)

    def playSound(self):
        _file = QUrl.fromLocalFile(self._current_sound_file)
        self._player.setSource(_file)
        self._player.play()

    @Slot(QItemSelection, QItemSelection)
    def selection_changed_slot(self, new_selection, old_selection):
        print(old_selection)

    @Slot()
    def delete(self):
        _indexes = self.treeview.selectedIndexes()
        if _indexes:
            _index = _indexes[0].parent()
            self._standard_model.removeRow(0, _index)
            self._standard_model.layoutChanged.emit()

    @Slot
    def save_to_db(self):
        root_node = self._standard_model.invisibleRootItem()
        _word_item = root_node.child(0, 0)
        text = _word_item.text()
        for i in range(_word_item.rowCount()):
            _translate_item = _word_item.child(i)
            if type(_translate_item) == TranslateItem:
                words = _translate_item.words
                for k in range(_translate_item.rowCount()):
                    _example_item = _translate_item.child(k)
                    item_text = _example_item.text()
