import matplotlib.pyplot as plt
from heapq import heappush, heappop
from shapely.geometry import Point, Polygon
import numpy as np

import voiture


import piste
from operator import itemgetter, attrgetter

PASDETEMPS = 0.1 # en secondes


class Node:

    def __init__(self, vitesse, acceleration, direction, temps, dstart, dend, couttot,indexdend, parent=None, position=None):
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

    def __lt__(self, other):
        return self.position.x < other.position.x and self.position.y < other.position.y

# rajouter affichage

def tripointg(listepointg):
    listepointgtrie=[]
    for index,point in enumerate(listepointg):
        listepointgtrie.append((point,index))
    listepointgtrie.sort(key=lambda index : index[0].x )
    return listepointgtrie


def astar(chemin, voit):

    coords = []
    for i in range(len(chemin[1])):
        coords.append((chemin[1][i].x,chemin[1][i].y))
    for j in range(len(chemin[2])-1,0,-1):
        coords.append((chemin[2][j].x, chemin[2][j].y))
    polygon = Polygon(coords)


    def newposition(currentnode):
        
        print('dend = ' + str(current_node.dend))


        #deltavirage = voit.calculdeltavirage(currentnode.vitesse)
        deltavirage = 5
        #print(deltavirage)
        for vir in range(-deltavirage, deltavirage + 1):
            newdirection = currentnode.direction + vir * voit.pasvirage
            for acc in range(-voit.deltaacc+3, voit.deltaacc + 4):
                newacceleration = currentnode.acceleration + acc * voit.pasacceleration
                newvitesse = currentnode.vitesse + PASDETEMPS * currentnode.acceleration

                if abs(newvitesse) > voit.vitessemax:
                    newvitesse = voit.vitessemax * np.sign(newvitesse)
                newposition = currentnode.position + piste.Point(-newvitesse * PASDETEMPS * np.sin(newdirection),newvitesse * PASDETEMPS * np.cos(newdirection))
                
                #if abs(newvitesse)<abs(current_node.vitesse):
                    #print('OK')

                if polygon.contains(Point(newposition.x, newposition.y)) or piste.intersect(currentnode.parent.position, newposition, chemin[1][-1], chemin[2][-1]):
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
                    


                    #dend = np.sqrt((chemin[0][-1].x-newposition.x)**2 + (chemin[0][-1].y-newposition.y)**2)
                    #dend = abs(chemin[0][-1].x - newposition.x) + abs(chemin[0][-1].y - newposition.y)
                    
                    
                    """c=0
                    longueur=0
                    while dstart>longueur:
                        longueur += np.sqrt((chemin[0][c+1].x - chemin[0][c].x) ** 2 + (chemin[0][c+1].y - chemin[0][c].y) ** 2)
                        c+=1
                    if len(chemin[0][c:])>10:
                        indexmilieu = int(len(chemin[0][c:])/2)
                        dend = np.sqrt((chemin[0][indexmilieu].x - newposition.x) ** 2 + (chemin[0][indexmilieu].y - newposition.y) ** 2) + np.sqrt((chemin[0][-1].x-chemin[0][indexmilieu].x)**2 + (chemin[0][-1].y-chemin[0][indexmilieu].y)**2)
                    else:
                        dend = np.sqrt((chemin[0][-1].x - newposition.x) ** 2 + (chemin[0][-1].y - newposition.y) ** 2)"""

                    couttot = dstart + dend
                    newnode = Node(newvitesse, newacceleration, newdirection, temps, dstart, dend, couttot,indexdend, currentnode,newposition)
                    heappush(heap, (newnode.couttot, newnode))

    
    """if len(chemin)==3:
        listetriee=tripointg(chemin[1])
    else :
        listetriee=chemin[3]"""

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
        return(-np.atan(dy/dx)+np.pi)
    elif dx<0:
        if dy>0:
            return(np.atan(dx/dy))
        elif dy<0:
            return(np.atan(dx/dy)+np.pi)
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
    