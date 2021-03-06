import sys, math
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import pyqtSignal, Qt



import matplotlib.pyplot as plt



import piste
import affichage
import affichage_piste

class MouseTracker(QWidget):
    listeMouseTracker = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        

    def initUI(self): # Initialisation de l'interface graphique
        self.setWindowTitle('Dessin Piste')
        self.label = QLabel(self)
        self.label.setText("Dessiner en maintenant shift + clic puis valider            Click droit supprime le dernier point")
        self.button = QPushButton('Ok', self)
        self.button.clicked.connect(self.valide)
        self.label.move(self.width() / 2 - 250, 0)
        self.button.move((self.width() / 2) + 400, 0)


        self.pointsm = [piste.Point(0, 0)]  # liste des points milieux subdiviser
        self.pointsg = []  # liste de points à gauche de l'axe de la piste subdiviser
        self.pointsd = []  # liste de points à droite de l'axe de la piste subdiviser
        self.angle = 0
        self.nbrsection = 0
        self.largeur = piste.LARGEUR

        self.pos = None
        self.pointsmclick = [piste.Point(-piste.PAS, 0), piste.Point(0, 0)]  # liste des points milieux cliquer
        self.pointsgclick = [piste.Point(-piste.PAS, self.largeur / 2)]  # liste de points à gauche de l'axe de la piste cliquer
        self.pointsdclick = [piste.Point(-piste.PAS, -self.largeur / 2)]  # liste de points à droite de l'axe de la piste cliquer



    def mouseMoveEvent(self, event):  #Evenement déplacement de la souris
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.pos = event.pos()
            self.update()


    def mousePressEvent(self, event): #Evenement clic de la souris
        if event.button() == Qt.LeftButton: #teste le bouton gauche est appuyé
            if QApplication.keyboardModifiers() == Qt.ShiftModifier: #teste le bouton shift

                newpoint = piste.Point(event.x(), event.y())  # récuperer le point cliqué

                if newpoint.x != self.pointsmclick[-1].x or newpoint.y != self.pointsmclick[-1].y:  # teste si on clique pas deux fois au même endroit

                    self.pointsmclick.append(newpoint)

                    if len(self.pointsmclick) == 3: #ajoute les premiers point gauche et droite
                        self.angle = affichage.call_angle(piste.Point(1, 0), self.pointsmclick[-2], self.pointsmclick[-1])

                        self.pointsgclick.append(piste.Point(self.pointsmclick[-2].x + (self.largeur / 2) * math.sin(self.angle),self.pointsmclick[-2].y - (self.largeur / 2) * math.cos(self.angle)))
                        self.pointsdclick.append(piste.Point(self.pointsmclick[-2].x - (self.largeur / 2) * math.sin(self.angle),self.pointsmclick[-2].y + (self.largeur / 2) * math.cos(self.angle)))

                        self.pointsg.append(piste.Point(self.pointsmclick[-2].x + (self.largeur / 2) * math.sin(self.angle),self.pointsmclick[-2].y - (self.largeur / 2) * math.cos(self.angle)))
                        self.pointsd.append(piste.Point(self.pointsmclick[-2].x - (self.largeur / 2) * math.sin(self.angle),self.pointsmclick[-2].y + (self.largeur / 2) * math.cos(self.angle)))

                    if len(self.pointsmclick) > 3:
                        angle = affichage.call_angle(self.pointsmclick[-1], self.pointsmclick[-2], self.pointsmclick[-3])
                        if angle>0:
                            angle = math.pi - angle
                        elif angle<0:
                            angle = -(math.pi - abs(angle))
                        demi_angle = angle/2
                        self.angle += demi_angle
                        self.pointsgclick.append(piste.Point(self.pointsmclick[-2].x + (self.largeur / 2) * math.sin(self.angle), self.pointsmclick[-2].y - (self.largeur / 2) * math.cos(self.angle)))
                        self.pointsdclick.append(piste.Point(self.pointsmclick[-2].x - (self.largeur / 2) * math.sin(self.angle), self.pointsmclick[-2].y + (self.largeur / 2) * math.cos(self.angle)))
                        longueur = math.sqrt((self.pointsmclick[-2].x - self.pointsmclick[-3].x) ** 2 + (self.pointsmclick[-2].y - self.pointsmclick[-3].y) ** 2)
                        self.nbrsection = int(longueur // (piste.PAS))
                        self.pointsm += self.sectionner(self.pointsmclick[-3], self.pointsmclick[-2])
                        self.pointsg += self.sectionner(self.pointsgclick[-2], self.pointsgclick[-1])
                        self.pointsd += self.sectionner(self.pointsdclick[-2],self.pointsdclick[-1])
                        self.angle += demi_angle
        self.update()


    def paintEvent(self, event): #Evenement qui met à jour l'affichage
        q = QPainter(self)
        q.setRenderHint(QPainter.Antialiasing, True)
        if len(self.pointsmclick)>=1:
            for i in range(len(self.pointsmclick) - 1):
                q.drawLine(self.pointsmclick[i].x, self.pointsmclick[i].y, self.pointsmclick[i + 1].x, self.pointsmclick[i + 1].y)
        if len(self.pointsdclick)>1:
            for j in range(len(self.pointsdclick) - 1):
                q.drawLine(self.pointsgclick[j].x, self.pointsgclick[j].y, self.pointsgclick[j + 1].x, self.pointsgclick[j + 1].y)
                q.drawLine(self.pointsdclick[j].x, self.pointsdclick[j].y, self.pointsdclick[j + 1].x, self.pointsdclick[j + 1].y)
        if self.pos:
            q.drawLine(self.pointsmclick[-1].x, self.pointsmclick[-1].y, self.pos.x(), self.pos.y())


    def valide(self): # Slot appelé lors du clic sur le bouton OK
        self.chemin = [self.pointsm, self.pointsg, self.pointsd]
        print(len(self.pointsm))
        self.listeMouseTracker.emit()
        self.close()


    def closeEvent(self, event):
        self.close()

    def sectionner(self,oldpoint,newpoint): #Fonction qui decoupe un segment en plusieur segment

        deltax, deltay = newpoint.x - oldpoint.x, newpoint.y - oldpoint.y
        if deltax !=0:
            coeff_directeur = deltay / deltax
            b = newpoint.y - coeff_directeur * newpoint.x
            pas = deltax / self.nbrsection
            liste = []
            for i in range(1, self.nbrsection):
                x = oldpoint.x + i * pas
                point = piste.Point(x, coeff_directeur * x + b)
                liste.append(point)
            liste.append(newpoint)
        else:
            pas = deltay / self.nbrsection
            liste = []
            for i in range(1, self.nbrsection):
                point = piste.Point(oldpoint.x, oldpoint.y + i * pas)
                liste.append(point)
            liste.append(newpoint)
        return liste

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MouseTracker()
    ex.show()
    sys.exit(app.exec_())
    