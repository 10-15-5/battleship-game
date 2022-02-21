import sqlite3

class CreateDatabase:

    def create(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, pw TEXT, wins INT, losses INT)")
        db.commit()
        db.close()


class UpdateDatabase:

    def __init__(self, username, pw=None):
        self.username = username
        self.pw = pw


    def user_win(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT wins from users WHERE username = ? ''' , (self.username,))
        wins = cursor.fetchone()
        wins = int(wins[0]) + 1
        cursor.execute('''UPDATE users set wins = ? where username = ? ''' , (wins,self.username))
        db.commit()
        db.close()


    def user_loss(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT losses from users WHERE username = ? ''' , (self.username,))
        losses = cursor.fetchone()
        losses = int(losses[0]) + 1
        cursor.execute('''UPDATE users set losses = ? where username = ? ''' , (losses,self.username))
        db.commit()
        db.close()


    def reset_password(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''UPDATE users set pw = ? where username = ? ''' , (self.pw,self.username))
        db.commit()
        db.close()


class SearchDatabase:

    def __init__(self, username=None):
        self.username = username


    def search_all(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM users''' )
        items = cursor.fetchall()
        db.close()

        return items

    
    def search_users(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT username FROM users''' )
        items = cursor.fetchall()
        db.close()

        return items
    
    
    def search_users_and_pw(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT username,pw FROM users''' )
        items = cursor.fetchall()
        db.close()

        return items

    def search_scores(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT wins,losses from users WHERE username = ? ''' , (self.username,))
        results = cursor.fetchone()
        db.close()

        return results


class CreateUser:

    def __init__(self, username, pw):
        self.username = username
        self.pw = pw


    def add(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute(''' INSERT INTO users(username,pw,wins,losses) values(?,?,0,0) ''', (self.username, self.pw))
        db.commit()
        db.close()


class LoginUser:

    def __init__(self, username, pw):
        self.username = username
        self.pw = pw

    def check_users(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT username FROM users''' )
        items = cursor.fetchall()
        for item in items:
            if item[0] == self.username:
                return True
        return False


    def check_pw(self):
        db = sqlite3.connect("battleship-database")
        cursor = db.cursor()
        cursor.execute('''SELECT username,pw FROM users''' )
        items = cursor.fetchall()
        for item in items:
            if item[0] == self.username:
                if item[1] == self.pw:
                    return True
        return False


