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
        self.position = []
        self.acceleration = []
        self.vitesse = []
        self.direction = []

    def get_position(self, t):
        return self.position[t]

    def newposition(self):
        res=[]
        for acc in range (-DELTAACC, DELTAACC +1):
            newacceleration = self.acceleration[-1]+ acc*ACCELERATION
            for vir in range (-DELTAVIR , DELTAVIR +1):
                newdirection = self.direction[-1]+vir*VIRAGE
                newvitesse=self.vitesse[-1] + PASDETEMPS * newacceleration
                newposition = self.position[-1] + piste.Point(-newvitesse * PASDETEMPS * np.cos(newdirection), newvitesse * PASDETEMPS * np.sin(newdirection)) #SIGNE A REVOIR
                res.append([newposition, newacceleration, newvitesse, newdirection])
        return res