#!/usr/bin/env python3
"""
Script para testar a API do ContentFlow AI
"""

import requests
import json

# URL base da API (altere conforme necessário)
BASE_URL = "http://localhost:5000"

def test_health():
    """Testa health check"""
    print("🔍 Testando Health Check...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    print()

def test_register():
    """Testa registro de usuário"""
    print("👤 Testando Registro...")
    data = {
        "username": "teste_user",
        "email": "teste@contentflow.ai",
        "password": "12345678",
        "full_name": "Usuário de Teste"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Resposta: {result}")
    
    if response.status_code == 201:
        return result.get('token')
    print()
    return None

def test_login():
    """Testa login"""
    print("🔐 Testando Login...")
    data = {
        "username": "teste_user",
        "password": "12345678"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Resposta: {result}")
    
    if response.status_code == 200:
        return result.get('token')
    print()
    return None

def test_generate_caption(token):
    """Testa geração de legenda"""
    print("📝 Testando Geração de Legenda...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "topic": "Dicas de produtividade para trabalho remoto",
        "platform": "instagram",
        "tone": "casual"
    }
    
    response = requests.post(f"{BASE_URL}/api/content/generate/caption", 
                           json=data, headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Legenda gerada: {result.get('caption', 'Erro')[:100]}...")
    print()

def test_generate_ideas(token):
    """Testa geração de ideias"""
    print("💡 Testando Geração de Ideias...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "keywords": "produtividade, trabalho remoto, organização"
    }
    
    response = requests.post(f"{BASE_URL}/api/content/generate/ideas", 
                           json=data, headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    ideas = result.get('ideas', [])
    print(f"Ideias geradas: {len(ideas)} ideias")
    if ideas:
        print(f"Primeira ideia: {ideas[0].get('title', 'N/A')}")
    print()

def test_generate_hashtags(token):
    """Testa geração de hashtags"""
    print("#️⃣ Testando Geração de Hashtags...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "content": "Dicas de produtividade para trabalho remoto",
        "platform": "instagram"
    }
    
    response = requests.post(f"{BASE_URL}/api/content/generate/hashtags", 
                           json=data, headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    hashtags = result.get('hashtags', [])
    print(f"Hashtags geradas: {len(hashtags)} hashtags")
    print(f"Primeiras 5: {hashtags[:5]}")
    print()

def test_profile(token):
    """Testa perfil do usuário"""
    print("👤 Testando Perfil...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/api/user/profile", headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Usuário: {result.get('username', 'N/A')}")
    print(f"Uso mensal: {result.get('monthly_usage', 0)}/{result.get('usage_limit', 0)}")
    print()

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da API ContentFlow AI\n")
    
    # Health check
    test_health()
    
    # Registro (pode falhar se usuário já existe)
    token = test_register()
    
    # Login
    if not token:
        token = test_login()
    
    if not token:
        print("❌ Não foi possível obter token. Parando testes.")
        return
    
    print(f"✅ Token obtido: {token[:20]}...\n")
    
    # Testes com autenticação
    test_generate_caption(token)
    test_generate_ideas(token)
    test_generate_hashtags(token)
    test_profile(token)
    
    print("✅ Todos os testes concluídos!")

if __name__ == "__main__":
    main()

