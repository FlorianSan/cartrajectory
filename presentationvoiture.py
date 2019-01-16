import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsView, QShortcut
import voiture
VITESSE_MAX=139
ACCEL_MAX= 14
VIRAGE_MAX=50
EMPAMAX = 5
FILE='voiture.txt'

# Test

class FirstView(QtWidgets.QWidget):
    voiturechoisie = pyqtSignal()
    def __init__(self):
        super().__init__()
        root_layout = QtWidgets.QGridLayout(self) #QVBoxLayout(self)
        self.setWindowTitle('caractéristique voiture')
        self.resize(100,600)

        self.car = voiture.Voiture()

        Voiture = self.add_voiture()
        for i in range(len(Voiture)):
            root_layout.addLayout(self.ajout_sld(Voiture[i]),i%4,i//4)



            
    def add_voiture(self):
        Voiture=[]
        with open(FILE,'r') as fichier:
            for line in fichier:
                line = line.split(' ')
                if line[0]!='#':
                    Voiture.append(line)
        return(Voiture)
        
    def ajout_sld(self,voiture):
        H=QtWidgets.QHBoxLayout()
        
        V=QtWidgets.QVBoxLayout()
        V.setContentsMargins(12,12,12,12)
        name=QtWidgets.QLabel(voiture[0])
        V.addWidget(name)
        A=horizontal_box(['accélération','m/s²'],ACCEL_MAX,float(voiture[2]))
        V.addLayout(A)
        Vi=horizontal_box(['vitesse','m/s'],VITESSE_MAX,float(voiture[1]))
        V.addLayout(Vi)
        Vir=horizontal_box(['virage','°'],VIRAGE_MAX,float(voiture[3]))
        V.addLayout(Vir)
        E = horizontal_box(['Empattement','m'],EMPAMAX,float(voiture[4]))
        V.addLayout(E)
        V.addStretch
        H.addLayout(V)
        radio = QtWidgets.QPushButton('prendre {}'.format(voiture[0]))
        radio.clicked.connect(lambda : self.btnstate(voiture))
        H.addWidget(radio)
        return(H)
        
    def btnstate(self,car):
        self.car.name = car[0]
        self.car.vitessemax =float(car[1])
        accelerationmax = float(car[2])
        virage = int(car[3])
        self.car.empattement = float(car[4])
        self.car.masse = int(car[5])
        self.car.longueur = float(car[6])
        self.car.largeur =  float(car[7])
        self.car.pasvirage = float(virage) * np.pi / (180 * self.car.deltavirage)
        self.car.pasacceleration = float(accelerationmax) / self.car.deltaacc
        self.close()
        self.voiturechoisie.emit()

        
        
def horizontal_box(nom,maxi,valeur):
    A=QtWidgets.QHBoxLayout()
    A.addWidget(QtWidgets.QLabel('{}'.format(nom[0])))
    A.addStretch
    W=QtWidgets.QProgressBar() #QtCore.Qt.Horizontal
    W.setValue(valeur*100/maxi)
    A.addWidget(W)
    A.addStretch
    A.addWidget(QtWidgets.QLabel('{} {}'.format(valeur,nom[1])))
    #A.addWidget(QtWidgets.QLabel('{}'.format(maxi)))
    return(A)
    
if __name__=='__main__':
    app = QtWidgets.QApplication([])
    main_window = FirstView()
    main_window.show()
    app.exec_()
    