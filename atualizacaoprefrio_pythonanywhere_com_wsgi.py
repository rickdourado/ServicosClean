"""
Arquivo WSGI para PythonAnywhere
Configurado para o usuário: atualizacaoprefrio
"""

import sys
import os

# Adiciona o caminho do projeto
path = '/home/atualizacaoprefrio'
if path not in sys.path:
    sys.path.insert(0, path)

# Carrega variáveis de ambiente
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

# Importa a aplicação
from app import app as application

if __name__ == "__main__":
    application.run()
