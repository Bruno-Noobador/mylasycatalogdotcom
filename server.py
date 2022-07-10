from flask import Flask, request, render_template
import json
from csv import writer

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start():
    #print(request.headers)
    userAgent = str(request.headers['User-Agent'])
    return(render_template('start.html', userAgent = userAgent))

@app.route('/', methods=['GET'])
def index():
    #print(request.headers)
    userAgent = str(request.headers['User-Agent'])
    return(render_template('index.html', userAgent = userAgent))

@app.route('/register_cliente', methods=['GET'])
def index1():
    return(render_template('cliente.html'))

@app.route('/register_vendedor', methods=['GET'])
def index2():
    return(render_template('vendedor.html'))

@app.route('/input_vendedores', methods=['POST'])
def index3():
    print(request.headers)
    print(request.form)
    reqData = request.form

    with open('database/vendedores.csv', 'a', newline='') as f_object:  
    # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        writer_object.writerow(reqData.values())  
        f_object.close()
        
    print('\n' + str(reqData))
    return('\nYou just posted.... ' + str(reqData) + '\n')

@app.route('/input_clientes', methods=['POST'])
def index4():
    print(request.headers)
    print(request.form)
    reqData = request.form

    with open('database/clientes.csv', 'a', newline='') as f_object:  
    # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        writer_object.writerow(reqData.values())  
        f_object.close()

    print('\n' + str(reqData))
    return('\nYou just posted.... ' + str(reqData) + '\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
