import sys
import time
import sqlite3
import random
import datetime
import qdarkstyle


from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer, QFile
from random import randrange
from WinRate import WidgetRate
from Sluz import *
from Profile import ProfileWindow
from PyQt5.QtCore import Qt


CONST_DBNAME = 'virusDB.db'


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        # Основное окно для запуска
        uic.loadUi('helloWin.ui', self)
        self.avtor.clicked.connect(self.get)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def get(self):
        # переход к окну Авторизации
        self.m = WidgetAuth()
        self.m.show()
        self.close()


class WidgetAuth(QMainWindow):
    def __init__(self):
        # окно авторизации
        super().__init__()
        uic.loadUi('authorize.ui', self)
        self.enter.clicked.connect(self.check_password)
        self.zareg.clicked.connect(self.registration)
        self.back.clicked.connect(self.goback)
        self.con = sqlite3.connect(CONST_DBNAME)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def keyPressEvent(self, event):
        # выход из окна по esc
        if event.key() == Qt.Key_Escape:
            self.goback()
        event.accept()

    def check_password(self):
        # проверка пароля и существования пользователя
        try:
            if self.login_user.text() == "" or self.pwd_user.text() == "":
                raise UserInvalidData()  # вызываем ошибку из-за не заполенных полей
            else:
                result = self.con.cursor().execute("""SELECT login, IdUser, rating FROM users where login = ? and pwd = ?""", (self.login_user.text(), self.pwd_user.text())).fetchone()  # находим пользователя с задаными логином и паролем
                if not(result is None):
                    self.curUser = User(self.login_user.text(), result[1], result[2])
                    self.t = ProfileWindow(self.curUser, self.con)
                    self.t.show()
                    self.close()
                else:
                    raise UserNotExists()  # вызываем ошибку из-за отсутствия такого пользователя

        except UserInvalidData as e:
            self.errorLabel.setText("Заполните все поля")
        except UserNotExists as e:
            self.errorLabel.setText("Неправильный логин/пароль")
        except Exception as e:
            self.errorLabel.setText('Непредвиденная ошибка %s' % e)

    def registration(self):
        # регестрируем нового пользователя
        cur = self.con.cursor()
        try:
            if self.login_user.text() == "" or self.pwd_user.text() == "":
                raise UserInvalidData()  # вызываем ошибку из-за не заполенных полей
            else:
                result = cur.execute("""SELECT * FROM users where login = ?""", (self.login_user.text(),)).fetchone()
                if result is None:
                    strQuery = "Insert into users (login, pwd) values(?,?)"
                    cur.execute(strQuery, (self.login_user.text(), self.pwd_user.text()))
                    iduser = cur.lastrowid
                    self.con.commit()
                    self.curUser = User(self.login_user.text(), iduser, 0)
                    self.t = ProfileWindow(self.curUser, self.con)
                    self.t.show()
                    self.close()
                else:
                    raise UserAlreadyExists()  # вызываем ошибку из-за уже существующего пользователя

        except UserInvalidData as e:
            self.errorLabel.setText("Заполните все поля")
        except UserAlreadyExists as e:
            self.errorLabel.setText("Логин занят")
        except Exception as e:
            self.errorLabel.setText('Непредвиденная ошибка %s' % e)

    def goback(self):
        self.m = MyWidget()
        self.m.show()
        self.close()              


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
