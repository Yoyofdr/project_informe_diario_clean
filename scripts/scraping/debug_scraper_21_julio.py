#!/usr/bin/env python
"""
Script de debug para investigar el scraping del 21 de julio
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

def debug_scraper():
    """Debug del scraper para el 21 de julio"""
    
    fecha = "21-07-2025"
    edition = "44204"  # Sabemos que este es el número correcto
    
    print("=== DEBUG SCRAPER DIARIO OFICIAL ===")
    print(f"Fecha: {fecha}")
    print(f"Edición: {edition}")
    
    # URL con edición
    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}&v=1"
    print(f"\nURL completa: {url}")
    
    try:
        # Headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        print("\nHaciendo petición HTTP...")
        response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        print(f"Status code: {response.status_code}")
        print(f"URL final: {response.url}")
        print(f"Tamaño respuesta: {len(response.text)} caracteres")
        
        # Analizar HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar título
        title = soup.find('title')
        if title:
            print(f"\nTítulo de la página: {title.text.strip()}")
        
        # Buscar tr.content (donde están las publicaciones)
        content_rows = soup.find_all('tr', class_='content')
        print(f"\n📋 Encontrados {len(content_rows)} elementos tr.content")
        
        if content_rows:
            print("\n--- PRIMERAS 5 PUBLICACIONES ---")
            for i, tr in enumerate(content_rows[:5]):
                tds = tr.find_all('td')
                if len(tds) >= 2:
                    titulo = tds[0].get_text(strip=True)
                    # Buscar enlace PDF
                    link = tds[1].find('a', href=True)
                    pdf_url = link['href'] if link else "Sin PDF"
                    
                    print(f"\n{i+1}. TÍTULO: {titulo[:100]}...")
                    print(f"   PDF: {pdf_url}")
        
        # Buscar tablas
        tables = soup.find_all('table')
        print(f"\n📊 Total de tablas en la página: {len(tables)}")
        
        # Buscar elementos con class="light" (otro posible contenedor)
        light_elements = soup.find_all(class_='light')
        print(f"📄 Elementos con class='light': {len(light_elements)}")
        
        # Buscar PDFs directamente
        pdf_links = soup.find_all('a', href=lambda x: x and x.endswith('.pdf'))
        print(f"\n📎 Total enlaces PDF encontrados: {len(pdf_links)}")
        
        if pdf_links:
            print("\n--- PRIMEROS 5 PDFs ---")
            for i, link in enumerate(pdf_links[:5]):
                texto = link.get_text(strip=True) or link.find_previous(text=True)
                print(f"{i+1}. {texto[:80]}... -> {link['href']}")
        
        # Buscar indicadores de que es la página correcta
        indicators = {
            "Diario Oficial": soup.text.count("Diario Oficial"),
            "Normas Generales": soup.text.count("Normas Generales"),
            "Normas Particulares": soup.text.count("Normas Particulares"),
            "Ver PDF": soup.text.count("Ver PDF"),
            "edición": soup.text.lower().count("edición")
        }
        
        print("\n🔍 INDICADORES DE CONTENIDO:")
        for key, count in indicators.items():
            print(f"   '{key}': {count} veces")
        
        # Guardar HTML para inspección manual
        debug_file = "debug_diario_21_julio.html"
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\n💾 HTML guardado en: {debug_file}")
        
        # Buscar mensajes de error o avisos
        error_messages = soup.find_all(text=lambda t: t and any(word in t.lower() for word in ['error', 'no se encontr', 'no hay', 'sin resultados']))
        if error_messages:
            print("\n⚠️  POSIBLES MENSAJES DE ERROR:")
            for msg in error_messages[:3]:
                print(f"   - {msg.strip()[:100]}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_scraper()