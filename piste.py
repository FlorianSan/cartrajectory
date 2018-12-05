import matplotlib.pyplot as plt
import numpy as np
import random as rd

LARGEUR = 15  # en mètre
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
        return (a != c and a != d and b != c and b != d and clockwise(a, b, c) != clockwise(a, b, d) and clockwise(a, c,
                                                                                                                   d) != clockwise(
            b, c, d))


class Piste:

    def __init__(self):
        self.pointsx = [Point(0, +LARGEUR / 2)]  # liste de points
        self.pointsy = [Point(0, -LARGEUR / 2)]  # liste de points
        self.pointsm = [Point(0, 0)]  # liste des points milieux
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
        pointx = Point(self.pointsm[-1].x + LARGEUR / 2 * np.sin(self.anglerad),
                       self.pointsm[-1].y + LARGEUR / 2 * np.cos(self.anglerad))
        pointy = Point(self.pointsm[-1].x - LARGEUR / 2 * np.sin(self.anglerad),
                       self.pointsm[-1].y - LARGEUR / 2 * np.cos(self.anglerad))

        return pointx, pointy

    def verificationpoint(self, pointx, pointy):
        verif = True
        for i in range(len(self.pointsx)):
            if intersect(pointx, self.pointsx[i], pointy, self.pointsy[i]):
                verif = False
        return verif

    def ajoutpoint(self, pointx, pointy, pointm):
        self.pointsx.append(pointx)
        self.pointsy.append(pointy)
        self.pointsm.append(pointm)


def creationpiste(nbiterations):
    piste = Piste()
    k = 0
    piste.zone = [0]  # initialisation nécessaire afin que le début de la piste soit rectiligne

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
                for j in range(l - (len(piste.zone) - 1) * NBETAPEPARTIE + 1): #si intersection alors on enlève les points de la partie en cours ainsi que ceux de la précdente
                    piste.pointsm.pop()
                    piste.pointsx.pop()
                    piste.pointsy.pop()
                piste.zone.pop()
        piste.miseajourzone()
        k = 0
    return piste.pointsm
