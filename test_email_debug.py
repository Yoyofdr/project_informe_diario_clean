#!/usr/bin/env python
"""
Script de diagnóstico para problemas de envío de email
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_django_settings():
    """Verificar configuración de Django"""
    print("=== CONFIGURACIÓN DE DJANGO ===")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if hasattr(settings, 'EMAIL_HOST_PASSWORD') else 'NO CONFIGURADO'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()

def test_smtp_connection():
    """Probar conexión SMTP directa"""
    print("=== PRUEBA DE CONEXIÓN SMTP ===")
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.set_debuglevel(1)  # Mostrar debug
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("✓ Conexión SMTP exitosa")
        server.quit()
        return True
    except Exception as e:
        print(f"✗ Error de conexión SMTP: {str(e)}")
        return False

def test_simple_email():
    """Enviar email simple de prueba"""
    print("\n=== ENVIANDO EMAIL DE PRUEBA SIMPLE ===")
    try:
        result = send_mail(
            subject='Prueba de Email - ' + datetime.now().strftime("%H:%M:%S"),
            message='Este es un email de prueba enviado desde Django.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['rfernandezdelrio@uc.cl'],
            fail_silently=False,
        )
        print(f"✓ Email enviado. Resultado: {result}")
        return True
    except Exception as e:
        print(f"✗ Error enviando email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_html_email():
    """Enviar email HTML de prueba"""
    print("\n=== ENVIANDO EMAIL HTML DE PRUEBA ===")
    try:
        html_content = """
        <html>
        <body>
            <h1>Prueba de Email HTML</h1>
            <p>Este es un email de prueba con formato HTML.</p>
            <p>Fecha: """ + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + """</p>
        </body>
        </html>
        """
        
        email = EmailMessage(
            subject='Prueba HTML - ' + datetime.now().strftime("%H:%M:%S"),
            body='Versión texto plano',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['rfernandezdelrio@uc.cl'],
        )
        email.content_subtype = "html"
        email.body = html_content
        
        result = email.send(fail_silently=False)
        print(f"✓ Email HTML enviado. Resultado: {result}")
        return True
    except Exception as e:
        print(f"✗ Error enviando email HTML: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_smtp_raw():
    """Enviar email directo con SMTP"""
    print("\n=== ENVIANDO EMAIL DIRECTO CON SMTP ===")
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = 'rfernandezdelrio@uc.cl'
        msg['Subject'] = 'Prueba SMTP Directo - ' + datetime.now().strftime("%H:%M:%S")
        
        body = 'Este es un email enviado directamente con SMTP.'
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(settings.EMAIL_HOST_USER, ['rfernandezdelrio@uc.cl'], text)
        server.quit()
        
        print("✓ Email SMTP directo enviado")
        return True
    except Exception as e:
        print(f"✗ Error enviando email SMTP directo: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("DIAGNÓSTICO DE ENVÍO DE EMAIL")
    print("=" * 50)
    
    # Verificar configuración
    test_django_settings()
    
    # Probar conexión
    if test_smtp_connection():
        # Si la conexión funciona, probar envíos
        test_simple_email()
        test_html_email()
        test_smtp_raw()
    
    print("\n" + "=" * 50)
    print("DIAGNÓSTICO COMPLETADO")
    print("\nNOTA: Si los emails se envían exitosamente pero no llegan:")
    print("1. Revisa la carpeta de SPAM")
    print("2. Verifica que la contraseña de aplicación de Gmail esté activa")
    print("3. Revisa la configuración de seguridad de Gmail")
    print("4. Verifica que no haya límites de envío alcanzados")

if __name__ == "__main__":
    main()