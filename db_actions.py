import sqlite3

class CreateDatabase:

    def create(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS logins(username TEXT, pw TEXT)")
        db.commit()
        db.close()


class SearchDatabase:

    def __init__(self) -> None:
        pass


    def search_all(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM logins''' )
        items = cursor.fetchall()
        db.close()

        return items

    
    def search_users(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT username FROM logins''' )
        items = cursor.fetchall()
        db.close()

        return items
    
    
    def search_users_and_pw(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT username,pw FROM logins''' )
        items = cursor.fetchall()
        db.close()

        return items


    def search_highscores(self):
        pass


class CreateUser:

    def __init__(self, username, pw):
        self.username = username
        self.pw = pw


    def add(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute(''' INSERT INTO logins(username,pw) values(?,?) ''', (self.username, self.pw))
        db.commit()
        db.close()


class LoginUser:

    def __init__(self, username, pw):
        self.username = username
        self.pw = pw

    def check_users(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT username FROM logins''' )
        items = cursor.fetchall()
        for item in items:
            if item[0] == self.username:
                return True
        return False


    def check_pw(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT username,pw FROM logins''' )
        items = cursor.fetchall()
        for item in items:
            if item[0] == self.username:
                if item[1] == self.pw:
                    return True
        return False


