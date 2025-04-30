from flask import Blueprint, request
from flask.views import MethodView
from .db import connect_db
from mysql.connector import Error

professor_bp = Blueprint("professores", __name__)

class ProfessorAPI(MethodView):
    def get(self):
        """GET /professores → lista todos os professores"""
        conn = connect_db()
        if conn is None:
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM Teste2")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return {"erro": "Nenhum professor encontrado"}, 404

        professores = [
            {"id": row[0], "nome": row[1], "email": row[2]}
            for row in results
        ]
        return {"professores": professores}, 200
    
    def post(self):
        """POST /professores → cria um novo professor"""
        data = request.get_json() or {}
        for campo in ("nome", "email"):
            if campo not in data:
                return {"erro": f"Campo obrigatório '{campo}' não preenchido"}, 400

        nome = data["nome"]
        email = data["email"]

        conn = connect_db()
        if conn is None or not conn.is_connected():
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Teste2 (nome, email) VALUES (%s, %s)"
            cursor.execute(sql, (nome, email))
            conn.commit()
            professor_id = cursor.lastrowid
            return {"id": professor_id, "nome": nome, "email": email}, 201
        except Error as err:
            return {"erro": "Erro ao inserir professor", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()
    
    def put(self):
        """PUT /professores → atualiza um professor existente (identificado pelo ID)"""
        data = request.get_json() or {}
        for campo in ("id", "nome", "email"):
            if campo not in data:
                return {"erro": f"Campo obrigatório '{campo}' não preenchido"}, 400

        id = data["id"]
        nome = data["nome"]
        email = data["email"]

        conn = connect_db()
        if conn is None or not conn.is_connected():
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor()
            sql = "UPDATE Teste2 SET nome=%s, email=%s WHERE id=%s"
            cursor.execute(sql, (nome, email, id))
            conn.commit()
            if cursor.rowcount == 0:
                return {"erro": "Nenhum professor encontrado com o ID fornecido"}, 404
            return {"id": id, "nome": nome, "email": email}, 200
        except Error as err:
            return {"erro": "Erro ao atualizar professor", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        """DELETE /professores → deleta um professor existente (identificado pelo ID)"""
        data = request.get_json() or {}
        if "id" not in data:
            return {"erro": "Campo obrigatório 'id' não preenchido"}, 400

        id = data["id"]

        conn = connect_db()
        if conn is None or not conn.is_connected():
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor()
            sql = "DELETE FROM Teste2 WHERE id=%s"
            cursor.execute(sql, (id,))
            conn.commit()
            if cursor.rowcount == 0:
                return {"erro": "Nenhum professor encontrado com o ID fornecido"}, 404
            return {"mensagem": "Professor deletado com sucesso"}, 200
        except Error as err:
            return {"erro": "Erro ao deletar professor", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()

view = ProfessorAPI.as_view("professor_api")
professor_bp.add_url_rule("/professores", view_func=view, methods=["GET", "POST", "PUT", "DELETE"])