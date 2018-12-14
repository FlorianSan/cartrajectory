
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRectF, QPoint
from PyQt5.QtGui import QTransform, QBrush
import math
import piste

PAS = 1

class CarMotion():
    def __init__(self, windows, car):

        self.t=1

        self.r=0
        self.car = car
        self.windows = windows

        self.car_group = QtWidgets.QGraphicsItemGroup()
        self.windows.scene.addItem(self.car_group)
        self.car_group.setZValue(0)
        self.path = QtGui.QPainterPath()
        self.voiture = QRectF(QPoint(self.car.position[1].x-self.car.longueur/2, self.car.position[1].y-self.car.largeur/2), QPoint(self.car.position[1].x+self.car.longueur/2, self.car.position[1].y+self.car.largeur/2))
        self.path.addRect(self.voiture)
        brush = QBrush(QtGui.QColor("Red"))
        item = QtWidgets.QGraphicsPathItem(self.path, self.car_group)
        item.setBrush(brush)



    def updateValues(self):
        if self.windows.play and self.t+1 < len(self.car.position):
            self.r += cal_angle(self.car.position[self.t-1],self.car.position[self.t],self.car.position[self.t+1])
            transform = QTransform()
            self.car_group.setTransformOriginPoint(self.car.position[self.t].x, self.car.position[self.t].y)
            transform.translate(self.car.position[self.t].x, self.car.position[self.t].y)
            transform.rotate(self.r)
            self.car_group.setTransform(transform)
            self.windows.update()  # <-- update the window!
            self.t+=1
        if self.windows.redemarrer:
            self.t=1
            self.windows.redemarrer = False





def cal_angle(point1, point2, point3):
    orientation = piste.clockwise(point1,point2,point3)
    if orientation:
        signe = 1
    else:
        signe = -1
    b = math.sqrt((point2.x-point3.x)**2+(point2.y-point3.y)**2)
    a = math.sqrt((point1.x-point3.x)**2+(point1.y-point3.y)**2)
    c = math.sqrt((point1.x-point2.x)**2+(point1.y-point2.y)**2)
    return signe*abs(math.acos((b**2+c**2-a**2)/(2*b*c)))*(360/(2*math.pi))

if __name__ == "__main__":
    p1=piste.Point(1,2)
    p2 = piste.Point(0, 0)
    p3 = piste.Point(0, 1)
    print(cal_angle(p1,p2,p3))
