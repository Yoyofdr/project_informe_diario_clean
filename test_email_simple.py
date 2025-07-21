#!/usr/bin/env python
"""
Script de prueba simple para diagnosticar envío de emails
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time

def test_email_simple():
    """Envía un email de prueba muy simple"""
    
    # Configuración
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "rodrigo@carvuk.com"
    sender_password = "swqjlcwjaoooyzcb"
    
    # Solo un destinatario para la prueba
    recipient = "rfernandezdelrio@uc.cl"
    
    try:
        print("=== TEST DE EMAIL SIMPLE ===")
        print(f"Fecha/Hora: {datetime.now()}")
        print(f"De: {sender_email}")
        print(f"Para: {recipient}")
        
        # Crear mensaje simple
        msg = MIMEText(f"Este es un email de prueba enviado a las {datetime.now().strftime('%H:%M:%S')}")
        msg['Subject'] = f'Test Simple - {datetime.now().strftime("%H:%M:%S")}'
        msg['From'] = sender_email
        msg['To'] = recipient
        
        # Conectar y enviar
        print("\nConectando a Gmail...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)  # Mostrar debug
        
        print("Iniciando TLS...")
        server.starttls()
        
        print("Autenticando...")
        server.login(sender_email, sender_password)
        
        print("Enviando mensaje...")
        server.send_message(msg)
        
        print("\n✅ Email enviado exitosamente")
        
        server.quit()
        
        print("\nREVISA:")
        print("1. Bandeja de entrada")
        print("2. Carpeta de SPAM")
        print("3. Carpeta de Promociones (Gmail)")
        print("4. Todas las carpetas")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_email_simple()