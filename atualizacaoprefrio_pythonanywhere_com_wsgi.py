"""
Arquivo WSGI para PythonAnywhere
Configurado para o usuário: atualizacaoprefrio
"""

import sys
import os


# Diretório do projeto (ajustado para conter a pasta ServicosClean)
project_home = '/home/atualizacaoprefrio/ServicosClean'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Carrega variáveis de ambiente do projeto, se existir
from dotenv import load_dotenv
env_path = os.path.join(project_home, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Importa a aplicação WSGI. Primeiro tenta `flask_app.application` (mais explícito),
# senão faz fallback para `app.app` para compatibilidade.
try:
    from flask_app import application
except Exception:
    from app import app as application

if __name__ == "__main__":
    application.run()
