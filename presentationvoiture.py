from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsView, QShortcut
VITESSE_MAX=85
ACCEL_MAX= 14
VIRAGE_MAX=50
EMPAMAX = 5
FILE='voiture.txt'

class FirstView(QtWidgets.QWidget):
    voiturechoisie = pyqtSignal()
    def __init__(self):
        super().__init__()
        root_layout = QtWidgets.QVBoxLayout(self)
        #truc=self.createH()
        self.setWindowTitle('caractéristique voiture')
        
        self.choisie = None
        Voiture = self.add_voiture()
        for i in range(len(Voiture)):
            root_layout.addLayout(self.ajout_sld(Voiture[i]))
            #return(self.ajout_sld(Voiture[i]))
            
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
        self.choisie = car
        self.voiturechoisie.emit()
        self.close()
        
        
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
    