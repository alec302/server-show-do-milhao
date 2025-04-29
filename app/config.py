# app/config.py
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        """
        Initializes the Config object by loading environment variables.
        No arguments are needed to create an instance.
        """
        load_dotenv('.env') # Load variables from .env file

        # Load database configuration from environment variables
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_PORT = os.getenv("DB_PORT") # Keep as string initially
        self.SSL_CA_PATH = os.getenv("SSL_CA_PATH")

        # Load Flask specific configs if needed (optional)
        self.DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1', 't')
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'a_default_secret_key')

    def get_connection_params(self):
        """Returns a dictionary suitable for mysql.connector.connect()"""
        params = {
            'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
            'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
            'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
            'database': os.getenv('DB_NAME'),  # Obtém o nome do banco de dados da variável de ambiente
            'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
            'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
        }
        
        if self.SSL_CA_PATH:
            params['ssl_ca'] = self.SSL_CA_PATH
            params['ssl_verify_cert'] = True
        
        return params

# Example of how to use it elsewhere (e.g., in app/db.py):
# from .config import Config
# config_instance = Config() # Just create an instance, it loads automatically
# connection_params = config_instance.get_connection_params()
# conn = mysql.connector.connect(**connection_params)


