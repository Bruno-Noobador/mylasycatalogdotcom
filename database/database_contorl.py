import sqlite3

con = sqlite3.connect('database/data.db')
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

# c.execute('''DROP TABLE IF EXISTS produtos''')

# c.execute('''CREATE TABLE produtos
#     (id INTEGER PRIMARY KEY,
#     nome TEXT,
#     valor TEXT, 
#     telefone TEXT,
#     email TEXT,
#     status TEXT,
#     imagem_nome TEXT);''')

# c.execute(f'INSERT INTO produtos (id) VALUES (1)')
# con.commit()

# c.execute('''SELECT * FROM clientes''')
# response = c.fetchall()
# print('\nClientes data:\n', response)

# c.execute('''SELECT * FROM vendedores''')
# response = c.fetchall()
# print('\nVendedores data:\n', response)

# c.execute(f'UPDATE produtos SET imagem_nome = "5_Carro_Rosa.jpg" WHERE id=5')
# con.commit()

string = 'produtos'

c.execute(f'SELECT * FROM {string}')
response = c.fetchall()
print('\nProdutos data:\n', response)

c.execute('''SELECT MAX(id) FROM produtos''')
response = c.fetchall()
print('\nProdutos data:\n', response)
