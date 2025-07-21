#!/usr/bin/env python
"""
Script para probar acceso directo sin parámetros extra
"""
import requests
from bs4 import BeautifulSoup

def test_acceso():
    """Prueba diferentes URLs y métodos de acceso"""
    
    print("=== TEST DE ACCESO DIRECTO ===\n")
    
    # URLs a probar
    urls_test = [
        # URL básica sin parámetros extra
        "https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date=21-07-2025&edition=44204",
        
        # URL con formato de fecha diferente
        "https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date=2025-07-21&edition=44204",
        
        # URL de publicación directa
        "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/",
        
        # URL del sumario
        "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/sumario",
        
        # URL alternativa
        "https://www.diariooficial.interior.gob.cl/edicionelectronica/?date=21-07-2025"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-CL,es;q=0.9,en;q=0.8',
    }
    
    for i, url in enumerate(urls_test, 1):
        print(f"\n{'='*60}")
        print(f"PRUEBA {i}: {url}")
        print(f"{'='*60}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            
            print(f"Status Code: {response.status_code}")
            print(f"URL Final: {response.url}")
            print(f"Tamaño: {len(response.text)} caracteres")
            
            # Analizar contenido
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Verificar título
                title = soup.find('title')
                if title:
                    print(f"Título: {title.text.strip()}")
                
                # Buscar indicadores clave
                indicadores = {
                    "Diario Oficial": response.text.count("Diario Oficial"),
                    "21 de julio": response.text.count("21 de julio"),
                    "21-07-2025": response.text.count("21-07-2025"),
                    "Edición N° 44.204": response.text.count("44.204") + response.text.count("44204"),
                    "Normas Generales": response.text.count("Normas Generales"),
                    ".pdf": response.text.count(".pdf"),
                    "TSPD": response.text.count("TSPD")  # Indicador de protección
                }
                
                print("\nIndicadores encontrados:")
                for key, count in indicadores.items():
                    if count > 0:
                        print(f"  ✓ {key}: {count} veces")
                
                # Buscar publicaciones
                publicaciones = soup.find_all('tr', class_='content')
                if publicaciones:
                    print(f"\n✅ ÉXITO: {len(publicaciones)} publicaciones encontradas")
                    print("Primeras 3:")
                    for j, pub in enumerate(publicaciones[:3], 1):
                        tds = pub.find_all('td')
                        if tds:
                            titulo = tds[0].get_text(strip=True)
                            print(f"  {j}. {titulo[:80]}...")
                
                # Buscar PDFs
                pdfs = soup.find_all('a', href=lambda x: x and '.pdf' in x)
                if pdfs:
                    print(f"\n📎 {len(pdfs)} enlaces PDF encontrados")
                
                # Guardar HTML si parece prometedor
                if indicadores["Diario Oficial"] > 0 and indicadores["TSPD"] == 0:
                    filename = f"test_acceso_{i}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"\n💾 HTML guardado: {filename}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "="*60)
    print("FIN DE LAS PRUEBAS")
    print("="*60)

if __name__ == "__main__":
    test_acceso()