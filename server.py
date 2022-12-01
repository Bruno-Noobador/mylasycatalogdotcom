from flask import Flask, request, render_template, send_file, send_from_directory, session, jsonify
from csv import writer
import sqlite3
import os
from werkzeug.utils import secure_filename
from libs import User, Product, parseId, getFileExtention, parseName, parseStatus, parseVendedorId

con = sqlite3.connect('database/data.db', check_same_thread=False)
c = con.cursor()

app = Flask(__name__)
app.secret_key = '123'

UPLOAD_FOLDER = os.path.join(os.getcwd(), "database\Produtos_imgs")

@app.route('/start', methods=['GET'])
def start():
    #print(request.headers)
    userAgent = str(request.headers['User-Agent'])
    return(render_template('start.html', userAgent = userAgent))

@app.route('/', methods=['GET'])
def index():
    #print(request.headers)

    produtos = []

    userAgent = str(request.headers['User-Agent'])
    
    c.execute(f'SELECT * FROM produtos ORDER BY id DESC LIMIT 6')
    response = c.fetchall()
    
    print(f'response: {response}')
    
    for produto in response:

            garbage_status = produto[5]

            id = produto[0]
            nome = produto[1]
            valor = produto[2]
            telefone = produto[3]
            email = produto[4]
            status = parseStatus (garbage_status)
            vendedorId = parseVendedorId (garbage_status)
            filename = produto[6]
            
            produto = Product(id, nome, valor, telefone, email, status, vendedorId, filename)

            produtos.append(produto)
            # print(f'Filename: {produto.filename}')

    print(f'produtos: {produtos}')

    return(render_template('Página Principal/index.html', produtos=produtos, session=session))

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

    c.execute(f'INSERT INTO vendedores (nome, email, senha) VALUES ("{nome}", "{email}", "{senha}")')
    con.commit()

    with open('database/vendedores.csv', 'a', newline='') as f_object:  
    # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        writer_object.writerow(reqData)  
        f_object.close()
        
    print('\n' + str(reqData))
    #return('\nYou just posted.... ' + str(reqData) + '\n')
    return '''
        <script>
                alert('Vendedor Cadastrado com sucesso!')
                location.href = "/";
        </script>'''

@app.route('/input_clientes', methods=['POST'])
def index4():
    print(request.headers)
    print(request.form)
    reqData = list(request.form.values())

    reqData.pop()
    nome = reqData[0]
    email = reqData[1]
    senha = reqData[2]

    c.execute(f'INSERT INTO clientes (nome, email, senha) VALUES ("{nome}", "{email}", "{senha}")')
    con.commit()

    # user = User()

    with open('database/clientes.csv', 'a', newline='') as f_object:  
    # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        writer_object.writerow(reqData)  
        f_object.close()

    print('\n' + str(reqData))
    # return('\nYou just posted.... ' + str(reqData) + '\n')
    return '''
        <script>
                alert('Cliente Cadastrado com sucesso!')
                location.href = "/";
        </script>'''


@app.route('/login', methods=['POST'])
def login():

    print(request.headers)
    print(request.form)
    reqData = list(request.form.values())

    input1 = reqData[0]
    senha = reqData[1]

    user = User (None, None, None, senha, None)

    c.execute(f'SELECT * FROM clientes WHERE (nome = "{input1}" OR email = "{input1}") AND senha = "{senha}"')
    response = c.fetchall()
    
    if len(response):
        id = parseId(response)

        user.id = id
        user.tipo = 'client'
        user.nome = user.getName()
        user.email = user.getEmail()

    if len(response) == 0:
        c.execute(f'SELECT * FROM vendedores WHERE (nome = "{input1}" OR email = "{input1}") AND senha = "{senha}"')
        response = c.fetchall()
        
        if len(response) == 0:
            return '''
            <script>
                alert('Nenhum usuário encontrado. Tente novamente')
                location.href = "/";
            </script>'''
        
        id = parseId(response)

        user.id = id
        user.tipo = 'vendedor'
        user.nome = user.getName()
        user.email = user.getEmail()

    session['user'] = user.toJSON()

    print(user.tipo)
    print(response)

    return '''
        <script>
                alert('Usuário Logado com sucesso!')
                location.href = "/";
        </script>'''


