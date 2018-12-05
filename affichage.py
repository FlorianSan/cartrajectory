
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer


class CarMotion():
    def __init__(self, windows):
        self.a = 10
        self.b = 15
        self.x = 90
        self.y = 60
        self.windows = windows
        car_group = QtWidgets.QGraphicsItemGroup()
        self.windows.scene.addItem(car_group)
        car_group.setZValue(1)
        path = QtGui.QPainterPath()
        path.addRect(self.a,self.b,self.x,self.y)
        QtWidgets.QGraphicsPathItem(path, car_group)



    def updateValues(self):
        self.a += 100
        self.x += 100
        self.windows.update()  # <-- update the window!