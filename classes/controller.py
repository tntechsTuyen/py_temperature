
class Controller():
    def __init__(self, _model):
        self.model = _model

    def getDataLog(self):
        data = self.model.readData(None)
        return data

    def writeDataLog(self, _obj):
        res = _obj.checkData()
        if res['check'] == 1 :
            self.model.writeData(None, _obj.getLog())
        return res['message'];