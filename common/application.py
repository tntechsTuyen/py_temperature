from tkinter import *
from tkinter.ttk import *
import mysql.connector

#Object
class ObjectTemp():
    def __init__(self):
        self.idFactory = 0
        self.name = ""
        self.win = 0
        self.weather = ""
        self.checkWeather = 1
        self.tempIn = 0
        self.tempOut = 0
        self.humidityIn = 0
        self.humidityOut = 0

    def setData(self, data):
        self.idFactory = 0
        self.name = data[0]
        self.win = data[1]
        self.checkWeather = 1
        self.tempIn = data[2]
        self.tempOut = data[3]
        self.humidityIn = data[4]
        self.humidityOut = data[5]
        self.weather = data[6]


    def setIdFactory(self, mIdFactory):
        self.idFactory = mIdFactory

    def setName(self, mName):
        self.name = mName

    def setWin(self, mWin):
        self.win = int(mWin)

    def setWeather(self, mWeather):
        self.weather = mWeather

    def setCheckWeather(self, mCheck):
        self.checkWeather = mCheck

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
            "id_factory": self.idFactory,
            "name": self.name,
            "win": self.win,
            "weather": {
                "text": self.weather,
                "check": self.checkWeather
            },
            "temp": {
                "in": self.tempIn,
                "out": self.tempOut
            },
            "humidity": {
                "in": "%.2f" % self.humidityIn,
                "out": "%.2f" % self.humidityOut
            },
            "humidity_max":{
                "in": "%.2f" % self.calHumidityMax(self.tempIn),
                "out": "%.2f" % self.calHumidityMax(self.tempOut)
            },
            "ah":{
                "in": "%.2f" % self.calAH(self.calHumidityMax(self.tempIn), self.humidityIn),
                "out": "%.2f" % self.calAH(self.calHumidityMax(self.tempOut), self.humidityOut)
            },
            "temp_point":{
                "in": "%.2f" % self.calTempPoint(self.tempIn, self.humidityIn),
                "out": "%.2f" % self.calTempPoint(self.tempOut, self.humidityOut),
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

    def findAll(self, column, tblName):
        queue = "SELECT "+column+" FROM "+tblName
        self.cursor.execute(queue)
        result = self.cursor.fetchall()
        return result

    def findDataTemp(self):
        queue = "SELECT fa.name, temp.win, temp.temp_in, temp.temp_out, temp.humidity_in, temp.humidity_out, temp.description, temp.created_at FROM factory fa INNER JOIN temperature temp ON fa.id = temp.id_factory LIMIT 100 "
        self.cursor.execute(queue)
        result = self.cursor.fetchall()
        return result

    def insertTemperature(self ,param):
        queue = "INSERT INTO `temperature`(`id_factory`, `win`, `temp_in`, `temp_out`, `humidity_in`, `humidity_out`, `description`) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(queue, param)
        self.conn.commit()
        print("tbl_temperature: ID = "+str(self.cursor.lastrowid))
        return self.cursor.lastrowid

    def insertFactory(self, param):
        queue = "INSERT INTO `factory`(`name`, `description`) " \
                "VALUES (%s, %s)"
        self.cursor.execute(queue, param)
        self.conn.commit()
        print("tbl_factory: ID = " + str(self.cursor.lastrowid))
        return self.cursor.lastrowid

#View
class View(Tk):
    def __init__(self):
        super().__init__()

        self.model = Model()

        self.title("EHS")
        self.tabControl = Notebook(self)
        self.tabStatistic = Frame(self.tabControl)
        self.tabTemp = Frame(self.tabControl)
        self.tabFactory = Frame(self.tabControl)
        self.tabControl.add(self.tabStatistic, text="Statistic")
        self.tabControl.add(self.tabTemp, text="Temp")
        self.tabControl.add(self.tabFactory, text="Factory")
        self.tabControl.pack(expand=1, fill="both")
        self.objTemp = ObjectTemp()
        self.createTabList()
        self.createTabTemp()
        self.createTabFactory()

    def createTabList(self):
        self.tbl = Treeview(self.tabStatistic)
        self.tbl.pack()
        self.tbl['columns'] = ('id', 'factory', "time", 'Tt', 'Tn', "RHt", "RHn", "AHt", "AHn", "Tdpt", "Tdpn", "At", "An", "description")

        self.tbl.column("#0", width=0, stretch=NO)
        self.tbl.column("id", anchor=CENTER, width=30)
        self.tbl.column("factory", anchor=CENTER, width=50)
        self.tbl.column("time", anchor=CENTER, width=130)
        self.tbl.column("Tt", anchor=CENTER, width=40)
        self.tbl.column("Tn", anchor=CENTER, width=40)
        self.tbl.column("RHt", anchor=CENTER, width=40)
        self.tbl.column("RHn", anchor=CENTER, width=40)
        self.tbl.column("AHt", anchor=CENTER, width=50)
        self.tbl.column("AHn", anchor=CENTER, width=50)
        self.tbl.column("Tdpt", anchor=CENTER, width=50)
        self.tbl.column("Tdpn", anchor=CENTER, width=50)
        self.tbl.column("At", anchor=CENTER, width=40)
        self.tbl.column("An", anchor=CENTER, width=40)
        self.tbl.column("description", anchor=CENTER, width=150)

        self.tbl.heading("#0", text="", anchor=CENTER)
        self.tbl.heading("id", text="#", anchor=CENTER)
        self.tbl.heading("factory", text="Factory", anchor=CENTER)
        self.tbl.heading("time", text="Time", anchor=CENTER)
        self.tbl.heading("Tt", text="Tt", anchor=CENTER)
        self.tbl.heading("Tn", text="Tn", anchor=CENTER)
        self.tbl.heading("RHt", text="RHt", anchor=CENTER)
        self.tbl.heading("RHn", text="RHn", anchor=CENTER)
        self.tbl.heading("AHt", text="AHt", anchor=CENTER)
        self.tbl.heading("AHn", text="AHn", anchor=CENTER)
        self.tbl.heading("Tdpt", text="Tdpt", anchor=CENTER)
        self.tbl.heading("Tdpn", text="Tdpn", anchor=CENTER)
        self.tbl.heading("At", text="At", anchor=CENTER)
        self.tbl.heading("An", text="An", anchor=CENTER)
        self.tbl.heading("description", text="Description", anchor=CENTER)

        data = self.model.findDataTemp()
        i = 1
        for item in data:
            tmpTemp = ObjectTemp()
            tmpTemp.setData(item)
            dataItem = tmpTemp.getData()
            time = item[7]
            self.tbl.insert(parent='', index='end', iid=i, text='',
                   values=(i, dataItem['name'], time
                           , dataItem['temp']['in'], dataItem['temp']['out']
                           , dataItem['humidity']['in'], dataItem['humidity']['out']
                           , dataItem['ah']['in'], dataItem['ah']['out']
                           , dataItem['temp_point']['in'], dataItem['temp_point']['out']
                           , dataItem['humidity_max']['in'], dataItem['humidity_max']['out']
                           , dataItem['weather']['text']))
            i+=1

    def getDataFactory(self):
        factories = self.model.findAll("id, name", "factory")
        result = {}
        for item in factories:
            result[item[1]] = item[0]
        return result

    def getDataView(self):
        valWeather = ""
        if self.cbWeather1.instate(['selected']) :
            valWeather += self.cbWeather1.cget("text") + ", "
            self.objTemp.setCheckWeather(0)
        if self.cbWeather2.instate(['selected']) :
            valWeather += self.cbWeather2.cget("text") + ", "
            self.objTemp.setCheckWeather(0)
        if self.cbWeather3.instate(['selected']) :
            valWeather += self.cbWeather3.cget("text")
            self.objTemp.setCheckWeather(0)

        self.objTemp.setWeather(valWeather)
        self.objTemp.setName(self.valFactory.get())
        self.objTemp.setIdFactory(self.optionFactory[self.valFactory.get()])
        self.objTemp.setTempIn(self.etTempIn.get())
        self.objTemp.setTempOut(self.etTempOut.get())
        self.objTemp.setHumidityIn(self.etHumidityIn.get())
        self.objTemp.setHumidityOut(self.etHumidityOut.get())
        self.objTemp.setWin(self.valWinLevel.get())

    def callbackBtnResult(self):
        message = "Không thông gió"
        self.getDataView()
        data = self.objTemp.getData()
        print(data)

        if data['weather']['check'] == int(1) and float(data['ah']['out']) < float(data['ah']['in']) and float(data['temp']['out']) <= float(32) and float(data['temp']['out']) >= float(10):
            if data['temp']['in'] <= data['temp']['out']:
                if data['temp_point']['in'] >= data['temp_point']['out']:
                    message = "Thông gió"
            else:
                if data['temp_point']['in'] < data['temp_point']['out']:
                    message = "Thông gió"


        self.lbResult.config(state=NORMAL)
        self.lbResult.delete(1.0, "end")
        self.lbResult.insert(END, message)
        self.lbResult.config(state=DISABLED)

        self.lbResTempPointIn.config(text=data['temp_point']['in'])
        self.lbResTempPointOut.config(text=data['temp_point']['out'])
        self.lbResAhIn.config(text=data['ah']['in'])
        self.lbResAhOut.config(text=data['ah']['out'])
        self.lbResHumidityMaxIn.config(text=data['humidity_max']['in'])
        self.lbResHumidityMaxOut.config(text=data['humidity_max']['out'])


    def callbackBtnSave(self):
        data = self.objTemp.getData()
        self.model.insertTemperature((data['id_factory'], data['win'], data['temp']['in'], data['temp']['out'], data['humidity']['in'], data['humidity']['out'], data['weather']['text']))
        return

    def callbackSaveFactory(self):
        return self.model.insertFactory((self.et1.get(), self.et2.get()))

    def createTabTemp(self):
        self.lbFactoryName = Label(self.tabTemp, text="Nhà kho số")
        self.lbWinLevel = Label(self.tabTemp, text="Cấp gió")
        self.lbWeather = Label(self.tabTemp, text="Thời tiết")
        self.lbTemp = Label(self.tabTemp, text="Nhiệt độ")
        self.lbHumidity = Label(self.tabTemp, text="Độ ẩm tương đối")

        self.lbResult = Text(self.tabTemp, height = 5, width = 20, background="orange red", foreground="white", borderwidth=2, relief="ridge", font=("Arial",16))

        self.frameWeather = Frame(self.tabTemp)
        self.cbWeather1 = Checkbutton(self.frameWeather, text="Sương mù", onvalue=1)
        self.cbWeather2 = Checkbutton(self.frameWeather, text="Mưa", onvalue=2)
        self.cbWeather3 = Checkbutton(self.frameWeather, text="Nắng", onvalue=3)

        self.lbIn = Label(self.tabTemp, text="TRONG KHO", font='Arial 15 bold', borderwidth=1, relief="solid")
        self.lbOut = Label(self.tabTemp, text="NGOÀI KHO", font='Arial 15 bold', borderwidth=1, relief="solid")
        self.lbTempPoint = Label(self.tabTemp, text="Nhiệt độ điểm sương")
        self.lbAh = Label(self.tabTemp, text="Độ ẩm tuyệt đối")
        self.lbHumidityMax = Label(self.tabTemp, text="Độ ẩm cực đại")

        self.lbResTempPointIn = Label(self.tabTemp)
        self.lbResTempPointOut = Label(self.tabTemp)
        self.lbResAhIn = Label(self.tabTemp)
        self.lbResAhOut = Label(self.tabTemp)
        self.lbResHumidityMaxIn = Label(self.tabTemp)
        self.lbResHumidityMaxOut = Label(self.tabTemp)

        # Select Option
        self.optionWin = ["0", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.valWinLevel = StringVar(self.tabTemp)
        self.valWinLevel.set(self.optionWin[0])  # default value
        self.etWinLevel = OptionMenu(self.tabTemp, self.valWinLevel, *self.optionWin)
        self.etWinLevel.config(width=16)

        self.optionFactory = self.getDataFactory()
        keyFactory = list(self.optionFactory.keys())
        keyFactory.insert(0, keyFactory[0])
        self.valFactory = StringVar(self.tabTemp)
        self.etFactoryName = OptionMenu(self.tabTemp, self.valFactory, *keyFactory)
        self.etFactoryName.config(width=16)
        ##Entry

        self.etTempIn = Entry(self.tabTemp, width=20)
        self.etTempOut = Entry(self.tabTemp, width=20)
        self.etHumidityIn = Entry(self.tabTemp, width=20)
        self.etHumidityOut = Entry(self.tabTemp, width=20)

        self.btnFrame = Frame(self.tabTemp)
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
        self.cbWeather3.grid(column=0, row=3, sticky=W)

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

        self.lbResult.grid(row=5, column=3, rowspan=10, padx=(12, 0))
        self.lbResult.insert('end', 'Có thông gió nhà kho hay không ???')
        self.lbResult.config(state=DISABLED)
        ###Button
        self.btnFrame.grid(column=1, row=11, pady=(16, 0))
        self.btnResult.grid(column=0, row=1)
        self.btnSave.grid(column=1, row=1)

    def createTabFactory(self):
        self.lb1 = Label(self.tabFactory, text="Nhà kho số")
        self.lb2 = Label(self.tabFactory, text="Mô tả")
        self.et1 = Entry(self.tabFactory, width=20)
        self.et2 = Entry(self.tabFactory, width=20)
        self.btn1 = Button(self.tabFactory, text="Lưu", command=self.callbackSaveFactory)
        self.lb1.grid(row=0, column=0, pady=(8, 0), sticky=W)
        self.et1.grid(row=0, column=1, pady=(8, 0))
        self.lb2.grid(row=1, column=0, pady=(8, 0), sticky=W)
        self.et2.grid(row=1, column=1, pady=(8, 0))
        self.btn1.grid(row=2, column=1, pady=(8, 0))

view = View()
view.mainloop()