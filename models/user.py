from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password, user_type):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.user_type = user_type

    def save_to_db(self, mysql:MySQL):
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, user_type)
            VALUES (%s, %s, %s)
        ''', (self.username, self.password_hash, self.user_type))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_username(mysql: MySQL, username):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user_data = cursor.fetchone()
        cursor.close()
        return user_data

    @staticmethod
    def get_by_id(mysql: MySQL, user_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        return user_data