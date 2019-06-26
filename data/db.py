import sqlite3

conn = sqlite3.connect("roasts.db")

c = conn.cursor()

try:
    c.execute("""CREATE TABLE roasts (
                id integer,
                roasts integer
                )""")
except sqlite3.OperationalError:
    print("[ERR] Table 'roasts' already exists")

conn.commit()
conn.close()
