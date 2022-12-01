import sqlite3, json

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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Product:
    def __init__ (self, id, nome, valor, telefone, email, status, vendedorId, filename):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.telefone = telefone
        self.email = email
        self.status = status
        self.filename = filename
        self.vendedorId = vendedorId

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


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

def parseStatus(status:str) -> str:
    
    realStatus = str(status.split(' ')[0])
    return realStatus

def parseVendedorId(status:str) -> int:
    
    vendedoriD = int(status.split(':')[1].split(';')[0])
    return vendedoriD
    
