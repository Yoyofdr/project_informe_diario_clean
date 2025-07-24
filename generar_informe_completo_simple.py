#!/usr/bin/env python3
"""
Generador de informe completo simplificado
Sin dependencias de Django, actualiza enlaces CMF automáticamente
"""

import json
import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import subprocess

# Configurar Django si es necesario
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
import django
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

def actualizar_enlaces_cmf(fecha):
    """
    Ejecuta el scraper CMF para actualizar los enlaces
    """
    # Convertir fecha al formato del scraper
    fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
    fecha_scraper = fecha_obj.strftime("%d/%m/%Y")
    
    print(f"Actualizando enlaces CMF para {fecha_scraper}...")
    
    # Ejecutar scraper
    resultado = subprocess.run(
        ['python', 'scraper_cmf_mejorado.py', fecha_scraper],
        capture_output=True,
        text=True
    )
    
    if resultado.returncode == 0:
        print("✅ Enlaces CMF actualizados")
    else:
        print("⚠️ Error al actualizar enlaces CMF")
        print(resultado.stderr)

def generar_informe_completo(fecha=None):
    """
    Genera informe completo con Diario Oficial + CMF
    """
    if not fecha:
        fecha = datetime.now().strftime("%d-%m-%Y")
    
    print(f"\n=== GENERANDO INFORME COMPLETO DEL {fecha} ===\n")
    
    # 1. Actualizar enlaces CMF
    actualizar_enlaces_cmf(fecha)
    
    # 2. Obtener datos del Diario Oficial
    print("\n1. Obteniendo datos del Diario Oficial...")
    resultado_diario = obtener_sumario_diario_oficial(fecha)
    
    # 3. Obtener hechos CMF del JSON actualizado
    print("\n2. Obteniendo hechos CMF...")
    hechos_cmf = []
    try:
        with open('hechos_cmf_selenium_reales.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
            todos_hechos = datos.get('hechos', [])
        
        # Filtrar por fecha
        hechos_cmf = [h for h in todos_hechos if h.get('fecha') == fecha]
        hechos_cmf.sort(key=lambda x: -x.get('relevancia', 0))
        hechos_cmf = hechos_cmf[:10]  # Top 10
        
        print(f"   - Hechos CMF encontrados: {len(hechos_cmf)}")
        
    except Exception as e:
        print(f"   ⚠️ Error al leer hechos CMF: {str(e)}")
    
    # 4. Generar HTML
    print("\n3. Generando informe HTML...")
    html = generar_html_completo(fecha, resultado_diario, hechos_cmf)
    
    # 5. Guardar archivo
    filename = f"informe_completo_{fecha.replace('-', '_')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"   📄 Informe guardado en: {filename}")
    
    # 6. Enviar por email
    print("\n4. Enviando por email...")
    enviar_informe(html, fecha)
    
    return True

def generar_html_completo(fecha, resultado_diario, hechos_cmf):
    """
    Genera el HTML completo del informe
    """
    # Formatear fecha
    fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
    fecha_formato = fecha_obj.strftime("%d de %B, %Y").replace("July", "Julio")
    
    # Obtener datos del Diario Oficial
    publicaciones = resultado_diario.get('publicaciones', [])
    normas_generales = [p for p in publicaciones if p.get('seccion') == 'Normas Generales']
    valores_monedas = resultado_diario.get('valores_monedas', {})
    
    # Inicio del HTML
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Diario • {fecha}</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f8fafc; color: #1e293b; line-height: 1.6;">
    
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8fafc;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                
                <table width="672" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); overflow: hidden;">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 48px 32px; text-align: center;">
                            <h1 style="margin: 0 0 8px 0; font-size: 28px; font-weight: 700; color: #ffffff; letter-spacing: -0.025em;">
                                Informe Diario
                            </h1>
                            <p style="margin: 0; color: #cbd5e1; font-size: 14px; font-weight: 500;">
                                {fecha_formato}
                            </p>
                        </td>
                    </tr>
                    
                    <tr>
                        <td style="padding: 32px;">"""
    
    # Sección Diario Oficial
    if normas_generales:
        html += """
                            <!-- NORMAS GENERALES -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 40px;">
                                <tr>
                                    <td>
                                        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #eff6ff;">
                                            <tr>
                                                <td>
                                                    <h2 style="margin: 0 0 2px 0; font-size: 18px; font-weight: 600; color: #1e293b;">
                                                        NORMAS GENERALES
                                                    </h2>
                                                    <p style="margin: 0; font-size: 14px; color: #6b7280;">
                                                        Leyes, decretos supremos y resoluciones de alcance general
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>"""
        
        for pub in normas_generales[:3]:
            html += f"""
                                <tr>
                                    <td style="padding-bottom: 16px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;">
                                            <tr>
                                                <td style="padding: 24px; border-top: 3px solid #6b7280; border-radius: 12px 12px 0 0;">
                                                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                                        {pub.get('titulo', '')}
                                                    </h3>
                                                    <p style="margin: 0 0 16px 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        {pub.get('resumen', '')}
                                                    </p>
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="background-color: #6b7280; border-radius: 6px;">
                                                                <a href="{pub.get('url_pdf', '#')}" style="display: inline-block; padding: 10px 20px; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500;">
                                                                    Ver documento oficial
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>"""
        
        html += "</table>"
    
    # Sección CMF
    if hechos_cmf:
        html += """
                            <!-- HECHOS ESENCIALES CMF -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 40px;">
                                <tr>
                                    <td>
                                        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #eff6ff;">
                                            <tr>
                                                <td>
                                                    <h2 style="margin: 0 0 2px 0; font-size: 18px; font-weight: 600; color: #1e293b;">
                                                        HECHOS ESENCIALES - CMF
                                                    </h2>
                                                    <p style="margin: 0; font-size: 14px; color: #7c3aed;">
                                                        Información relevante del mercado de valores
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>"""
        
        for hecho in hechos_cmf:
            # Usar el enlace directo si está disponible
            url_hecho = hecho.get('url_pdf', 'https://www.cmfchile.cl/institucional/hechos/hechos.php')
            
            html += f"""
                                <tr>
                                    <td style="padding-bottom: 16px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;">
                                            <tr>
                                                <td style="padding: 24px; border-top: 3px solid #7c3aed; border-radius: 12px 12px 0 0;">
                                                    <h3 style="margin: 0 0 8px 0; font-size: 18px; font-weight: 600; color: #1e293b;">
                                                        {hecho.get('entidad', '')}
                                                    </h3>
                                                    <div style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600; color: #6b7280;">
                                                        {hecho.get('titulo', hecho.get('materia', ''))}
                                                    </div>
                                                    <p style="margin: 0 0 16px 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        {hecho.get('resumen', '')}
                                                    </p>
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="background-color: #7c3aed; border-radius: 6px;">
                                                                <a href="{url_hecho}" style="display: inline-block; padding: 10px 20px; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500;">
                                                                    Ver hecho esencial
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>"""
        
        html += "</table>"
    
    # Valores de monedas
    if valores_monedas:
        html += f"""
                            <!-- VALORES DE MONEDAS -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 40px;">
                                <tr>
                                    <td>
                                        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #eff6ff;">
                                            <tr>
                                                <td>
                                                    <h2 style="margin: 0 0 2px 0; font-size: 18px; font-weight: 600; color: #1e293b;">
                                                        Valores del Día
                                                    </h2>
                                                    <p style="margin: 0; font-size: 14px; color: #2563eb;">
                                                        Tipos de cambio oficiales
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <table width="100%" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td width="50%" style="padding: 16px; background-color: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; text-align: center;">
                                                    <div style="font-size: 14px; color: #0369a1; margin-bottom: 4px;">Dólar Observado</div>
                                                    <div style="font-size: 24px; font-weight: 700; color: #0c4a6e;">{valores_monedas.get('dolar_observado', 'N/A')}</div>
                                                </td>
                                                <td width="8"></td>
                                                <td width="50%" style="padding: 16px; background-color: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; text-align: center;">
                                                    <div style="font-size: 14px; color: #0369a1; margin-bottom: 4px;">Euro</div>
                                                    <div style="font-size: 24px; font-weight: 700; color: #0c4a6e;">{valores_monedas.get('euro', 'N/A')}</div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>"""
    
    # Footer
    html += """
                        </td>
                    </tr>
                    
                    <tr>
                        <td style="background-color: #f8fafc; padding: 24px 32px; text-align: center; border-top: 1px solid #e2e8f0;">
                            <p style="margin: 0; font-size: 13px; color: #64748b; line-height: 1.5;">
                                Información obtenida directamente de fuentes oficiales
                            </p>
                        </td>
                    </tr>
                    
                </table>
                
            </td>
        </tr>
    </table>
    
</body>
</html>"""
    
    return html

def enviar_informe(html, fecha):
    """
    Envía el informe por email
    """
    # Configuración
    de_email = "rodrigo@carvuk.com"
    para_email = "rfernandezdelrio@uc.cl"
    password = "swqjlcwjaoooyzcb"
    
    # Formatear fecha para el asunto
    fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
    fecha_formato = fecha_obj.strftime("%d de %B, %Y").replace("July", "Julio")
    
    # Crear mensaje
    msg = MIMEMultipart('alternative')
    msg['From'] = de_email
    msg['To'] = para_email
    msg['Subject'] = f"Informe Diario • {fecha_formato}"
    
    # Agregar contenido HTML
    html_part = MIMEText(html, 'html', 'utf-8')
    msg.attach(html_part)
    
    try:
        # Enviar
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(de_email, password)
        server.send_message(msg)
        server.quit()
        
        print("\n✅ INFORME ENVIADO EXITOSAMENTE!")
        print(f"   De: {de_email}")
        print(f"   Para: {para_email}")
        
    except Exception as e:
        print(f"\n❌ Error al enviar email: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fecha = sys.argv[1]  # Formato: DD-MM-YYYY
        generar_informe_completo(fecha)
    else:
        generar_informe_completo()