from flask import Flask, session
from flask import render_template, request, redirect, url_for

import db
from user import User
from offer import Offer

app = Flask(__name__)
app.secret_key = "aZzWyKPkFeJ,:k234"


@app.route('/')
def hello_world():
    if 'email' in session:
        return redirect(url_for('logged'))
    else:
        return redirect(url_for('unlogged'))


@app.route('/logged', endpoint="logged")
def logged():
    return render_template('logged.html', offers=Offer.all())


@app.route('/unlogged')
def unlogged():
    return render_template('index.html')


@app.route('/offers/new', methods=['GET', 'POST'])
def new_offer():
    if request.method == 'GET':
        return render_template('new_offer.html')
    elif request.method == 'POST':
        user = User.find(request.form['email'])
        values = (None, user, request.form['title'],
                  request.form['description'],
                  request.form['price'],
                  request.form['date'])
        Offer(*values).create()
        return redirect(url_for('logged'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (None, request.form['email'],
                  User.hash_password(request.form['password']),
                  request.form['name'], request.form['adress'],
                  request.form['phone'])
        User(*values).create()
        session['email'] = values[1]
        return redirect(url_for('logged'))


@app.route('/checklogin')
def login():
    pass


if __name__ == '__main__':
    app.run()
