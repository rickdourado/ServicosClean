# ServiçosClean

Projeto para processamento e limpeza de descrições de serviços utilizando IA (Gemini).

## Estrutura do Projeto

```
ServicosClean/
├── app.py                   # Aplicação Flask principal
├── templates/              # Templates HTML
│   └── index.html          # Interface web
├── static/                 # Arquivos estáticos
│   ├── css/
│   │   └── style.css       # Estilos da aplicação
│   └── js/
│       └── main.js         # JavaScript da aplicação
├── docs/                    # Documentação do projeto
│   ├── changelogs/          # Changelogs diários (formato: AAAA-MM-DD.md)
│   ├── DEPLOY_PYTHONANYWHERE.md  # Guia de deploy
│   ├── LimpezaServicos.md   # Documentação das regras de limpeza
│   └── README_TESTE.md      # Documentação do script de teste
├── exemplos/                # Arquivos de exemplo
│   └── exemplo_entrada.txt  # Exemplo de entrada para o script
├── .cursor/                 # Configurações do Cursor
│   └── rules/              # Regras do projeto
├── teste_descricao_completa.py  # Script CLI de teste
├── wsgi.py.example          # Exemplo de arquivo WSGI para PythonAnywhere
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com:

```
GEMINI_API_KEY=sua_chave_api_aqui
```

## Uso

### Aplicação Web (Flask)

Execute a aplicação Flask localmente:

```bash
python app.py
```

Acesse `http://localhost:5000` no navegador.

### Script de Teste (CLI)

O script `teste_descricao_completa.py` processa descrições de serviços seguindo as regras definidas em `.cursor/rules/limpezaservicos.mdc`.

**Modo interativo:**
```bash
python teste_descricao_completa.py
```

**Usando arquivo de exemplo:**
```bash
python teste_descricao_completa.py exemplos/exemplo_entrada.txt
```

Para mais detalhes, consulte a [documentação completa](docs/README_TESTE.md).

### Deploy no PythonAnywhere

Para fazer deploy da aplicação no PythonAnywhere, consulte o [guia completo](docs/DEPLOY_PYTHONANYWHERE.md).

## Documentação

- [Regras de Limpeza de Serviços](docs/LimpezaServicos.md)
- [Documentação do Script de Teste](docs/README_TESTE.md)

## Changelog

Os changelogs são mantidos na pasta `docs/changelogs/` com formato `AAAA-MM-DD.md`.

