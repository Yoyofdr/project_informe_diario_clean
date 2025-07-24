#!/usr/bin/env python
"""
Envía el informe usando SMTP directo con las credenciales correctas
De: rodrigo@carvuk.com
Para: rfernandezdelrio@uc.cl
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_informe_smtp():
    """Envía el informe usando SMTP directo"""
    
    # Configuración SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "rodrigo@carvuk.com"
    smtp_password = "swqjlcwjaoooyzcb"
    
    # Direcciones
    remitente = "rodrigo@carvuk.com"
    destinatario = "rfernandezdelrio@uc.cl"
    
    print("=== ENVIANDO INFORME VÍA SMTP DIRECTO ===")
    print(f"De: {remitente}")
    print(f"Para: {destinatario}")
    
    # Leer el HTML del informe
    with open('informe_real_21_julio_2025.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Crear mensaje
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Informe Diario Oficial - 21 de Julio 2025 (Edición 44.203)"
    msg['From'] = remitente
    msg['To'] = destinatario
    
    # Agregar contenido HTML
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    try:
        print("\nConectando al servidor SMTP...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print("Autenticando...")
        server.login(smtp_user, smtp_password)
        
        print("Enviando email...")
        server.send_message(msg)
        server.quit()
        
        print("\n✅ Email enviado exitosamente")
        print(f"📧 De: {remitente}")
        print(f"📧 Para: {destinatario}")
        print("📋 Asunto: Informe Diario Oficial - 21 de Julio 2025 (Edición 44.203)")
        print("\n✅ El informe ha sido enviado correctamente a rfernandezdelrio@uc.cl")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error al enviar email: {str(e)}")
        return False

if __name__ == "__main__":
    enviar_informe_smtp()