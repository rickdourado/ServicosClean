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
RULES_FILE = Path('.cursor/rules/limpezaservicos.mdc')


def carregar_regras():
    """Carrega as regras do arquivo limpezaservicos.mdc"""
    try:
        with open(RULES_FILE, 'r', encoding='utf-8') as f:
            # Remove o frontmatter (linhas que começam com ---)
            content = f.read()
            # Remove o frontmatter YAML se existir
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2].strip()
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de regras não encontrado: {RULES_FILE}")
    except Exception as e:
        raise Exception(f"Erro ao carregar regras: {str(e)}")


def carregar_estrutura_principal():
    """
    Carrega a estrutura principal do prompt (linhas 65-79 do limpezaservicos.mdc).
    Esta é a estrutura padrão que deve ser seguida para padronizar todos os serviços.
    
    Referência: @limpezaservicos.mdc (65-79)
    As linhas 65-79 referem-se ao arquivo original completo (incluindo frontmatter).
    """
    try:
        with open(RULES_FILE, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
            # Linhas 65-79 do arquivo original (índices 64-78, pois começa em 0)
            # Contamos do início do arquivo, incluindo frontmatter
            linha_inicio = 64  # Linha 65 do arquivo (índice 64)
            linha_fim = 79      # Linha 79 do arquivo (índice 78, mas vamos até 79)
            
            # Garante que não ultrapassa o tamanho do arquivo
            if linha_fim > len(linhas):
                linha_fim = len(linhas)
            if linha_inicio >= len(linhas):
                raise Exception(f"Linha 65 não existe no arquivo (arquivo tem {len(linhas)} linhas)")
            
            estrutura = ''.join(linhas[linha_inicio:linha_fim])
            return estrutura.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de regras não encontrado: {RULES_FILE}")
    except Exception as e:
        raise Exception(f"Erro ao carregar estrutura principal: {str(e)}")


def criar_prompt(regras, texto_entrada):
    """
    Cria o prompt para o Gemini com as regras e o texto de entrada livre.
    
    O PROMPT PRINCIPAL é baseado na estrutura das linhas 65-79 do arquivo
    limpezaservicos.mdc, que define o formato padrão para padronizar todos os serviços.
    
    O Gemini deve processar o texto livre e retornar formatado seguindo essa estrutura.
    """
    # Carrega a estrutura principal (linhas 65-79)
    estrutura_principal = carregar_estrutura_principal()
    
    prompt = f"""{regras}

---

## ⚠️ LIMITAÇÃO CRÍTICA - Seção "O que é"

A seção "## O que é" DEVE ter EXATAMENTE:
- MÁXIMO de 1-2 parágrafos
- Cada parágrafo com MÁXIMO de 3-4 linhas
- Seja conciso e objetivo
- NÃO exceda esse limite mesmo que o texto de entrada seja extenso

---

## PROMPT PRINCIPAL - Estrutura Padrão (limpezaservicos.mdc linhas 65-79)

Esta é a estrutura PRINCIPAL que deve ser seguida para padronizar TODOS os serviços:

{estrutura_principal}

---

## Serviço a Processar

**Texto de entrada (texto livre):**

{texto_entrada}

---

## Instruções

Analise o texto livre acima e extraia/processe as informações para criar uma descrição completa.

SIGA EXATAMENTE a estrutura principal definida acima (linhas 65-79 do limpezaservicos.mdc), transformando o texto livre em uma saída padronizada com as três seções:

1. **## O que é** 
   - **LIMITE OBRIGATÓRIO: MÁXIMO de 1-2 parágrafos de 2-3 linhas cada**
   - Seja conciso e direto
   - NÃO exceda 2 parágrafos
  - Esse campo NÃO pode ficar em branco. 
   - Cada parágrafo deve ter no máximo 3-4 linhas
   - Explicação clara e objetiva do serviço

2. **## Para que serve**
   - **LIMITE OBRIGATÓRIO: MÁXIMO de 1 parágrafo de 2-3 linhas cada**
   - NÃO exceda 1 parágrafo
   - Seja OBJETIVO e centrado na ENTREGA que o serviço proporciona
   - Esse campo NÃO pode ficar em branco. 
   - NÃO seja genérico como "visa melhorar" ou "busca garantir"
   - Exemplos: "Fiscalização efetiva das frotas de ônibus", "Coleta/Remoção dos entulhos"

3. **## Quem pode solicitar** 
   - **LIMITE OBRIGATÓRIO: MÁXIMO de 1 parágrafo de 2-3 linhas cada**
   - NÃO exceda 1 parágrafo
   - Esse campo NÃO pode ficar em branco. Sempre deve ter alguém pra solicitar. Caso não esteja no documento, o cidadão carioca será utilizad.
   - Público-alvo e requisitos em parágrafos claros

**ATENÇÃO ESPECIAL:** A seção "O que é" DEVE ser curta e objetiva. Se o texto de entrada for extenso, extraia apenas as informações essenciais e resuma em no máximo 2 parágrafos de 3-4 linhas cada. NÃO inclua todos os detalhes, apenas o essencial para explicar o que é o serviço.

Siga TODAS as regras especificadas no início deste prompt, mas use a estrutura principal acima como referência PRINCIPAL para o formato de saída.

Retorne APENAS o JSON estruturado com o campo "descricao_completa" formatado em Markdown conforme a estrutura principal.
"""
    return prompt


def processar_com_gemini(prompt):
    """
    Processa o prompt usando a API do Gemini.
    """
    try:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não configurada")
        
        # Usa gemini-2.5-flash (modelo mais recente e disponível)
        # Modelos disponíveis: gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        # Extrai o texto da resposta
        texto_resposta = response.text.strip()
        
        # Tenta extrair JSON da resposta (pode vir com markdown code blocks)
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', texto_resposta, re.DOTALL)
        if json_match:
            texto_resposta = json_match.group(1)
        else:
            # Tenta encontrar JSON direto
            json_match = re.search(r'\{.*?\}', texto_resposta, re.DOTALL)
            if json_match:
                texto_resposta = json_match.group(0)
        
        # Parse do JSON
        resultado = json.loads(texto_resposta)
        return resultado
        
    except json.JSONDecodeError as e:
        raise Exception(f"Erro ao fazer parse do JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Erro ao processar com Gemini: {str(e)}")


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/processar', methods=['POST'])
def processar():
    """Endpoint para processar o texto"""
    try:
        data = request.get_json()
        texto_entrada = data.get('texto', '')
        
        if not texto_entrada.strip():
            return jsonify({
                'sucesso': False,
                'erro': 'Nenhum texto foi fornecido'
            }), 400
        
        # Carrega as regras
        regras = carregar_regras()
        
        # Cria o prompt com o texto livre (sem extrair seções)
        prompt = criar_prompt(regras, texto_entrada)
        
        # Processa com Gemini
        resultado = processar_com_gemini(prompt)
        
        return jsonify({
            'sucesso': True,
            'resultado': resultado.get('descricao_completa', '')
        })
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)

