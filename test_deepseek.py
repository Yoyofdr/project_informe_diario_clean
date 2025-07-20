#!/usr/bin/env python
"""
Script para probar DeepSeek API
"""
import os
import requests
from dotenv import load_dotenv

def test_deepseek():
    """Prueba la API de DeepSeek"""
    load_dotenv()
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    
    if not api_key:
        print("❌ DEEPSEEK_API_KEY no configurada")
        return
    
    print("=== PROBANDO DEEPSEEK API ===")
    print(f"API Key: {api_key[:10]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Eres un experto en análisis de normativas chilenas."},
            {"role": "user", "content": "Responde solo con 'funciona' si puedes leer esto"}
        ],
        "temperature": 0.1,
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ DeepSeek funciona correctamente")
            print(f"   Respuesta: {result['choices'][0]['message']['content']}")
            print(f"   Modelo: {result['model']}")
            print(f"   Tokens usados: {result.get('usage', {}).get('total_tokens', 'N/A')}")
            print("\n🎉 ¡DeepSeek está listo para usar en el informe diario!")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def verificar_estado():
    """Verifica el estado de todas las APIs"""
    load_dotenv()
    
    print("\n=== ESTADO DE LAS APIs ===")
    
    deepseek = os.environ.get('DEEPSEEK_API_KEY')
    gemini = os.environ.get('GEMINI_API_KEY')
    groq = os.environ.get('GROQ_API_KEY')
    
    if deepseek:
        print(f"✅ DeepSeek configurado: {deepseek[:10]}...")
    else:
        print("❌ DeepSeek NO configurado")
    
    if gemini:
        print(f"✅ Gemini configurado: {gemini[:15]}...")
    else:
        print("❌ Gemini NO configurado")
        
    if groq:
        print(f"✅ Groq configurado: {groq[:10]}...")
    else:
        print("❌ Groq NO configurado")
    
    print("\n=== PRIORIDAD DE USO ===")
    print("El sistema usará las APIs en este orden:")
    print("1. Groq (si está configurado)")
    print("2. DeepSeek (si está configurado)")
    print("3. Gemini (si está configurado)")
    print("4. Reglas básicas (sin IA)")
    
    if groq:
        print("\n📌 Actualmente usará: Groq")
    elif deepseek:
        print("\n📌 Actualmente usará: DeepSeek")
    elif gemini:
        print("\n📌 Actualmente usará: Gemini")
    else:
        print("\n📌 Actualmente usará: Reglas básicas")

if __name__ == "__main__":
    verificar_estado()
    print("\n")
    test_deepseek()