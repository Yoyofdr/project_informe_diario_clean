#!/usr/bin/env python
"""
Script para verificar si hay publicaciones el 18 de julio
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

import requests
from bs4 import BeautifulSoup

# URL del 18 de julio
url = "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/18/"

print(f"Verificando URL: {url}")

try:
    response = requests.get(url, timeout=30)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar el selector de edición
        edition_select = soup.find('select', {'id': 'ediciones'})
        if edition_select:
            editions = edition_select.find_all('option')
            print(f"\nEdiciones encontradas: {len(editions)}")
            for edition in editions[:5]:  # Mostrar las primeras 5
                print(f"- {edition.get('value')} - {edition.text.strip()}")
        
        # Buscar publicaciones
        publicaciones = soup.find_all('h5', class_='light')
        print(f"\nPublicaciones encontradas: {len(publicaciones)}")
        
        if publicaciones:
            print("\nPrimeras publicaciones:")
            for i, pub in enumerate(publicaciones[:5], 1):
                titulo = pub.get_text(strip=True)
                print(f"{i}. {titulo}")
        else:
            print("No se encontraron publicaciones con h5.light")
            
            # Buscar con otros selectores
            links = soup.find_all('a', href=True)
            pdf_links = [link for link in links if '.pdf' in link['href']]
            print(f"\nEnlaces PDF encontrados: {len(pdf_links)}")
            
    else:
        print(f"Error al acceder a la URL: {response.status_code}")
        
except Exception as e:
    print(f"Error: {str(e)}")