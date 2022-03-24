from classes.model import Model
from classes.view import View
from classes.controller import Controller

item1 = {
   "name": "name1",
   "url": "url1"
}

model = Model()
controller = Controller()
view = View(model, controller)