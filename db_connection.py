import psycopg2

class DatabaseConnection:
    
    def __init__(self):
        self.connection = psycopg2.connect("dbname=vaccination_details user=YOUR_POSTGRES_USER password=YOUR_POSTGRES_PASS")

    def create_table(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def create_update_query(self, id, params, table_name):
        set_string = ""

        for key in params:
            value = params[key]

            if len(set_string) == 0:
                str = "{} = '{}'".format(key, value)
                set_string += str 
            else: 
                str = ", {} = '{}'".format(key, value)
                set_string += str 
        
        update_string = "UPDATE {} SET {} WHERE id = {};".format(table_name, set_string, id)
        return update_string

    def create_insert_query(self, params, table_name):
        columns_string = ""
        values_string = ""

        for key in params:
            value = params[key]

            if len(columns_string) == 0:
                columns_string += key 
                values_string += "'{}'".format(value)
            else:
                columns_string += ", {}".format(key)
                values_string += ", '{}'".format(value)
            
        insert_string = "INSERT INTO {} ({}) VALUES ({});".format(table_name, columns_string, values_string)
        return insert_string

    def create_find_query(self, params):
        find_query = ""

        for key in params:
            value = params[key]

            if len(find_query) == 0:
                find_query += "{} = '{}'".format(key, value)
            else:
                find_query += "AND {} = '{}'".format(key, value)
            
        return find_query

    def create(self, params, table_name):
        sql = self.create_insert_query(params, table_name)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
 

    def update(self, id, params, table_name):
        sql = self.create_update_query(id, params, table_name)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
    
    def find(self, params, table_name):
        where_query = self.create_find_query(params)
        sql = "SELECT * FROM {} WHERE {};".format(table_name, where_query)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results  

    def find_by_id(self, id, table_name):
        sql = "SELECT * FROM {} WHERE id = {};".format(table_name, id)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()[0]
        cursor.close()
        return results  

    def delete(self, id, table_name):
        sql = "DELETE FROM {} WHERE id = {};".format(table_name, id)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def delete_all(self, table_name):
        sql = "DELETE FROM {};".format(table_name)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