@app.route('/test', methods=['POST'])
def index6():

    def download_file(image_name):
        return send_from_directory(UPLOAD_FOLDER, image_name, as_attachment=True)

    # app.static_folder = 'database\Produtos_imgs'
    app.static_url_path ='database\Produtos_imgs'
    produtos = []

    print(request.headers)
    print(request.form)

    reqData = list (request.form.values())

    busca = str (reqData[0])

    c.execute(f'SELECT * FROM produtos WHERE UPPER(nome) LIKE "%{busca}%"')
    response = c.fetchall()

    print(f'Busca: {busca}')
    print(f'response: {response}')


    # produto = Product (id, nome, valor, email, status)
    for produto in response:
            
            garbage_status = produto[5]

            id = produto[0]
            nome = produto[1]
            valor = produto[2]
            telefone = produto[3]
            email = produto[4]
            status = parseStatus (garbage_status)
            vendedorId = parseVendedorId (garbage_status)
            filename = produto[6]
            
            produto = Product(id, nome, valor, telefone, email, status, vendedorId, filename)

            produtos.append(produto)

    # return f'id: {produto.id} \n nome: {produto.nome} \n valor: {produto.valor} \n email: {produto.email} \n status: {produto.status}'
    return(render_template('Busca/busca.html', produtos=produtos))


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route('/cadastro_test', methods=['GET', 'POST'])
def index7():
    
    if 'user' in session:
        user = eval(session['user'])
        id = user['id']
    print(f'id: {id}')

    if request.method == 'GET':
        return(render_template('Produtos/produtos.html'))

    if request.method == 'POST':
        
        print(request.headers)
        print(request.form)
        reqData = list(request.form.values())
        print(f'id: {id}')

        nome = reqData[0]
        valor = reqData[1]
        telefone = reqData[2]
        email = reqData[3]
        status = f'Disponivel ,vendedor_id:{id}'
        # filename = "temp_name"


        c.execute('''SELECT MAX(id) FROM produtos''')
        response = c.fetchall()
        print(response)

        id = parseId (response)

        file = request.files['imagem']

        fileExtention = getFileExtention (file.filename)

        filename = secure_filename(f'{id+1}_{nome}.{fileExtention}')
        print(filename)

        c.execute(f'SELECT nome FROM produtos WHERE id = {id}')
        response = c.fetchall()
        nome_banco = parseName (response)

        print(f'nome banco {nome_banco}')

        c.execute(f'INSERT INTO produtos (nome, valor, telefone, email, status, imagem_nome) VALUES ("{nome}", "{valor}", "{telefone}", "{email}", "{status}", "{filename}")')
        con.commit()

        file.filename = filename
        savePath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(savePath)
        
        #test is being used for this never for something else
        
        return send_file(savePath)
        

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():

    produtos = []

    if "user" in session:
        user = eval(session['user'])
        
        print(user)
        name = user['nome']
        print(f"Nome: {name}")
        tipo = user['tipo']
        id = user['id']

        if tipo == 'vendedor':
            c.execute(f'SELECT * FROM produtos WHERE status LIKE "%{id}"')
            response = c.fetchall()

            for produto in response:
                garbage_status = produto[5]
                id = produto[0]
                nome = produto[1]
                valor = produto[2]
                telefone = produto[3]
                email = produto[4]
                status = parseStatus (garbage_status)
                vendedorId = parseVendedorId (garbage_status)
                filename = produto[6]
            
                produto = Product(id, nome, valor, telefone, email, status, vendedorId, filename)

                produtos.append(produto)


        if tipo == 'client':
            c.execute(f'SELECT * FROM produtos WHERE status LIKE "%{id}"')
            response = c.fetchall()

            for produto in response:
                garbage_status = produto[5]
                id = produto[0]
                nome = produto[1]
                valor = produto[2]
                telefone = produto[3]
                email = produto[4]
                status = parseStatus (garbage_status)
                vendedorId = parseVendedorId (garbage_status)
                filename = produto[6]
            
                produto = Product(id, nome, valor, telefone, email, status, vendedorId, filename)

                produtos.append(produto)

        return render_template ('Perfil/perfil.html', user=user, produtos=produtos)

    else:
        return '''
        <script>
                alert('Usuario não logado. Tente Novamente.')
                history.back()
        </script>'''

@app.route('/clean', methods=['GET'])
def clean():
    session.pop("user", None)
    return '''
        <script>
                alert('Usuario saiu de sessão')
                location.href = "/";
        </script>'''

@app.route('/site_dev', methods=['GET'])
def site_em_desenvolvimento():
    return '''
        <script>
                alert('Site em construção')
                location.href = "/";
        </script>'''

@app.route('/pagamento+<produto_id>', methods=['GET'])
def pagamento(produto_id):

    if eval(session['user'])['tipo'] == "vendedor":
        return '''
        <script>
                alert('Vendedores não podem fazer compras')
                location.href = "/";
        </script>'''

    c.execute(f'SELECT * FROM produtos WHERE id = {produto_id}')
    response = c.fetchall()

    for produto in response:
        garbage_status = produto[5]
        id = produto[0]
        nome = produto[1]
        valor = produto[2]
        telefone = produto[3]
        email = produto[4]
        status = parseStatus (garbage_status)
        vendedorId = parseVendedorId (garbage_status)
        filename = produto[6]

        produto = Product(id, nome, valor, telefone, email, status, vendedorId, filename)
    
    session['produto'] = produto.toJSON()
    print(eval(session['produto']))

    return render_template('Pagamento/pagamento.html', produto=produto)

@app.route('/check_pagamento')
def check_pagamento():

    if 'produto' in session:
        produto = eval(session['produto'])
        id = produto['id']

    vendedor_id = produto['vendedorId']
    cliente = eval(session['user'])

    cliente_id = cliente['id']
    c.execute(f'UPDATE produtos SET status = "Vendido ,vendedor_id:{vendedor_id}; cliente_id:{cliente_id}" WHERE id={id}')
    con.commit()

    return '''
        <script>
                alert('Compra realizada com sucesso')
                location.href = "/";
        </script>'''
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
