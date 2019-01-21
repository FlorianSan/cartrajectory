
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRectF, QPoint,Qt
from PyQt5.QtGui import QTransform, QBrush, QPen
import math
import piste


class CarMotion:
    def __init__(self, windows, car):

        self.t = 0
        self.car = car
        self.windows = windows

        self.car_group = QtWidgets.QGraphicsItemGroup()
        self.windows.scene.addItem(self.car_group)
        self.r = self.car.direction[0]*(180/math.pi) - 90
        transform = QTransform()
        transform.rotate(self.r)
        self.car_group.setTransform(transform)
        self.car_group.setZValue(1)
        self.path = QtGui.QPainterPath()
        self.voiture = QRectF(QPoint(self.car.position[0].x-self.car.longueur / 2, self.car.position[0].y-self.car.largeur / 2), QPoint(self.car.position[0].x + self.car.longueur / 2, self.car.position[0].y + self.car.largeur / 2))
        # self.voiture = QRectF(QPoint(self.car.position[0].x-self.car.largeur/2, self.car.position[0].y-self.car.longueur/2), QPoint(self.car.position[0].x+self.car.largeur/2, self.car.position[0].y+self.car.longueur/2))
        self.path.addRect(self.voiture)
        brush = QBrush(QtGui.QColor("Red"))
        item = QtWidgets.QGraphicsPathItem(self.path, self.car_group)
        item.setBrush(brush)
        item.setPen(QPen(QtGui.QColor("Red")))



    def updateValues(self):
        if self.t+1 < len(self.car.position):

            self.r = self.car.direction[self.t]*(360/(2*math.pi))-90
            transform = QTransform()
            transform.translate(self.car.position[self.t].x, self.car.position[self.t].y)
            transform.rotate(self.r)
            self.car_group.setTransform(transform)
            if self.t > 0:

                maxi = self.car.vitessemax
                vitesse = abs(int(self.car.vitesse[self.t - 1] * 255 / maxi))
                self.windows.scene.addLine(self.car.position[self.t-1].x, self.car.position[self.t - 1].y, self.car.position[self.t].x, self.car.position[self.t].y, QPen(QtGui.QColor(vitesse, 255 - vitesse, 0), 0))

            self.windows.update()  # <-- update the window!
            self.t += 1

    def redemarrer(self):
        self.t = 0
        self.r = self.car.direction[0]*(180/math.pi)-90
        transform = QTransform()
        # self.car_group.setTransformOriginPoint(self.car.position[self.t].x, self.car.position[self.t].y)
        transform.translate(self.car.position[self.t].x, self.car.position[self.t].y)
        transform.rotate(self.r)
        self.car_group.setTransform(transform)


def call_angle(point1, point2, point3):
    orientation = piste.clockwise(point1, point2, point3)

    if orientation:
        signe = 1

    else:
        signe = - 1

    b = math.sqrt((point2.x - point3.x) ** 2 + (point2.y - point3.y) ** 2)
    a = math.sqrt((point1.x - point3.x) ** 2 + (point1.y - point3.y) ** 2)
    c = math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
    return signe*abs(math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))


def call_angledeg(point1, point2, point3):
    return call_angle(point1, point2, point3)*(360/(2*math.pi))
