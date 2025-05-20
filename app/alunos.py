
from flask import Blueprint, request
from flask.views import MethodView
from .db import connect_db
from mysql.connector import Error

aluno_bp = Blueprint("alunos", __name__)

class AlunoAPI(MethodView):
    def get(self):
        """GET /alunos → lista todos os alunos"""
        conn = connect_db()
        if conn is None:
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, cpf, idade FROM Teste")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return {"erro": "Nenhum aluno encontrado"}, 404

        alunos = [
            {"id": row[0], "nome": row[1], "cpf": row[2], "idade": row[3]}
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
            sql = "INSERT INTO Teste (nome, cpf, idade) VALUES (%s, %s, %s)"
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
            return {"erro": "Erro ao conectar ao banco de dado"}, 500

        try:
            cursor = conn.cursor()
            sql = "UPDATE Teste SET nome = %s, idade = %s WHERE cpf = %s"
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
            sql = "DELETE FROM Teste WHERE cpf = %s"
            cursor.execute(sql, (cpf,))
            conn.commit()
            return {"cpf": cpf}, 200
        except Error as err:
            return {"erro": "Erro ao deletar aluno", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()

view = AlunoAPI.as_view("aluno_api")
aluno_bp.add_url_rule("/", methods=["GET","POST","PUT","DELETE"], view_func=view)