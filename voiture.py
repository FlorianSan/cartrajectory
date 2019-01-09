import numpy as np

import piste,presentationvoiture

PASDETEMPS = 0.1 #en secondes
ACCELERATION = 0.1 #en m/s²
DELTAACC = 5
VIRAGE = (8*np.pi)/180 #pas de virage
DELTAVIR = 5
VMAX = 40

class Voiture:
    def __init__(self, masse, longueur, largeur):
        self.masse = masse
        self.longueur = longueur
        self.largeur = largeur
        self.accelerationmax = 0
        self.vitssemax = 0
        self.pasvirage = 0
        self.position = [piste.Point(0,0)]
        self.acceleration = [0]
        self.vitesse = [0]
        self.direction = [np.pi]
        self.choisie = None
        self.firstview = presentationvoiture.FirstView()
        self.firstview.voiturechoisie.connect(self.defvoiture)
        self.firstview.show()

    def get_position(self, t):
        return self.position[t]

    def defvoiture(self):
        self.choisie = self.firstview.choisie
        self.vitssemax = self.choisie[1]
        self.accelerationmax = self.choisie[2]
        self.pasvirage = (self.choisie[3]/DELTAVIR)*np.pi/180

def newposition2(vitesse,acceleration,direction,position):
    res=[]
    for acc in range (-DELTAACC, DELTAACC +1):
        newacceleration = acceleration + acc*ACCELERATION
        for vir in range (-DELTAVIR , DELTAVIR +1):
            newdirection = direction+vir*VIRAGE
            newvitesse=vitesse + PASDETEMPS * newacceleration
            newposition = position + piste.Point(-newvitesse * PASDETEMPS * np.cos(newdirection), newvitesse * PASDETEMPS * np.sin(newdirection))
            #print(type(newposition))
            res.append([newposition, newacceleration, newvitesse, newdirection])
            #print(res)

    return res

def newposition(vitesse,acceleration,direction,position):
    res=[]
    for vir in range (-DELTAVIR , DELTAVIR +1):
        newdirection = direction + vir * VIRAGE
        for acc in range (-DELTAVIR , DELTAVIR +1):
            newacceleration = acceleration + acc * ACCELERATION
            newvitesse=vitesse + PASDETEMPS * newacceleration
            if newvitesse > VMAX :
                newvitesse = VMAX
            newposition = position + piste.Point(-newvitesse * PASDETEMPS * np.cos(newdirection), newvitesse * PASDETEMPS * np.sin(newdirection))
            #print(type(newposition))
            res.append([newposition, newacceleration, newvitesse, newdirection])
            #print(res)

    return res