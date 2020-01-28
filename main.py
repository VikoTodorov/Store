from flask import Flask
from flask import render_template, request, redirect, url_for

import db
from user import User
from offer import Offer

app = Flask(__name__)

@app.route('/')
def hello_world():
    return redirect(url_for('list_offers'))

@app.route('/offers')
def list_offers():
    return render_template('offers.html', offers=Offer.all())
