# Importa a biblioteca da biblioteca do Flask a aplicação, criação das requisições e parse do JSON
from flask import Flask, request, jsonify
from database import select, insert
app = Flask(__name__)

@app.route('/')
def index():
    # Uma mensagem de boas-vindas para a página root
    return "<h1>Seja bem-vindo a minha primeira API!</h1>"

@app.route('/users/', methods=['GET'])
def users():
    # Captura as informações de nome enviados
    parameters = request.args.get("parameters", None)
    
    # Para debugar, exibiremos a mensagem
    print(parameters)
    
    # Criação do objeto de resposta e definção dos retornos
    response = {}
    
    # Verifica se o usuário enviou alguma coisa
    if not parameters:
        response = select(table_name='public_api.users')
    elif isinstance(eval(parameters), dict):
        response = select(table_name='public_api.users', parameters=eval(parameters))
        
    return response

@app.route('/new_user/', methods=['POST'])
def new_user():
    # Verifica o tipo de conteúdo
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        request_body = request.json
    else:
        return 'Content-Type not supported!'
    
    print(request_body)
    
    response = insert(table_name='public_api.users', parameters=request_body)
        
    return response
   
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)