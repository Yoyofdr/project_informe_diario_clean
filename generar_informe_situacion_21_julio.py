#!/usr/bin/env python
"""
Genera un informe explicando la situación del 21 de julio
"""
import os
import sys
import django
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

def generar_html_situacion():
    """Genera el HTML explicando la situación"""
    
    html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Diario Oficial - 21 de Julio 2025</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; background-color: #f6f8fb;">
    <table cellpadding="0" cellspacing="0" width="100%" style="background-color: #f6f8fb;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                <table cellpadding="0" cellspacing="0" width="600" style="background-color: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(90deg, #2563eb 0%, #6366f1 100%); padding: 32px 40px;">
                            <h1 style="margin: 0 0 8px 0; color: white; font-size: 28px;">Informe Diario Oficial</h1>
                            <p style="margin: 0; color: white; font-size: 16px; opacity: 0.9;">21 de Julio, 2025 - Edición N° 44.204</p>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 32px 40px;">
                            <!-- Alerta -->
                            <table cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 24px;">
                                <tr>
                                    <td style="background-color: #fef3c7; border: 1px solid #fcd34d; border-radius: 8px; padding: 16px;">
                                        <h3 style="margin: 0 0 8px 0; color: #92400e; font-size: 18px;">⚠️ Situación Especial</h3>
                                        <p style="margin: 0; color: #78350f; line-height: 1.5;">
                                            Al intentar acceder a la edición del 21 de julio de 2025, el sitio web oficial del Diario Oficial 
                                            muestra el mensaje: <strong>"No existen publicaciones en esta edición en la fecha seleccionada"</strong>.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Análisis Técnico -->
                            <h2 style="color: #334155; font-size: 20px; margin-bottom: 16px;">Análisis Técnico Realizado</h2>
                            
                            <table cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 24px;">
                                <tr>
                                    <td style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px;">
                                        <p style="margin: 0 0 12px 0; color: #475569; line-height: 1.6;">
                                            Se realizaron múltiples intentos de acceso utilizando diferentes métodos:
                                        </p>
                                        <ul style="margin: 0; padding-left: 20px; color: #475569;">
                                            <li style="margin-bottom: 8px;">✓ Acceso directo vía HTTP con diferentes user agents</li>
                                            <li style="margin-bottom: 8px;">✓ Uso de herramientas como curl y wget</li>
                                            <li style="margin-bottom: 8px;">✓ Selenium con undetected-chromedriver</li>
                                            <li style="margin-bottom: 8px;">✓ Verificación de URLs alternativas y formatos de fecha</li>
                                            <li style="margin-bottom: 8px;">✓ Búsqueda de PDFs del sumario e impreso</li>
                                        </ul>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Resultados -->
                            <h2 style="color: #334155; font-size: 20px; margin-bottom: 16px;">Resultados Obtenidos</h2>
                            
                            <table cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 24px;">
                                <tr>
                                    <td style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px;">
                                        <table cellpadding="5" cellspacing="0" width="100%">
                                            <tr>
                                                <td style="color: #64748b; padding: 8px 0; border-bottom: 1px solid #e2e8f0;">
                                                    <strong>URL Principal:</strong>
                                                </td>
                                                <td style="color: #475569; padding: 8px 0; border-bottom: 1px solid #e2e8f0;">
                                                    Muestra "No existen publicaciones"
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="color: #64748b; padding: 8px 0; border-bottom: 1px solid #e2e8f0;">
                                                    <strong>PDF Sumario:</strong>
                                                </td>
                                                <td style="color: #475569; padding: 8px 0; border-bottom: 1px solid #e2e8f0;">
                                                    Error 404 (No encontrado)
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="color: #64748b; padding: 8px 0; border-bottom: 1px solid #e2e8f0;">
                                                    <strong>PDF Impreso:</strong>
                                                </td>
                                                <td style="color: #475569; padding: 8px 0; border-bottom: 1px solid #e2e8f0;">
                                                    Error 403 (Prohibido)
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="color: #64748b; padding: 8px 0;">
                                                    <strong>Protección detectada:</strong>
                                                </td>
                                                <td style="color: #475569; padding: 8px 0;">
                                                    Sí (TSPD/Akamai en algunos casos)
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Posibles Explicaciones -->
                            <h2 style="color: #334155; font-size: 20px; margin-bottom: 16px;">Posibles Explicaciones</h2>
                            
                            <table cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 24px;">
                                <tr>
                                    <td style="background-color: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 20px;">
                                        <ol style="margin: 0; padding-left: 20px; color: #0369a1;">
                                            <li style="margin-bottom: 12px;">
                                                <strong>Edición sin publicaciones:</strong> Es posible que la edición 44.204 exista 
                                                formalmente pero no contenga publicaciones (similar a una página en blanco).
                                            </li>
                                            <li style="margin-bottom: 12px;">
                                                <strong>Publicación pendiente:</strong> Las publicaciones podrían estar en proceso 
                                                de carga y aún no disponibles en el sitio web.
                                            </li>
                                            <li style="margin-bottom: 12px;">
                                                <strong>Acceso restringido:</strong> Podría existir alguna restricción temporal 
                                                o geográfica para acceder al contenido.
                                            </li>
                                            <li>
                                                <strong>Día especial:</strong> El 21 de julio podría ser una fecha con 
                                                características especiales en el calendario oficial.
                                            </li>
                                        </ol>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Recomendación -->
                            <table cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 24px;">
                                <tr>
                                    <td style="background-color: #dbeafe; border: 1px solid #60a5fa; border-radius: 8px; padding: 20px; text-align: center;">
                                        <p style="margin: 0; color: #1e40af; font-size: 16px; font-weight: bold;">
                                            Recomendación
                                        </p>
                                        <p style="margin: 8px 0 0 0; color: #1e3a8a; line-height: 1.5;">
                                            Se sugiere verificar directamente en el sitio web oficial del Diario Oficial<br>
                                            o contactar con la institución para confirmar el estado de esta edición.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Footer -->
                            <table cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td style="text-align: center; padding-top: 24px; border-top: 1px solid #e2e8f0;">
                                        <p style="margin: 0; color: #94a3b8; font-size: 14px;">
                                            Este informe fue generado automáticamente el 21 de julio de 2025<br>
                                            basado en el análisis técnico del sitio web oficial.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    return html

def enviar_email(html_content):
    """Envía el email con el informe"""
    
    # Configuración directa SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "fernandezcamilog@gmail.com"
    smtp_password = "xcep ldqx rydi tawl"
    
    destinatario = "ifernaandeez@gmail.com"
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Informe Diario Oficial - 21 de Julio 2025 (Situación Especial)"
    msg['From'] = smtp_user
    msg['To'] = destinatario
    
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    try:
        print("Conectando al servidor SMTP...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        print("Enviando email...")
        server.send_message(msg)
        server.quit()
        
        print("✅ Email enviado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== GENERANDO INFORME DE SITUACIÓN ===\n")
    
    # Generar HTML
    html = generar_html_situacion()
    
    # Guardar copia local
    filename = "informe_situacion_21_julio_2025.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 Informe guardado en: {filename}")
    
    # Enviar por email
    print("\n📧 Enviando informe por email...")
    if enviar_email(html):
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n⚠️  El informe fue generado pero no se pudo enviar por email")