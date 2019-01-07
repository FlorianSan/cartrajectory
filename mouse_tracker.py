import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter

import piste
import affichage_piste

class MouseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Dessin Piste')
        self.label = QLabel(self)
        self.label.resize(500, 40)
        self.show()
        self.pos = None
        self.point = []
        self.close = False


    def mouseMoveEvent(self, event):
        self.pos = event.pos()
        self.update()

    def mousePressEvent(self, event):
        self.point.append(piste.Point(event.x(), event.y()))
        self.update()

    def paintEvent(self, event):
        q = QPainter(self)
        if len(self.point)>1:
            for i in range(len(self.point)-1):
                q.drawLine(self.point[i].x, self.point[i].y, self.point[i+1].x,self.point[i+1].y)
            if self.pos :
                q.drawLine(self.point[len(self.point)-1].x, self.point[len(self.point)-1].y,  self.pos.x(),  self.pos.y())

    def closeEvent(self, event):
        self.close = True


def dessinpiste():
    app = QApplication(sys.argv)
    ex = MouseTracker()
    sys.exit(app.exec_())
    while not ex.close:
        if ex.close:
            return

if __name__ == "__main__":

    dessinpiste()