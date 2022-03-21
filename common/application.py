from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from dotenv import dotenv_values
import mysql.connector

#Object Model
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
        if len(mTempIn.strip()) == 0:
            self.tempIn = 0
        else:
            self.tempIn = float(mTempIn)

    def setTempOut(self, mTempOut):
        if len(mTempOut.strip()) == 0:
            self.tempOut = 0
        else:
            self.tempOut = float(mTempOut)

    def setHumidityIn(self, mHumidityIn):
        if len(mHumidityIn.strip()) == 0:
            self.humidityIn = 0
        else:
            self.humidityIn = float(mHumidityIn)

    def setHumidityOut(self, mHumidityOut):
        if len(mHumidityOut.strip()) == 0:
            self.humidityOut = 0
        else:
            self.humidityOut = float(mHumidityOut)

    def calHumidityMax(self, t):
        return 5.018 + (0.32321 * t) + (8.1847 * 0.001 * t ** 2) + (3.1243 * 0.0001 * t ** 3)

    def calAH(self, h1, h2):
        return h1 * h2

    def calTempPoint(self, t, h):
        return t - (100 - h) / 5

    def getSolution(self):
        data = self.getData()
        message = "Nhà kho không đủ điều kiện thông gió"
        if data['weather']['check'] == int(1) and float(data['ah']['out']) < float(data['ah']['in']) and float(
                data['temp']['out']) <= float(32) and float(data['temp']['out']) >= float(10):
            if data['temp']['in'] <= data['temp']['out']:
                if data['temp_point']['in'] >= data['temp_point']['out']:
                    message = "Nhà kho đủ điều kiện thông gió"
            else:
                if data['temp_point']['in'] < data['temp_point']['out']:
                    message = "Nhà kho đủ điều kiện thông gió"
        return message

    def checkData(self):
        message = ""
        check = 1
        if len(self.name.strip()) == 0:
            check = 0
            message = "Bạn chưa nhập tên nhà kho"
        return {"check": check, "message": message}

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
                "in": self.humidityIn,
                "out": self.humidityOut
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
        config = dotenv_values(".env")
        self.conn = mysql.connector.connect(
          host=config['DATABASE.HOST'],
          user=config['DATABASE.USER'],
          password=config['DATABASE.PASS'],
          database=config['DATABASE.NAME']
        )
        self.cursor = self.conn.cursor()

    def findDataTemp(self):
        queue = "SELECT name, win, temp_in, temp_out, humidity_in, humidity_out, description, DATE_FORMAT(`created_at`, '%d/%m/%Y'), DATE_FORMAT(`created_at`, '%H:%i:%s'), id FROM temperature temp ORDER BY created_at DESC LIMIT 1000 "
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

