from db_connection import *
from datetime import * 
class User: 
    def __init__(self, id=None, email=None, username=None, phone=None, age=None, pin_code=None, vaccination_date=None, vaccination_centre=None, slot=None):
        self.db_connection = DatabaseConnection()
        self.id = id
        self.email = email 
        self.username = username
        self.phone = phone
        self.age = age 
        self.pin_code = pin_code
        self.vaccination_date = vaccination_date
        self.vaccination_centre = vaccination_centre
        self.slot = slot

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            phone BIGINT NOT NULL, 
            age INTEGER NOT NULL,
            pin_code INTEGER NOT NULL,
            vaccination_date DATE NOT NULL,
            vaccination_centre VARCHAR(255) NOT NULL, 
            slot VARCHAR(255) NOT NULL
        );
        """
        self.db_connection.create_table(sql)

    def create_class_instance(self, data):
        id = data[0]
        email = data[1]
        username = data[2]
        phone = data[3]
        age = data[4]
        pin_code = data[5]
        vaccination_date = data[6]
        vaccination_centre = data[7]
        slot = data[8]

        user = User(id, email, username, phone, age, pin_code, vaccination_date, vaccination_centre, slot)

        return user 

    def create(self, params):
        self.db_connection.create(params, "users")

    def update(self, id, params):
        self.db_connection.update(id, params, 'users')

    def find(self, params):
        data = self.db_connection.find(params, "users")
        results = []

        for datum in data:
            instance = self.create_class_instance(datum)
            results.append(instance)

        return results

    def find_by_id(self, id):
        data = self.db_connection.find_by_id(id, 'users')
        result = self.create_class_instance(data)
        return result

    def delete(self, id):
        self.db_connection.delete(id, 'users')
    
    def delete_all(self):
        self.db_connection.delete_all()

    def already_exists(self, params):
        user = self.find(params)
        return len(user) != 0

#u.create_table()
#u.create({'email': 'tEstUSer3@gmail.com', 'username': 'Test User 3', 'phone': 9999999999, 'age': 19, 'pin_code': 110010, 'vaccination_date': '09-02-2022', 'vaccination_centre': 'None', 'slot': 'None'})