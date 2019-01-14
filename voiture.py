import numpy as np

import piste


class Voiture:
    def __init__(self):
        self.masse = 0
        self.longueur = 0
        self.largeur = 0
        self.pasacceleration = 0
        self.deltaacc = 5
        self.vitessemax = 0
        self.pasvirage = 0
        self.deltavirage = 5
        self.empatement = 0
        self.position = []
        self.acceleration = []
        self.vitesse = []
        self.direction = []
        self.name = None

        

    def get_position(self, t):
        return self.position[t]




