import tkinter
from tkinter import *
from tkinter.ttk import *

ws = Tk()
ws.title("EHS")
ws.geometry("600x400")

#UI Content
tabControl = Notebook(ws)
tabStatistic = Frame(tabControl)
tabInsert = Frame(tabControl)
tabControl.add(tabStatistic, text="Statistic")
tabControl.add(tabInsert, text="Insert")
tabControl.pack(expand=1, fill="both")

#TabInsert
##Label
lbFactoryName = Label(tabInsert, text = "Nhà kho số")
lbWinLevel = Label(tabInsert, text = "Cấp gió")
lbWeather = Label(tabInsert, text = "Thời tiết")
lbTemp = Label(tabInsert, text = "Nhiệt độ (T)")
lbHumidity = Label(tabInsert, text = "Độ ẩm (RH)")

frameWeather = Frame(tabInsert)
cbWeather1 = Checkbutton(frameWeather, text="Không sương mù", onvalue=1)
cbWeather2 = Checkbutton(frameWeather, text="Không mưa", onvalue=2)

lbIn = Label(tabInsert, text="TRONG KHO", font='Arial 15 bold', borderwidth=1, relief="solid")
lbOut = Label(tabInsert, text="NGOÀI KHO", font='Arial 15 bold', borderwidth=1, relief="solid")
lbTempPoint = Label(tabInsert, text="Nhiệt độ điểm sương")
lbAh = Label(tabInsert, text="AH")
lbHumidityMax = Label(tabInsert, text="Độ ẩm cực đại")

lbResTempPointIn = Label(tabInsert)
lbResTempPointOut = Label(tabInsert)
lbResAhIn = Label(tabInsert)
lbResAhOut = Label(tabInsert)
lbResHumidityMaxIn = Label(tabInsert)
lbResHumidityMaxOut = Label(tabInsert)

##Data
OPTIONS = ["0", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

variable = StringVar(tabInsert)
variable.set(OPTIONS[0]) # default value
etWinLevel = OptionMenu(tabInsert, variable, *OPTIONS)
etWinLevel.config(width=16)

##Entry
etFactoryName = Entry(tabInsert, width = 20)
etTempIn = Entry(tabInsert, width = 20)
etTempOut = Entry(tabInsert, width = 20)
etHumidityIn = Entry(tabInsert, width = 20)
etHumidityOut = Entry(tabInsert, width = 20)

#CallBack Btn
def btnResultCallBack():
    valTempIn = int(etTempIn.get())
    valTempOut = int(etTempOut.get())
    valHumidityIn = int(etHumidityIn.get())
    valHumidityOut = int(etHumidityOut.get())

    humidityMaxIn = calHumidityMax(valTempIn)
    ahIn = calAH(humidityMaxIn, valHumidityIn)
    TempPointIn = calTempPoint(valTempIn, valHumidityIn)

    humidityMaxOut = calHumidityMax(valTempOut)
    ahOut = calAH(humidityMaxOut, valHumidityOut)
    TempPointOut = calTempPoint(valTempOut, valHumidityOut)

    lbResTempPointIn.config(text="%.2f" % TempPointIn)
    lbResTempPointOut.config(text="%.2f" % TempPointOut)
    lbResAhIn.config(text="%.2f" % ahIn)
    lbResAhOut.config(text="%.2f" % ahOut)
    lbResHumidityMaxIn.config(text="%.2f" % humidityMaxIn)
    lbResHumidityMaxOut.config(text="%.2f" % humidityMaxOut)
    return 1

def btnSaveCallBack():
    return 1

##Button
btnFrame = Frame(tabInsert)
btnResult = Button(btnFrame, text = "Kết quả", command = btnResultCallBack)
btnSave = Button(btnFrame, text = "Lưu")

##GridView UI
###Factory Name
lbFactoryName.grid(column=0, row=1, pady=(16, 0), sticky=W)
etFactoryName.grid(column=1, row=1, pady=(16, 0))
###Win Level
lbWinLevel.grid(column=0, row=2, pady=(4, 0), sticky=W)
etWinLevel.grid(column=1, row=2, pady=(4, 0))
###Weather
lbWeather.grid(column=0, row=3, pady=(4, 0), sticky='W,N')
frameWeather.grid(column=1, row=3, pady=(4, 0))
cbWeather1.grid(column=0, row=1, sticky=W)
cbWeather2.grid(column=0, row=2, sticky=W)

lbIn.grid(column=1, row=5, pady=(16, 4))
lbOut.grid(column=2, row=5, pady=(16, 4))

###Temp
lbTemp.grid(column=0, row=6, sticky=W)
etTempIn.grid(column=1, row=6)
etTempOut.grid(column=2, row=6)

###Humidity
lbHumidity.grid(column=0, row=7, pady=8, sticky=W)
etHumidityIn.grid(column=1, row=7)
etHumidityOut.grid(column=2, row=7)

###Result
lbTempPoint.grid(column=0, row=8, pady=(8, 0), sticky=W)
lbResTempPointIn.grid(column=1, row=8, pady=(8, 0))
lbResTempPointOut.grid(column=2, row=8, pady=(8, 0))

lbAh.grid(column=0, row=9, pady=(8, 0), sticky=W)
lbResAhIn.grid(column=1, row=9, pady=(8, 0))
lbResAhOut.grid(column=2, row=9, pady=(8, 0))

lbHumidityMax.grid(column=0, row=10, pady=(8, 0), sticky=W)
lbResHumidityMaxIn.grid(column=1, row=10, pady=(8, 0))
lbResHumidityMaxOut.grid(column=2, row=10, pady=(8, 0))

###Button
btnFrame.grid(column=1, row=11, pady=(16, 0))
btnResult.grid(column=0, row=1)
btnSave.grid(column=1, row=1)


def calHumidityMax(mTemp):
    return 5.018 + (0.32321*mTemp) + (8.1847*0.001*mTemp**2) + (3.1243*0.0001*mTemp**3)

def calAH(mHumidityMax, mHumidity):
    return mHumidityMax * mHumidity

def calTempPoint(mTemp, mHumidity):
    return mTemp - (100-mHumidity)/5

#Tab Statistic
tbl = Treeview(tabStatistic)
tbl.pack()

tbl['columns']= ('id', 'factory', 'temp', "humidity", "created_at")

tbl.column("#0", width=0,  stretch=NO)
tbl.column("id",anchor=CENTER, width=80)
tbl.column("factory",anchor=CENTER, width=80)
tbl.column("temp",anchor=CENTER, width=80)
tbl.column("humidity",anchor=CENTER, width=80)
tbl.column("created_at",anchor=CENTER, width=80)

tbl.heading("#0",text="",anchor=CENTER)
tbl.heading("id",text="#",anchor=CENTER)
tbl.heading("factory",text="Factory",anchor=CENTER)
tbl.heading("temp",text="Temp",anchor=CENTER)
tbl.heading("humidity",text="Humidity",anchor=CENTER)
tbl.heading("created_at",text="Created At",anchor=CENTER)

tbl.insert(parent='',index='end',iid=0,text='',
values=('1','B04','20', '81', '2022/01/01 08:43:21'))
tbl.insert(parent='',index='end',iid=1,text='',
values=('2','B06','22', '81', '2022/01/01 08:46:42'))
tbl.insert(parent='',index='end',iid=2,text='',
values=('3','BN3','24', '85', '2022/01/01 08:50:14'))

ws.mainloop()