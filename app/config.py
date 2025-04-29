# app/config.py
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        """
        Initializes the Config object by loading environment variables.
        No arguments are needed to create an instance.
        """
        load_dotenv('.env') 

        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_PORT = os.getenv("DB_PORT") 
        self.SSL_CA_PATH = os.getenv("SSL_CA_PATH")

        # Load Flask specific configs if needed (optional)
        self.DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1', 't')
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'a_default_secret_key')

    def get_connection_params(self):
        """Returns a dictionary suitable for mysql.connector.connect()"""
        params = {
            'host': os.getenv('DB_HOST', 'localhost'),  
            'user': os.getenv('DB_USER'), 
            'password': os.getenv('DB_PASSWORD'),  
            'database': os.getenv('DB_NAME'),  
            'port': int(os.getenv('DB_PORT', 3306)),  
            'ssl_ca': os.getenv('SSL_CA_PATH') 
        }
        
        if self.SSL_CA_PATH:
            params['ssl_ca'] = self.SSL_CA_PATH
            params['ssl_verify_cert'] = True
        
        return params


