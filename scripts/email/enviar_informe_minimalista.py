#!/usr/bin/env python
"""
Script para enviar el informe del 18 de julio con diseño minimalista
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
fecha = "18-07-2025"
filename = f"informe_secciones_{fecha.replace('-', '_')}.html"

if not os.path.exists(filename):
    print(f"Error: No se encuentra el archivo {filename}")
    sys.exit(1)

with open(filename, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Configurar el email
subject = f'Informe Diario Oficial - {fecha} (Diseño Minimalista)'
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
    print("\n✓ Nuevo diseño minimalista:")
    print("  - Tipografía elegante (Georgia/Times New Roman)")
    print("  - Solo blanco y negro")
    print("  - Sin colores ni gradientes")
    print("  - Espaciado generoso")
    print("  - Diseño limpio y profesional")
except Exception as e:
    print(f"✗ Error al enviar el correo: {e}")