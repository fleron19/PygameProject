CONST_DBNAME = "geography.db"
CONST_QUESTCOUNT = 5


class User():
    # класс для хранения всех данных про игрока
    def __init__(self, login, userid, rating):
        self.login = login
        self.iduser = userid
        self.testid = 0
        self.rezhim = 'test'
        self.questcount = CONST_QUESTCOUNT
        self.rating = rating
        self.errNum = 0

    def getLogin(self):
        return self.login

    def rateUpdate(self, rat):
        self.rating = rat


class UserError(Exception):
    pass


class UserInvalidData(UserError):
    pass


class UserAlreadyExists(UserError):
    pass


class UserNotExists(UserError):
    pass


class GameError(Exception):
    pass


class GameNotExists(GameError):
    pass


class DBException(Exception):
    pass
