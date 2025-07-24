#!/usr/bin/env python
"""
Script para enviar el informe moderno del 21 de julio por SMTP
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def enviar_informe_moderno():
    """Envía el informe moderno directamente usando SMTP"""
    
    # Configuración del servidor
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "rodrigo@carvuk.com"
    sender_password = "swqjlcwjaoooyzcb"
    
    # Destinatarios
    recipients = ["rfernandezdelrio@uc.cl", "rodrigo@carvuk.com"]
    
    try:
        # Leer el informe HTML moderno
        with open("informe_diario_oficial_21_07_2025_moderno.html", "r", encoding="utf-8") as f:
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
            msg['Subject'] = f"Informe Diario Oficial - Lunes 21 de julio de 2025 - Edición N° 44.204"
            
            # Versión texto plano
            text = """
INFORME DIARIO OFICIAL
Lunes 21 de julio de 2025
Edición N° 44.204

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 RESUMEN DEL DÍA
• 7 publicaciones totales
• 1 licitación pública

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NORMAS GENERALES (3 publicaciones)

1. LEY NÚM. 21.791 - INCLUSIÓN LABORAL DE PERSONAS CON DISCAPACIDAD
   Establece cuotas obligatorias del 1% en empresas con 100+ trabajadores.

2. DECRETO SUPREMO Nº 147 - VALORES UF
   Actualiza valores de la UF para agosto-septiembre 2025.

3. DECRETO SUPREMO Nº 312 - PROTECCIÓN DE DATOS EN E-COMMERCE
   Nuevas normas para el tratamiento de datos personales en comercio electrónico.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NORMAS PARTICULARES (2 publicaciones)

1. RESOLUCIÓN SII - DOCUMENTOS TRIBUTARIOS ELECTRÓNICOS
   Nuevos requisitos para operaciones con criptoactivos.

2. RESOLUCIÓN TRANSPORTES - RESTRICCIÓN VEHICULAR
   Emergencia ambiental días 22-23 de julio en RM.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 AVISOS DESTACADOS (2 publicaciones)

1. BANCO CENTRAL - TIPOS DE CAMBIO
   Valores oficiales del día.

2. [LICITACIÓN] MUNICIPALIDAD DE SANTIAGO - CICLOVÍAS
   Construcción de 12 km de ciclovías ($4.500 millones).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💱 VALORES DEL DÍA
• Dólar Observado: $943.28
• Euro: $1,026.45

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para ver el informe completo con formato visual, abra este email en un cliente que soporte HTML.
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
        
        print("\n✅ Informe moderno enviado exitosamente")
        print("📧 Revisa tu bandeja de entrada")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== ENVÍO DE INFORME MODERNO ===")
    print(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    enviar_informe_moderno()