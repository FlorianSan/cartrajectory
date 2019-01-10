import matplotlib.pyplot as plt
import numpy as np

import piste
import voiture
from operator import itemgetter, attrgetter


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
    for point,index in enumerate(listepointg):
        listepointgtrie.append((point,index))
    listepointgtrie.sort()
    return listepointgtrie


def obindex(listepointgtrie,point):
    indextrie=piste.recherche_dichotomique(point,listepointgtrie,voiture.VMAX * voiture.PASDETEMPS)
    listindex=[indextrie-2]
    while indextrie<len(listepointgtrie) and listepointgtrie[indextrie][0] - point.x < voiture.VMAX * voiture.PASDETEMPS :
        listindex.append(listepointgtrie[indextrie][1])
        indextrie+=1
    i=0
    indextrie+=1
    while indextrie<len(listepointgtrie) and i<3:
        listindex.append(indextrie)
        indextrie+=1
        i=i+1
    return listindex


def verifpoint(chemin,listepointgtrie,point1, point2):
    listindex=obindex(listepointgtrie,point1)
    verif = True
    for j in range(len(listindex)-1):
                if piste.intersect(point1, point2, chemin[1][j],
                                   chemin[1][j + 1]) or piste.intersect(point1, point2,
                                                                        chemin[2][j], chemin[2][j + 1]):
                    verif = False
    return verif

def astar(chemin, voit):
    
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
    l = -1
    d = chemin[0][l].distance(chemin[0][l - 1]) #A reprendre
    while chemin[0][l].distance(start_node.position) > piste.LARGEUR:
        start_node.dend += d
        l = l - 1
    # start_node.dend = ((start_node.position.x - chemin[-1][0].x) ** 2 +v(start_node.position.y - chemin[-1][0].y) ** 2) ** 0.5
    start_node.couttot = start_node.dstart + start_node.dend

    # Initialisation des deux listes
    open_list = []  # liste des noeuds a traiter  FILE DE PRIORITe
    closed_list = []  # liste des noeuds deja traites

    # Ajoute le noeud de depart
    open_list.append(start_node)

    # On boucle jusqu'au noeud final
    while len(open_list) > 0:  # tant qu'il y a des noeuds a traiter

        # Acceder au noeud courant
        for i in range(1, len(open_list)):
            if open_list[i - 1].couttot > open_list[i].couttot:
                open_list[i - 1], open_list[i] = open_list[i], open_list[i - 1]
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

        # Genere les children
        children = []

        res = voiture.newposition(current_node.vitesse, current_node.acceleration, current_node.direction,
                                  current_node.position)
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
                
            if not verifpoint(chemin, listetriee, current_node.position, children[-1].position):
                children.pop()
        if len(children) == 0:
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
                current = current.parent
            voit.position=voit.position[::-1]
            voit.direction=voit.direction[::-1]
            return (voit.position, voit.direction)  # return le chemin
        

        # On boucle sur les children
        for child in children:

            # Create coutrest, dstart, dend
            child.dstart = current_node.dstart + child.vitesse * child.temps * voiture.PASDETEMPS

            while indexdend>0 and chemin[0][indexdend].distance(child.position) > 2*piste.LARGEUR :
                indexdend-=1
            child.dend = chemin[0][indexdend].distance(child.position) + longueur.get(indexdend)
            if indexdend + DELTAINDEX > len(chemin[0]):
                indexdend=len(chemin[0])-1
            else :
                indexdend+= DELTAINDEX
            
            """l = -1
            while abs(l)<len(chemin[0]) and chemin[0][l].distance(child.position) > piste.LARGEUR:
                child.dend += chemin[0][l].distance(chemin[0][l - 1])
                l = l - 1
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
    chemin = piste.creationpiste(600)
    afficherpiste(chemin[1], chemin[2])

    voit = voiture.Voiture(100, 10, 10)

    ast = astar(chemin, voit)
    afficherastar(ast[0])
