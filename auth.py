import sqlite3
from flask import session

DB_FILE_PATH = 'data/data.db'

class Auth:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def create_user(self, username, password):
        # Create a user with given password
        '''Create a user with given password'''
        data = (username, password)
        self.cursor.execute('insert into user (username, password) values (?, ?)', data)
        self.conn.commit()

    def login(self, username, password):
        # If we have a user with the given user name and password, return True.
        # Otherwise, return False
        self.cursor.execute('''select * from user ''')
        user_row = self.cursor.fetchall()
        user_list = []
        for i in user_row:
            a = i[1]
            b = i[2]
            user_list.append([a, b])
        if [username, password] in user_list:
            session['username'] = username
            return True
        else:
            return False

    def logout(self):
        session.pop('username', None)
        return

    def is_logged_in(self):
        return 'username' in session

    def get_current_user(self):
        if self.is_logged_in():
            user = session['username']
            self.cursor.execute('select * from user where username = ?', user)
            selected = self.cursor.fetchone()
            return selected
        return None

    def has_user(self, username):
        self.cursor.execute('select count(1) from user where username = ?', (username,))
        row = self.cursor.fetchone()
        count = row[0]
        return count > 0