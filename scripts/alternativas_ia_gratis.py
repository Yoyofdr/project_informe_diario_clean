#!/usr/bin/env python
"""
Script para configurar alternativas gratuitas de IA
"""
import os
import requests
from dotenv import load_dotenv

def verificar_apis():
    """Verifica el estado de diferentes APIs gratuitas"""
    load_dotenv()
    
    print("=== ALTERNATIVAS GRATUITAS DE IA ===\n")
    
    # 1. Gemini
    print("1. GOOGLE GEMINI (gemini-1.5-flash)")
    print("   - Límite: 50 requests/día gratis")
    print("   - Obtener en: https://makersuite.google.com/app/apikey")
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if gemini_key:
        print(f"   ✓ Configurada: {gemini_key[:10]}...")
    else:
        print("   ✗ No configurada")
    
    # 2. Groq
    print("\n2. GROQ (mixtral-8x7b)")
    print("   - Límite: 30 requests/minuto gratis")
    print("   - Obtener en: https://console.groq.com/keys")
    groq_key = os.environ.get('GROQ_API_KEY')
    if groq_key:
        print(f"   ✓ Configurada: {groq_key[:10]}...")
    else:
        print("   ✗ No configurada")
    
    # 3. Together AI
    print("\n3. TOGETHER AI")
    print("   - Límite: $25 créditos gratis")
    print("   - Obtener en: https://api.together.xyz/")
    together_key = os.environ.get('TOGETHER_API_KEY')
    if together_key:
        print(f"   ✓ Configurada: {together_key[:10]}...")
    else:
        print("   ✗ No configurada")
    
    # 4. Hugging Face
    print("\n4. HUGGING FACE")
    print("   - Límite: Generoso para modelos pequeños")
    print("   - Obtener en: https://huggingface.co/settings/tokens")
    hf_key = os.environ.get('HF_API_TOKEN')
    if hf_key:
        print(f"   ✓ Configurada: {hf_key[:10]}...")
    else:
        print("   ✗ No configurada")
    
    # 5. Cohere
    print("\n5. COHERE")
    print("   - Límite: 1000 requests/mes gratis")
    print("   - Obtener en: https://dashboard.cohere.com/api-keys")
    cohere_key = os.environ.get('COHERE_API_KEY')
    if cohere_key:
        print(f"   ✓ Configurada: {cohere_key[:10]}...")
    else:
        print("   ✗ No configurada")
    
    print("\n=== RECOMENDACIONES ===")
    print("1. Usar Groq como primera opción (30 req/min es GRATIS y suficiente)")
    print("2. Crear múltiples cuentas de Google con diferentes emails")
    print("3. Rotar entre APIs según disponibilidad")
    print("4. Ya tenemos implementado el soporte para Groq!")
    
    print("\n🎯 RECOMENDACIÓN PRINCIPAL:")
    print("   Ejecuta: python configurar_groq.py")
    print("   Groq es la mejor opción gratuita para tu caso de uso")
    
    print("\n=== CONFIGURACIÓN ===")
    print("Agrega las API keys al archivo .env:")
    print("GEMINI_API_KEY=...")
    print("GROQ_API_KEY=...")
    print("TOGETHER_API_KEY=...")
    print("COHERE_API_KEY=...")
    print("HF_API_TOKEN=...")

def test_groq():
    """Prueba rápida de Groq API"""
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("\nGroq API key no configurada")
        return
    
    print("\n=== PROBANDO GROQ API ===")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "user", "content": "Di 'funciona' si puedes leer esto"}
        ],
        "temperature": 0.1,
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Groq funciona: {result['choices'][0]['message']['content']}")
        else:
            print(f"✗ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    verificar_apis()
    test_groq()