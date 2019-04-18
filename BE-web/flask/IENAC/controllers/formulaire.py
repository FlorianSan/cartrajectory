#! C:\Program Files (x86)\Python\Python37\python.exe
# -*- coding: UTF-8 -*-
# enable debugging

from flask import session
from IENAC.data.bdd import *


###################################################################################################
#ajoute un commentaire dans la BD

def add_person(dataform):
    idPersonne = dataform['idPersonne']
    login = dataform['login']
    motdepasse = dataform['motdepasse']
    nom = dataform['nom']
    prenom = dataform['prenom']
    mail = dataform['mail']
    telephone = dataform['telephone']
    dateNaiss = dataform['dateNaiss']

    info = "insPerson_success"
    msg=add_personData(idPersonne, login, motdepasse, nom, prenom, mail, telephone, dateNaiss)
    if msg != "":
        info="insPerson_fail"

    return info

def verif_connect(dataform):
    login = dataform['login']
    mdp = dataform['MDP']
    res = authentification(login, mdp)
    try :
        session["id"]=res[0]["id"]
        session["nom"] = res[0]["nom"]
        session["prenom"] = res[0]["prenom"]
        session["logged_in"]=1
        page_redirect=["index","auth_success"]
    except (KeyError, IndexError) as e :
        page_redirect=["login","auth_fail"]
    return page_redirect