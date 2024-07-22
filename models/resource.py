from flask_mysqldb import MySQL
from datetime import datetime

class Resource:
    def __init__(self, name, resource_type_id, description, available_from, booked_by, booked_at):
        self.name = name
        self.resource_type_id = resource_type_id
        self.description = description
        self.available_from = available_from
        self.booked_by = booked_by
        self.booked_at = booked_at
        
    def save_to_db(self, mysql: MySQL):
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO resources (name, resource_type_id, description, available_from, booked_by, booked_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (self.name, self.resource_type_id, self.description, self.available_from, self.booked_by, self.booked_at))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_all_by_company(mysql: MySQL, company_id):
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT * FROM resources
            WHERE booked_by = %s
        ''', (company_id,))
        resources = cursor.fetchall()
        cursor.close()
        return resources
    
    @staticmethod
    def book(mysql: MySQL, resource_id, user_id):
        booked_at = datetime.now().date()
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE resources
            SET booked_by = %s, booked_at = %s
            WHERE id = %s
        ''', (user_id, booked_at, resource_id))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def release(mysql: MySQL, resource_id):
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE resources
            SET booked_by = NULL, booked_at = NULL
            WHERE id = %s
        ''', (resource_id,))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_all(mysql: MySQL):
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT * FROM resources
        ''')
        mysql.connection.commit()
        cursor.close()

    # @staticmethod
    # def get_by_type(mysql, resource_type_id):
    #     cursor = mysql.connection.cursor()
    #     cursor.execute('SELECT * FROM resources WHERE resource_type_id = %s', [resource_type_id])
    #     resources = cursor.fetchall()
    #     cursor.close()
    #     return resources

    # @staticmethod
    # def book_resource(mysql, resource_id, user_id):
    #     cursor = mysql.connection.cursor()
    #     cursor.execute('''
    #         UPDATE resources
    #         SET booked_by = %s, booked_at = CURDATE()
    #         WHERE id = %s
    #     ''', (user_id, resource_id))
    #     mysql.connection.commit()
    #     cursor.execute('''
    #         INSERT INTO bookings (resource_id, user_id, booked_at)
    #         VALUES (%s, %s, CURDATE())
    #     ''', (resource_id, user_id))
    #     mysql.connection.commit()
    #     cursor.close()

    # @staticmethod
    # def release_resource(mysql, resource_id):
    #     cursor = mysql.connection.cursor()
    #     cursor.execute('''
    #         UPDATE resources
    #         SET booked_by = NULL, booked_at = NULL
    #         WHERE id = %s
    #     ''', [resource_id])
    #     mysql.connection.commit()
    #     cursor.execute('''
    #         UPDATE bookings
    #         SET released_at = CURDATE()
    #         WHERE resource_id = %s AND released_at IS NULL
    #     ''', [resource_id])
    #     mysql.connection.commit()
    #     cursor.close()
