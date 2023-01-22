# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'list_words.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                               QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                               QMainWindow, QMenuBar, QPushButton, QSizePolicy,
                               QSpacerItem, QStatusBar, QTableView, QVBoxLayout,
                               QWidget)
from Views.Generate.MyWidgets import MyTable2


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(840, 616)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.tableView = MyTable2(self.centralwidget)
        self.tableView.setObjectName(u"tableView")

        self.gridLayout.addWidget(self.tableView, 2, 1, 1, 2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 20, -1, -1)
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_2.addWidget(self.checkBox)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_2.addWidget(self.pushButton_5)

        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 2, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.verticalLayout_2.addWidget(self.lineEdit_2)

        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_3.addWidget(self.lineEdit)

        self.gridLayout.addLayout(self.verticalLayout_3, 1, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.horizontalSpacer_2 = QSpacerItem(108, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout.addWidget(self.pushButton_4)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 840, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0441\u043f\u0438\u0441\u043a\u0438:", None))
        self.checkBox.setText("")
        self.pushButton_2.setText(
            QCoreApplication.translate("MainWindow", u"\u0443\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.pushButton.setText(
            QCoreApplication.translate("MainWindow", u"\u0434\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.pushButton_5.setText(
            QCoreApplication.translate("MainWindow", u"\u0441\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow",
                                                        u"\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u043f\u0438\u0441\u043a\u0430:",
                                                        None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0441\u043b\u043e\u0432\u0430:", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow",
                                                             u"\u0441\u043e\u0437\u0434\u0430\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a",
                                                             None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow",
                                                             u"\u0443\u0434\u0430\u043b\u0438\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a",
                                                             None))
    # retranslateUi
