from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
from flask_httpauth import HTTPBasicAuth
import json
from functools import wraps

import db
from user import User
from offer import Offer

app = Flask(__name__)
auth = HTTPBasicAuth()

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            return redirect('/login/failed')
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def hello_world():
    return redirect(url_for('list_offers'))

@app.route('/offers')
def list_offers():
    return render_template('offers.html', offers=Offer.all())

@app.route('/offers/new', methods=['GET', 'POST'])
@require_login
def new_offer():
    if request.method == 'GET':
        return render_template('new_offer.html')
    elif request.method == 'POST':
        user = User.find(request.form['email'])
        values = (None, user, request.form['title'], request.form['description'], request.form['price'], request.form['date'])
        Offer(*values).create()
        return redirect(url_for('list_offers'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (None, request.form['email'], User.hash_password(request.form['password']), request.form['name'], request.form['adress'], request.form['phone'])
        User(*values).create()
        return redirect(url_for('list_offers'))

@auth.verify_password
def verify_password(name, password):
    user = User.find_by_name(name)
    if user:
        return user.verify_password(password)
    return False

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        data = json.loads(request.data.decode('ascii'))
        name = data['name']
        password = data['password']
        user = User.find_by_name(name)
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        return jsonify({'token': token})

@app.route('/login/failed', methods=["GET", "POST"])
def login_failed():
    if request.method == "GET":
        return render_template('login_failed.html')
    elif request.method == "POST":
        data = json.loads(request.data.decode('ascii'))
        name = data['name']
        password = data['password']
        user = User.find_by_name(name)
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        return jsonify({'token': token})
