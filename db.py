import sqlite3

DB_NAME = 'store.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email NVARCHAR(255),
        password TEXT NOT NULL,
        name TEXT,
        adress TEXT,
        phone INTEGER
    ) ''')

conn.cursor().execute('''CREATE TABLE IF NOT EXISTS offers
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        price REAL,
        date TEXT,
        status BIT(1),
        FOREIGN KEY(user_id) REFERENCES users(id)
    ) ''')

conn.commit()

class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()