import tkinter
from tkinter import *
from tkinter.ttk import *

class View(Tk):
    def __init__(self):
        super().__init__()
        self.title("EHS")
        self.geometry("600x400")
        self.tabControl = Notebook(self)
        self.tabStatistic = Frame(self.tabControl)
        self.tabInsert = Frame(self.tabControl)
        self.tabControl.add(self.tabStatistic, text="Statistic")
        self.tabControl.add(self.tabInsert, text="Insert")
        self.tabControl.pack(expand=1, fill="both")

    def createTabList(self):
        self.tbl = Treeview(self.tabStatistic)
        self.tbl.pack()
        self.tbl['columns'] = ('id', 'factory', 'temp', "humidity", "created_at")

        self.tbl.column("#0", width=0, stretch=NO)
        self.tbl.column("id", anchor=CENTER, width=80)
        self.tbl.column("factory", anchor=CENTER, width=80)
        self.tbl.column("temp", anchor=CENTER, width=80)
        self.tbl.column("humidity", anchor=CENTER, width=80)
        self.tbl.column("created_at", anchor=CENTER, width=80)

        self.tbl.heading("#0", text="", anchor=CENTER)
        self.tbl.heading("id", text="#", anchor=CENTER)
        self.tbl.heading("factory", text="Factory", anchor=CENTER)
        self.tbl.heading("temp", text="Temp", anchor=CENTER)
        self.tbl.heading("humidity", text="Humidity", anchor=CENTER)
        self.tbl.heading("created_at", text="Created At", anchor=CENTER)

        # tbl.insert(parent='', index='end', iid=0, text='',
        #            values=('1', 'B04', '20', '81', '2022/01/01 08:43:21'))
        print("Create tablist")
        return 1

    def btnResultCallBack(self):
        valTempIn = int(self.etTempIn.get())
        valTempOut = int(self.etTempOut.get())
        valHumidityIn = int(self.etHumidityIn.get())
        valHumidityOut = int(self.etHumidityOut.get())

        humidityMaxIn = self.calHumidityMax(valTempIn)
        ahIn = self.calAH(humidityMaxIn, valHumidityIn)
        tempPointIn = self.calTempPoint(valTempIn, valHumidityIn)

        humidityMaxOut = self.calHumidityMax(valTempOut)
        ahOut = self.calAH(humidityMaxOut, valHumidityOut)
        TempPointOut = self.calTempPoint(valTempOut, valHumidityOut)

        self.lbResTempPointIn.config(text="%.2f" % tempPointIn)
        self.lbResTempPointOut.config(text="%.2f" % TempPointOut)
        self.lbResAhIn.config(text="%.2f" % ahIn)
        self.lbResAhOut.config(text="%.2f" % ahOut)
        self.lbResHumidityMaxIn.config(text="%.2f" % humidityMaxIn)
        self.lbResHumidityMaxOut.config(text="%.2f" % humidityMaxOut)
        print(self.getDataInTabInsert())
        return 1

    def calHumidityMax(self, t):
        return 5.018 + (0.32321 * t) + (8.1847 * 0.001 * t ** 2) + (3.1243 * 0.0001 * t ** 3)

    def calAH(self, h1, h2):
        return h1 * h2

    def calTempPoint(self, t, h):
        return t - (100 - h) / 5

    def createTabInsert(self):
        self.lbFactoryName = Label(self.tabInsert, text="Nhà kho số")
        self.lbWinLevel = Label(self.tabInsert, text="Cấp gió")
        self.lbWeather = Label(self.tabInsert, text="Thời tiết")
        self.lbTemp = Label(self.tabInsert, text="Nhiệt độ (T)")
        self.lbHumidity = Label(self.tabInsert, text="Độ ẩm (RH)")

        self.frameWeather = Frame(self.tabInsert)
        self.cbWeather1 = Checkbutton(self.frameWeather, text="Không sương mù", onvalue=1)
        self.cbWeather2 = Checkbutton(self.frameWeather, text="Không mưa", onvalue=2)

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

        variable = StringVar(self.tabInsert)
        variable.set(self.OPTIONS[0])  # default value
        self.etWinLevel = OptionMenu(self.tabInsert, variable, *self.OPTIONS)
        self.etWinLevel.config(width=16)

        ##Entry
        self.etFactoryName = Entry(self.tabInsert, width=20)
        self.etTempIn = Entry(self.tabInsert, width=20)
        self.etTempOut = Entry(self.tabInsert, width=20)
        self.etHumidityIn = Entry(self.tabInsert, width=20)
        self.etHumidityOut = Entry(self.tabInsert, width=20)

        self.btnFrame = Frame(self.tabInsert)
        self.btnResult = Button(self.btnFrame, text="Kết quả", command = self.btnResultCallBack)
        self.btnSave = Button(self.btnFrame, text="Lưu")

        ##GridView UI
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

        ###Button
        self.btnFrame.grid(column=1, row=11, pady=(16, 0))
        self.btnResult.grid(column=0, row=1)
        self.btnSave.grid(column=1, row=1)
        print("Create tabInsert")
        return 1

    def getDataInTabInsert(self):
        return {
            "factory": self.etFactoryName.get(),
            "win": "",
            "weather": "",
            "t1": self.etTempIn.get(),
            "t2": self.etTempOut.get(),
            "h1": self.etHumidityIn.get(),
            "h2": self.etHumidityOut.get()
        }

view = View()
view.createTabList()
view.createTabInsert()
view.mainloop()