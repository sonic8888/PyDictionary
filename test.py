import sys, os
import sqlite3
from sqlite3 import connect, Cursor
from typing import Any
import re
from enum import Enum
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap

from PySide6.QtCore import QSize, Qt, Slot, QItemSelection
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QListView

from Servise.tools import request, ConnectDb, get_data_general

select_word = "SELECT Word, Transcription, SoundName FROM Words WHERE WordId = {:d}"
select_translates = "SELECT TranslateId, Translate, PartOfSpeach FROM Translates WHERE WordId = {:d}"
select_examples = "SELECT Example FROM Examples WHERE TranslateId = {:d}"

regx_pattern = r'\w+\s?\(\w+\)'
regx_split_pattern = r'\s?\('


class MyItem(QStandardItem):
    def __init__(self, words=None, *args, **kwargs):
        super(MyItem, self).__init__(*args, **kwargs)
        self.words = words or []

    def data(self, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            text = '{} ({})'.format(self.words[0], self.words[1])
            return text

    def setData(self, value: Any, role: int = ...) -> None:
        if role == Qt.EditRole:
            if re.fullmatch(regx_pattern, value):
                _list_val = re.split(regx_split_pattern, value)
                _list_val[1] = _list_val[1][:-1]
                self.words = _list_val
            else:
                print('No Match!')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        icon = QIcon('Icons/database_dark.png')
        self._standard_model = QStandardItemModel(self)
        self.root_node = self._standard_model.invisibleRootItem()
        self.item1 = QStandardItem("one")
        # self.item2 = QStandardItem()
        # self.item2.setData("Two", Qt.DisplayRole)
        self.item2 = MyItem(['addition', 'сущ'])
        self.item3 = QStandardItem("Three")
        self.root_node.appendRow(self.item1)
        self.root_node.appendRow(self.item2)
        self.root_node.appendRow(self.item3)
        self.layout = QVBoxLayout()
        pm = QPixmap('Icons/database_dark.png')
        self.label = QLabel("test")
        self.label.setPixmap(pm)
        self.label.setWindowIcon(icon)
        self.listView = QListView()
        self.listView.setModel(self._standard_model)
        self.button = QPushButton(icon, "Press ME")
        # self.button.setWindowIcon(icon)
        self.button.clicked.connect(self.clicked)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.listView)
        self.layout.addWidget(self.button)
        widjet_icon = QWidget()
        widjet_icon.setWindowIcon(icon)
        self.layout.addWidget(widjet_icon)
        self.widget = QWidget()
        self.selection_model = self.listView.selectionModel()
        self.selection_model.selectionChanged.connect(self.selection_changed_slot)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.index = None

    @Slot(QItemSelection, QItemSelection)
    def selection_changed_slot(self, new_selection, old_selection):
        self.index = self.selection_model.currentIndex()
        # selected_text = index.data(Qt.DisplayRole)
        # hierarchy_level = 1
        # seek_root = index
        # while seek_root.parent().isValid():
        #     seek_root = seek_root.parent()
        #     hierarchy_level += 1
        #     print(seek_root)
        #     print(hierarchy_level)

    def clicked(self):
        # model = self.listView.model()
        # strr = model.data(self.index)
        print(self.index.row())
        child = self.root_node.child(self.index.row(), 0)


def main():
    list_t = [('one', 'ooo'), ('two', 'tttt'), ('three', 'tttt'), ('one', 'ooo',)]
    s = set(list_t)
    for item in s:
        print(item)


class Test:
    def __init__(self, **kwargs):
        _my_dic = {'path_name': None, 'time': 500, 'url': False}
        print(type(kwargs))
        for key, value in kwargs.items():
            if key in _my_dic:
                _my_dic[key] = value
        self.path_name = _my_dic['path_name']
        self.time = _my_dic['time']
        self.url = _my_dic['url']
        print(f'path_name: {self.path_name}, time: {self.time}, url: {self.url}')


def test_fun(con, cur, fun_execute, fun_fetch, sql, my_tuple):
    # res = cur.my_function(sql, my_tuple)
    f = getattr(cur, fun_execute)
    f(sql, my_tuple)
    fetch = getattr(cur, fun_fetch)
    res = fetch()
    print(res[0])
    cur.close()
    con.close()
    # cur.__getattribute__(my_function)


def create_test(**kwargs):
    x = kwargs.get('x', 67)
    y = kwargs.get('y', 'yes')
    z = kwargs.get('x', True)
    print("x=%s, y=%s, z=%s" % (x, y, z))


if __name__ == '__main__':
    # create_test(y='word', x=5, z=89, f=67)
    portfolio = [
        {'name': 'IBM', 'shares': 100, 'price': 91.1},
        {'name': 'MSFT', 'shares': 50, 'price': 45.67},
        {'name': 'HPE', 'shares': 75, 'price': 34.51},
        {'name': 'CAT', 'shares': 60, 'price': 67.89},
        {'name': 'IBM', 'shares': 200, 'price': 95.25}
    ]

    # _l_name = [item['name'] for item in portfolio if item['shares'] > 100]
    # print(_l_name)
    for i , item in enumerate(portfolio, start=100):
        print(i)