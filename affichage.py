
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRectF, QPointF, QSizeF
from PyQt5.QtGui import QTransform, QBrush


PAS = 1

class CarMotion():
    def __init__(self, windows, car):

        self.t=0

        self.r=0
        self.car = car
        self.windows = windows

        self.car_group = QtWidgets.QGraphicsItemGroup()
        self.windows.scene.addItem(self.car_group)
        self.car_group.setZValue(0)
        self.path = QtGui.QPainterPath()
        voiture = QRectF(QPointF(self.car.position[0].x, self.car.position[0].y), QSizeF(self.car.longueur, self.car.largeur))
        self.path.addRect(voiture)
        self.car_group.setTransformOriginPoint(voiture.center())
        brush = QBrush(QtGui.QColor("Red"))
        item = QtWidgets.QGraphicsPathItem(self.path, self.car_group)
        item.setBrush(brush)



    def updateValues(self):
        if self.windows.play:
            self.r+=0

            transform = QTransform()
            transform.translate(self.car.position[self.t].x, self.car.position[self.t].y)
            transform.rotate(self.r)


            self.car_group.setTransform(transform)
            self.windows.update()  # <-- update the window!
            self.t+=1