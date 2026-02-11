"""
Script para verificar quais modelos e serviços do Gemini estão disponíveis
com a API key configurada no arquivo .env
"""

import os
from dotenv import load_dotenv
from google import genai

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da API do Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("[ERRO] GEMINI_API_KEY nao encontrada no arquivo .env")
    print("Certifique-se de que o arquivo .env existe e contem: GEMINI_API_KEY=sua_chave_aqui")
    exit(1)

print("=" * 70)
print("Verificacao de Servicos do Gemini (google.genai SDK)")
print("=" * 70)
print()
print(f"[OK] API Key encontrada: {GEMINI_API_KEY[:10]}...{GEMINI_API_KEY[-4:]}")
print()

# Configura a API
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("[OK] Cliente configurado com sucesso")
except Exception as e:
    print(f"[ERRO] Erro ao configurar Cliente: {e}")
    exit(1)

print()
print("-" * 70)
print("1. Listando modelos disponíveis...")
print("-" * 70)
print()

try:
    # Lista todos os modelos disponíveis
    # Pager for list_models
    modelos_disponiveis = []
    modelos_geracao = []
    
    # The new SDK list methods returns a pager. 
    # We iterate through it.
    for modelo in client.models.list():
        nome = modelo.name
        # Check supported methods if available in the object property
        # The new SDK model object structure depends on the version.
        # usually it has supported_generation_methods
        
        metodos_suportados = getattr(modelo, 'supported_generation_methods', [])
        
        modelos_disponiveis.append({
            'nome': nome,
            'metodos': metodos_suportados
        })
        
        # Verifica se suporta generateContent
        if 'generateContent' in metodos_suportados:
            modelos_geracao.append(nome)
    
    print(f"Total de modelos encontrados: {len(modelos_disponiveis)}")
    print()
    
    if modelos_geracao:
        print("[OK] Modelos que suportam 'generateContent' (podem ser usados):")
        print()
        for modelo_nome in modelos_geracao:
            # Extrai apenas o nome do modelo (sem o prefixo 'models/')
            nome_limpo = modelo_nome.replace('models/', '')
            print(f"  - {nome_limpo}")
        print()
    else:
        print("[AVISO] Nenhum modelo encontrado que suporta 'generateContent' (ou propriedade não disponível)")
        # Fallback: list all names if supported_generation_methods is empty
        if not modelos_geracao and modelos_disponiveis:
             print("Listando todos os modelos (filtro de método não aplicável):")
             for m in modelos_disponiveis:
                 print(f" - {m['nome']}")
        print()
    
    print("-" * 70)
    print("2. Testando modelos específicos...")
    print("-" * 70)
    print()
    
    # Modelos para testar
    modelos_para_testar = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-2.0-flash', # Trying 2.0-flash as it is the new standard
        'gemini-2.0-flash-exp',
        'gemini-2.5-flash', # Testing the one used in app.py
    ]
    
    modelos_funcionando = []
    modelos_erro = []
    
    for modelo_nome in modelos_para_testar:
        try:
            # Tenta gerar uma resposta simples para verificar se funciona
            response = client.models.generate_content(
                model=modelo_nome,
                contents="Teste"
            )
            modelos_funcionando.append(modelo_nome)
            print(f"  [OK] {modelo_nome}: FUNCIONANDO")
        except Exception as e:
            modelos_erro.append((modelo_nome, str(e)))
            print(f"  [ERRO] {modelo_nome}: ERRO - {str(e)[:60]}...")
    
    print()
    print("-" * 70)
    print("3. Resumo")
    print("-" * 70)
    print()
    
    if modelos_funcionando:
        print("[OK] Modelos que funcionam com sua API key:")
        for modelo in modelos_funcionando:
            print(f"   - {modelo}")
        print()
    else:
        print("[AVISO] Nenhum modelo testado funcionou. Verifique sua API key.")
    
except Exception as e:
    print(f"[ERRO] Erro ao listar/testar modelos: {e}")

print()
print("=" * 70)
print("Verificação concluída!")
print("=" * 70)
