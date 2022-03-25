from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

class View(Tk):
    def __init__(self, _model, _controller):
        self.model = _model
        self.controller = _controller

        self.iconbitmap("../icon.ico")
        self.title("Phần mềm tính toán điều kiện thông gió nhà kho súng pháo, khí tài lục quân")
        self.tabControl = Notebook(self)
        self.tabStatistic = Frame(self.tabControl)  # Tab Thống kê
        self.tabTemp = Frame(self.tabControl)  # Tab nhập nhiệt độ
        self.tabControl.add(self.tabStatistic, text="Thống kê")  # Thêm tab
        self.tabControl.add(self.tabTemp, text="Nhập dữ liệu")
        self.tabControl.pack(expand=1, fill="both")