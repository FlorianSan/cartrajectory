import time

import matplotlib.pyplot as plt

from math import sqrt

import random as rd

import numpy as np

import astar2

#Test

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

    def __repr__(self):
        return "({},{})".format(self.x,self.y)

    def mini(self, other):
        return Point(min(self.x, other.x), min(self.y, other.y))

    def maxi(self, other):
        return Point(max(self.x, other.x), max(self.y, other.y))
        
    def distance(self,other):
        return sqrt((self.x-other.x)**2 + (self.y-other.y)**2)


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
        self.pointsgtrie=[(Point(-PAS,+LARGEUR / 2),1),(Point(-PAS,+LARGEUR/2),0)]
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
        pointg = Point(self.pointsm[-1].x + LARGEUR / 2 * np.sin(self.anglerad),self.pointsm[-1].y + LARGEUR / 2 * np.cos(self.anglerad))
        pointd = Point(self.pointsm[-1].x - LARGEUR / 2 * np.sin(self.anglerad),self.pointsm[-1].y - LARGEUR / 2 * np.cos(self.anglerad))

        return pointg, pointd
        

    def ajoutpoint(self, nouveaupointg, nouveaupointd, nouveaupointm):
        self.pointsg.append(nouveaupointg)
        self.pointsgtrie.append((nouveaupointg,len(self.pointsg)))
        self.pointsgtrie.sort(key=lambda index : index[0].x)
        self.pointsd.append(nouveaupointd)
        self.pointsm.append(nouveaupointm)




def recherche_dichotomique(point, liste_triee, epsilon ):
    element=point.x- epsilon
    a = 0
    b = len(liste_triee)-1
    m = (a+b)//2
    while a < b :
        if abs(liste_triee[m][0].x - element) <  epsilon :
            return m
        elif liste_triee[m][0].x - element > epsilon:
            b = m-1
        else :
            a = m+1
        m = (a+b)//2
    return a

def verifpoint(piste,point1, point2, epsilon):
    listindex=obtindex(piste, point1, epsilon)
    for j in listindex :
        if j<len(piste.pointsg)-1 and j-1 in listindex :
            if intersect(point1, point2, piste.pointsg[j], piste.pointsg[j + 1]) or intersect(point1, point2, piste.pointsd[j], piste.pointsd[j + 1]) :
                return False
        elif j<len(piste.pointsg)-1 and j>0 :
            if intersect(point1, point2, piste.pointsg[j], piste.pointsg[j + 1]) or intersect(point1, point2, piste.pointsd[j], piste.pointsd[j + 1]) or intersect(point1, point2, piste.pointsg[j], piste.pointsg[j - 1]) or intersect(point1, point2, piste.pointsd[j], piste.pointsd[j - 1]) :
                return False
    return True

def obtindex(piste, point, epsilon):
    indextrie=recherche_dichotomique(point,piste.pointsgtrie,epsilon) #voiture.vitessemax * PASDETEMPS)
    listindex=[]
    if indextrie-1>0 :
        listindex.append(piste.pointsgtrie[indextrie-1][1])
    while indextrie<len(piste.pointsgtrie)-1 and piste.pointsgtrie[indextrie][1]<len(piste.pointsd) and piste.pointsgtrie[indextrie][0].x - piste.pointsgtrie[0][0].x > 2 *epsilon and abs(piste.pointsd[piste.pointsgtrie[indextrie][1]].distance(point)) <= epsilon :
        listindex.append(piste.pointsgtrie[indextrie][1])
        indextrie+=1
    if indextrie+1 < len(piste.pointsgtrie) :
        listindex.append(piste.pointsgtrie[indextrie+1][1])
    return listindex


def creationpiste(nbiterations):
    piste = Piste()
    k = 0
    while len(piste.pointsm) < nbiterations:

        #print(len(piste.pointsm))
        
        while k < NBETAPEPARTIE:
            piste.miseajourangle()
            pm = piste.miseajourpointm()
            px, py = piste.creationpointspiste()
            if verifpoint(piste, px, py, PAS): #vérifie que les nouveaux points de la piste n'intesectent pas des anciens points
                piste.ajoutpoint(px, py, pm)
                k = k + 1
                print(len(piste.pointsm))
            else:
                l = len(piste.pointsm)
                piste.pointsgtrie=sorted(piste.pointsgtrie, key = lambda index : index[1])
                for j in range(l - (len(piste.zone) - 1) * NBETAPEPARTIE + 1 ): #si intersection alors on enlève les points de la partie en cours ainsi que ceux de la précédente
                    piste.pointsm.pop()
                    piste.pointsg.pop()
                    piste.pointsd.pop()
                    piste.pointsgtrie.pop()
                piste.pointsgtrie.sort(key=lambda index : index[0].x)
                piste.zone.pop()
        piste.miseajourzone()
        k = 0
    return [piste.pointsm, piste.pointsg, piste.pointsd]

if __name__ == "__main__":
    #chemin=creationpiste(300)
    p1 = Point(14, 37)
    p2 = Point(34, 7)
    p3 = Point(43, 30)
