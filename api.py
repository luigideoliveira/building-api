# Importa a biblioteca da biblioteca do Flask a aplicação, criação das requisições e parse do JSON
from flask import Flask, request, jsonify
from database import select
app = Flask(__name__)

@app.route('/')
def index():
    # Uma mensagem de boas-vindas para a página root
    return "<h1>Seja bem-vindo a minha primeira API!</h1>"

@app.route('/users/', methods=['GET'])
def users_response():
    # Captura as informações de nome enviados
    table_name = request.args.get("table_name", None)
    parameters = eval(request.args.get("parameters", None))
    
    # Para debugar, exibiremos a mensagem
    print(table_name)
    print(parameters)
    
    # Criação do objeto de resposta e definção dos retornos
    response = {}
    
    # Verifica se o usuário enviou alguma coisa
    if not table_name:
        response["ERROR"] = "No table name found. Please send a name."
    elif not parameters:
        response = select(table_name=table_name)
    elif isinstance(parameters, dict):
        response = select(table_name=table_name, parameters=parameters)
        
    return response
   
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)