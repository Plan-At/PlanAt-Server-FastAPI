import sqlite3

db = sqlite3.connect("token.db")

db.execute(f"""CREATE TABLE IF NOT EXISTS exampleTable (firstToken int)""")