#!/usr/bin/env python
"""
Script para enviar el informe con el diseño original correcto
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def enviar_informe_correcto():
    """Envía el informe con el diseño correcto usando SMTP"""
    
    # Configuración del servidor
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "rodrigo@carvuk.com"
    sender_password = "swqjlcwjaoooyzcb"
    
    # Destinatarios
    recipients = ["rfernandezdelrio@uc.cl", "rodrigo@carvuk.com"]
    
    try:
        # Leer el informe HTML con diseño correcto
        with open("informe_diario_oficial_21_07_2025_diseño_original.html", "r", encoding="utf-8") as f:
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
            msg['Subject'] = "📋 Diario Oficial • Lunes 21 de julio, 2025"
            
            # Versión texto plano
            text = """
DIARIO OFICIAL
Lunes 21 de julio, 2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ESTADÍSTICAS
• 47 Total Documentos
• 7 Publicaciones Relevantes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PUBLICACIONES DESTACADAS

[Sección I - Normas Generales]

LEY NÚM. 21.791 - INCLUSIÓN LABORAL
Cuotas obligatorias del 1% para personas con discapacidad en empresas 100+ trabajadores.

DECRETO SUPREMO Nº 147 - VALORES UF
Actualización de valores UF para agosto-septiembre 2025.

DECRETO SUPREMO Nº 312 - PROTECCIÓN DE DATOS
Normas para datos personales en comercio electrónico.

[Sección II - Normas Particulares]

RESOLUCIÓN SII - DOCUMENTOS ELECTRÓNICOS
Nuevos requisitos para operaciones con criptoactivos.

RESOLUCIÓN TRANSPORTES - RESTRICCIÓN VEHICULAR
Emergencia ambiental 22-23 julio en RM.

[Sección III - Avisos Destacados]

BANCO CENTRAL - TIPOS DE CAMBIO
Dólar: $943.28 | Euro: $1,026.45

MUNICIPALIDAD DE SANTIAGO - LICITACIÓN CICLOVÍAS
Construcción 12 km ciclovías ($4.500 millones).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para ver el informe completo con diseño visual, abra este email en HTML.
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
        print("🎨 Este es el diseño exacto del código React que compartiste:")
        print("   - Fondo: bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50")
        print("   - Header: from-black via-gray-900 to-gray-700")
        print("   - Hover effects: hover:shadow-xl hover:shadow-blue-100/50")
        print("   - Animación: hover:-translate-y-1")
        print("   - Línea superior animada en las publicaciones")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== ENVÍO DE INFORME CON DISEÑO CORRECTO ===")
    print(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    enviar_informe_correcto()