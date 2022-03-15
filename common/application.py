from tkinter import *
from tkinter.ttk import *
import mysql.connector

#Object
class ObjectTemp():
    def __init__(self):
        self.name = ""
        self.win = 0
        self.weather = ""
        self.tempIn = 0
        self.tempOut = 0
        self.humidityIn = 0
        self.humidityOut = 0

    def setName(self, mName):
        self.name = mName

    def setWin(self, mWin):
        self.win = int(mWin)

    def setWeather(self, mWeather):
        self.weather = mWeather

    def setTempIn(self, mTempIn):
        self.tempIn = float(mTempIn)

    def setTempOut(self, mTempOut):
        self.tempOut = float(mTempOut)

    def setHumidityIn(self, mHumidityIn):
        self.humidityIn = float(mHumidityIn)

    def setHumidityOut(self, mHumidityOut):
        self.humidityOut = float(mHumidityOut)

    def calHumidityMax(self, t):
        return 5.018 + (0.32321 * t) + (8.1847 * 0.001 * t ** 2) + (3.1243 * 0.0001 * t ** 3)

    def calAH(self, h1, h2):
        return h1 * h2

    def calTempPoint(self, t, h):
        return t - (100 - h) / 5

    def getData(self):
        return {
            "name": self.name,
            "win": self.win,
            "weather": self.weather,
            "temp": {
                "in": self.tempIn,
                "out": self.tempOut
            },
            "humidity": {
                "in": self.humidityIn,
                "out": self.humidityOut
            },
            "humidity_max":{
                "in": self.calHumidityMax(self.tempIn),
                "out": self.calHumidityMax(self.tempOut)
            },
            "ah":{
                "in": self.calAH(self.calHumidityMax(self.tempIn), self.humidityIn),
                "out": self.calAH(self.calHumidityMax(self.tempOut), self.humidityOut)
            },
            "temp_point":{
                "in": self.calTempPoint(self.tempIn, self.humidityIn),
                "out": self.calTempPoint(self.tempOut, self.humidityOut),
            }
        }

#Database
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

    def findDataTemp(self):
        queue = "SELECT fa.name AS 'name', temp.temp_in, temp.temp_out, temp.humidity_in, temp.humidity_out, temp.description, temp.created_at FROM factory fa INNER JOIN temperature temp ON fa.id = temp.id_factory LIMIT 100 "
        self.cursor.execute(queue)
        result = self.cursor.fetchall()
        return result

    def insertTemperature(self ,param):
        queue = "INSERT INTO `temperature`(`id_factory`, `temp_in`, `temp_out`, `humidity_in`, `humidity_out`, `description`) " \
                "VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(queue, param)
        self.conn.commit()
        print("tbl_temperature: ID = "+str(self.cursor.lastrowid))
        return self.cursor.lastrowid


