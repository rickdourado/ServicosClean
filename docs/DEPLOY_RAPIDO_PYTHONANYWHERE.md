# Guia Rápido de Deploy - PythonAnywhere

## Configuração para: atualizacaoprefrio

### 1. Upload dos Arquivos

Faça upload dos seguintes arquivos para `/home/atualizacaoprefrio/`:

```
/home/atualizacaoprefrio/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── .cursor/
    └── rules/
        └── limpezaservicos.mdc
```

### 2. Criar arquivo .env

No console Bash do PythonAnywhere:

```bash
cd /home/atualizacaoprefrio
nano .env
```

Adicione:
```
GEMINI_API_KEY=sua_chave_api_aqui
```

Salve: Ctrl+X → Y → Enter

### 3. Instalar Dependências

```bash
cd /home/atualizacaoprefrio
pip3 install --user -r requirements.txt
```

### 4. Configurar WSGI

Edite o arquivo: `/var/www/atualizacaoprefrio_pythonanywhere_com_wsgi.py`

Cole este conteúdo:

```python
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
```

### 5. Configurar Static Files

No painel **Web** do PythonAnywhere:

- **URL:** `/static/`
- **Directory:** `/home/atualizacaoprefrio/static/`

### 6. Reload

Clique em **Reload** no painel Web.

### 7. Testar

Acesse: `https://atualizacaoprefrio.pythonanywhere.com`

## Checklist

- [ ] Arquivos enviados para `/home/atualizacaoprefrio/`
- [ ] Arquivo `.env` criado com GEMINI_API_KEY
- [ ] Dependências instaladas
- [ ] WSGI configurado em `/var/www/atualizacaoprefrio_pythonanywhere_com_wsgi.py`
- [ ] Static files configurados
- [ ] Aplicação recarregada
- [ ] Teste realizado

## Troubleshooting Rápido

**Erro 500:** Verifique os logs em Web → Error log

**Module not found:** Execute novamente `pip3 install --user -r requirements.txt`

**GEMINI_API_KEY não encontrada:** Verifique se o `.env` está em `/home/atualizacaoprefrio/.env`

**Static files não carregam:** Confirme o caminho `/home/atualizacaoprefrio/static/` no painel Web
