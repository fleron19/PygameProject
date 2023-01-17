import sys
import time
import datetime


from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer
from random import randrange


class WidgetRate(QMainWindow):
    def __init__(self, curuser, con):
        super().__init__()
        print(1)
        uic.loadUi('rate.ui', self)
        print(4)
        self.back.clicked.connect(self.goback)
        print(3)
        self.curUser = curuser
        self.con = con
        print(2)
        st = "select * from Games WHERE IdUser = " + str(self.curUser.iduser)
        res = self.con.cursor().execute(st).fetchall()
        del res[1]
        del res[0]
        print(res)
        # Заполним размеры таблицы
        self.tableWidget.setRowCount(len(res))

        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(["Статус", "Название", "1", "3", "4", "5", "6", "7"])

        # Заполняем таблицу элементами
        m = -1
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def goback(self):
        from Profile import ProfileWindow
        self.m = ProfileWindow(self.curUser, self.con)
        self.m.show()
        self.close()
