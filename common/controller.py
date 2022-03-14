from model import Model
from view import View

model = Model()
factory = model.findAll("factory")
print(factory)