#View
class View(Tk):
    def __init__(self):
        super().__init__()
        self.model = Model()

        self.iconbitmap("icon.ico")
        self.title("Phần mềm tính toán điều kiện thông gió nhà kho súng pháo, khí tài lục quân")
        self.tabControl = Notebook(self)
        self.tabStatistic = Frame(self.tabControl) #Tab Thống kê
        self.tabTemp = Frame(self.tabControl) #Tab nhập nhiệt độ
        self.tabControl.add(self.tabStatistic, text="Thống kê") #Thêm tab
        self.tabControl.add(self.tabTemp, text="Nhập dữ liệu")
        self.tabControl.pack(expand=1, fill="both")
        self.createTabStatistic() #Khởi tạo tab thống kê
        self.createTabTemp() #Khởi tạo tab nhập nhiệt độ
        self.createFooter() #Khởi tạo nội dung người tạo

    def createTabStatistic(self):
        style = Style()
        style.configure("Treeview", fieldbackground='red')
        style.configure("Treeview.Heading", foreground='black', font=('Arial Bold', 8))
        self.tbl = Treeview(self.tabStatistic)
        self.tbl.pack(fill='both', expand=True)
        self.tbl['columns'] = ('date', "time", "name", "win", 'Tt', 'Tn', "RHt", "RHn", "AHt", "AHn", "Tdpt", "Tdpn", "weather", "solution")

        self.tbl.column("#0", width=0, stretch=NO)
        self.tbl.column("date", anchor=CENTER, width=80)
        self.tbl.column("time", anchor=CENTER, width=60)
        self.tbl.column("name", anchor=CENTER, width=30)
        self.tbl.column("win", anchor=CENTER, width=30)
        self.tbl.column("Tt", anchor=CENTER, width=90)
        self.tbl.column("Tn", anchor=CENTER, width=90)
        self.tbl.column("RHt", anchor=CENTER, width=80)
        self.tbl.column("RHn", anchor=CENTER, width=80)
        self.tbl.column("AHt", anchor=CENTER, width=140)
        self.tbl.column("AHn", anchor=CENTER, width=140)
        self.tbl.column("Tdpt", anchor=CENTER, width=155)
        self.tbl.column("Tdpn", anchor=CENTER, width=155)
        self.tbl.column("weather", anchor=CENTER, width=120)
        self.tbl.column("solution", anchor=CENTER, width=230)

        self.tbl.heading("#0", text="", anchor=CENTER)
        self.tbl.heading("date", text="Ngày", anchor=CENTER)
        self.tbl.heading("time", text="Thời gian", anchor=CENTER)
        self.tbl.heading("name", text="Kho", anchor=CENTER)
        self.tbl.heading("win", text="Gió", anchor=CENTER)
        self.tbl.heading("Tt", text="Nhiệt độ trong", anchor=CENTER)
        self.tbl.heading("Tn", text="Nhiệt độ ngoài", anchor=CENTER)
        self.tbl.heading("RHt", text="Độ ẩm trong", anchor=CENTER)
        self.tbl.heading("RHn", text="Độ ẩm ngoài", anchor=CENTER)
        self.tbl.heading("AHt", text="Độ ẩm tuyệt đối trong", anchor=CENTER)
        self.tbl.heading("AHn", text="Độ ẩm tuyệt đối ngoài", anchor=CENTER)
        self.tbl.heading("Tdpt", text="Nhiệt độ điểm sương trong", anchor=CENTER)
        self.tbl.heading("Tdpn", text="Nhiệt độ điểm sương ngoài", anchor=CENTER)
        self.tbl.heading("weather", text="Thời tiết", anchor=CENTER)
        self.tbl.heading("solution", text="Biện pháp", anchor=CENTER)
        self.loadDataStatistic()

    def loadDataStatistic(self):
        self.tbl.delete(*self.tbl.get_children())
        data = self.model.findDataTemp()
        for item in data:
            tmpTemp = ObjectTemp()
            tmpTemp.setData(item)
            dataItem = tmpTemp.getData()
            id = item[9]
            date = item[7]
            time = item[8]
            self.tbl.insert(parent='', index='end', iid=id, text='',
                            values=(date, time, dataItem['name'], dataItem['win']
                                    , dataItem['temp']['in'], dataItem['temp']['out']
                                    , dataItem['humidity']['in'], dataItem['humidity']['out']
                                    , dataItem['ah']['in'], dataItem['ah']['out']
                                    , dataItem['temp_point']['in'], dataItem['temp_point']['out']
                                    , dataItem['weather']['text'], tmpTemp.getSolution()))

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

        self.objTemp.setWeather(valWeather)
        self.objTemp.setName(self.etFactoryName.get())
        self.objTemp.setIdFactory(1)
        self.objTemp.setTempIn(self.etTempIn.get())
        self.objTemp.setTempOut(self.etTempOut.get())
        self.objTemp.setHumidityIn(self.etHumidityIn.get())
        self.objTemp.setHumidityOut(self.etHumidityOut.get())
        self.objTemp.setWin(self.valWinLevel.get())

    def callbackBtnResult(self):
        self.objTemp = ObjectTemp()
        self.getDataView()
        data = self.objTemp.getData()
        self.lbResult.config(state=NORMAL)
        self.lbResult.delete(1.0, "end")
        self.lbResult.insert(END, self.objTemp.getSolution())
        self.lbResult.config(state=DISABLED)

        self.lbResTempPointIn.config(text=data['temp_point']['in'])
        self.lbResTempPointOut.config(text=data['temp_point']['out'])
        self.lbResAhIn.config(text=data['ah']['in'])
        self.lbResAhOut.config(text=data['ah']['out'])
        self.lbResHumidityMaxIn.config(text=data['humidity_max']['in'])
        self.lbResHumidityMaxOut.config(text=data['humidity_max']['out'])


    def callbackBtnSave(self):
        data = self.objTemp.getData()
        check = self.objTemp.checkData()
        if check['check'] == 0:
            messagebox.showwarning("Cảnh báo", 'Bạn chưa nhập thông tin '+check["message"])
            return

        self.model.insertTemperature((data['id_factory'], data['name'], data['win'], data['temp']['in'], data['temp']['out'], data['humidity']['in'], data['humidity']['out'], data['weather']['text']))
        self.loadDataStatistic()
        messagebox.showinfo("Thông báo", "Thêm dữ liệu thành công")
        return

    def createTabTemp(self):
        self.lbFactoryName = Label(self.tabTemp, text="Nhà kho số")
        self.lbWinLevel = Label(self.tabTemp, text="Cấp gió")
        self.lbWeather = Label(self.tabTemp, text="Thời tiết")
        self.lbTemp = Label(self.tabTemp, text="Nhiệt độ")
        self.lbHumidity = Label(self.tabTemp, text="Độ ẩm tương đối")
        self.lbResult = Text(self.tabTemp, height = 5, width = 35, background="white", foreground="orange red", borderwidth=2, relief="ridge", font=("Arial",14))

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
        self.valWinLevel.set(self.optionWin[0])  #giá trị mặc định cấp gió
        self.etWinLevel = OptionMenu(self.tabTemp, self.valWinLevel, *self.optionWin)
        self.etWinLevel.config(width=16)

        ##Entry
        self.etFactoryName = Entry(self.tabTemp, width=20)
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
        ###Button
        self.btnFrame.grid(column=1, row=11, pady=(16, 0))
        self.btnResult.grid(column=0, row=1)
        self.btnSave.grid(column=1, row=1)

        self.lbResult.grid(row=12, column=0, columnspan=3, pady=(8, 0))
        self.lbResult.config(state=DISABLED)

    def createFooter(self):
        self.lbFooter = Label(self, text="Copyright by Dương Thế Tuấn Anh", anchor="e")
        self.lbFooter.pack(fill='both')

view = View()
view.mainloop()

# pyinstaller --onefile temperature\common\application.py
# pyinstaller --onefile --windowed application.py --path=C:\Users\emtuy\AppData\Local\Programs\Python\Python310\Lib\site-packages
# pyinstaller --onefile --windowed application.py --path=C:\Users\User01\AppData\Local\Programs\Python\Python310\Lib\site-packages