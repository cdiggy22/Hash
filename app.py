from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shhhhh2323'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)