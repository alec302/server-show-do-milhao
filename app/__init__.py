# app/__init__.py
from flask import Flask
from .config import Config
from .alunos import aluno_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)       # puxa todos os atributos UPPERCASE
    app.register_blueprint(aluno_bp, url_prefix="/alunos")
    return app
