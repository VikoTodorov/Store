from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
from flask_httpauth import HTTPBasicAuth    #need for authenticate users
from functools import wraps #new import
import json    #for data formating


import db
from user import User
from offer import Offer

app = Flask(__name__)
auth = HTTPBasicAuth()  #

# login request
def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

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
        user = User.find(request.form['email'])
        values = (None, user, request.form['title'], request.form['description'], request.form['price'], request.form['date'])
        Offer(*values).create()
        return redirect(url_for('list_offers'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (None, request.form['email'], request.form['password'], request.form['name'], request.form['adress'], request.form['phone'])
        User(*values).create()
        return redirect(url_for('list_offers'))

# verifying password
@auth.verify_password
def verify_password(email, password):
    user = User.find(email)
    if user:
        return user.verify_password(password)
    return False

# login implementation
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        data = json.loads(request.data.decode('ascii'))
        email = data['email']
        password = data['password']
        user = User.find(email)         # here searching not by id but by email
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        return jsonify({'token': token})

        