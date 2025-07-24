#!/usr/bin/env python
"""
Genera el informe del 21 de julio usando el scraper original del proyecto
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
from alerts.views import generar_html_informe_especial

def main():
    """Genera y envía el informe del 21 de julio usando el sistema existente"""
    
    fecha = "21-07-2025"
    print(f"=== GENERANDO INFORME DEL {fecha} ===\n")
    
    # Usar el scraper existente con la edición correcta
    print("1. Obteniendo datos del Diario Oficial...")
    os.environ['DIARIO_OFICIAL_EDITION_OVERRIDE'] = '44203'  # Forzar edición correcta
    
    resultado = obtener_sumario_diario_oficial(fecha)
    
    if not resultado or not resultado.get('publicaciones'):
        print("❌ No se obtuvieron publicaciones")
        return
    
    print(f"✅ {len(resultado['publicaciones'])} publicaciones obtenidas")
    print(f"   Total documentos: {resultado.get('total_documentos', 0)}")
    
    # Generar HTML con la función existente
    print("\n2. Generando HTML con la plantilla oficial...")
    html = generar_html_informe_especial(resultado, fecha)
    
    # Guardar copia
    filename = f"informe_oficial_{fecha.replace('-', '_')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"📄 Informe guardado en: {filename}")
    
    # Enviar email
    print("\n3. Enviando email...")
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Informe Diario Oficial - {fecha} (Edición 44.203)"
    msg['From'] = "rodrigo@carvuk.com"
    msg['To'] = "rfernandezdelrio@uc.cl"
    
    html_part = MIMEText(html, 'html')
    msg.attach(html_part)
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("rodrigo@carvuk.com", "swqjlcwjaoooyzcb")
        server.send_message(msg)
        server.quit()
        
        print("✅ Email enviado exitosamente")
        print(f"   De: rodrigo@carvuk.com")
        print(f"   Para: rfernandezdelrio@uc.cl")
        
    except Exception as e:
        print(f"❌ Error enviando email: {str(e)}")

if __name__ == "__main__":
    main()