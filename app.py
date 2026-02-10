"""
Aplicação Flask para processar descrições de serviços
utilizando as regras do arquivo limpezaservicos.mdc e a API do Gemini.
"""

import os
import json
import re
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da API do Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("AVISO: GEMINI_API_KEY não encontrada no arquivo .env")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Cria a aplicação Flask
app = Flask(__name__)

# Caminho do arquivo de regras




def carregar_prompt_arquivo(tipo):
    """
    Carrega o prompt do arquivo .txt correspondente na pasta prompts/
    """
    try:
        arquivo = Path(f'prompts/{tipo}.txt')
        if not arquivo.exists():
            raise FileNotFoundError(f"Arquivo de prompt não encontrado: {arquivo}")
            
        with open(arquivo, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        raise Exception(f"Erro ao carregar prompt de {tipo}: {str(e)}")


def criar_prompt(tipo, texto_entrada):
    """
    Cria o prompt apropriado com base no tipo (servico ou informacao).
    Lê o arquivo de template em prompts/{tipo}.txt e injeta o texto de entrada.
    """
    regras = carregar_prompt_arquivo(tipo)
    
    if tipo == 'informacao':
        prompt = f"""{regras}

---

## Conteúdo a Processar

**Texto de entrada:**

{texto_entrada}

---

## Instruções de Saída

Retorne APENAS um JSON com os seguintes campos (use os nomes exatos das chaves):

- `o_que_e`: string (Markdown)
- `como_funciona`: string (Markdown)
- `publico_alvo`: string (Markdown)
- `informacoes_importantes`: string (Markdown)

Se uma informação não estiver disponível, retorne string vazia.
"""
    else: # tipo == 'servico' (padrão)
        prompt = f"""{regras}

---

## PROMPT PRINCIPAL - PADRONIZAÇÃO DE SERVIÇOS

Siga a estrutura definida nas regras acima para padronizar o serviço.

---

## Serviço a Processar

**Texto de entrada (texto livre):**

{texto_entrada}

---

## Instruções

Analise o texto livre acima e extraia/processe as informações para criar uma descrição completa.

Siga TODAS as regras especificadas.

Retorne APENAS um JSON com os seguintes campos:
- `descricao_resumida`
- `descricao_completa`
- `servico_nao_cobre`
- `tempo_atendimento`
- `custo`
- `resultado_solicitacao`
- `documentos_necessarios`
- `instrucoes_solicitante`
- `canais_digitais`
- `canais_presenciais`
- `legislacao_relacionada`
"""
    return prompt


def processar_com_gemini(prompt):
    """
    Processa o prompt usando a API do Gemini.
    """
    try:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não configurada")
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        texto_resposta = response.text.strip()
        
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', texto_resposta, re.DOTALL)
        if json_match:
            texto_resposta = json_match.group(1)
        else:
            json_match = re.search(r'\{.*?\}', texto_resposta, re.DOTALL)
            if json_match:
                texto_resposta = json_match.group(0)
        
        resultado = json.loads(texto_resposta)
        return resultado
        
    except json.JSONDecodeError as e:
        # Se falhar o parse, tenta retornar um erro estruturado ou o texto cru em um campo 'erro_parse'
        raise Exception(f"Erro ao fazer parse do JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Erro ao processar com Gemini: {str(e)}")


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/servicos')
def servicos():
    """Página de serviços"""
    return render_template('servicos.html')


@app.route('/informacao')
def informacao():
    """Página de informação"""
    return render_template('informacao.html')


@app.route('/processar', methods=['POST'])
def processar():
    """Endpoint para processar o texto"""
    try:
        data = request.get_json()
        texto_entrada = data.get('texto', '')
        tipo = data.get('tipo', 'servico') # 'servico' ou 'informacao'
        
        if not texto_entrada.strip():
            return jsonify({
                'sucesso': False,
                'erro': 'Nenhum texto foi fornecido'
            }), 400
        
        # Cria o prompt apropriado
        prompt = criar_prompt(tipo, texto_entrada)
        
        # Processa com Gemini
        resultado = processar_com_gemini(prompt)

        # Garante que retornamos um dicionário
        if not isinstance(resultado, dict):
            raise Exception('Resposta do modelo não veio como JSON/dicionário')

        # Normaliza campos dependendo do tipo
        if tipo == 'informacao':
            campos = ['o_que_e', 'como_funciona', 'publico_alvo', 'informacoes_importantes']
        else:
            campos = [
                'descricao_resumida', 'descricao_completa', 'servico_nao_cobre',
                'tempo_atendimento', 'custo', 'resultado_solicitacao',
                'documentos_necessarios', 'instrucoes_solicitante',
                'canais_digitais', 'canais_presenciais', 'legislacao_relacionada'
            ]
            
        for c in campos:
            if c not in resultado:
                resultado[c] = ''

        return jsonify({
            'sucesso': True,
            'resultado': resultado
        })
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)

