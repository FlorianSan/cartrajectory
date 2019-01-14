import numpy as np

import piste


class Voiture:
    def __init__(self, masse, longueur, largeur):
        self.masse = masse
        self.longueur = longueur
        self.largeur = largeur
        self.accelerationmax = 0
        self.deltaacc = 5
        self.vitessemax = 0
        self.pasvirage = 0
        self.deltavirage = 5
        self.position = []
        self.acceleration = []
        self.vitesse = []
        self.direction = []
        self.name = None

        

    def get_position(self, t):
        return self.position[t]




