from flask import Flask, request
from flask.views import MethodView
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from app.config import Config

app = Flask(__name__)

# config = {
#     'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
#     'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
#     'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
#     'database': os.getenv('DB_NAME', 'db_escola'),  # Obtém o nome do banco de dados da variável de ambiente
#     'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
#     'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
# }

config = Config()

def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None
    
class AlunoAPI(MethodView):
    def get(self):
        """GET /alunos → lista todos os alunos"""
        conn = connect_db()
        if conn is None:
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM tbl_alunos")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return {"erro": "Nenhum aluno encontrado"}, 404

        alunos = [
            {"id": row[0], "nome": row[1], "email": row[2]}
            for row in results
        ]
        return {"alunos": alunos}, 200

    def post(self):
        """POST /alunos → cria um novo aluno"""
        data = request.get_json() or {}
        for campo in ("nome", "cpf"):
            if campo not in data:
                return {"erro": f"Campo obrigatório '{campo}' não preenchido"}, 400

        nome = data["nome"]
        cpf = data["cpf"]
        idade = data.get("idade", 0)

        conn = connect_db()
        if conn is None or not conn.is_connected():
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO tbl_alunos (nome, cpf, idade) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, cpf, idade))
            conn.commit()
            aluno_id = cursor.lastrowid
            return {"id": aluno_id, "nome": nome, "cpf": cpf, "idade": idade}, 201
        except Error as err:
            return {"erro": "Erro ao inserir aluno", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()

    def put(self):
        """PUT /alunos → atualiza um aluno existente (identificado pelo CPF)"""
        data = request.get_json() or {}
        for campo in ("nome", "cpf"):
            if campo not in data:
                return {"erro": f"Campo obrigatório '{campo}' não preenchido"}, 400

        nome = data["nome"]
        cpf = data["cpf"]
        idade = data.get("idade", 0)

        conn = connect_db()
        if conn is None or not conn.is_connected():
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor()
            sql = "UPDATE tbl_alunos SET nome = %s, idade = %s WHERE cpf = %s"
            cursor.execute(sql, (nome, idade, cpf))
            conn.commit()
            return {"nome": nome, "cpf": cpf, "idade": idade}, 200
        except Error as err:
            return {"erro": "Erro ao atualizar aluno", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        """DELETE /alunos → exclui um aluno (identificado pelo CPF)"""
        data = request.get_json() or {}
        if "cpf" not in data:
            return {"erro": "Campo obrigatório 'cpf' não preenchido"}, 400

        cpf = data["cpf"]
        conn = connect_db()
        if conn is None or not conn.is_connected():
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor()
            sql = "DELETE FROM tbl_alunos WHERE cpf = %s"
            cursor.execute(sql, (cpf,))
            conn.commit()
            return {"cpf": cpf}, 200
        except Error as err:
            return {"erro": "Erro ao deletar aluno", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()
    
@app.route('get_professores', methods=['GET'])
def get_professores():
    # conectar colm a base
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    
    # se chegou até, tenho uma conexão válida
    cursor = conn.cursor()

    sql = "SELECT * from tbl_professores"
    cursor.execute(sql)

    results = cursor.fetchall()
    if not results:
        resp = {"erro": "Nenhum aluno encontrado"}
        return resp, 404
    else:
        professores = []
        for professor in results:
            professor_dict = {
                "id": professor[0],
                "nome": professor[1],
                "email": professor[2]
            }
            professores.append(professor_dict)

        resp = {"professores": professores}
        return resp, 200
    
aluno_view = AlunoAPI.as_view("aluno_api")
app.add_url_rule(
    "/alunos",
    view_func=aluno_view,
    methods=["GET", "POST", "PUT", "DELETE"]
)


@app.route('add_professor', methods=['POST'])
def add_professor():

    success = False

    entrada_dados = request.json
    campos_obrigatorios = ['nome', 'cpf']
    for campo in campos_obrigatorios:
        if campo not in entrada_dados:
            resp = {'erro': f"Campo orbigatório {campo} não preenchido"}
            return resp, 404
    
    idade = entrada_dados.get('idade', 0)
    nome = entrada_dados['nome']
    cpf = entrada_dados['cpf']

    conn = connect_db()
    professor_id = None
    if conn.is_connected():
        try:
            cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
            sql = "INSERT INTO tbl_professores (nome, cpf, idade) VALUES (%s, %s, %s)"  # Comando SQL para inserir um aluno
            values = (nome, cpf, idade)  # Dados a serem inseridos

            # Executa o comando SQL com os valores fornecidos
            print(f"Executando SQL: {sql} com valores: {values}")
            cursor.execute(sql, values)
            
            # Confirma a transação no banco de dados
            conn.commit()

            # Obtém o ID do registro recém-inserido
            professor_id = cursor.lastrowid
            success = True
            
        except Error as err:
            # Em caso de erro na inserção, imprime a mensagem de erro
            error = str(err)
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()
    
    if success:
        resp = {"id": professor_id, "nome": nome, "cpf": cpf, "idade": idade}
        return resp, 201
    else:
        resp = {"erro": "Erro ao inserir aluno", "message": error}
        return resp, 500

@app.route('up_professor', methods=['POST'])
def up_professor():
    
    success = False

    entrada_dados = request.json
    campos_obrigatorios = ['nome', 'cpf']
    for campo in campos_obrigatorios:
        if campo not in entrada_dados:
            resp = {'erro': f"Campo orbigatório {campo} não preenchido"}
            return resp, 404
    
    idade = entrada_dados.get('idade', 0)
    nome = entrada_dados['nome']
    cpf = entrada_dados['cpf']

    conn = connect_db()
    professor_id = None
    if conn.is_connected():
        try:
            cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
            sql = "UPDATE tbl_professores SET nome = %s, idade = %s WHERE cpf = %s" # Comando SQL para inserir um aluno
            values = (nome, cpf, idade)  # Dados a serem inseridos

            # Executa o comando SQL com os valores fornecidos
            print(f"Executando SQL: {sql} com valores: {values}")
            cursor.execute(sql, values)
            
            # Confirma a transação no banco de dados
            conn.commit()

            # Obtém o ID do registro recém-inserido
            professor_id = cursor.lastrowid
            success = True
            
        except Error as err:
            # Em caso de erro na inserção, imprime a mensagem de erro
            error = str(err)
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()
    
    if success:
        resp = {"id": professor_id, "nome": nome, "cpf": cpf, "idade": idade}
        return resp, 201
    else:
        resp = {"erro": "Erro ao inserir aluno", "message": error}
        return resp, 500
    
@app.route('del_professor', methods=['POST'])
def del_professor():
    
    success = False

    entrada_dados = request.json
    campos_obrigatorios = ['cpf']
    for campo in campos_obrigatorios:
        if campo not in entrada_dados:
            resp = {'erro': f"Campo orbigatório {campo} não preenchido"}
            return resp, 404
    
    cpf = entrada_dados['cpf']

    conn = connect_db()
    professor_id = None
    if conn.is_connected():
        try:
            cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
            sql = "DELETE FROM tbl_professores WHERE cpf = %s" # Comando SQL para inserir um aluno
            values = (cpf,)  # Dados a serem inseridos

            # Executa o comando SQL com os valores fornecidos
            print(f"Executando SQL: {sql} com valores: {values}")
            cursor.execute(sql, values)
            
            # Confirma a transação no banco de dados
            conn.commit()

            # Obtém o ID do registro recém-inserido
            professor_id = cursor.lastrowid
            success = True
            
        except Error as err:
            # Em caso de erro na inserção, imprime a mensagem de erro
            error = str(err)
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()
    
    if success:
        resp = {"id": professor_id, "cpf": cpf}
        return resp, 201
    else:
        resp = {"erro": "Erro ao inserir aluno", "message": error}
        return resp, 500










    
if __name__ == '__main__':
    app.run(debug=False)

