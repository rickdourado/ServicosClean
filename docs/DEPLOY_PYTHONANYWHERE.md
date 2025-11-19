# Guia de Deploy no PythonAnywhere

Este guia explica como fazer o deploy da aplicação Flask no PythonAnywhere.

## Pré-requisitos

1. Conta no PythonAnywhere (gratuita ou paga)
2. API Key do Gemini configurada

## Passo a Passo

### 1. Preparar o Código

Certifique-se de que todos os arquivos estão organizados:

```
ServicosClean/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── .cursor/
│   └── rules/
│       └── limpezaservicos.mdc
└── .env (não faça upload deste arquivo!)
```

### 2. Fazer Upload dos Arquivos

1. Acesse o **Dashboard** do PythonAnywhere
2. Vá em **Files**
3. Navegue até sua pasta de usuário (geralmente `/home/seuusuario/`)
4. Crie uma pasta para o projeto (ex: `ServicosClean`)
5. Faça upload de todos os arquivos:
   - `app.py`
   - `requirements.txt`
   - `templates/index.html`
   - `static/css/style.css`
   - `static/js/main.js`
   - `.cursor/rules/limpezaservicos.mdc` (crie a estrutura de pastas se necessário)

**⚠️ IMPORTANTE:** NÃO faça upload do arquivo `.env`!

### 3. Configurar Variáveis de Ambiente

1. No PythonAnywhere, vá em **Tasks** → **Always-on task** (ou crie um novo)
2. Ou configure via **Web** → **Web app** → **Static files** e **WSGI configuration file**

**Opção 1: Via Console (Recomendado)**

1. Abra um **Bash console** no PythonAnywhere
2. Navegue até a pasta do projeto:
   ```bash
   cd ~/ServicosClean
   ```
3. Crie o arquivo `.env`:
   ```bash
   nano .env
   ```
4. Adicione sua API key:
   ```
   GEMINI_API_KEY=sua_chave_api_aqui
   ```
5. Salve (Ctrl+X, depois Y, depois Enter)

**Opção 2: Via Interface Web**

1. Vá em **Files**
2. Crie o arquivo `.env` na pasta do projeto
3. Adicione: `GEMINI_API_KEY=sua_chave_api_aqui`

### 4. Instalar Dependências

1. Abra um **Bash console**
2. Navegue até a pasta do projeto:
   ```bash
   cd ~/ServicosClean
   ```
3. Crie um ambiente virtual (recomendado):
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```bash
   pip install --user -r requirements.txt
   ```

### 5. Configurar a Aplicação Web

1. Vá em **Web** no dashboard
2. Clique em **Add a new web app**
3. Escolha **Flask**
4. Selecione **Python 3.10** (ou a versão disponível)
5. Escolha o caminho para o arquivo WSGI

### 6. Configurar o Arquivo WSGI

O arquivo WSGI já está configurado em `atualizacaoprefrio_pythonanywhere_com_wsgi.py`.

**No PythonAnywhere:**

1. Vá em **Web** → **WSGI configuration file**
2. O caminho deve ser: `/var/www/atualizacaoprefrio_pythonanywhere_com_wsgi.py`
3. Copie o conteúdo do arquivo `atualizacaoprefrio_pythonanywhere_com_wsgi.py` do projeto
4. Cole no editor do PythonAnywhere
5. Salve o arquivo

**Conteúdo do arquivo WSGI:**

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

### 7. Configurar Static Files

No painel **Web**, configure os arquivos estáticos:

- **URL:** `/static/`
- **Directory:** `/home/atualizacaoprefrio/static/`

### 8. Reiniciar a Aplicação

1. Vá em **Web**
2. Clique em **Reload** para reiniciar a aplicação

### 9. Testar

Acesse sua URL: `https://atualizacaoprefrio.pythonanywhere.com`

## Estrutura de Arquivos no PythonAnywhere

```
/home/atualizacaoprefrio/
├── app.py
├── requirements.txt
├── .env
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

**Arquivo WSGI (gerenciado pelo PythonAnywhere):**
```
/var/www/atualizacaoprefrio_pythonanywhere_com_wsgi.py
```

## Troubleshooting

### Erro: "Module not found"

- Certifique-se de que instalou todas as dependências
- Verifique se o caminho no WSGI está correto
- Tente usar `pip install --user` se houver problemas de permissão

### Erro: "GEMINI_API_KEY não encontrada"

- Verifique se o arquivo `.env` existe na pasta do projeto
- Confirme que o caminho no WSGI está carregando o `.env` corretamente
- Verifique se a variável está escrita corretamente (sem espaços)

### Erro: "File not found" para limpezaservicos.mdc

- Verifique se o arquivo foi enviado para `.cursor/rules/limpezaservicos.mdc`
- Confirme que o caminho relativo está correto no `app.py`

### Aplicação não carrega

- Verifique os logs em **Web** → **Error log**
- Certifique-se de que reiniciou a aplicação após mudanças
- Verifique se o arquivo WSGI está configurado corretamente

## Limitações da Conta Gratuita

- A aplicação fica inativa após 3 meses sem uso
- Limite de requisições por dia
- Não pode usar HTTPS customizado

## Atualizações Futuras

Para atualizar o código:

1. Faça upload dos arquivos modificados
2. Reinicie a aplicação em **Web** → **Reload**

## Suporte

Para mais informações, consulte a [documentação do PythonAnywhere](https://help.pythonanywhere.com/).

