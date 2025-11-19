"""Entrypoint WSGI mínimo para PythonAnywhere.

Este arquivo importa a instância `app` definida em `app.py`
e a expõe como `application`, que é o nome esperado pelo WSGI.

Coloque este arquivo na raiz do projeto (já está aqui) e aponte
o WSGI file do PythonAnywhere para `flask_app.application`.
"""
import os
import sys

# Garante que o diretório do projeto esteja no sys.path
PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))
if PROJECT_HOME not in sys.path:
    sys.path.insert(0, PROJECT_HOME)

# Importa a app Flask do arquivo app.py e a expõe como `application`
from app import app as application
