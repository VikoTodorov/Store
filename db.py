import sqlite3

DB_NAME = 'store.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''CREATE TABLE IF NOT EXISTS USERS
    (
        ID         INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
        EMAIL      NVARCHAR(255),
        PASSWORD   TEXT NOT NULL,
        NAME       NVARCHAR(60),
        ADRESS     TEXT,
        PHONE      INTEGER
    ); ''')

conn.cursor().execute('''CREATE TABLE IF NOT EXISTS OFFERS
    (
        ID         INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
        USER_ID    INTEGER,
        TITLE      TEXT,
        DESCRIOPTION TEXT,
        PRICE      REAL,
        DATE       TEXT,
        STATUS     INTEGER,
        FOREIGN KEY(USER_ID) REFERENCES USERS(ID)
    ); ''')

conn.commit()


class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
