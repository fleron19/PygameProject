import sys
import time
import datetime


from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QTimer
from random import randrange
import qdarkstyle


class WidgetRate(QMainWindow):
    def __init__(self, curuser, con):
        super().__init__()
        uic.loadUi('rate.ui', self)
        self.back.clicked.connect(self.goback)
        self.curUser = curuser
        self.con = con
        st = "select * from Games WHERE IdUser = " + str(self.curUser.iduser)
        res = self.con.cursor().execute(st).fetchall()
        result = []
        for i in res:
            tup = tuple(
                item for item in i if item != self.curUser.iduser
            )
            result.append(tup)

        # Заполним размеры таблицы
        self.tableWidget.setRowCount(len(res))

        self.tableWidget.setColumnCount(9)
        for i in range(10):
            self.tableWidget.setColumnWidth(i, 150)
        self.tableWidget.setHorizontalHeaderLabels(["ID Игры", "Результат", "Название", "Смертность", "Заразность",
                                                    "Срок болезни", "Зона заражения", "Инкуб. Период",
                                                    "Время иммунитета"])

        # Заполняем таблицу элементами
        m = -1
        for i, elem in enumerate(reversed(result)):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def goback(self):
        from Profile import ProfileWindow
        self.m = ProfileWindow(self.curUser, self.con)
        self.m.show()
        self.close()
