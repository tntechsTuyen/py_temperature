class Temp():
    def __init__(self):
        self.name = ""
        self.win = 0
        self.weather = ""
        self.checkWeather = 1
        self.tempIn = 0
        self.tempOut = 0
        self.humidityIn = 0
        self.humidityOut = 0

    def setData(self, data):
        self.name = data[0]
        self.win = data[1]
        self.checkWeather = 1
        self.tempIn = data[2]
        self.tempOut = data[3]
        self.humidityIn = data[4]
        self.humidityOut = data[5]
        self.weather = data[6]

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

    def getLog(self):
        return {
            "name": self.name,
            "win": self.win,
            "weather": self.weather,
            "temp_in": self.tempIn,
            "temp_out": self.tempOut,
            "humidity_in": self.humidityIn,
            "humidity_out": self.humidityOut,

        }

    def getData(self):
        return {
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
