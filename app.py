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
    Carrega a estrutura principal do prompt (limpezaservicos.mdc).
    Esta é a estrutura padrão que deve ser seguida para padronizar todos os serviços.
    
    Referência: @limpezaservicos.mdc 
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
    
    O PROMPT PRINCIPAL é baseado na estrutura do arquivo
    limpezaservicos.mdc, que define o formato padrão para padronizar todos os serviços.
    
    O Gemini deve processar o texto livre e retornar formatado seguindo essa estrutura.
    """
    # Carrega a estrutura principal (linhas 65-79)
    estrutura_principal = carregar_estrutura_principal()
    
    prompt = f"""{regras}

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

Siga TODAS as regras especificadas no início deste prompt, mas use a estrutura principal acima como referência PRINCIPAL para o formato de saída.

Retorne APENAS um JSON com os seguintes campos (use os nomes exatos das chaves):

- `descricao_resumida`: string (resumo curto, 1-2 frases)
- `descricao_completa`: string (Markdown com as 3 seções: "O que é", "Para que serve", "Quem pode solicitar")
- `servico_nao_cobre`: string ou lista Markdown (limitações)
- `tempo_atendimento`: string (prazos, ex: "72 horas", "até 20 dias")
- `custo`: string (valores ou "isento"/"gratuito")
- `resultado_solicitacao`: string (resultado/entregáveis esperados)
- `documentos_necessarios`: string ou Markdown list (lista de documentos)
- `instrucoes_solicitante`: string ou Markdown (instruções passo a passo)
- `canais_digitais`: string ou Markdown (URLs / plataformas)
- `canais_presenciais`: string ou Markdown (endereços e horários)
- `legislacao_relacionada`: string ou Markdown (referências legais)

        Cada campo deve ser preenchido — se uma informação não estiver disponível no texto de entrada, retorne uma string vazia para esse campo. Retorne o JSON puro (pode estar dentro de um bloco de código ```json```).
        
        ---
        
        Regras específicas por campo (siga rigorosamente):
        
        descricao_resumida
        - Objetivo: Resumo curto e direto do serviço em 1-2 frases.
        - Fontes: descricao, detalhes.
        - Regras: Texto sucinto; sem listas/seções; linguagem simples; sem prazos/documentos/canais/legislação.
        
        descricao_completa
        - Objetivo: Texto detalhado e estruturado em Markdown com as seções "O que é", "Para que serve", "Quem pode solicitar".
        - Fontes: descricao, detalhes, como_funciona, informacoes.
        - Regras: Preservar toda a informação do original; manter prazos, exceções e observações; usar apenas as 3 seções; não incluir instruções/documentos/canais/legislação.
        - Limites por subseção: "O que é" (1-2 parágrafos, 3-4 linhas cada), "Para que serve" (1 parágrafo, 2-3 linhas), "Quem pode solicitar" (1 parágrafo, 2-3 linhas).
        - Regras do campo `descricao_completa` (composto pelas 3 subseções abaixo):

            1. **## O que é**
                - **LIMITE OBRIGATÓRIO:** 1-2 parágrafos, cada um com 3-4 linhas
                - Seja conciso e direto; explicação clara e objetiva do serviço
                - NÃO exceda 2 parágrafos; campo obrigatório (não pode ficar em branco)

            2. **## Para que serve**
                - **LIMITE OBRIGATÓRIO:** 1 parágrafo de 2-3 linhas
                - Seja OBJETIVO e centrado na ENTREGA do serviço
                - NÃO use textos genéricos como "visa melhorar" ou "busca garantir"
                - Exemplos de entrega: "Fiscalização efetiva das frotas de ônibus", "Coleta/Remoção dos entulhos"

            3. **## Quem pode solicitar**
                - **LIMITE OBRIGATÓRIO:** 1 parágrafo de 2-3 linhas
                - Campo obrigatório; sempre deve haver público-alvo
                - Caso não esteja explícito, usar o cidadão carioca como público padrão
                - Descrever público-alvo e requisitos de forma clara

                **ATENÇÃO ESPECIAL:** A seção "O que é" DEVE ser curta e objetiva. Se o texto de entrada for extenso, extraia apenas as informações essenciais e resuma em no máximo 2 parágrafos de 3-4 linhas cada. NÃO inclua todos os detalhes, apenas o essencial para explicar o que é o serviço.
        
        servico_nao_cobre
        - Objetivo: Listar o que o serviço NÃO cobre.
        - Fontes: detalhes, informacoes.
        - Regras: Itens curtos em lista; não misturar com instruções ou documentos.
        
        tempo_atendimento
        - Objetivo: Informar prazo/tempo estimado (ex.: 72 horas, até 20 dias).
        - Fontes: detalhes, informacoes.
        - Regras: Apenas o prazo; discriminar prazos por etapa se existirem; não colocar este conteúdo em descricao_completa.
        
        custo
        - Objetivo: Informar custo/taxa quando aplicável.
        - Fontes: detalhes, informacoes.
        - Regras: Especificar valores e quando são cobrados; se não houver custo, usar "isento" ou "gratuito".
        
        resultado_solicitacao
        - Objetivo: Descrever o resultado esperado após a conclusão (entregáveis/ações concluídas).
        - Fontes: detalhes, informacoes.
        - Regras: Ser objetivo e listar o output final.
        
        documentos_necessarios
        - Objetivo: Listar documentos exigidos.
        - Fontes: detalhes, informacoes.
        - Regras: Lista de itens; incluir somente documentos explicitamente mencionados.
        
        instrucoes_solicitante
        - Objetivo: Instruções passo a passo.
        - Fontes: como_funciona, detalhes.
        - Regras: Permite lista ordenada; não incluir conteúdo de descricao_completa nem legislação.
        
        canais_digitais
        - Objetivo: Canais digitais oficiais (URLs, plataformas, APIs).
        - Fontes: informacoes, detalhes.
        - Regras: Fornecer URLs/identificadores oficiais; não usar links dentro de descricao_completa.
        
        canais_presenciais
        - Objetivo: Locais físicos e horários.
        - Fontes: informacoes, detalhes.
        - Regras: Endereços completos e horários; não colocar endereços em descricao_completa.
        
        legislacao_relacionada
        - Objetivo: Referências legais, decretos ou normas.
        - Fontes: detalhes, informacoes.
        - Regras: Listar leis/decretos com identificação (nº, ano) e breve nota quando necessário; não inserir textos legais longos.
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

        # Garante que retornamos um dicionário com os campos esperados
        if not isinstance(resultado, dict):
            raise Exception('Resposta do modelo não veio como JSON/dicionário')

        # Preenche chaves ausentes com string vazia
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

