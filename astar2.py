import matplotlib.pyplot as plt
import numpy as np

import time

import piste
from operator import itemgetter, attrgetter

PASDETEMPS = 0.1 # en secondes


class Node:

    def __init__(self, vitesse, acceleration, direction, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.dstart = 0
        self.dend = 0
        self.couttot = 0

        self.temps = 0  # nb de pas de temps pour arriver à ce noeud

        self.vitesse = vitesse
        self.direction = direction
        self.acceleration = acceleration

    def __eq__(self, autre):
        return self.position == autre.position




# rajouter affichage

def tripointg(listepointg):
    listepointgtrie=[]
    for index,point in enumerate(listepointg):
        listepointgtrie.append((point.x,index))
    listepointgtrie.sort()
    return listepointgtrie


def obindex(listepointgtrie,point, voiture):
    indextrie=piste.recherche_dichotomique(point,listepointgtrie,voiture.vitessemax * PASDETEMPS)
    listindex=[]
    i=1
    while indextrie-i>0 and i<20:
        listindex.append(listepointgtrie[indextrie-i][1])
        i+=1
    while indextrie<len(listepointgtrie) and listepointgtrie[indextrie][0] - point.x > 2*voiture.vitessemax * PASDETEMPS :
        listindex.append(listepointgtrie[indextrie][1])
        indextrie+=1
    j=1
    while indextrie+j<len(listepointgtrie) and j<20:
        listindex.append(listepointgtrie[indextrie+j][1])
        j+=1
    return listindex




def verifpoint(chemin,listepointgtrie,point1, point2, voiture):
    listindex=obindex(listepointgtrie,point1,voiture)
    verif = True
    for j in listindex :
        if j<len(chemin[1])-1 :
            if piste.intersect(point1, point2, chemin[1][j], chemin[1][j + 1]) or piste.intersect(point1, point2, chemin[2][j], chemin[2][j + 1]):
                verif = False
    return verif

def astar(chemin, voit):

    def newposition(vitesse, acceleration, direction, position, voiture):
        res = []
        voiture.calculdeltavirage()
        for vir in range(-voiture.deltavirage, voiture.deltavirage + 1):
            newdirection = direction + vir * voiture.pasvirage
            for acc in range(-voiture.deltaacc, voiture.deltaacc + 1):
                newacceleration = acceleration + acc * voiture.pasacceleration
                newvitesse = vitesse + PASDETEMPS * acc * voiture.pasacceleration
                if abs(newvitesse) > voiture.vitessemax:
                    newvitesse = voiture.vitessemax * np.sign(newvitesse)
                newposition = position + piste.Point(-newvitesse * PASDETEMPS * np.cos(newdirection),
                                                     newvitesse * PASDETEMPS * np.sin(newdirection))
                # print(type(newposition))
                res.append([newposition, newacceleration, newvitesse, newdirection])
                # print(res)

        return res
    
    
    
    if len(chemin)==3:
        listetriee=tripointg(chemin[1])
    else :
        listetriee=chemin[3]
    
    compteur = 0
    DELTAINDEX = 20
    indexdend=DELTAINDEX
    
    longueur={} #création d'un dictionnaire de longueur de la piste à patir de la fin
    longueur[len(chemin[0])-1]=0
    for l in range (len(chemin[0])-2,-1,-1):
        longueur[l]=longueur.get(l+1) + chemin[0][l].distance(chemin[0][l+1])

    # cree le noeud de debut et de fin
    start_node = Node(0, 0, np.pi, None, chemin[0][0])
    start_node.dstart = 0
    
    """l = -1
    d = chemin[0][l].distance(chemin[0][l - 1]) #A reprendre avec longueur
    while chemin[0][l].distance(start_node.position) > piste.LARGEUR:
        start_node.dend += d
        l = l - 1"""
        
    start_node.dend=longueur.get(0)

    start_node.couttot = start_node.dstart + start_node.dend

    # Initialisation des deux listes
    open_list = []  # liste des noeuds a traiter  FILE DE PRIORITe
    closed_list = []  # liste des noeuds deja traites

    # Ajoute le noeud de depart
    open_list.append(start_node)

    # On boucle jusqu'au noeud final
    while len(open_list) > 0:  # tant qu'il y a des noeuds a traiter
    

        # Acceder au noeud courant
        """for i in range(1, len(open_list)): # ???
            if open_list[i - 1].couttot > open_list[i].couttot:
                open_list[i - 1], open_list[i] = open_list[i], open_list[i - 1]"""
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.couttot < current_node.couttot:
                current_node = item
                current_index = index

        # On retire le current node de la liste des noeuds a traiter et on l'ajoute dans la liste des noeuds traites
        open_list.pop(current_index)
        closed_list.append(current_node)
        


        compteur += 1
        print(compteur)
        #print(current_node.dend)


        # Genere les children
        children = []

        res = newposition(current_node.vitesse, current_node.acceleration, current_node.direction,current_node.position, voit)
        
        
        for i in range(len(res)):
            children.append(Node(res[i][2], res[i][1], res[i][3], current_node, res[i][0]))
            children[-1].temps = current_node.temps + 1

            """verif = True  # Test si child se trouve dans la piste
            for j in range(len(chemin[1]) - 1):
                if piste.intersect(current_node.position, children[-1].position, chemin[1][j],
                                   chemin[1][j + 1]) or piste.intersect(current_node.position, children[-1].position,
                                                                        chemin[2][j], chemin[2][j + 1]):
                    verif = False
            if not verif:
                children.pop()"""
            if not verifpoint(chemin, listetriee, current_node.position, children[-1].position, voit):
                children.pop()
        if len(children) == 0: #current node pas dans open_list ??
            open_list.pop(0)

        # Si on a atteint la fin
        
        listendnode=[]
        for child in children :
            if piste.intersect(current_node.position, child.position, chemin[1][-1], chemin[2][-1]):
                listendnode.append(child)
        if len(listendnode)>0:
            endchild=listendnode[0]
            difdir=abs(current_node.direction-endchild.direction)
            for child in listendnode :
                if difdir> abs(child.direction-current_node.direction):
                    endchild=child
                    difdir=abs(child.direction-current_node.direction)
            path = []  # initialise le chemin
            current = endchild
            #print(endchild.temps)
            while current is not None:  # on cree le chemin en partant de la fin
                voit.position.append(current.position)
                voit.direction.append(current.direction)
                voit.vitesse.append(current.vitesse)
                current = current.parent
            voit.position=voit.position[::-1]
            voit.direction=voit.direction[::-1]
            voit.vitesse=voit.vitesse[::-1]
            return (voit.position, voit.direction, voit.vitesse)  # return le chemin
        

        # On boucle sur les children
        for child in children:

            # Create coutrest, dstart, dend
            child.dstart = current_node.dstart + child.vitesse * child.temps * PASDETEMPS

            while indexdend>0 and chemin[0][indexdend].distance(child.position) > 2*piste.LARGEUR :
                indexdend-=1
            child.dend = chemin[0][indexdend].distance(child.position) + longueur.get(indexdend)
            if indexdend + DELTAINDEX >= len(chemin[0]):
                indexdend=len(chemin[0])-1
            else :
                indexdend+= DELTAINDEX
            
            """l = -1
            while abs(l)<len(chemin[0]) and chemin[0][l].distance(child.position) > piste.LARGEUR :
                child.dend += chemin[0][l].distance(chemin[0][l - 1])
                l = l - 1
                #print(l)
            child.dend += chemin[0][l].distance(child.position)"""

            child.couttot = child.dstart + child.dend

            open_list.append(child)





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
    
    #t1=time.clock()
    
    chemin = piste.creationpiste(300)
    afficherpiste(chemin[1], chemin[2])

    voit = voiture.Voiture(100, 10, 10)

    ast = astar(chemin, voit)
    afficherastar(ast[0])
    
    #t2=time.clock()
    #print(t2-t1)
