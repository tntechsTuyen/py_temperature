import mysql.connector

class Model:
    def __init__(self):
        self.conn = mysql.connector.connect(
          host="localhost",
          user="root",
          password="12345678",
          database="temperature"
        )
        self.cursor = self.conn.cursor()

    def findDataTemp(self):
        queue = "SELECT name, win, temp_in, temp_out, humidity_in, humidity_out, description, DATE_FORMAT(`created_at`, '%d/%m/%Y'), DATE_FORMAT(`created_at`, '%H:%i:%s'), id FROM temperature temp ORDER BY created_at ASC LIMIT 1000 "
        self.cursor.execute(queue)
        result = self.cursor.fetchall()
        return result

    def insertTemperature(self ,param):
        queue = "INSERT INTO `temperature`(`id_factory`, `name`, `win`, `temp_in`, `temp_out`, `humidity_in`, `humidity_out`, `description`) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(queue, param)
        self.conn.commit()
        print("tbl_temperature: ID = "+str(self.cursor.lastrowid))
        return self.cursor.lastrowid