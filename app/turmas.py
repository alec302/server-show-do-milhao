from flask import Blueprint, request
from flask.views import MethodView
from .db import connect_db
from mysql.connector import Error

turmas_bp = Blueprint("turmas", __name__)

class TurmaAPI(MethodView):
    def get(self):
        """GET /turmas → lista todas as turmas"""
        conn = connect_db()
        if conn is None:
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        cursor = conn.cursor()
        cursor.execute("SELECT id, id_turma, ano FROM Teste3")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return {"erro": "Nenhuma turma encontrada"}, 404

        turmas = [
            {"id": row[0], "nome": row[1], "ano": row[2]}
            for row in results
        ]
        return {"turmas": turmas}, 200
    
    def post(self):
        """POST /turmas → cria uma nova turma"""
        data = request.get_json() or {}
        for campo in ("id_turma", "ano"):
            if campo not in data:
                return {"erro": f"Campo obrigatório '{campo}' não preenchido"}, 400

        id_turma = data["id_turma"]
        ano = data["ano"]

        conn = connect_db()
        if conn is None or not conn.is_connected():
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Teste3 (id_turma, ano) VALUES (%s, %s)"
            cursor.execute(sql, (id_turma, ano))
            conn.commit()
            turma_id = cursor.lastrowid
            return {"id": turma_id, "id_turma": id_turma, "ano": ano}, 201
        except Error as err:
            return {"erro": "Erro ao inserir turma", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()
    
    def put(self):
        """PUT /turmas → atualiza uma turma existente (identificada pelo ID)"""
        data = request.get_json() or {}
        for campo in ("id", "id_turma", "ano"):
            if campo not in data:
                return {"erro": f"Campo obrigatório '{campo}' não preenchido"}, 400

        id_turma = data["id_turma"]
        ano = data["ano"]
        id = data["id"]

        conn = connect_db()
        if conn is None or not conn.is_connected():
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor()
            sql = "UPDATE Teste3 SET id_turma = %s, ano = %s WHERE id = %s"
            cursor.execute(sql, (id_turma, ano, id))
            conn.commit()
            return {"id": id, "id_turma": id_turma, "ano": ano}, 200
        except Error as err:
            return {"erro": "Erro ao atualizar turma", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        """DELETE /turmas → deleta uma turma existente (identificada pelo ID)"""
        data = request.get_json() or {}
        for campo in ("id",):
            if campo not in data:
                return {"erro": f"Campo obrigatório '{campo}' não preenchido"}, 400

        id = data["id"]

        conn = connect_db()
        if conn is None or not conn.is_connected():
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor()
            sql = "DELETE FROM Teste3 WHERE id = %s"
            cursor.execute(sql, (id,))
            conn.commit()
            if cursor.rowcount == 0:
                return {"erro": "Nenhuma turma encontrada com o ID fornecido"}, 404
            return {"mensagem": "Turma deletada com sucesso"}, 200
        except Error as err:
            return {"erro": "Erro ao deletar turma", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()

view = TurmaAPI.as_view("turma_api")
turmas_bp.add_url_rule("/turmas", view_func=view, methods=["GET", "POST"])
turmas_bp.add_url_rule("/turmas/<int:id>", view_func=view, methods=["PUT", "DELETE"])