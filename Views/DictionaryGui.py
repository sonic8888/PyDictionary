import re
from typing import Any
from Views.MessageBoxess import *
import PySide6
from PySide6 import QtCore
from PySide6.QtCore import QSize, QRect, Qt, Slot, QItemSelection
from PySide6.QtGui import QPalette, QColor, QAction, QIcon, QMouseEvent, QStandardItemModel, QStandardItem, QFont, \
    QBrush
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QToolBar, QListWidget, QListView, \
    QLineEdit, QTreeView, QTableView, QPushButton, QLabel
from Models.WordsModel import Words
from Servise.Db.Sqlite.SqliteApplication import select_data

import main
from Servise.Variable import minSizeWindow, maxSizeWindow

regx_pattern = r'\w+\s?\(\w+\)'
regx_split_pattern = r'\s?\('


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
                message_critical_(self.window, 'No Match!')

    def type(self) -> int:
        return 13456794


class DictionaryWindow(QMainWindow):
    def __init__(self, geometryWindow, widowParent):
        super(DictionaryWindow, self).__init__()
        self.text_lineEdit = ''
        self._standard_model = None
        self.setWindowTitle("Dictionary")
        self.geometryWindow = geometryWindow
        self.setGeometry(self.geometryWindow)
        self.windowParent = widowParent
        self.name = 'DictionaryWindow'
        minSize = QSize(int(geometryWindow.width() * minSizeWindow), int(geometryWindow.height() * minSizeWindow))
        self.setMinimumSize(minSize)
        self.toolbar = QToolBar("toolbar")
        self.addToolBar(self.toolbar)
        # QAction
        button_action = QAction(QIcon('Icons/home_white.png'), "Your button", self)
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
        # self.treeview.setModel(self._standard_model)
        self.treeview.setHeaderHidden(True)

        # self.treeview.expandAll()
        self.widgetRight = QWidget()
        self.layoutVWidgetRight = QVBoxLayout()
        self.widgetTopRight = QWidget()
        self.layoutVWidgetRight.addWidget(self.widgetTopRight)
        self.widgetRight.setLayout(self.layoutVWidgetRight)
        self.iconSound = QIcon('Icons/speaker-32.png')
        self.buttonSound = QPushButton(self.iconSound, '')
        self.buttonSound.clicked.connect(self.playSound)
        self.labelWord = QLabel('')
        self.labelWord.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelWord.setStyleSheet("font: 17pt")

        self.labelTranscription = QLabel('')
        self.labelTranscription.setStyleSheet('font: 15pt Georgia; color: lightGrey')
        # self.labelTranscription.setStyleSheet('color: red')
        self.layoutHWidgetTopRight = QHBoxLayout()
        self.layoutHWidgetTopRight.addWidget(self.buttonSound)
        self.layoutHWidgetTopRight.addWidget(self.labelWord, stretch=3)
        self.layoutHWidgetTopRight.addWidget(self.labelTranscription, stretch=3)
        self.widgetTopRight.setLayout(self.layoutHWidgetTopRight)
        self.widgetForTree = QWidget()
        self.layoutForTree = QHBoxLayout()
        self.layoutForTree.addWidget(self.treeview)
        self.widgetForTree.setLayout(self.layoutForTree)
        self.layoutForTree.setContentsMargins(10, 0, 0, 0)
        self.layoutVWidgetRight.addWidget(self.widgetForTree, stretch=9)
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
        data = listData[1]
        wordId = listData[0]
        self.setData(wordId, data)

    def test(self):
        print("hello")

    def setData(self, idWord, word):
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
        selection_model = self.treeview.selectionModel()
        selection_model.selectionChanged.connect(self.selection_changed_slot)

    def playSound(self):
        print(self.current_sound)

    @Slot(QItemSelection, QItemSelection)
    def selection_changed_slot(self, new_selection, old_selection):
        print("selection_changed_slot")
