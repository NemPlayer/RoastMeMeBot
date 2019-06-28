import sqlite3
import logging

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] [%(asctime)s] - %(message)s")

conn = sqlite3.connect("data/roasts.db")

c = conn.cursor()

try:
    c.execute("""CREATE TABLE roasts (
                id integer,
                roasts integer
                )""")
except sqlite3.OperationalError:
    logging.error("Table 'roasts' already exists")

conn.commit()
conn.close()
