import numpy as np
import math

import piste

µ = 0.8  # Utile si on veut changer les valeurs ?
DELTAVIR = 5
DELTAACC = 5


class Voiture:
    def __init__(self):
        self.masse = 0
        self.longueur = 0
        self.largeur = 0
        self.pasacceleration = 0
        self.deltaacc = DELTAACC
        self.vitessemax = 0
        self.pasvirage = 0
        self.deltavirage = DELTAVIR
        self.empattement = 0
        self.position = []
        self.acceleration = []
        self.vitesse = []
        self.direction = []
        self.name = None

    def calculdeltavirage(self):
        if len(self.vitesse) != 0:
            alpha = math.asin(self.empattement * self.vitesse[-1] / 9.81 * µ)
            if alpha >= DELTAVIR * self.pasvirage:
                return (DELTAVIR)
            else:
                return (alpha // self.pasvirage)
        else:
            return (DELTAVIR)

    def get_position(self, t):
        return self.position[t]




