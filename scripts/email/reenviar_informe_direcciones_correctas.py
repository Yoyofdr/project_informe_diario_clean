#!/usr/bin/env python
"""
Reenvía el informe del 21 de julio con las direcciones correctas
De: rodrigo@carvuk.com
Para: rfernandezdelrio@uc.cl
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from django.core.mail import EmailMessage
from django.conf import settings

def reenviar_informe():
    """Reenvía el informe con las direcciones correctas"""
    
    # Leer el HTML del informe generado
    with open('informe_real_21_julio_2025.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Configurar el email con las direcciones correctas
    remitente = settings.DEFAULT_FROM_EMAIL  # rodrigo@carvuk.com
    destinatario = "rfernandezdelrio@uc.cl"
    
    print("=== REENVIANDO INFORME CON DIRECCIONES CORRECTAS ===")
    print(f"De: {remitente}")
    print(f"Para: {destinatario}")
    
    email = EmailMessage(
        subject="Informe Diario Oficial - 21 de Julio 2025 (Edición 44.203)",
        body=html_content,
        from_email=remitente,
        to=[destinatario],
    )
    email.content_subtype = "html"
    
    try:
        email.send()
        print("\n✅ Email enviado exitosamente")
        print(f"📧 Remitente: {remitente}")
        print(f"📧 Destinatario: {destinatario}")
        print("📋 Asunto: Informe Diario Oficial - 21 de Julio 2025 (Edición 44.203)")
        return True
        
    except Exception as e:
        print(f"\n❌ Error al enviar email: {str(e)}")
        
        # Si falla con Django, intentar con SMTP directo
        print("\nIntentando con SMTP directo...")
        
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Informe Diario Oficial - 21 de Julio 2025 (Edición 44.203)"
        msg['From'] = remitente
        msg['To'] = destinatario
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        try:
            # Usar configuración de Django
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            
            server.send_message(msg)
            server.quit()
            
            print("✅ Email enviado exitosamente con SMTP directo")
            return True
            
        except Exception as e2:
            print(f"❌ Error con SMTP directo: {str(e2)}")
            return False

if __name__ == "__main__":
    if reenviar_informe():
        print("\n✅ Proceso completado")
    else:
        print("\n⚠️  No se pudo enviar el email")
        print("\nVerifica que las credenciales SMTP estén configuradas correctamente.")
        print("Las variables de entorno necesarias son:")
        print("- EMAIL_HOST")
        print("- EMAIL_HOST_USER")
        print("- EMAIL_HOST_PASSWORD")