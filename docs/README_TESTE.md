# Script de Teste - Descrição Completa de Serviços

Script Python para processar descrições de serviços utilizando as regras do arquivo `limpezaservicos.mdc` e a API do Gemini.

## Pré-requisitos

1. Python 3.7 ou superior
2. API Key do Gemini configurada no arquivo `.env`

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Certifique-se de que o arquivo `.env` existe na raiz do projeto e contém:

```
GEMINI_API_KEY=sua_chave_api_aqui
```

## Uso

### Modo Interativo

Execute o script sem argumentos e digite o texto diretamente:

```bash
python teste_descricao_completa.py
```

Quando executar, você poderá digitar o texto com as seções:
- O que é?
- Para que serve?
- Quem pode solicitar?

Pressione `Ctrl+Z` seguido de `Enter` (Windows) ou `Ctrl+D` (Linux/Mac) para finalizar a entrada.

### Modo Arquivo

Execute o script passando um arquivo de texto como argumento:

```bash
python teste_descricao_completa.py exemplo_entrada.txt
```

## Formato de Entrada

O script aceita texto livre com as seções identificadas pelos títulos:

```
O que é?

[Descrição do serviço]

Para que serve?

[Objetivo e entrega do serviço]

Quem pode solicitar?

[Público-alvo e requisitos]
```

Ou você pode usar variações como:
- `O QUE É?`
- `Para que serve?`
- `QUEM PODE SOLICITAR?`

O script tentará identificar automaticamente as seções mesmo sem os títulos explícitos.

## Saída

O script gera:
1. **Saída no console**: JSON formatado com o campo `descricao_completa`
2. **Arquivo `resultado_descricao_completa.json`**: Resultado salvo em arquivo

## Exemplo

Veja o arquivo `exemplos/exemplo_entrada.txt` para um exemplo de entrada.

Execute:
```bash
python teste_descricao_completa.py exemplos/exemplo_entrada.txt
```

## Estrutura do Resultado

O resultado será um JSON no formato:

```json
{
  "descricao_completa": "## O que é\n\n[Texto formatado em Markdown]\n\n## Para que serve\n\n[Texto formatado em Markdown]\n\n## Quem pode solicitar\n\n[Texto formatado em Markdown]"
}
```

O campo `descricao_completa` conterá o texto formatado em Markdown seguindo todas as regras especificadas no arquivo `limpezaservicos.mdc`.

