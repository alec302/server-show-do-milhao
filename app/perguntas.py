from flask import Blueprint, request
from flask.views import MethodView
from .db import connect_db
from mysql.connector import Error

perguntas_bp = Blueprint("perguntas", __name__)

class PerguntaAPI(MethodView):
    def get(self):

        conn = connect_db()
        if conn is None:
            return {"erro": "Erro ao conectar ao banco de dados"}, 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, pergunta, resposta FROM Perguntas")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return {"erro": "Nenhuma pergunta encontrada"}, 404
        
        perguntas = [
            {"id": row[0], "pergunta": row[1], "resposta": row[2]}
            for row in results
        ]
        return {"perguntas": perguntas}, 200

    def post(self):
        data = request.get_json() or {}
        for campo in ("pergunta", "resposta"):
            if campo not in data:
                return {"erro": f"Campo obrigatório '{campo}' não preenchido"}, 400

        pergunta = data["pergunta"]
        resposta = data["resposta"]

        conn = connect_db()
        if conn is None or not conn.is_connected():
            return {"erro": "Erro ao conectar ao banco de dados"}, 500

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Perguntas (pergunta, resposta) VALUES (%s, %s)"
            cursor.execute(sql, (pergunta, resposta))
            conn.commit()
            pergunta_id = cursor.lastrowid
            return {"id": pergunta_id, "pergunta": pergunta, "resposta": resposta}, 201
        except Error as err:
            return {"erro": "Erro ao inserir pergunta", "message": str(err)}, 500
        finally:
            cursor.close()
            conn.close()

    # def put(self):
    #     data = request.get_json() or {}
    #     for campo in ("id", "pergunta", "resposta"):
    #         if campo not in data:
    #             return {"erro": f"Campo obrigatório '{campo}' não preenchido"}, 400

    #     pergunta_id = data["id"]
    #     pergunta = data["pergunta"]
    #     resposta = data["resposta"]

    #     conn = connect_db()
    #     if conn is None or not conn.is_connected():
    #         return {"erro": "Erro ao conectar ao banco de dados"}, 500

    #     try:
    #         cursor = conn.cursor()
    #         sql = "UPDATE Perguntas SET pergunta = %s, resposta = %s WHERE id = %s"
    #         cursor.execute(sql, (pergunta, resposta, pergunta_id))
    #         conn.commit()
    #         if cursor.rowcount == 0:
    #             return {"erro": "Pergunta não encontrada"}, 404
    #         return {"id": pergunta_id, "pergunta": pergunta, "resposta": resposta}, 200
    #     except Error as err:
    #         return {"erro": "Erro ao atualizar pergunta", "message": str(err)}, 500
    #     finally:
    #         cursor.close()
    #         conn.close()

view = PerguntaAPI.as_view("pergunta_api")
perguntas_bp.add_url_rule("/perguntas", view_func=view, methods=["GET", "POST"])