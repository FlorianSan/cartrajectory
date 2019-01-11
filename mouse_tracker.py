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
        self.pos = None
        self.pointsmclick = [piste.Point(0, 0)]  # liste des points milieux
        self.pointsgclick = []  # liste de points à gauche de l'axe de la piste  piste.Point(50, 50-piste.LARGEUR / 2)
        self.pointsdclick = []  # liste de points à droite de l'axe de la piste  piste.Point(50, 50+piste.LARGEUR / 2)
        self.pointsm = [piste.Point(0, 0)]  # liste des points milieux
        self.pointsg = []  # liste de points à gauche de l'axe de la piste  piste.Point(50, 50-piste.LARGEUR / 2)
        self.pointsd = []  # liste de points à droite de l'axe de la piste  piste.Point(50, 50+piste.LARGEUR / 2)
        self.angle = 0
        self.iteration = 0


    def mouseMoveEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.pos = event.pos()
            self.update()


    def mousePressEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.pointsmclick.append(piste.Point(event.x(), event.y()))
            self.iteration = int((self.pointsmclick[-1].x- self.pointsmclick[-2].x)// (piste.PAS*2))

            if len(self.pointsmclick) == 2:
                self.angle = affichage.call_angle(piste.Point(1, 0), self.pointsmclick[-2], self.pointsmclick[-1])
                self.pointsgclick.append(piste.Point(0 + (piste.LARGEUR / 2) * math.sin(self.angle), 0 - (piste.LARGEUR / 2) * math.cos(self.angle)))
                self.pointsdclick.append(piste.Point(0 - (piste.LARGEUR / 2) * math.sin(self.angle), 0 + (piste.LARGEUR / 2) * math.cos(self.angle)))
                self.pointsg.append(piste.Point(0 + (piste.LARGEUR / 2) * math.sin(self.angle), 0 - (piste.LARGEUR / 2) * math.cos(self.angle)))
                self.pointsd.append(piste.Point(0 - (piste.LARGEUR / 2) * math.sin(self.angle), 0 + (piste.LARGEUR / 2) * math.cos(self.angle)))

            if len(self.pointsmclick) > 2:
                angle = affichage.call_angle(self.pointsmclick[-1], self.pointsmclick[-2], self.pointsmclick[-3])
                if angle>0:
                    angle = math.pi - angle
                elif angle<0:
                    angle = -(math.pi - abs(angle))
                self.angle += angle/2
                self.pointsgclick.append(piste.Point(self.pointsmclick[-2].x + (piste.LARGEUR / 2) * math.sin(self.angle), self.pointsmclick[-2].y - (piste.LARGEUR / 2) * math.cos(self.angle)))
                self.pointsdclick.append(piste.Point(self.pointsmclick[-2].x - (piste.LARGEUR / 2) * math.sin(self.angle), self.pointsmclick[-2].y + (piste.LARGEUR / 2) * math.cos(self.angle)))
                self.pointsm += self.sectionner(self.pointsmclick[-3], self.pointsmclick[-2])
                self.pointsg += self.sectionner(self.pointsgclick[-2], self.pointsgclick[-1])
                self.pointsd+=self.sectionner(self.pointsdclick[-2],self.pointsdclick[-1])
        self.update()


    def paintEvent(self, event):

        q = QPainter(self)
        if len(self.pointsmclick)>=1:
            for i in range(len(self.pointsmclick) - 1):
                q.drawLine(self.pointsmclick[i].x, self.pointsmclick[i].y, self.pointsmclick[i + 1].x, self.pointsmclick[i + 1].y)
        if len(self.pointsdclick)>1:
            for j in range(len(self.pointsdclick) - 1):
                q.drawLine(self.pointsgclick[j].x, self.pointsgclick[j].y, self.pointsgclick[j + 1].x, self.pointsgclick[j + 1].y)
                q.drawLine(self.pointsdclick[j].x, self.pointsdclick[j].y, self.pointsdclick[j + 1].x, self.pointsdclick[j + 1].y)
        if self.pos:
            q.drawLine(self.pointsmclick[-1].x, self.pointsmclick[-1].y, self.pos.x(), self.pos.y())



    def closeEvent(self, event):
        self.chemin = [self.pointsm, self.pointsg, self.pointsd]
        self.listeMouseTracker.emit()
        self.close()

    def sectionner(self,oldpoint,newpoint):
        deltax, deltay = newpoint.x - oldpoint.x, newpoint.y - oldpoint.y
        coeff_directeur = deltay / deltax
        k = newpoint.y - coeff_directeur * newpoint.x
        pas = deltax // self.iteration
        liste=[]
        for i in range(1, self.iteration):
            x = oldpoint.x + i * pas
            liste.append(piste.Point(x, coeff_directeur * x + k))
        liste.append(newpoint)
        return liste

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MouseTracker()
    ex.show()
    sys.exit(app.exec_())