#View
class View(Tk):
    def __init__(self):
        super().__init__()

        self.model = Model()

        self.title("EHS")
        self.tabControl = Notebook(self)
        self.tabStatistic = Frame(self.tabControl)
        self.tabInsert = Frame(self.tabControl)
        self.tabControl.add(self.tabStatistic, text="Statistic")
        self.tabControl.add(self.tabInsert, text="Insert")
        self.tabControl.pack(expand=1, fill="both")
        self.objTemp = ObjectTemp()
        self.createTabList()
        self.createTabInsert()

    def createTabList(self):
        self.tbl = Treeview(self.tabStatistic)
        self.tbl.pack()
        self.tbl['columns'] = ('id', 'factory', 'temp_in', 'temp_out', "humidity_in", "humidity_out", "description", "created_at")

        self.tbl.column("#0", width=0, stretch=NO)
        self.tbl.column("id", anchor=CENTER, width=30)
        self.tbl.column("factory", anchor=CENTER, width=70)
        self.tbl.column("temp_in", anchor=CENTER, width=70)
        self.tbl.column("temp_out", anchor=CENTER, width=70)
        self.tbl.column("humidity_in", anchor=CENTER, width=70)
        self.tbl.column("humidity_out", anchor=CENTER, width=70)
        self.tbl.column("description", anchor=CENTER, width=150)
        self.tbl.column("created_at", anchor=CENTER, width=130)

        self.tbl.heading("#0", text="", anchor=CENTER)
        self.tbl.heading("id", text="#", anchor=CENTER)
        self.tbl.heading("factory", text="Factory", anchor=CENTER)
        self.tbl.heading("temp_in", text="Temp IN", anchor=CENTER)
        self.tbl.heading("temp_out", text="Temp OUT", anchor=CENTER)
        self.tbl.heading("humidity_in", text="Humidity IN", anchor=CENTER)
        self.tbl.heading("humidity_out", text="Humidity OUT", anchor=CENTER)
        self.tbl.heading("description", text="Description", anchor=CENTER)
        self.tbl.heading("created_at", text="Created At", anchor=CENTER)

        data = self.model.findDataTemp()
        i = 1
        for item in data:
            print(item)
            self.tbl.insert(parent='', index='end', iid=i, text='',
                   values=(i, item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
            i+=1

    def getDataView(self):
        valWeather = ""
        if self.cbWeather1.instate(['selected']) :
            valWeather += self.cbWeather1.cget("text") + ", "
        if self.cbWeather2.instate(['selected']) :
            valWeather += self.cbWeather2.cget("text")

        self.objTemp.setWeather(valWeather)
        self.objTemp.setName(self.etFactoryName.get())
        self.objTemp.setTempIn(self.etTempIn.get())
        self.objTemp.setTempOut(self.etTempOut.get())
        self.objTemp.setHumidityIn(self.etHumidityIn.get())
        self.objTemp.setHumidityOut(self.etHumidityOut.get())
        self.objTemp.setWin(self.valWinLevel.get())

    def callbackBtnResult(self):
        self.getDataView()
        data = self.objTemp.getData()
        print(data)

        self.lbResTempPointIn.config(text="%.2f" % data['temp_point']['in'])
        self.lbResTempPointOut.config(text="%.2f" % data['temp_point']['out'])
        self.lbResAhIn.config(text="%.2f" % data['ah']['in'])
        self.lbResAhOut.config(text="%.2f" % data['ah']['out'])
        self.lbResHumidityMaxIn.config(text="%.2f" %  data['humidity_max']['in'])
        self.lbResHumidityMaxOut.config(text="%.2f" % data['humidity_max']['out'])

    def callbackBtnSave(self):
        data = self.objTemp.getData()
        self.model.insertTemperature((1, data['temp']['in'], data['temp']['out'], data['humidity']['in'], data['humidity']['out'], data['weather']))
        return

    def createTabInsert(self):
        self.lbFactoryName = Label(self.tabInsert, text="Nhà kho số")
        self.lbWinLevel = Label(self.tabInsert, text="Cấp gió")
        self.lbWeather = Label(self.tabInsert, text="Thời tiết")
        self.lbTemp = Label(self.tabInsert, text="Nhiệt độ (T)")
        self.lbHumidity = Label(self.tabInsert, text="Độ ẩm (RH)")

        self.lbResult = Label(self.tabInsert, text="Không được thông gió", background="orange red", foreground="white", borderwidth=2, relief="ridge", width=15, font=("Arial",20))

        self.frameWeather = Frame(self.tabInsert)
        self.cbWeather1 = Checkbutton(self.frameWeather, text="Có sương mù", onvalue=1)
        self.cbWeather2 = Checkbutton(self.frameWeather, text="Có mưa", onvalue=2)

        self.lbIn = Label(self.tabInsert, text="TRONG KHO", font='Arial 15 bold', borderwidth=1, relief="solid")
        self.lbOut = Label(self.tabInsert, text="NGOÀI KHO", font='Arial 15 bold', borderwidth=1, relief="solid")
        self.lbTempPoint = Label(self.tabInsert, text="Nhiệt độ điểm sương")
        self.lbAh = Label(self.tabInsert, text="AH")
        self.lbHumidityMax = Label(self.tabInsert, text="Độ ẩm cực đại")

        self.lbResTempPointIn = Label(self.tabInsert)
        self.lbResTempPointOut = Label(self.tabInsert)
        self.lbResAhIn = Label(self.tabInsert)
        self.lbResAhOut = Label(self.tabInsert)
        self.lbResHumidityMaxIn = Label(self.tabInsert)
        self.lbResHumidityMaxOut = Label(self.tabInsert)
        self.OPTIONS = ["0", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.valWinLevel = StringVar(self.tabInsert)
        self.valWinLevel.set(self.OPTIONS[0])  # default value
        self.etWinLevel = OptionMenu(self.tabInsert, self.valWinLevel, *self.OPTIONS)
        self.etWinLevel.config(width=16)

        ##Entry
        self.etFactoryName = Entry(self.tabInsert, width=20)
        self.etTempIn = Entry(self.tabInsert, width=20)
        self.etTempOut = Entry(self.tabInsert, width=20)
        self.etHumidityIn = Entry(self.tabInsert, width=20)
        self.etHumidityOut = Entry(self.tabInsert, width=20)

        self.btnFrame = Frame(self.tabInsert)
        self.btnResult = Button(self.btnFrame, text="Kết quả", command = self.callbackBtnResult)
        self.btnSave = Button(self.btnFrame, text="Lưu", command = self.callbackBtnSave)

        ###Factory Name
        self.lbFactoryName.grid(column=0, row=1, pady=(16, 0), sticky=W)
        self.etFactoryName.grid(column=1, row=1, pady=(16, 0))
        ###Win Level
        self.lbWinLevel.grid(column=0, row=2, pady=(4, 0), sticky=W)
        self.etWinLevel.grid(column=1, row=2, pady=(4, 0))
        ###Weather
        self.lbWeather.grid(column=0, row=3, pady=(4, 0), sticky='W,N')
        self.frameWeather.grid(column=1, row=3, pady=(4, 0))
        self.cbWeather1.grid(column=0, row=1, sticky=W)
        self.cbWeather2.grid(column=0, row=2, sticky=W)

        self.lbIn.grid(column=1, row=5, pady=(16, 4))
        self.lbOut.grid(column=2, row=5, pady=(16, 4))

        ###Temp
        self.lbTemp.grid(column=0, row=6, sticky=W)
        self.etTempIn.grid(column=1, row=6)
        self.etTempOut.grid(column=2, row=6)

        ###Humidity
        self.lbHumidity.grid(column=0, row=7, pady=8, sticky=W)
        self.etHumidityIn.grid(column=1, row=7)
        self.etHumidityOut.grid(column=2, row=7)

        ###Result
        self.lbTempPoint.grid(column=0, row=8, pady=(8, 0), sticky=W)
        self.lbResTempPointIn.grid(column=1, row=8, pady=(8, 0))
        self.lbResTempPointOut.grid(column=2, row=8, pady=(8, 0))

        self.lbAh.grid(column=0, row=9, pady=(8, 0), sticky=W)
        self.lbResAhIn.grid(column=1, row=9, pady=(8, 0))
        self.lbResAhOut.grid(column=2, row=9, pady=(8, 0))

        self.lbHumidityMax.grid(column=0, row=10, pady=(8, 0), sticky=W)
        self.lbResHumidityMaxIn.grid(column=1, row=10, pady=(8, 0))
        self.lbResHumidityMaxOut.grid(column=2, row=10, pady=(8, 0))

        self.lbResult.grid(row =0, column=3, rowspan=10, padx=(12, 0))
        self.lbResult.configure(anchor="center")
        ###Button
        self.btnFrame.grid(column=1, row=11, pady=(16, 0))
        self.btnResult.grid(column=0, row=1)
        self.btnSave.grid(column=1, row=1)

view = View()
view.mainloop()