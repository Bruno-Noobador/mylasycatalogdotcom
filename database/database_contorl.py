import sqlite3

# con = sqlite3.connect('database/users.db')
con = sqlite3.connect('users.db')
c = con.cursor()

# c.execute('''CREATE TABLE clientes
#     (id INTEGER PRIMARY KEY,
#     nome TEXT,
#     email TEXT, 
#     senha TEXT);''')

# c.execute('''DROP TABLE IF EXISTS clientes''')

# c.execute('''CREATE TABLE vendedores
#     (id INTEGER PRIMARY KEY,
#     nome TEXT,
#     email TEXT, 
#     senha TEXT);''')

# c.execute('''DROP TABLE IF EXISTS vendedores''')

# c.execute('''DROP TABLE IF EXISTS clientes''')

c.execute('''CREATE TABLE produtos
    (id INTEGER PRIMARY KEY,
    nome TEXT,
    email TEXT, 
    senha TEXT);''')

# c.execute('''DROP TABLE IF EXISTS produtos''')


c.execute('''SELECT * FROM clientes''')
response = c.fetchall()
print('\nClientes data:\n', response)

c.execute('''SELECT * FROM vendedores''')
response = c.fetchall()
print('\nVendedores data:\n', response)

c.execute('''SELECT * FROM produtos''')
response = c.fetchall()
print('\nProdutos data:\n', response)