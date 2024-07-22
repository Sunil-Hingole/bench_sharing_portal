from flask_mysqldb import MySQL

class ResourceType:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def save_to_db(self, mysql:MySQL):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO resource_types (name, description) VALUES (%s, %s)", 
                    (self.name, self.description))
        mysql.connection.commit()
        cursor.close() 

    @staticmethod
    def get_all(mysql:MySQL):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM resource_types")
        resource_types = cursor.fetchall()
        cursor.close()
        return resource_types
    

    @staticmethod
    def get_by_id(mysql: MySQL, id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM resource_types WHERE id = %s', (id,))
        resource_type = cursor.fetchone()
        cursor.close()
        return resource_type

    @staticmethod
    def update(mysql: MySQL, id, name, description):
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE resource_types
            SET name = %s, description = %s
            WHERE id = %s
        ''', (name, description, id))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def delete(mysql: MySQL, id):
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM resource_types WHERE id = %s', (id,))
        mysql.connection.commit()
        cursor.close()