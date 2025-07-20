#!/usr/bin/env python
"""
Script para configurar Groq API Key
"""
import os
import requests
from dotenv import load_dotenv

def configurar_groq():
    print("=== CONFIGURACIÓN DE GROQ (ALTERNATIVA GRATUITA) ===")
    print("\nGroq ofrece 30 requests por minuto GRATIS")
    print("Perfecto para el informe diario del Diario Oficial")
    
    print("\nPara usar Groq:")
    print("1. Ve a https://console.groq.com/")
    print("2. Crea una cuenta gratuita")
    print("3. Ve a 'API Keys' en el menú")
    print("4. Crea una nueva API key")
    print("5. Copia la API key")
    
    # Verificar si existe .env
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    # Leer contenido actual si existe
    env_content = []
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            env_content = f.readlines()
    
    # Buscar si ya existe GROQ_API_KEY
    groq_exists = False
    for i, line in enumerate(env_content):
        if line.startswith('GROQ_API_KEY='):
            groq_exists = True
            break
    
    if not groq_exists:
        print(f"\nAgregando GROQ_API_KEY al archivo .env...")
        with open(env_path, 'a') as f:
            if env_content and not env_content[-1].endswith('\n'):
                f.write('\n')
            f.write('GROQ_API_KEY=\n')
        print(f"✓ Línea agregada al archivo .env")
    
    print(f"\n📝 INSTRUCCIONES:")
    print(f"1. Abre el archivo: {env_path}")
    print("2. Busca la línea: GROQ_API_KEY=")
    print("3. Agrega tu API key después del signo igual:")
    print("   GROQ_API_KEY=gsk_tu_api_key_aqui")
    print("4. Guarda el archivo")
    
    # Verificar configuración actual
    load_dotenv()
    
    groq_key = os.environ.get('GROQ_API_KEY')
    deepseek_key = os.environ.get('DEEPSEEK_API_KEY')
    gemini_key = os.environ.get('GEMINI_API_KEY')
    
    print("\n=== ESTADO ACTUAL ===")
    if groq_key:
        print(f"✓ Groq API Key configurada: {groq_key[:10]}...")
    else:
        print("✗ Groq API Key NO configurada")
    
    if deepseek_key:
        print(f"✓ DeepSeek API Key configurada: {deepseek_key[:10]}...")
    else:
        print("✗ DeepSeek API Key NO configurada")
    
    if gemini_key:
        print(f"✓ Gemini API Key configurada: {gemini_key[:10]}...")
    else:
        print("✗ Gemini API Key NO configurada")
    
    print("\n=== ORDEN DE PRIORIDAD ===")
    print("El sistema intentará usar las APIs en este orden:")
    print("1. Groq (30 req/min gratis)")
    print("2. DeepSeek (si está configurado)")
    print("3. Gemini (si está configurado)")
    print("4. Reglas básicas (sin IA)")
    
    if groq_key:
        print("\n✅ El sistema usará Groq para evaluar relevancia")
        print("   (30 requests/minuto es suficiente para el informe diario)")
    elif deepseek_key:
        print("\n⚠️  El sistema usará DeepSeek")
    elif gemini_key:
        print("\n⚠️  El sistema usará Gemini (puede tener límites de cuota)")
    else:
        print("\n⚠️  El sistema usará reglas básicas (sin IA)")

def test_groq():
    """Prueba la API de Groq"""
    load_dotenv()
    api_key = os.environ.get('GROQ_API_KEY')
    
    if not api_key:
        print("\n❌ No se puede probar: GROQ_API_KEY no configurada")
        return
    
    print("\n=== PROBANDO GROQ API ===")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "user", "content": "Responde solo con la palabra 'funciona' si puedes leer esto"}
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
            print(f"✅ Groq funciona correctamente")
            print(f"   Respuesta: {result['choices'][0]['message']['content']}")
            print(f"   Modelo: {result['model']}")
            print("\n🎉 ¡Todo listo para usar Groq en el informe diario!")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    configurar_groq()
    
    # Preguntar si quiere probar
    load_dotenv()
    if os.environ.get('GROQ_API_KEY'):
        print("\n¿Quieres probar la API? (s/n): ", end='')
        if input().lower() == 's':
            test_groq()