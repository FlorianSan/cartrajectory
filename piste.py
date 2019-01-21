from math import sqrt

import random as rd

import numpy as np


LARGEUR = 15 # en mètre
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


def intersect(a, b, c, d): #détermine si les segments ab et cd s'intersectent
    if a == d and b == c:
        return True
    else:
        return (a != c and a != d and b != c and b != d and clockwise(a, b, c) != clockwise(a, b, d) and clockwise(a, c, d) != clockwise(b, c, d))


class Piste:

    def __init__(self):
        self.pointsg = [Point(0,+LARGEUR / 2),Point(-PAS,+LARGEUR/2)] #liste de points à gauche de l'axe de la piste
        self.pointsgtrie=[(Point(-PAS,+LARGEUR / 2),1),(Point(-PAS,+LARGEUR/2),0)] #liste de tuple contenant les points à gauche de l'axe de piste triés par abscisse croissant et leur indice correspondant dans la liste pointsg
        self.pointsd = [Point(0,-LARGEUR / 2),Point(-PAS,-LARGEUR/2)] #liste de points à droite de l'axe de la piste
        self.pointsm = [Point(0, 0),Point(-PAS, 0)] #liste des points se trouvant sur l'axe de piste (points milieux)
        self.zone = [0]  # initialisation à 0 nécessaire afin que le début de la piste soit rectiligne
        self.angle = 0  # en degré
        self.anglerad = 0  # en rad (nécessaire pour les calculs)
        


    def miseajourzone(self): #on définit aléatoirement la valeur de la nouvelle zone
        self.zone.append(rd.randint(self.zone[-1] - INTENSITEVIRAGE, self.zone[-1] + INTENSITEVIRAGE))

    def miseajourangle(self): #on définit aléatoirement la nouvelle valeur de l'angle
        self.angle = rd.randint(0, ANGLEZONE) + ANGLEZONE * self.zone[-1]
        self.anglerad = self.angle * np.pi / 180

    def miseajourpointm(self): #on calcule la position du nouveau point milieu
        return Point(self.pointsm[-1].x - PAS * np.cos(self.anglerad), self.pointsm[-1].y + PAS * np.sin(self.anglerad))

    def creationpointspiste(self): #avec la position du point milieu on détermine celles des points à gauche et à droite de l'axe de piste
        pointg = Point(self.pointsm[-1].x + LARGEUR / 2 * np.sin(self.anglerad),self.pointsm[-1].y + LARGEUR / 2 * np.cos(self.anglerad))
        pointd = Point(self.pointsm[-1].x - LARGEUR / 2 * np.sin(self.anglerad),self.pointsm[-1].y - LARGEUR / 2 * np.cos(self.anglerad))
        return pointg, pointd
        
        
    def ajoutpoint(self, nouveaupointg, nouveaupointd, nouveaupointm):
        self.pointsg.append(nouveaupointg)
        self.pointsgtrie.append((nouveaupointg,len(self.pointsg))) #on ajoute nouveaupointg dans pointsgtrie (len(self.pointsg) correspond à son indice dans la liste pointsg)
        self.pointsgtrie.sort(key=lambda index : index[0].x) # on retrie la liste pointsgtrie
        self.pointsd.append(nouveaupointd)
        self.pointsm.append(nouveaupointm)




def recherche_dichotomique(point, liste_triee, epsilon ):
    element = point.x - 2 * PAS #on se place 2*PAS avant l'abscisse du point afin de parcourir la liste par ordre d'abscisse croissant dans un intervalle de 4*PAS
    a = 0
    b = len(liste_triee)-1
    m = (a+b)//2
    while a < b :
        if abs(liste_triee[m][0].x - element) <  epsilon :
            return m
        elif liste_triee[m][0].x - element > epsilon :
            b = m-1
        else :
            a = m+1
        m = (a+b)//2
    return a # on retourne son indice
    
    
def obtindex(piste, point, epsilon): # on obtient la liste des points de la piste pouvant potentiellement intersecter 'point'
    indextrie=recherche_dichotomique(point,piste.pointsgtrie,epsilon)
    listindex=[]
    if indextrie-1>0 :
        listindex.append(piste.pointsgtrie[indextrie-1][1])
    while indextrie<len(piste.pointsgtrie) and piste.pointsgtrie[indextrie][1]<len(piste.pointsd) and abs(piste.pointsgtrie[indextrie][0].x - point.x) < 4 *epsilon : #on vérifie que les éléments à mettre dans listindex ont leur abscisse comprise entre -4epsilon et +4epsilon
        listindex.append(piste.pointsgtrie[indextrie][1]) #on ajoute l'indice de l'élément dans listindex
        indextrie+=1
    if indextrie+1 < len(piste.pointsgtrie) :
        listindex.append(piste.pointsgtrie[indextrie+1][1])
    return listindex
    

def verifpoint(piste,point1, point2, epsilon): # on vérifie que le segment [point1,point2] n'intersecte pas la piste existante
    listindex=obtindex(piste, point1, epsilon) # on vérifie uniquement l'intersection avec des segments où l'un des deux points appartient à listindex
    for j in listindex :
        if j<len(piste.pointsg)-1 and j-1 in listindex : #on vérifie que le segment [point1,point2] n'intersecte pas les segments gauches et droits définis par les points d'indices j et j+1
            if intersect(point1, point2, piste.pointsg[j], piste.pointsg[j + 1]) or intersect(point1, point2, piste.pointsd[j], piste.pointsd[j + 1]) :
                return False
        elif j<len(piste.pointsg)-1 and j>0 : #si j-1 n'est pas dans listindex alors on procède à une double vérification j-1/j et j/j+1
            if intersect(point1, point2, piste.pointsg[j], piste.pointsg[j + 1]) or intersect(point1, point2, piste.pointsd[j], piste.pointsd[j + 1]) or intersect(point1, point2, piste.pointsg[j], piste.pointsg[j - 1]) or intersect(point1, point2, piste.pointsd[j], piste.pointsd[j - 1]) :
                return False
    return True


def creationpiste(nbiterations):
    piste = Piste()
    k = 0
    while len(piste.pointsm) < nbiterations:
        
        while k < NBETAPEPARTIE: 
        
            piste.miseajourangle()
            pm = piste.miseajourpointm()
            px, py = piste.creationpointspiste()
            
            if verifpoint(piste, px, py, PAS) : #on vérifie que les nouveaux points de la piste n'intersectent pas des anciens points
                piste.ajoutpoint(px, py, pm)
                k = k + 1
                
            else : #si il y a intersection
                l = len(piste.pointsm)
                piste.pointsgtrie=sorted(piste.pointsgtrie, key = lambda index : index[1]) #on trie la liste des pointsgtrie en fonction de l'indice des points pour pouvoir utiliser la fonction pop
                
                for j in range(l - (len(piste.zone) - 1) * NBETAPEPARTIE + 1 ) : #si intersection alors on enlève les points de la partie en cours ainsi que ceux de la précédente
                    piste.pointsm.pop() #on retire les derniers éléments ajoutés
                    piste.pointsg.pop()
                    piste.pointsd.pop()
                    piste.pointsgtrie.pop()
                piste.pointsgtrie.sort(key=lambda index : index[0].x) #on retrie la liste par abscisse croissant 
                piste.zone.pop() #on retire la valeur de la dernière zone pour éviter une nouvelle intersection
                
        piste.miseajourzone() #on change de zone qu'après NBETAPEPARTIE itérations
        k = 0 #on met à jour la velaur de k
        
    return [piste.pointsm, piste.pointsg, piste.pointsd]

