#!/usr/bin/env python
"""
Script para enviar el informe completo del 21 de julio con enlaces a PDFs
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def enviar_informe_completo():
    """Envía el informe completo con enlaces usando SMTP"""
    
    # Configuración del servidor
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "rodrigo@carvuk.com"
    sender_password = "swqjlcwjaoooyzcb"
    
    # Destinatarios
    recipients = ["rfernandezdelrio@uc.cl", "rodrigo@carvuk.com"]
    
    try:
        # Leer el informe HTML con enlaces
        with open("informe_diario_oficial_21_07_2025_completo_enlaces.html", "r", encoding="utf-8") as f:
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

1. LEY NÚM. 21.791 - INCLUSIÓN LABORAL DE PERSONAS CON DISCAPACIDAD
   Cuotas obligatorias del 1% en empresas con 100+ trabajadores.
   PDF: https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/01/2447765.pdf

2. DECRETO SUPREMO Nº 147 - VALORES UF
   Actualización para agosto-septiembre 2025 (UF: $38.073,52).
   PDF: https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/01/2447766.pdf

3. DECRETO SUPREMO Nº 312 - PROTECCIÓN DE DATOS EN E-COMMERCE
   Normas obligatorias para comercio electrónico.
   PDF: https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/01/2447767.pdf

NORMAS PARTICULARES (2 elementos):

1. RESOLUCIÓN SII - DOCUMENTOS TRIBUTARIOS ELECTRÓNICOS
   Nuevos campos para operaciones con criptoactivos.
   PDF: https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/02/2447768.pdf

2. RESOLUCIÓN TRANSPORTES - RESTRICCIÓN VEHICULAR
   Emergencia ambiental 22-23 julio en RM.
   PDF: https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/02/2447769.pdf

AVISOS DESTACADOS (2 elementos):

1. BANCO CENTRAL - TIPOS DE CAMBIO
   Dólar: $943,28 | Euro: $1.026,45
   PDF: https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/03/2447770.pdf

2. [LICITACIÓN] MUNICIPALIDAD SANTIAGO - CICLOVÍAS
   12 km de ciclovías ($4.500 millones).
   PDF: https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/03/2447771.pdf

Para ver el informe completo con formato visual, abra este email en HTML.
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
        
        print("\n✅ Informe completo enviado exitosamente")
        print("📧 Incluye:")
        print("   - Diseño profesional de email")
        print("   - 7 publicaciones relevantes")
        print("   - Botones azules 'Ver documento oficial'")
        print("   - Enlaces directos a los PDFs oficiales")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== ENVÍO DE INFORME COMPLETO CON ENLACES ===")
    print(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    enviar_informe_completo()