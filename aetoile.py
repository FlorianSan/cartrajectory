class Path:
    def __init__(self, noeud, coutot):
        self.noeud = noeud
        self.coutot = coutot

    def getNoeud(self):
        return self.noeud

    def getTotalMoveCost(self):
        return self.coutot


class Node:
    def __init__(self, location, mcout, id, parent=None):
        self.location = location  # où est situé le noeud dans l'arbre
        self.mcout = mcout  # coût total pour attiendre ce noeud
        self.parent = parent  # parent du noeud
        self.score = 0  # score qui détermine si c'est un best node
        self.id = id  # met en place un id de localisation pour chaque loc sur la carte

    def __eq__(self, n):  # fonction 'est égale à'
        return n.id == self.id


class AStar:

    def __init__(self, map):  # initialise map
        self.mh = map

    def getBestOpenNode(self):  # obtient le meilleur noeud pas encore calculé
        bestnoeud = None
        for n in self.on:  # pour chaque dans la liste de noeuds à traiter
            if not bestnoeud:
                bestnoeud = n
            else:
                if n.score <= bestnoeud.score:
                    bestnoeud = n
        return bestnoeud

    def tracePath(self, n):  # trace le chemin en remontant l'arbre
        noeuds = []
        coutot = n.mcout  # cout total = cout tot du noeud
        p = n.parent
        noeuds.insert(0, n)  # ajoute le noeud en début de liste

        while True:  # tant que l'id == n
            if p.parent is None:  # si en haut de liste (pas de parent)
                break

            noeuds.insert(0, p)  # on met le parent de début de liste des noeuds
            p = p.parent

        return Path(noeuds, coutot)

    def handleNode(self, noeud, fin):  # fction qui gère chaque noeud
        i = self.o.index(noeud.id)  # index du noeud dans la liste des noeuds à traiter
        self.on.pop(i)  # on supprime ce noeud des noeuds courants
        self.o.pop(i)  # on le supprime des noeuds à traiter
        self.c.append(noeud.id)  # on l'aoute dans la liste des noeuds traités

        noeuds1 = self.mh.getAdjacentNodes(noeud, fin)  # fction getAdjacentNodes ???????
        noeuds = self.mh.neighbors(noeud)

        for n in noeuds:  # pour chaque noeud
            if n.location == fin:  # on a atteint la destination
                return n
            elif n.id in self.c:  # déjà dans la liste des noeuds traités, on continue
                continue
            elif n.id in self.o:  # déjà dans la liste des noeuds à traiter, on vérifie si il y a pas de meilleur score
                i = self.o.index(n.id)
                on = self.on[i]  # on prend la valeur du noeud courant d'indice i
                if n.mcout < on.mcout:  # si le noeud à traiter a un cout plus faible que le noeud courant
                    self.o.pop(i)  # on supprime l'indice du noeud à traiter
                    self.on.append(n)  # n devient un noeud courant (dans liste d'ouverts)
                    self.o.append(n.id)  # on ajoute l'id de n à la liste des noeuds à traiter
            else:  # si c'est un nouveau noeud, on l'ajoute à la liste des noeuds à traiter
                self.on.append(n)
                self.o.append(n.id)

        return None

    def findPath(self, delocation, verslocation):
        self.o = []  # id des noeuds à traiter
        self.on = []  # valeur des noeuds à traiter
        self.c = []  # déjà étudiés

        fin = verslocation
        tnode = self.mh.getNode(delocation)  # noeud de la map en la position fromlocation rentré dans tnode
        self.on.append(tnode)  # on ajoute ce noeud dans la liste des noeuds à traiter
        self.o.append(tnode.id)  # ...
        noeudsuivant = tnode  # tnode devient le prochain noeud

        while noeudsuivant is not None:  # tant qu'on a pas tout parcouru
            termine = self.handleNode(noeudsuivant, fin)  # la fin devient le nextnode
            if termine:  # si on a finit
                return self.tracePath(termine)  # on trace le chemin
            noeudsuivant = self.getBestOpenNode()  # le next noeud est le best node suivant

        return None