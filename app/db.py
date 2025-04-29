import mysql.connector
from mysql.connector import Error
from .config import Config

config = Config().get_connection_params()

def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        print(f"Erro: {err}")
        return None