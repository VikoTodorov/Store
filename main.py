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
    if 'email' in session:
        return render_template('logged.html', offers=Offer.all())
    else:
        return redirect(url_for('unlogged'))


@app.route('/unlogged')
def unlogged():
    return render_template('index.html')


@app.route('/register')
def return_register():
    return render_template('register.html')


@app.route('/login')
def return_login():
    return render_template('login.html')


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


@app.route('/register-check', methods=['GET', 'POST'])
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


@app.route('/checklogin', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find(email)
        if not user and user.verify_password(password):
            return render_template("/login.html", error="Invalid email or \
                                   password")
        else:
            session['email'] = email
            return render_template('/logged.html')


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
