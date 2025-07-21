#!/usr/bin/env python
"""
Obtener datos del 21 de julio con la edición CORRECTA: 44203
"""
import os
import sys
import django
import requests
from bs4 import BeautifulSoup

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

def obtener_publicaciones_edicion_correcta():
    """Obtiene las publicaciones con el número de edición correcto"""
    
    fecha = "21-07-2025"
    edicion = "44203"  # EDICIÓN CORRECTA
    
    print("=== OBTENIENDO DATOS CON EDICIÓN CORRECTA ===")
    print(f"Fecha: {fecha}")
    print(f"Edición: {edicion} (CORREGIDA)")
    
    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edicion}"
    print(f"\nURL: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-CL,es;q=0.9',
    }
    
    try:
        # Primero con curl para evitar protección
        import subprocess
        curl_cmd = f'curl -s -L -H "User-Agent: Mozilla/5.0" "{url}"'
        print("\nObteniendo con curl...")
        
        result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True)
        html_content = result.stdout
        
        print(f"Tamaño respuesta: {len(html_content)} caracteres")
        
        # Guardar para análisis
        with open("edicion_correcta_21_julio.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Analizar contenido
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Buscar publicaciones
        publicaciones = []
        content_rows = soup.find_all('tr', class_='content')
        
        if content_rows:
            print(f"\n✅ ÉXITO: {len(content_rows)} publicaciones encontradas!")
            
            for i, tr in enumerate(content_rows[:10], 1):  # Primeras 10
                tds = tr.find_all('td')
                if len(tds) >= 2:
                    titulo = tds[0].get_text(strip=True)
                    link = tds[1].find('a', href=True)
                    pdf_url = link['href'] if link else ""
                    
                    if pdf_url and not pdf_url.startswith('http'):
                        pdf_url = f"https://www.diariooficial.interior.gob.cl{pdf_url}"
                    
                    publicacion = {
                        'titulo': titulo,
                        'url_pdf': pdf_url,
                        'seccion': 'NORMAS GENERALES',  # Por defecto
                        'resumen': f"Publicación del Diario Oficial del {fecha}"
                    }
                    publicaciones.append(publicacion)
                    
                    print(f"\n{i}. {titulo[:80]}...")
                    if pdf_url:
                        print(f"   PDF: {pdf_url}")
        
        # Verificar si hay mensaje de error
        no_found = soup.find('p', class_='nofound')
        if no_found:
            print(f"\n⚠️ Mensaje del sitio: {no_found.text.strip()}")
        
        # Buscar valores de monedas si están disponibles
        valores_monedas = {}
        # Aquí podrías agregar lógica para extraer valores de monedas
        
        return {
            'publicaciones': publicaciones,
            'valores_monedas': valores_monedas,
            'total_documentos': len(publicaciones),
            'edicion': edicion,
            'fecha': fecha
        }
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    resultado = obtener_publicaciones_edicion_correcta()
    
    if resultado and resultado['publicaciones']:
        print(f"\n{'='*60}")
        print(f"RESUMEN FINAL:")
        print(f"Total publicaciones encontradas: {resultado['total_documentos']}")
        print(f"Edición correcta: {resultado['edicion']}")
        print(f"{'='*60}")
    else:
        print("\n⚠️ No se pudieron obtener publicaciones")