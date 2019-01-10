import sys, math
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import pyqtSignal, Qt



import piste
import affichage

class MouseTracker(QWidget):
    listeMouseTracker = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Dessin Piste')
        self.label = QLabel(self)
        self.label.resize(500, 40)
        self.pos = None
        self.pointsm = [piste.Point(0, 0)]  # liste des points milieux
        self.pointsg = []  # liste de points à gauche de l'axe de la piste  piste.Point(50, 50-piste.LARGEUR / 2)
        self.pointsd = []  # liste de points à droite de l'axe de la piste  piste.Point(50, 50+piste.LARGEUR / 2)
        self.angle = 0


    def mouseMoveEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.pos = event.pos()
            self.update()


    def mousePressEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.pointsm.append(piste.Point(event.x(), event.y()))
            if len(self.pointsm) == 2:
                self.angle = affichage.call_angle(piste.Point(1, 0), self.pointsm[-2], self.pointsm[-1])
                self.pointsg.append(piste.Point(0 + (piste.LARGEUR / 2) * math.sin(self.angle),0 - (piste.LARGEUR / 2) * math.cos(self.angle)))
                self.pointsd.append(piste.Point(0 - (piste.LARGEUR / 2) * math.sin(self.angle),0 + (piste.LARGEUR / 2) * math.cos(self.angle)))

            if len(self.pointsm) > 2:
                angle = affichage.call_angle(self.pointsm[-1], self.pointsm[-2], self.pointsm[-3])
                if angle>0:
                    angle = math.pi - angle
                elif angle<0:
                    angle = -(math.pi - abs(angle))
                self.angle += angle/2
                self.pointsg.append(piste.Point(self.pointsm[-2].x + (piste.LARGEUR / 2) * math.sin(self.angle), self.pointsm[-2].y - (piste.LARGEUR / 2) * math.cos(self.angle)))
                self.pointsd.append(piste.Point(self.pointsm[-2].x - (piste.LARGEUR / 2) * math.sin(self.angle), self.pointsm[-2].y + (piste.LARGEUR / 2) * math.cos(self.angle)))

            self.update()


    def paintEvent(self, event):

        q = QPainter(self)
        if len(self.pointsm)>=1:
            for i in range(len(self.pointsm) - 1):
                q.drawLine(self.pointsm[i].x, self.pointsm[i].y, self.pointsm[i+1].x,self.pointsm[i+1].y)
        if len(self.pointsd)>1:
            for j in range(len(self.pointsd) - 1):
                q.drawLine(self.pointsg[j].x, self.pointsg[j].y, self.pointsg[j + 1].x, self.pointsg[j + 1].y)
                q.drawLine(self.pointsd[j].x, self.pointsd[j].y, self.pointsd[j + 1].x, self.pointsd[j + 1].y)
        if self.pos:
            q.drawLine(self.pointsm[-1].x, self.pointsm[-1].y, self.pos.x(), self.pos.y())



    def closeEvent(self, event):
        self.pointsm.pop()
        self.chemin = [self.pointsm,self.pointsg,self.pointsd]
        self.listeMouseTracker.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MouseTracker()
    ex.show()
    sys.exit(app.exec_())