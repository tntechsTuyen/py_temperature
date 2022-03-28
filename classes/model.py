import jsonlines
import datetime
import os

class Model():
    @classmethod
    # Kiểm tra đã có thư mục data chưa
    def checkDir(self):
        if os.path.isdir("data"):
            print("")
        else:
            os.mkdir("data")

    @classmethod
    # Kiểm tra có file dữ liệu không
    def checkPath(self, _fileName):
        self.checkDir()

        if _fileName == None:
            currentTime = datetime.datetime.now()
            mDate = currentTime.strftime("%Y%m")
            _fileName = mDate

        if os.path.isfile(_fileName):
            print("")
        else:
            with open(_fileName, 'w'): pass
        return _fileName

    @classmethod
    # Đọc dữ liệu từ file
    def readData(self, _fileName):
        currentTime = datetime.datetime.now()
        mDate = currentTime.strftime("%Y%m")
        if _fileName == None:
            _fileName = "data/" + mDate+".logs"

        self.checkPath(_fileName)
        with jsonlines.open(_fileName) as reader:
            return list(reader)

    @classmethod
    # Ghi dữ liệu ra file
    def writeData(self, _fileName, _data):
        currentTime = datetime.datetime.now()
        mDate = currentTime.strftime("%Y%m")
        if _fileName == None:
            _fileName = "data/" + mDate + ".logs"
        _data['created_at'] = currentTime.strftime("%Y/%m/%d %H:%M:%S.%f")
        self.checkPath(_fileName)
        with jsonlines.open(_fileName, "a") as writer:  # for writing
            writer.write(_data)
        return True