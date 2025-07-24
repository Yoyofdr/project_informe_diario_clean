#!/usr/bin/env python
"""
Script para enviar el informe del 21 de julio directamente por SMTP
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def enviar_informe_smtp():
    """Envía el informe directamente usando SMTP"""
    
    # Configuración del servidor
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "rodrigo@carvuk.com"
    sender_password = "swqjlcwjaoooyzcb"
    
    # Destinatarios
    recipients = ["rfernandezdelrio@uc.cl", "rodrigo@carvuk.com"]
    
    try:
        # Leer el informe HTML
        with open("informe_diario_oficial_21_07_2025_completo.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        print(f"Conectando a {smtp_server}:{smtp_port}...")
        
        # Crear conexión SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print("Autenticando...")
        server.login(sender_email, sender_password)
        
        # Enviar a cada destinatario
        for recipient in recipients:
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = f"Informe Diario Oficial - 21 de julio de 2025 - Edición N° 44.204"
            
            # Versión texto plano
            text = """
Informe Diario Oficial
Lunes 21 de julio de 2025
Edición N° 44.204

RESUMEN:
- 47 documentos publicados
- 5 publicaciones relevantes
- 1 licitación pública

PUBLICACIONES DESTACADAS:
1. Ley de inclusión laboral de personas con discapacidad
2. Actualización de valores UF
3. Reglamento de protección de datos en comercio electrónico
4. Modificación documentos tributarios electrónicos
5. Tipos de cambio del Banco Central

VALORES DEL DÍA:
- Dólar: $943.28
- Euro: $1,026.45
- UF: $38,073.52

Para ver el informe completo con todos los detalles, abra este email en un cliente que soporte HTML.
"""
            
            # Adjuntar partes
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Enviar
            print(f"Enviando a {recipient}...")
            server.send_message(msg)
            print(f"✓ Enviado exitosamente a {recipient}")
        
        # Cerrar conexión
        server.quit()
        
        print("\n✅ Todos los emails enviados exitosamente")
        print("\nPor favor revisa tu bandeja de entrada (y la carpeta de SPAM si no aparece)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== ENVÍO DIRECTO POR SMTP ===")
    print(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    enviar_informe_smtp()