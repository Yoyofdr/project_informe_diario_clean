#!/usr/bin/env python
"""
Script para enviar el informe del 21 de julio con el diseño correcto de email
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def enviar_informe_final():
    """Envía el informe con el diseño de email correcto usando SMTP"""
    
    # Configuración del servidor
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "rodrigo@carvuk.com"
    sender_password = "swqjlcwjaoooyzcb"
    
    # Destinatarios
    recipients = ["rfernandezdelrio@uc.cl", "rodrigo@carvuk.com"]
    
    try:
        # Leer el informe HTML
        with open("informe_diario_oficial_21_07_2025_email.html", "r", encoding="utf-8") as f:
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
            msg['Subject'] = "Informe Diario Oficial - 21 de julio de 2025"
            
            # Versión texto plano
            text = """
Informe Diario Oficial
21 de julio de 2025

RESUMEN:
- 47 documentos totales
- 7 publicaciones relevantes

NORMAS GENERALES (3 elementos):
1. Ley 21.791 - Inclusión laboral de personas con discapacidad
2. Decreto 147 - Valores UF agosto-septiembre 2025
3. Decreto 312 - Protección de datos en comercio electrónico

NORMAS PARTICULARES (2 elementos):
1. Resolución SII - Documentos tributarios electrónicos para criptoactivos
2. Resolución Transportes - Restricción vehicular 22-23 julio

AVISOS DESTACADOS (2 elementos):
1. Banco Central - Tipos de cambio (Dólar: $943,28 | Euro: $1.026,45)
2. [LICITACIÓN] Municipalidad Santiago - Construcción 12 km ciclovías

Para ver el informe completo, abra este email en un cliente que soporte HTML.
Información obtenida de diariooficial.interior.gob.cl
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
        
        print("\n✅ Informe enviado con el diseño correcto")
        print("📧 Diseño profesional de email con:")
        print("   - Header con gradiente gris oscuro")
        print("   - Estadísticas en sección azul")
        print("   - Publicaciones con borde superior azul")
        print("   - Diseño compatible con todos los clientes de correo")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== ENVÍO DE INFORME DIARIO OFICIAL ===")
    print(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    enviar_informe_final()