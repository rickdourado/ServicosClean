"""
Script para verificar quais modelos e serviços do Gemini estão disponíveis
com a API key configurada no arquivo .env
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da API do Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("[ERRO] GEMINI_API_KEY nao encontrada no arquivo .env")
    print("Certifique-se de que o arquivo .env existe e contem: GEMINI_API_KEY=sua_chave_aqui")
    exit(1)

print("=" * 70)
print("Verificacao de Servicos do Gemini")
print("=" * 70)
print()
print(f"[OK] API Key encontrada: {GEMINI_API_KEY[:10]}...{GEMINI_API_KEY[-4:]}")
print()

# Configura a API
try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("[OK] API configurada com sucesso")
except Exception as e:
    print(f"[ERRO] Erro ao configurar API: {e}")
    exit(1)

print()
print("-" * 70)
print("1. Listando modelos disponíveis...")
print("-" * 70)
print()

try:
    # Lista todos os modelos disponíveis
    modelos = genai.list_models()
    
    modelos_disponiveis = []
    modelos_geracao = []
    
    for modelo in modelos:
        nome = modelo.name
        metodos_suportados = list(modelo.supported_generation_methods)
        
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
        print("[AVISO] Nenhum modelo encontrado que suporta 'generateContent'")
        print()
    
    print("-" * 70)
    print("2. Testando modelos específicos...")
    print("-" * 70)
    print()
    
    # Modelos para testar
    modelos_para_testar = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-1.5-flash-latest',
        'gemini-1.5-pro-latest',
        'gemini-pro',
        'gemini-2.0-flash-exp',
    ]
    
    modelos_funcionando = []
    modelos_erro = []
    
    for modelo_nome in modelos_para_testar:
        try:
            model = genai.GenerativeModel(modelo_nome)
            # Tenta gerar uma resposta simples para verificar se funciona
            response = model.generate_content("Teste")
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
        print(f"[RECOMENDACAO] Use '{modelos_funcionando[0]}' (primeiro da lista)")
    else:
        print("[AVISO] Nenhum modelo testado funcionou. Verifique sua API key.")
    
    print()
    print("-" * 70)
    print("4. Informações detalhadas dos modelos")
    print("-" * 70)
    print()
    
    for modelo_info in modelos_disponiveis[:10]:  # Mostra os primeiros 10
        nome_limpo = modelo_info['nome'].replace('models/', '')
        metodos = ', '.join(modelo_info['metodos'])
        print(f"Modelo: {nome_limpo}")
        print(f"  Métodos suportados: {metodos}")
        print()
    
    if len(modelos_disponiveis) > 10:
        print(f"... e mais {len(modelos_disponiveis) - 10} modelos")
        print()
    
except Exception as e:
    print(f"[ERRO] Erro ao listar modelos: {e}")
    print()
    print("Tentando verificar diretamente...")
    print()
    
    # Tenta testar modelos diretamente
    modelos_para_testar = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-1.5-flash-latest',
        'gemini-1.5-pro-latest',
    ]
    
    for modelo_nome in modelos_para_testar:
        try:
            model = genai.GenerativeModel(modelo_nome)
            response = model.generate_content("Teste")
            print(f"[OK] {modelo_nome}: FUNCIONANDO")
        except Exception as e:
            print(f"[ERRO] {modelo_nome}: {str(e)[:80]}")

print()
print("=" * 70)
print("Verificação concluída!")
print("=" * 70)

