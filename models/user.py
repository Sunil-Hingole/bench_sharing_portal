from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password, user_type):
        self.username = username
        self.password = password
        self.user_type = user_type

    def save_to_db(self, db):
        cursor = db.connection.cursor()  # Adjusted to use db.connection.cursor()
        query = "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)"
        cursor.execute(query, (self.username, self.password, self.user_type))
        db.connection.commit()
        cursor.close()


    @staticmethod
    def get_by_username(db, username):
        cursor = db.connection.cursor()  # Adjusted to use db.connection.cursor()
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result

    @staticmethod
    def get_by_id(mysql: MySQL, user_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        return user_data