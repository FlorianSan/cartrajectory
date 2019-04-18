#! C:\Program Files (x86)\Python\Python37\python.exe
# Filename: views.py
# encoding: utf-8

from flask import render_template, request, redirect, url_for
from . import app
from IENAC.controllers.formulaire import *
from IENAC.controllers.functions import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/car')
def car():
    return render_template('car.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/flight')
def flight():
    return render_template('flight.html')


@app.route('/controllers/formulaire',methods = ['POST', 'GET'])
def formulaire():
    button_submit = request.form["btn_submit"]

    if button_submit == "form_create":
        add_person(request.form)
        return redirect(url_for("index"))
    if button_submit == "form_connect":
        page_redirect = verif_connect(request.form)
        return redirect(url_for(page_redirect[0], info=page_redirect[1]))


'''@app.route('/commentaire')
def comment():
    msg = msg_info(request.args)
    comments = get_allCommentData()
    return render_template('commentaire.html',data=comments, info=msg)


@app.route('/formulaire',methods = ['POST', 'GET'])
def formulaire():
    button_submit = request.form["btn_submit"]
    if button_submit == "form_comment":
        add_comment(request.form)
        return redirect(url_for("comment"))
    if button_submit == "form_connect":
        page_redirect = verif_connect(request.form)
        return redirect(url_for(page_redirect[0], info=page_redirect[1]))

@app.route('/login')
def login():
    msg = msg_info(request.args)
    return render_template('connecter.html', info = msg)


@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('index'))'''



