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


@app.route('/offers/new', methods=['GET', 'POST'])
def new_offer():
    if request.method == 'GET':
        return render_template('new_offer.html')
    elif request.method == 'POST':
        user = User.find(request.form['EMAIL'])
        values = (None, user,
                  request.form['TITLE'],
                  request.form['DESCRIPTION'],
                  request.form['PRICE'],
                  request.form['DATE'])
        Offer(*values).create()
        return redirect(url_for('list_offers'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (None, request.form['EMAIL'],
                  request.form['PASSWORD'],
                  request.form['NAME'],
                  request.form['ADDRESS'],
                  request.form['PHONE'])
        User(*values).create()
        return redirect(url_for('list_offers'))
