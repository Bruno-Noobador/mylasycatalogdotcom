import sqlite3

con = sqlite3.connect('database/data.db', check_same_thread=False)
c = con.cursor()

class User:
    def __init__(self, id, nome, email, senha, tipo):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo

    def getName (self):
        c.execute(f'SELECT nome FROM "{self.tipo}es" WHERE id = "{self.id}"')
        response = c.fetchall()
        return str ((str (response[0]).split(',')[0]).replace('(', '').replace("'", ""))

    def getEmail (self):
        c.execute(f'SELECT email FROM "{self.tipo}es" WHERE id = "{self.id}"')
        response = c.fetchall()
        return str ((str (response[0]).split(',')[0]).replace('(', '').replace("'", ""))

class Product:
    def __init__ (self, id, nome, valor, telefone, email, status, filename):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.telefone = telefone
        self.email = email
        self.status = status
        self.filename = filename


def parseId (database_response) -> int:
    
    values = str (database_response[0])
    
    return int ((values.split(',')[0]).replace('(', ''))



def parseName (database_response:list) -> str:
    
    print(f'response {database_response}')

    values = str (database_response[0])
    
    return str (values.replace ('(', '').replace (')', '').replace (',', ''))



def parseEmail (database_response) -> str:
    
    values = str (database_response[0])
    
    return str (values.replace ('(', '').replace (')', '').replace (',', ''))



def getFileExtention (filename) -> str:

    garbage = filename.split('.')
    fileExtention = str (garbage [-1])

    return fileExtention
