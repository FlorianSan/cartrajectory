import random as rd

import numpy as np

LARGEUR = 15# en mètre
PAS = 2  # en mètre
NBETAPEPARTIE = 30  # nb étapes avant le choix d'une nouvelle zone
NBZONE = 24  # nb de zones
ANGLEZONE = 360 // NBZONE  # en degré
INTENSITEVIRAGE = 4  # plus cette valeur est importante et plus les virages auront tendance à être serrés


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def mini(self, other):
        return Point(min(self.x, other.x), min(self.y, other.y))

    def maxi(self, other):
        return Point(max(self.x, other.x), max(self.y, other.y))


def clockwise(a, b, c):
    x1 = b.x - a.x
    y1 = b.y - a.y
    x2 = c.x - a.x
    y2 = c.y - a.y
    return x1 * y2 - x2 * y1 < 0


def intersect(a, b, c, d): #détermine si les segments ab et cs d'intersectent
    if a == d and b == c:
        return True
    else:
        return (a != c and a != d and b != c and b != d and clockwise(a, b, c) != clockwise(a, b, d) and clockwise(a, c, d) != clockwise(b, c, d))


class Piste:

    def __init__(self):
        self.pointsg = [Point(0,+LARGEUR / 2),Point(-PAS,+LARGEUR/2)] #liste de points à gauche de l'axe de la piste
        self.pointsd = [Point(0,-LARGEUR / 2),Point(-PAS,-LARGEUR/2)] #liste de points à droite de l'axe de la piste
        self.pointsm = [Point(0, 0),Point(-PAS, 0)] #liste des points milieux
        self.zone = [0]  # initialisation à 0 nécessaire afin que le début de la piste soit rectiligne
        self.angle = 0  # en degré
        self.anglerad = 0  # en rad (nécessaire pour les calculs)

    def miseajourzone(self):
        self.zone.append(rd.randint(self.zone[-1] - INTENSITEVIRAGE, self.zone[-1] + INTENSITEVIRAGE))

    def miseajourangle(self):
        self.angle = rd.randint(0, ANGLEZONE) + ANGLEZONE * self.zone[-1]
        self.anglerad = self.angle * np.pi / 180

    def miseajourpointm(self):
        return Point(self.pointsm[-1].x - PAS * np.cos(self.anglerad), self.pointsm[-1].y + PAS * np.sin(self.anglerad))

    def creationpointspiste(self):
        pointg = Point(self.pointsm[-1].x + LARGEUR / 2 * np.sin(self.anglerad),
                       self.pointsm[-1].y + LARGEUR / 2 * np.cos(self.anglerad))
        pointd = Point(self.pointsm[-1].x - LARGEUR / 2 * np.sin(self.anglerad),
                       self.pointsm[-1].y - LARGEUR / 2 * np.cos(self.anglerad))

        return pointg, pointd

    def verificationpoint(self, nouveaupointg, nouveaupointd):
        verif = True
        for i in range(len(self.pointsg)):
            if intersect(nouveaupointg, self.pointsg[i], nouveaupointd, self.pointsd[i]):
                verif = False
        return verif

    def ajoutpoint(self, nouveaupointg, nouveaupointd, nouveaupointm):
        self.pointsg.append(nouveaupointg)
        self.pointsd.append(nouveaupointd)
        self.pointsm.append(nouveaupointm)


def creationpiste(nbiterations):
    piste = Piste()
    k = 0
    while len(piste.pointsm) < nbiterations:

        while k < NBETAPEPARTIE:
            piste.miseajourangle()
            pm = piste.miseajourpointm()
            px, py = piste.creationpointspiste()
            if piste.verificationpoint(px, py): #vérifie que les nouveaux points de la piste n'intesectent pas des anciens points
                piste.ajoutpoint(px, py, pm)
                k = k + 1
            else:
                l = len(piste.pointsm)
                for j in range(l - (len(piste.zone) - 1) * NBETAPEPARTIE): #si intersection alors on enlève les points de la partie en cours ainsi que ceux de la précdente
                    piste.pointsm.pop()
                    piste.pointsg.pop()
                    piste.pointsd.pop()
                piste.zone.pop()
        piste.miseajourzone()
        k = 0
    return [piste.pointsm, piste.pointsg, piste.pointsd]

