import math
import pickle
import sys

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QWidget, QComboBox
from PyQt5 import QtCore, Qt


import astar2
import mouse_tracker
import piste
import presentationvoiture

import affichage_piste


class Selector(QWidget):
    def __init__(self):
        super().__init__()

        self.cb = QComboBox()
        self.cb.addItems(["Aléatoire", "100", "200", "300", "400", "500", "600", "700", "800", "900", "1000"])
        b2 = QPushButton("Enregistré (sans A*)")
        b3 = QPushButton("Enregistré (avec A*)")
        b4 = QPushButton("Dessin manuel")

        self.cb.currentIndexChanged.connect(self.aleatoire)
        b2.clicked.connect(self.enregistresansA)
        b3.clicked.connect(self.enregistreavecA)
        b4.clicked.connect(self.manuel)

        vbox = QVBoxLayout()
        h1box = QHBoxLayout()
        h2box = QHBoxLayout()
        vbox.addLayout(h1box)
        vbox.addLayout(h2box)
        h1box.addWidget(self.cb)
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
        self.chemin = piste.creationpiste(int(self.cb.currentText()))
        self.lancervoitureselector()


    def enregistresansA(self):
        self.close()

        try:
            with open('data', 'rb') as fichier:
                mon_depickler = pickle.Unpickler(fichier)
                self.chemin = mon_depickler.load()
                self.lancervoitureselector()
        except:
            print("Il n'y a pas de fichier enregistré")

    def enregistreavecA(self):
        self.close()
        try:
            with open('alldata', 'rb') as fichier:
                depickler = pickle.Unpickler(fichier)
                [self.chemin, self.car] = depickler.load()
                self.affichagefentresimu()
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
        self.firstview.voiturechoisie.connect(self.creervoiture)
        self.firstview.show()

    def creervoiture(self):
        self.car = self.firstview.car
        if not self.car.position:
            astar2.astar(self.chemin,self.car)
        self.affichagefentresimu()

    def affichagefentresimu(self):
        windows = affichage_piste.Dessin(self.chemin, self.car)
        windows.show()

    def fermetureMousetrcker(self):
        self.chemin = self.ex.chemin
        self.lancervoitureselector()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = Selector()

    sys.exit(app.exec_())