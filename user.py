from db import DB
import hashlib
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

SECRET_KEY = 'Bfb<jbcMbbf1^MASHm@snw2212JmM'



class User:
    def __init__(self, id, email, password, name, adress, phone):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.adress = adress
        self.phone = phone

    def create(self):
        with DB() as db:
            values = (self.email,
                      self.password,
                      self.name,
                      self.adress,
                      self.phone)
            db.execute('INSERT INTO USERS (EMAIL, PASSWORD, NAME, ADRESS, \
                PHONE) VALUES (?, ?, ?, ?, ?)', values)
            return self

<<<<<<< HEAD
    @staticmethod    
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def find(email):
        with DB() as db:
            row = db.execute('SELECT * FROM users WHERE email = ?', (email, )).fetchone()
            return User(*row)

    @staticmethod
    def find_by_name(name):
        if not name:
            return None
        with DB() as db:
            row = db.execute('SELECT * FROM users WHERE name = ?', (name, )).fetchone()
            return User(*row)

    def generate_token(self):
        s = Serializer(SECRET_KEY, expires_in=600)
        return s.dumps({'name' : self.name})
    
    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            s.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return True
=======
    @staticmethod
    def find(email):
        with DB() as db:
            row = db.execute('SELECT * FROM USERS WHERE EMAIL = ?',
                             (email, )).fetchone()
            return User(*row)
>>>>>>> 5b7646931f2cd95d4120950a6f5cff6b50196a62
