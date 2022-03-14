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

    def insert(self, tblName ,param):
        mParam = ",".join(param.keys())
        queue = "INSERT INTO "+tblName+" ("")"
        return 1

maps = {"id": 1, "user": "tuyen", "time": "2022/01/01"}
#model = Model()
#print(model.findAll("FACTORY"))
for key in maps.keys():
    print(str(maps[key])+ "  -  "+key)