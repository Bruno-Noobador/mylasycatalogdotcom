from flask import Flask, request, render_template, send_file
from csv import writer
import sqlite3
import os
from werkzeug.utils import secure_filename

con = sqlite3.connect('database/users.db', check_same_thread=False)
c = con.cursor()

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "database\Produtos_imgs")

@app.route('/start', methods=['GET'])
def start():
    #print(request.headers)
    userAgent = str(request.headers['User-Agent'])
    return(render_template('start.html', userAgent = userAgent))

@app.route('/', methods=['GET'])
def index():
    #print(request.headers)
    userAgent = str(request.headers['User-Agent'])
    return(render_template('Página Principal/index.html', userAgent = userAgent))

@app.route('/register_cliente', methods=['GET'])
def index1():
    return(render_template('Clientes/cadastro.html'))

@app.route('/register_vendedor', methods=['GET'])
def index2():
    return(render_template('Vendedores/cadastro.html'))

@app.route('/input_vendedor', methods=['POST'])
def index3():
    print(request.headers)
    print(request.form)
    reqData = list(request.form.values())

    reqData.pop()
    nome = reqData[0]
    email = reqData[1]
    senha = reqData[2]

    c.execute('''INSERT INTO vendedores (nome, email, senha) VALUES (?,?,?)''', (nome, email, senha))
    con.commit()

    with open('database/vendedores.csv', 'a', newline='') as f_object:  
    # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        writer_object.writerow(reqData)  
        f_object.close()
        
    print('\n' + str(reqData))
    #return('\nYou just posted.... ' + str(reqData) + '\n')
    return('\nVendedor cadastrado com sucesso')

@app.route('/input_clientes', methods=['POST'])
def index4():
    print(request.headers)
    print(request.form)
    reqData = list(request.form.values())

    reqData.pop()
    nome = reqData[0]
    email = reqData[1]
    senha = reqData[2]

    c.execute('''INSERT INTO clientes (nome, email, senha) VALUES (?,?,?)''', (nome, email, senha))
    con.commit()

    with open('database/clientes.csv', 'a', newline='') as f_object:  
    # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        writer_object.writerow(reqData)  
        f_object.close()

    print('\n' + str(reqData))
    # return('\nYou just posted.... ' + str(reqData) + '\n')
    return('\nCliente cadastrado com sucesso')


@app.route('/login', methods=['POST'])
def index5():

    print(request.headers)
    print(request.form)
    reqData = list(request.form.values())

    nome = reqData[0]
    senha = reqData[1]

    c.execute('''SELECT * FROM clientes WHERE nome = (?) AND senha = (?)''', (nome, senha))
    response = c.fetchall()
    logado_como = 'Cliente'

    if len(response) == 0:
        c.execute('''SELECT * FROM vendedores WHERE nome = (?) AND senha = (?)''', (nome, senha))
        response = c.fetchall()
        logado_como = 'Vendedor'

    print(logado_como)
    print(response)
    mensagem = 'logado como: ' + str(logado_como) + '\n' + str(response)

    return mensagem

@app.route('/test', methods=['GET'])
def index6():

    return(render_template('Busca/busca.html'))

@app.route('/cadastro_test', methods=['GET', 'POST'])
def index7():

    if request.method == 'GET':
        return(render_template('Produtos/produtos.html'))

    if request.method == 'POST':

        print(request.headers)
        print(request.form)

        file = request.files['imagem']
        savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(savePath)
        
        #test is being used for this never for something else
        
        return send_file(savePath)
        
            

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
