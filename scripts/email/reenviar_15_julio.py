#!/usr/bin/env python
"""
Script para reenviar el informe del 15 de julio con la edición correcta
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')

# Cargar variables del .env
from dotenv import load_dotenv
load_dotenv()

django.setup()

from django.core.mail import EmailMessage
from django.conf import settings
from enviar_informes_multiples import generar_informe_email

# Ejecutar
fecha = "15-07-2025"
print(f"Reenviando informe del {fecha} con edición corregida...")

try:
    # Generar el informe
    html_content = generar_informe_email(fecha)
    
    # Configurar el email
    subject = f'[CORREGIDO] Informe Diario Oficial - {fecha}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['rfernandezdelrio@uc.cl']
    
    # Crear el mensaje
    msg = EmailMessage(
        subject,
        '',
        from_email,
        recipient_list
    )
    
    # Establecer el contenido HTML
    msg.content_subtype = 'html'
    msg.body = html_content
    
    # Enviar
    msg.send()
    print(f"✓ Informe del {fecha} reenviado exitosamente con edición 44199")
    
except Exception as e:
    print(f"✗ Error: {e}")