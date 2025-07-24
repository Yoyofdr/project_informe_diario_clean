#!/usr/bin/env python
"""
Script para obtener el sumario PDF del 21 de julio
"""
import requests
import os

def descargar_sumario():
    """Descarga el sumario PDF del 21 de julio"""
    
    # URL del sumario PDF encontrada en el HTML
    url_sumario = "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/sumarios/44204.pdf"
    
    print("=== DESCARGANDO SUMARIO PDF ===")
    print(f"URL: {url_sumario}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(url_sumario, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'No especificado')}")
        print(f"Tamaño: {len(response.content)} bytes")
        
        if response.status_code == 200 and 'pdf' in response.headers.get('Content-Type', '').lower():
            # Guardar el PDF
            filename = "sumario_21_julio_2025.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"\n✅ PDF descargado exitosamente: {filename}")
            return True
        else:
            print("\n❌ No se pudo descargar el PDF")
            # Guardar la respuesta para debug
            with open("debug_sumario_response.html", 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("Respuesta guardada en: debug_sumario_response.html")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    descargar_sumario()