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


    def mouseMoveEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.pos = event.pos()
            self.update()


    def mousePressEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.pointsmclick.append(piste.Point(event.x(), event.y()))
            self.pointsm+=self.sectionner(self.pointsmclick[-2],self.pointsmclick[-1])
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
        minimun = min(len(self.pointsm),len(self.pointsd),len(self.pointsg))
        self.chemin = [self.pointsm[:minimun], self.pointsg[:minimun], self.pointsd[:minimun]]
        self.listeMouseTracker.emit()
        self.close()

    def sectionner(self,oldpoint,newpoint):

        deltax, deltay = newpoint.x - oldpoint.x, newpoint.y - oldpoint.y
        iteration = int(deltax // piste.PAS)
        coeff_directeur = deltay / deltax
        k = newpoint.y - coeff_directeur * newpoint.x
        liste=[]
        for i in range(1, iteration):
            x = oldpoint.x + i * piste.PAS
            liste.append(piste.Point(x, coeff_directeur * x + k))
        liste.append(newpoint)
        return liste

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MouseTracker()
    ex.show()
    sys.exit(app.exec_())