import numpy as np
import math

import piste

u = 0.8  # Utile si on veut changer les valeurs ?
DELTAVIR = 5
DELTAACC = 5

# Test

class Voiture:
    def __init__(self):
        self.masse = 0
        self.longueur = 0
        self.largeur = 0
        self.pasacceleration = 1
        self.deltaacc = DELTAACC
        self.vitessemax = 40
        self.pasvirage = 0.139
        self.deltavirage = DELTAVIR
        self.empattement = 2
        self.position = []
        self.acceleration = []
        self.vitesse = []
        self.direction = []
        self.name = None

    def calculdeltavirage(self, vitesse):
        cst = self.empattement * 9.81 * u
        if math.sqrt(cst) <= abs(vitesse):
            alpha = math.asin(cst / (vitesse ** 2))
            if alpha >= DELTAVIR * self.pasvirage:
                return (DELTAVIR)
            else:
                print(int(alpha // self.pasvirage))
                return (int(alpha // self.pasvirage))

        else:
            return (DELTAVIR)
        

    def calculvitessevirage(self, r):
        return np.sqrt((u*r)/self.masse)


    def get_position(self, t):
        return self.position[t]




