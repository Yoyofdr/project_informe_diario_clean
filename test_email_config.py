#!/usr/bin/env python
"""
Script de prueba para verificar la configuración de email
"""

import os
import sys
import django
from datetime import datetime

# Configurar el entorno Django
sys.path.append('/Users/rodrigofernandezdelrio/Desktop/Project Diario Oficial')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    """Prueba la configuración de email actual"""
    
    print("=== PRUEBA DE CONFIGURACIÓN DE EMAIL ===")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # Mostrar configuración actual
    print(f"EMAIL_MODE: {settings.EMAIL_MODE}")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    
    if settings.EMAIL_MODE == 'smtp':
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'No configurado'}")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    else:
        print(f"EMAIL_FILE_PATH: {settings.EMAIL_FILE_PATH}")
    
    print("-" * 50)
    
    # Intentar enviar un email de prueba
    try:
        destinatario = input("Ingrese el email destinatario para la prueba (o presione Enter para usar rodrigo@carvuk.com): ")
        if not destinatario:
            destinatario = "rodrigo@carvuk.com"
        
        print(f"\nEnviando email de prueba a: {destinatario}")
        
        resultado = send_mail(
            subject='Prueba de Configuración - Informe Diario Oficial',
            message='Este es un email de prueba para verificar la configuración del sistema de Informe Diario Oficial.',
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else settings.EMAIL_HOST_USER,
            recipient_list=[destinatario],
            fail_silently=False,
            html_message="""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #333;">Prueba de Configuración Exitosa</h2>
                    <p>Este email confirma que la configuración de correo está funcionando correctamente.</p>
                    <hr style="border: 1px solid #ccc;">
                    <h3>Detalles de la configuración:</h3>
                    <ul>
                        <li><strong>Modo de email:</strong> {}</li>
                        <li><strong>Backend:</strong> {}</li>
                        <li><strong>Fecha y hora:</strong> {}</li>
                    </ul>
                    <p style="color: #666; font-size: 14px; margin-top: 20px;">
                        Este es un email automático del sistema de Informe Diario Oficial.
                    </p>
                </body>
            </html>
            """.format(
                settings.EMAIL_MODE,
                settings.EMAIL_BACKEND,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        )
        
        if resultado > 0:
            print(f"\n✅ EMAIL ENVIADO EXITOSAMENTE")
            if settings.EMAIL_MODE == 'filebased':
                print(f"📁 El archivo del email se guardó en: {settings.EMAIL_FILE_PATH}")
        else:
            print("\n❌ Error: No se pudo enviar el email")
            
    except Exception as e:
        print(f"\n❌ ERROR AL ENVIAR EMAIL: {type(e).__name__}: {e}")
        print("\nDetalles del error:")
        import traceback
        traceback.print_exc()
        
        # Si hay error con SMTP, sugerir alternativas
        if settings.EMAIL_MODE == 'smtp':
            print("\n💡 Sugerencias:")
            print("1. Verifica que las credenciales en .env sean correctas")
            print("2. Si usas Gmail, asegúrate de tener habilitado el acceso de aplicaciones menos seguras")
            print("3. O genera una contraseña de aplicación en: https://myaccount.google.com/apppasswords")
            print("\n📌 Para probar con emails guardados localmente, cambia EMAIL_MODE='filebased' en .env")

if __name__ == "__main__":
    test_email_configuration()