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

    def findAll(self, tblName):
        queue = "SELECT * FROM "+tblName
        self.cursor.execute(queue)
        result = self.cursor.fetchall()
        return result

    def findByParams(self):
        return 1

    def insertTemperature(self ,param):
        queue = "INSERT INTO `temperature`(`id_factory`, `term_in`, `temp_out`, `humidity_in`, `humidity_out`, `description`) " \
                "VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(queue, param)
        self.conn.commit()
        print("tbl_temperature: ID = "+str(self.cursor.lastrowid))
        return self.cursor.lastrowid
