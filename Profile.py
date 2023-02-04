from PyQt5 import uic
from subprocess import call

import qdarkstyle
from PyQt5 import uic
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from WinRate import WidgetRate


class ProfileWindow(QMainWindow):
    def __init__(self, user, con):
        # окно личного кабинета
        super().__init__()
        uic.loadUi('profileWin.ui', self)
        self.btnPlay.clicked.connect(self.Play)
        self.btnHistory.clicked.connect(self.history)
        self.btnImage.clicked.connect(self.getImage)
        self.curUser = user
        self.con = con
        self.lblUser.setText(self.lblUser.text() + ' ' + user.getLogin() + '!')
        result = self.con.cursor().execute("""SELECT * FROM Games where IdUser = ? and status = 'победа'""",
                                           (self.curUser.iduser,)).fetchall()
        # выводим рейтинг в личный кабинет
        self.Bal.setText(str(len(result)))
        self.id.setText(str(self.curUser.iduser))
        if QFile.exists("avatars/" + str(self.curUser.iduser) + ".jpg"):
            pixmap = QPixmap("avatars/" + str(self.curUser.iduser) + ".jpg")
        else:
            pixmap = QPixmap("avatars/user.png")
        pixmap = pixmap.scaledToWidth(80)
        pixmap = pixmap.scaledToHeight(80)
        self.lblImage_2.setPixmap(pixmap)
        self.lblImage_2.show()  # выводим в личный кабинет аватар пользователя
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.goback()
        event.accept()

    def goback(self):
        from Main_start import WidgetAuth
        self.m = WidgetAuth()
        self.m.show()
        self.close()

    def Play(self):
        lnme = 10
        print(2)
        self.m = SettingGame(self.curUser, self.con)
        print(3)
        self.m.show()
        self.close()

    def history(self):
        self.m = WidgetRate(self.curUser, self.con)
        self.m.show()
        self.close()

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        if fname != '':
            fname2 = "avatars/" + str(self.curUser.iduser) + ".jpg"
            pixmap = QPixmap(fname)
            p2 = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
            p2.save(fname2)

            self.lblImage_2.setPixmap(p2)
            self.lblImage_2.show()


class SettingGame(QMainWindow):
    def __init__(self, user, con):
        super().__init__()
        print(1)
        self.curUser = user
        self.con = con
        uic.loadUi('settingGame.ui', self)
        self.back.clicked.connect(self.goback)
        self.btnPlay.clicked.connect(self.start_game)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def start_game(self):
        print(4)
        cur = self.con.cursor()
        # self.curUser = user
        dan = [self.curUser.iduser, 'online', self.lbl_name.text(), int(self.lbl_mortality.text()),
               int(self.lbl_contagious.text()), int(self.lbl_term.text()), int(self.lbl_zona.text()),
               int(self.lbl_period.text()), int(self.lbl_time_vac.text())]
        print(0)
        # strQuery = "Update Games set Mort = ? where IdGame = ?"  # обновляем рейтинг игрока
        # cur.execute(strQuery, (dan[1], 1))
        strQuery = "Insert into Games (IdUser, status, virusname, mort, cont, term, zona, period, timevac) values(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        print(strQuery)
        print(dan)
        cur.execute(strQuery, (dan[0], dan[1], dan[2], dan[3], dan[4], dan[5], dan[6], dan[7], dan[8]))
        self.con.commit()
        call(["python", "main.py"])

    def goback(self):
        self.m = ProfileWindow(self.curUser, self.con)
        self.m.show()
        self.close()
