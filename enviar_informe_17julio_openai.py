#!/usr/bin/env python
"""
Script para enviar el informe del 17 de julio generado con OpenAI
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

# Leer el archivo HTML del informe
fecha = "17-07-2025"
filename = f"informe_secciones_{fecha.replace('-', '_')}.html"

if not os.path.exists(filename):
    print(f"Error: No se encuentra el archivo {filename}")
    sys.exit(1)

with open(filename, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Configurar el email
subject = f'Informe Diario Oficial - {fecha} (Generado con OpenAI)'
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
try:
    msg.send()
    print(f"✓ Informe del {fecha} enviado exitosamente a {recipient_list[0]}")
    print("✓ Este informe fue generado usando OpenAI para análisis más precisos")
except Exception as e:
    print(f"✗ Error al enviar el correo: {e}")