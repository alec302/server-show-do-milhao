# app/__init__.py
from flask import Flask
from .config import Config
from .alunos import aluno_bp
from .professores import professor_bp
from .turmas import turmas_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)       
    app.register_blueprint(aluno_bp, url_prefix="/alunos")
    app.register_blueprint(professor_bp, url_prefix="/professores")
    app.register_blueprint(turmas_bp, url_prefix="/turmas")
    return app
