#!/usr/bin/env python
"""
Script para enviar el informe Bolt del 21 de julio por SMTP
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def enviar_informe_bolt():
    """Envía el informe Bolt directamente usando SMTP"""
    
    # Configuración del servidor
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "rodrigo@carvuk.com"
    sender_password = "swqjlcwjaoooyzcb"
    
    # Destinatarios
    recipients = ["rfernandezdelrio@uc.cl", "rodrigo@carvuk.com"]
    
    try:
        # Leer el informe HTML Bolt
        with open("informe_diario_oficial_21_07_2025_bolt.html", "r", encoding="utf-8") as f:
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
            msg['Subject'] = "📋 Diario Oficial • Lunes 21 de julio de 2025"
            
            # Versión texto plano
            text = """
DIARIO OFICIAL
Lunes 21 de julio de 2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 RESUMEN DEL DÍA
• 47 documentos totales
• 7 publicaciones relevantes seleccionadas

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NORMAS GENERALES (3 publicaciones)

LEY NÚM. 21.791 - INCLUSIÓN LABORAL
Cuotas obligatorias del 1% para personas con discapacidad en empresas 100+ trabajadores.

DECRETO SUPREMO Nº 147 - VALORES UF
Actualización de valores UF para agosto-septiembre 2025.

DECRETO SUPREMO Nº 312 - PROTECCIÓN DE DATOS
Nuevas normas para datos personales en comercio electrónico.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 NORMAS PARTICULARES (2 publicaciones)

RESOLUCIÓN SII - DOCUMENTOS ELECTRÓNICOS
Nuevos requisitos para operaciones con criptoactivos.

RESOLUCIÓN TRANSPORTES - RESTRICCIÓN VEHICULAR
Emergencia ambiental 22-23 julio en RM.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ AVISOS DESTACADOS (2 publicaciones)

BANCO CENTRAL - TIPOS DE CAMBIO
Valores oficiales del día.

[LICITACIÓN] MUNICIPALIDAD DE SANTIAGO
Construcción 12 km ciclovías ($4.500 millones).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💱 VALORES DEL DÍA
• Dólar: $943.28
• Euro: $1,026.45

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para ver el informe completo con diseño visual, abra este email en HTML.
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
        
        print("\n✅ Informe Bolt enviado exitosamente")
        print("📧 Este es el diseño correcto trabajado con Bolt")
        print("🎨 Incluye el header con gradiente, estadísticas, y botones azules")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== ENVÍO DE INFORME BOLT (DISEÑO CORRECTO) ===")
    print(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    enviar_informe_bolt()