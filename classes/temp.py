class Temp():
    @classmethod
    # Constructor: Phương thức khời tạo đối tượng
    def __init__(self):
        self.name = ""
        self.win = 0
        self.weather = ""
        self.checkWeather = 1
        self.tempIn = 0
        self.tempOut = 0
        self.humidityIn = 0
        self.humidityOut = 0

    @classmethod
    # cập nhật dữ liệu
    def setData(self, _data):
        self.name = _data['name']
        self.win = _data['win']
        self.checkWeather = 1
        self.tempIn = _data["temp_in"]
        self.tempOut = _data["temp_out"]
        self.humidityIn = _data['humidity_in']
        self.humidityOut = _data['humidity_in']
        self.weather = _data['weather']

    @classmethod
    # cập nhật tên nhà kho
    def setName(self, mName):
        self.name = mName

    @classmethod
    # Cập nhật cấp độ gió
    def setWin(self, mWin):
        self.win = int(mWin)

    @classmethod
    # Cập nhật thời tiết
    def setWeather(self, mWeather):
        self.weather = mWeather

    def setCheckWeather(self, mCheck):
        self.checkWeather = mCheck

    @classmethod
    # Cập nhật nhiệt độ trong nhà kho
    def setTempIn(self, mTempIn):
        if len(mTempIn.strip()) == 0:
            self.tempIn = 0
        else:
            self.tempIn = float(mTempIn)

    @classmethod
    # Cập nhật nhiệt độ ngoài nhà kho
    def setTempOut(self, mTempOut):
        if len(mTempOut.strip()) == 0:
            self.tempOut = 0
        else:
            self.tempOut = float(mTempOut)

    @classmethod
    # Cập nhật độ ẩm trong nhà kho
    def setHumidityIn(self, mHumidityIn):
        if len(mHumidityIn.strip()) == 0:
            self.humidityIn = 0
        else:
            self.humidityIn = float(mHumidityIn)

    @classmethod
    # Cập nhật độ ẩm ngoài nhà kho
    def setHumidityOut(self, mHumidityOut):
        if len(mHumidityOut.strip()) == 0:
            self.humidityOut = 0
        else:
            self.humidityOut = float(mHumidityOut)

    @classmethod
    # Tính toán độ ẩm cực đại
    def calHumidityMax(self, t):
        return 5.018 + (0.32321 * t) + (8.1847 * 0.001 * t ** 2) + (3.1243 * 0.0001 * t ** 3)

    @classmethod
    # Tính toán độ ẩm tuyệt đối
    def calAH(self, h1, h2):
        return h1 * h2

    @classmethod
    # Tính toán nhiệt độ điểm sương
    def calTempPoint(self, t, h):
        return t - (100 - h) / 5

    @classmethod
    # Lấy ra biện pháp đối với dữ liệu đầu vào
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

    @classmethod
    # Kiểm tra dữ liệu đầu vào
    def checkData(self):
        message = ""
        check = 1
        if len(self.name.strip()) == 0:
            check = 0
            message = "Bạn chưa nhập tên nhà kho"
        elif self.tempIn <= 0 or self.tempOut <= 0:
            check = 0
            message = "Nhiệt độ không hợp lệ"
        elif self.humidityIn <= 0 or self.humidityOut <= 0:
            check = 0
            message = "Độ ẩm không hợp lệ"

        return {"check": check, "message": message}

    @classmethod
    # Dữ liệu lưu file
    def getLog(self):
        return {
            "name": self.name,
            "win": self.win,
            "weather": self.weather,
            "temp_in": self.tempIn,
            "temp_out": self.tempOut,
            "humidity_in": self.humidityIn,
            "humidity_out": self.humidityOut
        }

    @classmethod
    # Dữ liệu hiển thị
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
