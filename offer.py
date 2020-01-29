from db import DB
from user import User

class Offer:
    def __init__(self, id, user, title, description, price, date):
        self.id = id
        self.user = user
        self.title = title
        self.description = description
        self.price = price
        self.date = date
        self.status = 1

    def create(self):
        with DB() as db:
            values = (self.user.id, self.title, self.description, self.price, self.date, self.status)
            db.execute('INSERT INTO offers(user_id, title, description, price, date, status) VALUES(?, ?, ?, ?, ?, ?)', values)
            return self

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM offers').fetchall()
            return [Offer(*row) for row in rows]
    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM offers WHERE id = ?', (id, )).fetchone()
            return Offer(*row) # :)
