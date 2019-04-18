# Filename: __init__.py
# encoding: utf-8

from flask import Flask

app = Flask(__name__, template_folder='template')
app.config.from_object('config')

