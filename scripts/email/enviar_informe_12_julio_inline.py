#!/usr/bin/env python
"""
Script para generar y enviar el informe del 12 de julio con estilos inline para email
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')

# Cargar variables del .env ANTES de django.setup()
from dotenv import load_dotenv
load_dotenv()

django.setup()

from django.core.mail import EmailMessage
from django.conf import settings
from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
from utils_fecha import formatear_fecha_espanol
from collections import defaultdict

def generar_informe_email(fecha):
    """Genera el informe en formato HTML con estilos inline para email"""
    
    print(f"Generando informe para email: {fecha}")
    
    # Obtener datos del scraper
    resultado = obtener_sumario_diario_oficial(fecha, force_refresh=True)
    
    publicaciones = resultado.get('publicaciones', [])
    valores_monedas = resultado.get('valores_monedas', {})
    total_documentos = resultado.get('total_documentos', 0)
    
    # Organizar publicaciones por sección
    publicaciones_por_seccion = defaultdict(list)
    for pub in publicaciones:
        seccion = pub.get('seccion', 'Sin sección').upper()
        if 'NORMAS GENERALES' in seccion:
            seccion = 'NORMAS GENERALES'
        elif 'NORMAS PARTICULARES' in seccion:
            seccion = 'NORMAS PARTICULARES'
        elif 'AVISOS' in seccion or 'DESTACADO' in seccion:
            seccion = 'AVISOS DESTACADOS'
        publicaciones_por_seccion[seccion].append(pub)
    
    secciones_config = {
        'NORMAS GENERALES': 'Normativas de aplicación general',
        'NORMAS PARTICULARES': 'Normativas específicas y sectoriales',
        'AVISOS DESTACADOS': 'Avisos de interés público y licitaciones'
    }
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diario Oficial • {fecha}</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f8fafc; color: #1e293b; line-height: 1.6;">
    
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8fafc;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                
                <!-- Wrapper -->
                <table width="672" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); overflow: hidden;">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 48px 32px; text-align: center;">
                            <h1 style="margin: 0 0 8px 0; font-size: 28px; font-weight: 700; color: #ffffff; letter-spacing: -0.025em;">
                                Diario Oficial
                            </h1>
                            <p style="margin: 0; color: #cbd5e1; font-size: 14px; font-weight: 500;">
                                {formatear_fecha_espanol(fecha)}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Stats -->
                    <tr>
                        <td style="background: linear-gradient(90deg, #eff6ff 0%, #eef2ff 100%); border-bottom: 1px solid #dbeafe;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td width="50%" style="text-align: center; padding: 24px; border-right: 1px solid #dbeafe;">
                                        <div style="font-size: 32px; font-weight: 700; line-height: 1; margin-bottom: 4px; color: #1d4ed8;">
                                            {total_documentos}
                                        </div>
                                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #2563eb;">
                                            Total Documentos
                                        </div>
                                    </td>
                                    <td width="50%" style="text-align: center; padding: 24px;">
                                        <div style="font-size: 32px; font-weight: 700; line-height: 1; margin-bottom: 4px; color: #059669;">
                                            {len(publicaciones)}
                                        </div>
                                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #059669;">
                                            Relevantes
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 32px;">
"""
    
    if not publicaciones:
        html += """
                            <p style="text-align: center; padding: 60px 32px; color: #64748b; font-size: 16px;">
                                No se encontraron publicaciones relevantes para esta fecha.
                            </p>
"""
    else:
        orden_secciones = ['NORMAS GENERALES', 'NORMAS PARTICULARES', 'AVISOS DESTACADOS']
        
        for seccion in orden_secciones:
            if seccion in publicaciones_por_seccion and publicaciones_por_seccion[seccion]:
                pubs = publicaciones_por_seccion[seccion]
                subtitle = secciones_config.get(seccion, '')
                
                html += f"""
                            <!-- {seccion} -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 40px;">
                                <tr>
                                    <td>
                                        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #eff6ff;">
                                            <tr>
                                                <td>
                                                    <h2 style="margin: 0 0 2px 0; font-size: 18px; font-weight: 600; color: #1e293b;">
                                                        {seccion.title()}
                                                    </h2>
                                                    <p style="margin: 0; font-size: 14px; color: #2563eb;">
                                                        {subtitle}
                                                    </p>
                                                </td>
                                                <td align="right">
                                                    <span style="font-size: 14px; color: #6366f1; font-weight: 500;">
                                                        {len(pubs)} elemento{'s' if len(pubs) != 1 else ''}
                                                    </span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
"""
                
                for pub in pubs:
                    es_licitacion = 'licitación' in pub.get('titulo', '').lower()
                    
                    html += f"""
                                <tr>
                                    <td style="padding-bottom: 16px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;">
                                            <tr>
                                                <td style="padding: 24px; border-top: 3px solid #3b82f6; border-radius: 12px 12px 0 0;">
                                                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                                        {pub.get('titulo', 'Sin título')}
                                                        {f'<span style="display: inline-block; padding: 4px 8px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; border-radius: 4px; margin-left: 8px; background-color: #dbeafe; color: #1e40af;">Licitación</span>' if es_licitacion else ''}
                                                    </h3>
                                                    <p style="margin: 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        {pub.get('resumen', 'Resumen no disponible.')}
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
"""
                
                html += """
                            </table>
"""
    
    html += """
                        </td>
                    </tr>
"""
    
    # Valores de monedas
    if valores_monedas:
        html += f"""
                    <!-- Currency Values -->
                    <tr>
                        <td style="padding: 0 32px 32px 32px;">
                            <table width="100%" cellpadding="0" cellspacing="0" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;">
                                <tr>
                                    <td style="padding: 24px; text-align: center;">
                                        <h3 style="margin: 0 0 16px 0; font-size: 14px; font-weight: 600; color: #1e293b; text-transform: uppercase; letter-spacing: 0.05em;">
                                            Valores de Referencia del Día
                                        </h3>
                                        <table width="100%" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td width="50%" style="text-align: center; padding: 0 8px;">
                                                    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 16px;">
                                                        <div style="font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
                                                            Dólar Observado
                                                        </div>
                                                        <div style="font-size: 24px; font-weight: 700; color: #1e293b;">
                                                            ${valores_monedas.get('dolar', 'N/A')}
                                                        </div>
                                                    </div>
                                                </td>
                                                <td width="50%" style="text-align: center; padding: 0 8px;">
                                                    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 16px;">
                                                        <div style="font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
                                                            Euro
                                                        </div>
                                                        <div style="font-size: 24px; font-weight: 700; color: #1e293b;">
                                                            ${valores_monedas.get('euro', 'N/A')}
                                                        </div>
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
"""
    
    html += """
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8fafc; padding: 24px 32px; text-align: center; border-top: 1px solid #e2e8f0;">
                            <p style="margin: 0; font-size: 13px; color: #64748b; line-height: 1.5;">
                                Información obtenida directamente del sitio diariooficial.interior.gob.cl
                            </p>
                        </td>
                    </tr>
                    
                </table>
                <!-- End Wrapper -->
                
            </td>
        </tr>
    </table>
    
</body>
</html>
"""
    
    return html

# Ejecutar
fecha = "12-07-2025"
print(f"Generando informe del {fecha} con estilos inline para email...")

try:
    html_content = generar_informe_email(fecha)
    
    # Guardar localmente
    filename = f"informe_email_{fecha.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✓ Informe guardado como: {filename}")
    
    # Configurar el email
    subject = f'Informe Diario Oficial - {fecha}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['rfernandezdelrio@uc.cl']
    
    # Crear el mensaje
    msg = EmailMessage(
        subject,
        '',
        from_email,
        recipient_list
    )
    
    # Establecer el contenido HTML
    msg.content_subtype = 'html'
    msg.body = html_content
    
    # Enviar
    print("Enviando email...")
    msg.send()
    print(f"✓ Informe del {fecha} reenviado exitosamente con formato correcto")
    
except Exception as e:
    print(f"✗ Error: {e}")