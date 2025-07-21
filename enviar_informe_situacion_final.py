#!/usr/bin/env python
"""
Envía el informe de situación del 21 de julio
"""
import os
import sys
import django
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

# Leer el HTML generado
with open('informe_situacion_21_julio_2025.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Configuración SMTP
from django.conf import settings

# Usar la configuración de Django
smtp_server = settings.EMAIL_HOST
smtp_port = settings.EMAIL_PORT
smtp_user = settings.EMAIL_HOST_USER
smtp_password = settings.EMAIL_HOST_PASSWORD

destinatario = "ifernaandeez@gmail.com"

# Crear mensaje
msg = MIMEMultipart('alternative')
msg['Subject'] = "Informe Diario Oficial - 21 de Julio 2025 (Situación Especial)"
msg['From'] = smtp_user
msg['To'] = destinatario

# Adjuntar HTML
html_part = MIMEText(html_content, 'html')
msg.attach(html_part)

try:
    print("Conectando al servidor SMTP con configuración de Django...")
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    
    print("Enviando email...")
    server.send_message(msg)
    server.quit()
    
    print("✅ Email enviado exitosamente")
    print(f"📧 Destinatario: {destinatario}")
    print(f"📋 Asunto: {msg['Subject']}")
    
except Exception as e:
    print(f"❌ Error al enviar email: {str(e)}")
    print("\nIntentando con método alternativo...")
    
    # Si falla, intentar con send_mail de Django
    from django.core.mail import EmailMessage
    
    email = EmailMessage(
        subject=msg['Subject'],
        body=html_content,
        from_email=smtp_user,
        to=[destinatario],
    )
    email.content_subtype = "html"
    
    try:
        email.send()
        print("✅ Email enviado exitosamente con Django")
    except Exception as e2:
        print(f"❌ Error con Django: {str(e2)}")