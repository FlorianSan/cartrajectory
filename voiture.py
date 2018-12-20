import numpy as np

import piste

PASDETEMPS = 0.1 #en secondes
ACCELERATION = 0.1 #en m/s²
DELTAACC = 1
VIRAGE = (17*np.pi)/180 #angle de virage en radian
DELTAVIR = 1

class Voiture:
    def __init__(self, masse, longueur, largeur):
        self.masse = masse
        self.longueur = longueur
        self.largeur = largeur
        self.position = [piste.Point(0,0)]
        self.acceleration = [0]
        self.vitesse = [0]
        self.direction = [0]

    def get_position(self, t):
        return self.position[t]

def newposition(vitesse,acceleration,direction,position):
    res=[]
    for acc in range (-DELTAACC, DELTAACC +1):
        newacceleration = acceleration+ acc*ACCELERATION
        for vir in range (-DELTAVIR , DELTAVIR +1):
            newdirection = direction+vir*VIRAGE
            newvitesse=vitesse + PASDETEMPS * newacceleration
            newposition = position + piste.Point(-newvitesse * PASDETEMPS * np.cos(newdirection), newvitesse * PASDETEMPS * np.sin(newdirection)) #SIGNE A REVOIR
            res.append([newposition, newacceleration, newvitesse, newdirection])

    return res

