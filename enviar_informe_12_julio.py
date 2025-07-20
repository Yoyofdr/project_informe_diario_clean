#!/usr/bin/env python
"""
Script para generar y enviar el informe del 12 de julio
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')

# Cargar variables del .env ANTES de django.setup()
from dotenv import load_dotenv
load_dotenv()

django.setup()

from django.core.mail import EmailMessage
from django.conf import settings
from generar_informe_bolt_refinado import generar_informe_html

# Generar el informe
fecha = "12-07-2025"
print(f"Generando informe del {fecha}...")

try:
    html_content = generar_informe_html(fecha)
    
    # Guardar localmente
    filename = f"informe_bolt_refinado_{fecha.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✓ Informe guardado como: {filename}")
    
    # Configurar el email
    subject = f'Informe Diario Oficial - {fecha}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['rfernandezdelrio@uc.cl']
    
    # Crear el mensaje
    msg = EmailMessage(
        subject,
        '',  # Cuerpo vacío ya que usamos html
        from_email,
        recipient_list
    )
    
    # Establecer el contenido HTML
    msg.content_subtype = 'html'
    msg.body = html_content
    
    # Enviar
    print("Enviando email...")
    msg.send()
    print(f"✓ Informe del {fecha} enviado exitosamente a {recipient_list[0]}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print(f"Si el email falla, el informe está guardado localmente como: {filename}")