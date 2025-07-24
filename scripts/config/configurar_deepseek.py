#!/usr/bin/env python
"""
Script para configurar DeepSeek API Key
"""
import os

def configurar_deepseek():
    print("=== CONFIGURACIÓN DE DEEPSEEK ===")
    print("\nPara usar DeepSeek en lugar de Gemini, necesitas:")
    print("1. Obtener una API key de https://platform.deepseek.com/")
    print("2. Agregar la API key al archivo .env")
    
    # Verificar si existe .env
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_path):
        print("\nCreando archivo .env...")
        with open(env_path, 'w') as f:
            f.write("# Configuración de APIs\n")
            f.write("DEEPSEEK_API_KEY=\n")
            f.write("GEMINI_API_KEY=\n")
        print(f"✓ Archivo .env creado en: {env_path}")
    
    print("\nPara configurar DeepSeek:")
    print(f"1. Abre el archivo: {env_path}")
    print("2. Agrega tu API key de DeepSeek:")
    print("   DEEPSEEK_API_KEY=tu_api_key_aqui")
    print("\n3. Guarda el archivo")
    
    # Verificar configuración actual
    from dotenv import load_dotenv
    load_dotenv()
    
    deepseek_key = os.environ.get('DEEPSEEK_API_KEY')
    gemini_key = os.environ.get('GEMINI_API_KEY')
    
    print("\n=== ESTADO ACTUAL ===")
    if deepseek_key:
        print(f"✓ DeepSeek API Key configurada: {deepseek_key[:10]}...")
    else:
        print("✗ DeepSeek API Key NO configurada")
    
    if gemini_key:
        print(f"✓ Gemini API Key configurada: {gemini_key[:10]}...")
    else:
        print("✗ Gemini API Key NO configurada")
    
    if deepseek_key:
        print("\n✅ El sistema usará DeepSeek para evaluar relevancia")
    elif gemini_key:
        print("\n⚠️  El sistema usará Gemini (puede tener límites de cuota)")
    else:
        print("\n⚠️  El sistema usará reglas básicas (sin IA)")

if __name__ == "__main__":
    configurar_deepseek()