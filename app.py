from tkinter import *
from common.view import View

class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("EHS")
        self.geometry("600x400")
        view = View(self)


        view.createTabList()
        view.createTabInsert()

if __name__ == '__main__':
    app = App()
    app.mainloop()