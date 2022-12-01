import sqlite3

con = sqlite3.connect('database/data.db')
c = con.cursor()

c.execute(f'UPDATE produtos SET status = "Disponivel ,vendedor_id:1"')
con.commit()

print("Everything is reset")