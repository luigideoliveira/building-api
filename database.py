import psycopg2, os, json
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

def connect_database():
    try:
        conn = psycopg2.connect(host=db_host,port=db_port,dbname=db_name,user=db_user,password=db_password)
        cursor = conn.cursor()
        print("Database connection was succesull!")
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        
    return conn, cursor

def parse_cursor_return(cursor):
    # Captura o nome das colunas
    colunas = [desc[0] for desc in cursor.description]

    # Obter os resultados do cursor
    rows = cursor.fetchall()

    # Transformar os resultados em um objeto JSON
    resultado_json = []
    for row in rows:
        #resultado_dict = {coluna: str(valor) if type(valor) == bool else valor for coluna, valor in zip(colunas, row)}
        resultado_dict = {coluna: valor for coluna, valor in zip(colunas, row)}
        resultado_json.append(resultado_dict)
    
    resultado_json_string = json.dumps({"data":resultado_json})

    # Imprimir o resultado como uma string JSON
    return resultado_json_string
    
        
def select(table_name, parameters=None):
    conn, cursor = connect_database()
    
    if not parameters:
        # Executa a instrução SQL
        cursor.execute(f"SELECT * FROM {table_name}")
        json_message = parse_cursor_return(cursor)
        
    else:
        # Transforma as chaves do dicionário em uma lista
        parameters_keys_list = list(parameters.keys())
        
        # Cria um template da consulta a ser realizada
        sql_query = f'SELECT * FROM {table_name} WHERE '
        
        # Para cada chave no dicionário dos parâmetros da query
        for param in parameters.keys():
            # Verifica se é o último parâmetro do dicionário
            if len(parameters_keys_list) - 1 == parameters_keys_list.index(param):
                # Verifica se é uma string ou um número para, corretamente, montar a query SQL
                if isinstance(parameters[param], str):
                    if '%' in parameters[param]:
                        sql_query += f"{param} like '{parameters[param]}'"
                    else:
                        sql_query += f"{param} = '{parameters[param]}'"
                elif isinstance(parameters[param], (int, float)):
                    sql_query += f"{param} = {parameters[param]}"
            else:
                # Caso não seja o último parâmetro do dicionário, adiciona a cláusula AND
                if isinstance(parameters[param], str):
                    if '%' in parameters[param]:
                        sql_query += f"{param} like '{parameters[param]}' and "
                    else: 
                        sql_query += f"{param} = '{parameters[param]}' and "
                elif isinstance(parameters[param], (int, float)):
                    sql_query += f"{param} = {parameters[param]} and "
                
        print(sql_query)
        # Executa a instrução SQL
        cursor.execute(sql_query)
        
        json_message = parse_cursor_return(cursor)
            
    cursor.close()
    conn.close()
    
    return json_message

# json_return = select('public_api.users', {'status':'true', 'user_name': '%oliveira'})

# print(json_return)