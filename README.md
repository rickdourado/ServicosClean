# ServiçosClean

Projeto para processamento e limpeza de descrições de serviços e informações utilizando IA (Gemini).

## Estrutura do Projeto

```
ServicosClean/
├── app.py                   # Aplicação Flask principal
├── templates/              # Templates HTML
│   ├── index.html          # Interface web principal
│   ├── servicos.html       # Interface para serviços
│   └── informacao.html     # Interface para informações
├── static/                 # Arquivos estáticos
│   ├── css/
│   │   └── style.css       # Estilos da aplicação
│   └── js/
│       └── main.js         # JavaScript da aplicação
├── docs/                    # Documentação do projeto
│   ├── changelogs/          # Changelogs diários (formato: AAAA-MM-DD.md)
│   ├── DEPLOY_PYTHONANYWHERE.md  # Guia de deploy
│   ├── LimpezaServicos.md   # Documentação das regras de limpeza
│   └── README_TESTE.md      # Documentação (Legado)
├── exemplos/                # Arquivos de exemplo
│   └── exemplo_entrada.txt  # Exemplo de entrada
├── prompts/                 # Prompts de sistema para a IA
│   ├── servico.md          # Prompt para serviços
│   └── informacao.md       # Prompt para informações
├── pyproject.toml           # Configuração do projeto e dependências (uv)
├── uv.lock                  # Arquivo de trava das dependências (uv)
├── .env                     # Variáveis de ambiente (não versionado)
└── README.md               # Este arquivo
```

## Instalação

Este projeto utiliza o [uv](https://github.com/astral-sh/uv) para gerenciamento de dependências.

1.  Certifique-se de ter o `uv` instalado.
2.  Instale as dependências executando:

```bash
uv sync
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com sua chave da API do Google Gemini:

```ini
GEMINI_API_KEY=sua_chave_api_aqui
GEMINI_MODEL=gemini-2.5-flash
```

## Uso

### Aplicação Web (Flask)

Para executar a aplicação web localmente:

```bash
uv run app.py
```

Ou, se você já estiver com o ambiente virtual ativado:

```bash
python app.py
```

Acesse `http://localhost:5000` no navegador.

A aplicação oferece duas funcionalidades principais:
1.  **Limpeza de Serviços:** Padronização e estruturação de descrições de serviços públicos.
2.  **Limpeza de Informações:** Criação de scripts informativos claros e diretos para o cidadão.

### Deploy no PythonAnywhere

Para fazer deploy da aplicação no PythonAnywhere, consulte o [guia completo](docs/DEPLOY_PYTHONANYWHERE.md).

## Documentação

- [Regras de Limpeza de Serviços](docs/LimpezaServicos.md)

## Changelog

Os changelogs são mantidos na pasta `docs/changelogs/` com formato `AAAA-MM-DD.md`.
