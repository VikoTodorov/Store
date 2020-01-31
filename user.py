from db import DB
import hashlib
# from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


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
            values = (self.email, self.password, self.name,
                      self.adress,
                      self.phone)
            db.execute('INSERT INTO users (email, password, name, adress, \
                phone) VALUES (?, ?, ?, ?, ?)', values)
            return self

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def find(email):
        with DB() as db:
            row = db.execute('SELECT * FROM users WHERE email = ?',
                             (email, )).fetchone()
            if row:
                return User(*row)

    @staticmethod
    def find_by_id(id):
        if not id:
            return None
        with DB() as db:
            row = db.execute('SELECT * FROM users WHERE id = ?',
                             (id, )).fetchone()
            return User(*row)
