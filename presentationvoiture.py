from PyQt5 import QtGui, QtCore, QtWidgets
#from PyQt5.QtGui import 
from PyQt5.QtWidgets import QGraphicsView, QShortcut
VITESSE_MAX=300
VITESSE_MIN=0
ACCEL_MAX= 1.5*9.81
ACCEL_MIN=0  #0.5*9.81
VIRAGE_MAX=50
VIRAGE_MIN=0
FILE='voiture.txt'

class FirstView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root_layout = QtWidgets.QVBoxLayout(self)
        #truc=self.createH()
        self.setWindowTitle('caractéristique voiture')
        Voiture = self.add_voiture()
        for i in range(len(Voiture)):
            root_layout.addLayout(self.ajout_sld(Voiture[i]))
            #return(self.ajout_sld(Voiture[i]))
            
    def add_voiture(self):
        Voiture=[]
        with open(FILE,'r') as fichier:
            for line in fichier:
                Voiture.append(line.split(' '))
        return(Voiture)
        
    def ajout_sld(self,voiture):
        H=QtWidgets.QHBoxLayout()
        V=QtWidgets.QVBoxLayout()
        V.setContentsMargins(12,12,12,12)
        name=QtWidgets.QLabel(voiture[0])
        V.addWidget(name)
        A=horizontal_box('accélération',int(ACCEL_MIN),int(ACCEL_MAX),int(voiture[2]))
        V.addLayout(A)
        Vi=horizontal_box('vitesse',VITESSE_MIN,VITESSE_MAX,int(voiture[1]))
        V.addLayout(Vi)
        Vir=horizontal_box('virage',VIRAGE_MIN,VIRAGE_MAX,int(voiture[3]))
        V.addLayout(Vir)
        V.addStretch
        H.addLayout(V)
        radio = QtWidgets.QPushButton('prendre {}'.format(voiture[0]))
        radio.clicked.connect(lambda : self.btnstate(voiture))
        H.addWidget(radio)
        return(H)
        
    def btnstate(self,car):
        self.close()
        print(car.split('\n'))
        
        
def horizontal_box(nom,mini,maxi,valeur):
    A=QtWidgets.QHBoxLayout()
    A.addWidget(QtWidgets.QLabel('{}'.format(nom)))
    W=QtWidgets.QProgressBar() #QtCore.Qt.Horizontal
    W.setValue((valeur-mini)*100/(maxi-mini))
    A.addWidget(W)
    A.addWidget(QtWidgets.QLabel('{}'.format(valeur)))
    A.addWidget(QtWidgets.QLabel('{}'.format(maxi)))
    return(A)
    
if __name__=='__main__':
    app = QtWidgets.QApplication([])
    main_window = FirstView()
    main_window.show()
    app.exec_()
    