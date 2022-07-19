import sqlite3

conn = sqlite3.connect('database.db')
with open('db.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()
cur.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
            ('123', 'abc')
            )
cur.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
            ('456', 'def')
            )
conn.commit()
conn.close()
