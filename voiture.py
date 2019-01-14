import numpy as np

import piste

PASDETEMPS = 0.1 # en secondes
ACCELERATION = 8 # en m/s²
DELTAACC = 5
VIRAGE = (8*np.pi)/180 #angle de virage en radian
DELTAVIR = 5
VMAX = 50

class Voiture:
    def __init__(self, masse, longueur, largeur):
        self.masse = masse
        self.longueur = longueur
        self.largeur = largeur
        self.accelerationmax = 0
        self.vitessemax = 0
        self.pasvirage = 0
        self.position = []
        self.acceleration = []
        self.vitesse = []
        self.direction = []
        self.name = None
        self.DELTAVIR = DELTAVIR
        

    def get_position(self, t):
        return self.position[t]


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
        for acc in range (-DELTAACC , DELTAACC +1):
            newacceleration = acceleration + acc * ACCELERATION
            newvitesse=vitesse + PASDETEMPS * acc * ACCELERATION
            if abs(newvitesse) > VMAX :
                newvitesse = VMAX * np.sign(newvitesse)
            newposition = position + piste.Point(-newvitesse * PASDETEMPS * np.cos(newdirection), newvitesse * PASDETEMPS * np.sin(newdirection))
            #print(type(newposition))
            res.append([newposition, newacceleration, newvitesse, newdirection])
            #print(res)

    return res

