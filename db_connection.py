import psycopg2

class DatabaseConnection:
    
    def __init__(self):
        self.connection = psycopg2.connect("dbname=vaccination_details user=raghapbean password=postgres")

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
                str = "{} = '{}',".format(key, value)
                set_string += str 
        
        update_string = "UPDATE {} SET {} WHERE id = {};".format(table_name, set_string, id)
        return update_string

    def create_insert_query(self, )

    def update(self, id, params, table_name):
        sql = self.create_update_query(id, params, table_name)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()
