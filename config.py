import os
from dotenv import load_dotenv

class Config:
    def __init__(self, host, user, password, database, port, ssl_ca):
        self.DB_HOST = host
        self.DB_USER = user
        self.DB_PASSWORD = password
        self.DB_NAME = database
        self.DB_PORT = port
        self.SSL_CA_PATH = ssl_ca
    
    @classmethod
    def from_env(cls):
        load_dotenv('.env')
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")
        port = os.getenv("DB_PORT")
        ssl_ca = os.getenv("SSL_CA_PATH")
        
        return cls(host, user, password, database, port, ssl_ca)

    
    