#!/usr/bin/env python
"""
Script para probar el envío real de correos
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

# Ahora configurar Django
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=== VERIFICACIÓN DE CONFIGURACIÓN DE EMAIL ===\n")

# Mostrar configuración actual
print(f"EMAIL_MODE: {os.environ.get('EMAIL_MODE', 'No definido')}")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")

# Verificar si está en modo SMTP
if 'smtp' in settings.EMAIL_BACKEND:
    print("\n✅ Configurado para envío SMTP real")
else:
    print("\n❌ NO está configurado para envío real")
    print(f"   Backend actual: {settings.EMAIL_BACKEND}")

# Intentar enviar correo de prueba
print("\n=== ENVIANDO CORREO DE PRUEBA ===")

try:
    result = send_mail(
        subject='Prueba de envío - Informe Diario Oficial',
        message='Este es un correo de prueba para verificar que el sistema de envío funciona correctamente.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['rfernandezdelrio@uc.cl'],
        fail_silently=False,
        html_message="""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>✅ Prueba exitosa</h2>
            <p>Si estás recibiendo este correo, significa que el sistema de envío está funcionando correctamente.</p>
            <p>Los informes del Diario Oficial se enviarán desde esta misma configuración.</p>
            <hr>
            <p><small>Enviado desde: {}</small></p>
        </body>
        </html>
        """.format(settings.DEFAULT_FROM_EMAIL)
    )
    
    print(f"✅ Correo enviado exitosamente!")
    print(f"   Resultado: {result}")
    print(f"   Destinatario: rfernandezdelrio@uc.cl")
    print(f"   Remitente: {settings.DEFAULT_FROM_EMAIL}")
    
except Exception as e:
    print(f"❌ Error al enviar correo: {e}")
    print(f"   Tipo de error: {type(e).__name__}")
    
    # Si es error de autenticación
    if "Authentication" in str(e) or "credentials" in str(e).lower():
        print("\n⚠️  Posible problema de autenticación:")
        print("   1. Verifica que el email y contraseña sean correctos")
        print("   2. Si usas Gmail, asegúrate de usar una 'App Password'")
        print("   3. Habilita el acceso de apps menos seguras o usa 2FA con App Password")