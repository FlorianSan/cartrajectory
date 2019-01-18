import matplotlib.pyplot as plt
from heapq import heappush, heappop
from shapely.geometry import Point, Polygon, LineString
import numpy as np
import time

import voiture


import piste
from operator import itemgetter, attrgetter

PASDETEMPS = 0.1 # en secondes


class Node:

    def __init__(self, vitesse, acceleration, direction, temps, dstart, dend, couttot, indexdend, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.dstart = dstart
        self.dend = dend
        self.couttot = couttot
        
        self.indexdend=indexdend #index du point de l'axe de piste le plus proche du noeud

        self.temps = temps  # nb de pas de temps pour arriver à ce noeud

        self.vitesse = vitesse
        self.direction = direction
        self.acceleration = acceleration

    def __eq__(self, autre):
        return self.position == autre.position


    def __repr__(self):
        return str(self.temps)

# rajouter affichage

def tripointg(listepointg):
    listepointgtrie=[]
    for index,point in enumerate(listepointg):
        listepointgtrie.append((point,index))
    listepointgtrie.sort(key=lambda index : index[0].x )
    return listepointgtrie


def astar(chemin, voit):

    coords = []
    coordligneg = []
    coordligned =[]
    for i in range(len(chemin[1])):
        coords.append((chemin[1][i].x,chemin[1][i].y))
        coordligneg.append((chemin[1][i].x,chemin[1][i].y))
    for j in range(len(chemin[2])-1,0,-1):
        coords.append((chemin[2][j].x, chemin[2][j].y))
        coordligned.append((chemin[2][j].x, chemin[2][j].y))
    polygon = Polygon(coords)
    ligneg = LineString(coordligneg)
    ligned = LineString(coordligned)
    lignefin = LineString([(chemin[1][-1].x,chemin[1][-1].y),(chemin[2][-1].x,chemin[2][-1].y)])



    def newposition(currentnode):
        
        #print('dend = ' + str(current_node.dend))


        #deltavirage = voit.calculdeltavirage(currentnode.vitesse)
        deltavirage = 5
        #print(deltavirage)
        for vir in range(-deltavirage, deltavirage + 1):
            newdirection = currentnode.direction + vir * voit.pasvirage
            for acc in range(-voit.deltaacc, voit.deltaacc + 1):
                newacceleration = currentnode.acceleration + acc * voit.pasacceleration
                newvitesse = currentnode.vitesse + PASDETEMPS * currentnode.acceleration

                if abs(newvitesse) > voit.vitessemax:
                    newvitesse = voit.vitessemax * np.sign(newvitesse)
                newposition = currentnode.position + piste.Point(-newvitesse * PASDETEMPS * np.sin(newdirection),newvitesse * PASDETEMPS * np.cos(newdirection))
                
                if abs(newvitesse)<abs(current_node.vitesse):
                    print('OK')
                ligne = LineString([(currentnode.position.x, currentnode.position.y), (newposition.x, newposition.y)])
                if (polygon.contains(Point(newposition.x, newposition.y)) and (not ligned.intersects(ligne) or not ligneg.intersects(ligne))) or ligne.intersects(lignefin):
                    temps = currentnode.temps + 1
                    #print(temps)
                    dstart = currentnode.dstart + newvitesse * PASDETEMPS
                    
                    
                    if current_node.indexdend + 20 >= len(chemin[0]):
                        indexdend=len(chemin[0]) - 1
                    else :
                        indexdend=current_node.indexdend+20

                    while indexdend > 0 and chemin[0][indexdend].distance(newposition) > 2 * piste.LARGEUR:
                        indexdend -= 1
                    dend = chemin[0][indexdend].distance(newposition) + longueur.get(indexdend)
                    couttot = dstart + dend
                    newnode = Node(newvitesse, newacceleration, newdirection, temps, dstart, dend, couttot,indexdend, currentnode,newposition)
                    heappush(heap, (newnode.couttot, newnode))

    longueur = {}  # création d'un dictionnaire de longueur de la piste à patir de la fin
    longueur[len(chemin[0]) - 1] = 0
    for l in range(len(chemin[0]) - 2, -1, -1):
        longueur[l] = longueur.get(l + 1) + chemin[0][l].distance(chemin[0][l + 1])

    # cree le noeud de debut et de fin
    start_node = Node(0, 0, directioninit(chemin[0][1],chemin[0][0]), 0, 0, longueur.get(0), longueur.get(0),len(chemin[0])-1, None, chemin[0][1],)
    

    # Initialisation des deux listes
    heap = []  # liste des noeuds a traiter  FILE DE PRIORITe


    # Ajoute le noeud de depart
    heappush(heap, (start_node.couttot, start_node))
    i=0
    # On boucle jusqu'au noeud final
    while heap:  # tant qu'il y a des noeuds a traiter

        current_node = heappop(heap)[1]

        #test fin
        if len(heap)>1 and piste.intersect(current_node.parent.position, current_node.position, chemin[1][-1], chemin[2][-1]):
            position,acceleration, direction, vitesse =[],[],[],[]
            while current_node is not None:
                position.append(current_node.position)
                acceleration.append(current_node.acceleration)
                direction.append(current_node.direction)
                vitesse.append(current_node.vitesse)
                current_node = current_node.parent

            voit.position = position[::-1]
            voit.acceleration = acceleration[::-1]
            voit.vitesse = vitesse[::-1]
            voit.direction = direction[::-1]
            return None

        newposition(current_node)
        print(i)
        i+=1



def directioninit(Point1,Point2):
    dx,dy=Point1.x-Point2.x,Point1.y-Point2.y
    if dx>0:
        return(-np.arctan(dy/dx)+np.pi)
    elif dx<0:
        if dy>0:
            return(np.arctan(dx/dy))
        elif dy<0:
            return(np.arctan(dx/dy)+np.pi)
        else:
            return(3*np.pi/2)
    else:
        if dy>0:
            return(0)
        else:
            return(np.pi)



def afficherpiste(l1, l2):
    for k in range(len(l1) - 1):
        a = [l1[k].x, l1[k + 1].x]
        b = [l1[k].y, l1[k + 1].y]
        c = [l2[k].x, l2[k + 1].x]
        d = [l2[k].y, l2[k + 1].y]
        plt.plot(a, b)
        plt.plot(c, d)
        plt.axis('equal')




def afficherastar(l1):
    for k in range(len(l1) - 1):
        a = [l1[k].x, l1[k + 1].x]
        b = [l1[k].y, l1[k + 1].y]
        plt.plot(a, b)
        plt.axis('equal')
    plt.show()



if __name__ == "__main__":
    

    
    chemin = piste.creationpiste(300)
    afficherpiste(chemin[1], chemin[2])

    voit = voiture.Voiture()

    ast = astar(chemin, voit)
    afficherastar(voit.position)
    