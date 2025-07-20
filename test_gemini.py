#!/usr/bin/env python
"""
Script para probar Gemini API
"""
import os
from dotenv import load_dotenv

def test_gemini():
    """Prueba la API de Gemini"""
    load_dotenv()
    
    try:
        import google.generativeai as genai
        
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY no configurada")
            return
        
        print("=== PROBANDO GEMINI API ===")
        print(f"API Key: {api_key[:15]}...")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Responde solo con 'funciona' si puedes leer esto")
        print(f"✅ Gemini respondió: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if "quota" in str(e).lower():
            print("   Parece que excediste la cuota diaria de Gemini")
        return False

if __name__ == "__main__":
    test_gemini()