import pickle
import sys

import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QWidget
from PyQt5 import QtCore

import astar2
import mouse_tracker
import piste
import presentationvoiture
import voiture
import affichage_piste


class Selector(QWidget):
    def __init__(self):
        super().__init__()

        self.car = voiture.Voiture()

        b1 = QPushButton("Aléatoire")
        b2 = QPushButton("Enregistré (sans A*)")
        b3 = QPushButton("Enregistré (avec A*)")
        b4 = QPushButton("Dessin manuel")

        b1.clicked.connect(self.aleatoire)
        b2.clicked.connect(self.enregistresansA)
        b3.clicked.connect(self.enregistreavecA)
        b4.clicked.connect(self.manuel)

        vbox = QVBoxLayout()
        h1box = QHBoxLayout()
        h2box = QHBoxLayout()
        vbox.addLayout(h1box)
        vbox.addLayout(h2box)
        h1box.addWidget(b1)
        h1box.addWidget(b2)
        h2box.addWidget(b3)
        h2box.addWidget(b4)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 150)
        self.setFixedSize(300, 150)
        self.setWindowTitle('Selector')
        self.show()

    def aleatoire(self):
        self.close()
        self.chemin = piste.creationpiste(300)
        self.lancervoitureselector()


    def enregistresansA(self):
        self.close()
        self.lancervoitureselector()
        try:
            with open('data', 'rb') as fichier:
                mon_depickler = pickle.Unpickler(fichier)
                self.chemin = mon_depickler.load()
        except:
            print("Il n'y a pas de fichier enregistré")

    def enregistreavecA(self):
        self.close()
        self.lancervoitureselector()
        try:
            with open('alldata', 'rb') as fichier:
                depickler = pickle.Unpickler(fichier)
                [self.chemin, self.car] = depickler.load()
        except:
            print("Il n'y a pas de fichier enregistré")


    def manuel(self):
        self.close()

        self.ex = mouse_tracker.MouseTracker()
        self.ex.listeMouseTracker.connect(self.fermetureMousetrcker)
        self.ex.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ex.show()

    def lancervoitureselector(self):
        self.firstview = presentationvoiture.FirstView()
        self.firstview.voiturechoisie.connect(self.defvoiture)
        self.firstview.show()

    def defvoiture(self):

        voiture = self.firstview.choisie
        A=[voiture[0],float(voiture[1]),float(voiture[2]),int(voiture[3]),float(voiture[4]),int(voiture[5]),float(voiture[6]),float(voiture[7])]
        [self.car.name,self.car.vitessemax,accelerationmax,virage,self.car.empattement,self.car.masse, self.car.longueur, self.car.largeur] = A
        self.car.pasvirage = float(virage)*np.pi/(180*self.car.deltavirage)
        self.car.pasacceleration = float(accelerationmax)/self.car.deltaacc
        if not self.car.position:
            astar2.astar(self.chemin,self.car)
        windows = affichage_piste.Dessin(self.chemin,self.car)
        windows.show()


    def fermetureMousetrcker(self):
        self.chemin = self.ex.chemin
        self.lancervoitureselector()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = Selector()
    sys.exit(app.exec_())