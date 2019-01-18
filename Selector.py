import math
import pickle
import sys
import os

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
        self.exec = Lancerexec()
        self.cb = QComboBox()
        self.cb.addItems(["Aléatoire", "Petite piste", "Moyenne piste", "Grande piste", "Géante piste"])
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
        self.setFixedSize(400, 150)
        self.setWindowTitle('Selector')
        self.show()

    def aleatoire(self):
        self.close()
        if self.cb.currentText() == "Petite piste":
            longueur = 250
        elif self.cb.currentText() == "Moyenne piste":
            longueur = 500
        elif self.cb.currentText() == "Grande piste":
            longueur = 750
        elif self.cb.currentText() == "Géante piste":
            longueur = 1000
        self.exec.chemin = piste.creationpiste(longueur)
        self.exec.lancervoitureselector()


    def enregistresansA(self):
        self.close()
        listefichier = ['sans A*']+os.listdir('./DATA')
        self.data = DATA(listefichier,'./DATA')
        self.data.show()

    def enregistreavecA(self):
        self.close()
        listefichier = ['avec A*']+os.listdir('./DATAstar')
        self.data = DATA(listefichier,'./DATAstar')
        self.data.show()        

    def manuel(self):
        self.close()

        self.ex = mouse_tracker.MouseTracker()
        self.ex.listeMouseTracker.connect(lambda : self.exec.fermetureMousetrcker(self.ex.chemin))
        self.ex.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ex.showMaximized()

class DATA(QWidget):
    def __init__(self,listefichier,racine):
        super().__init__()
        self.racine = racine
        self.exec = Lancerexec()
        self.cb = QComboBox()
        if len(listefichier)==1:
            print("Il n'y a pas de fichier enregistré")
            self.close()
        else:
            self.cb.addItems(listefichier)
            self.cb.currentIndexChanged.connect(self.fichierchoisi)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.cb)
        self.setLayout(vbox)
        self.setFixedSize(230, 70)
        self.setWindowTitle('Choix data')
        self.show()
    
    def fichierchoisi(self):
        self.close()
        self.filename = self.racine+'/'+self.cb.currentText()
        if self.racine == './DATAstar':
            self.exec.avecA(self.filename)
        else:
            self.exec.sansA(self.filename)
            
class Lancerexec(): #nouvelle classe car utilisée par DATA et Selector.manuel Selector.aleatoire
    def sansA(self,filename):
        with open(filename, 'rb') as fichier:
            mon_depickler = pickle.Unpickler(fichier)
            self.chemin = mon_depickler.load()
            self.lancervoitureselector()

    def avecA(self, filename):
        with open(filename, 'rb') as fichier:
            depickler = pickle.Unpickler(fichier)
            [self.chemin, self.car] = depickler.load()
            self.affichagefentresimu()

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

    def fermetureMousetrcker(self,chemin):
        self.chemin = chemin
        self.lancervoitureselector()
        





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = Selector()

    sys.exit(app.exec_())