#!/usr/bin/env python
"""
Script para generar el informe del Diario Oficial con diseño profesional tipo newsletter
Basado en las mejores prácticas de diseño de email 2025
"""
import os
import sys
import django
from datetime import datetime
from collections import defaultdict
from utils_fecha import formatear_fecha_espanol

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

def generar_informe_html(fecha):
    """Genera el informe en formato HTML con diseño profesional de newsletter"""
    
    print(f"Generando informe profesional para: {fecha}")
    
    # Obtener datos del scraper
    resultado = obtener_sumario_diario_oficial(fecha, force_refresh=True)
    
    publicaciones = resultado.get('publicaciones', [])
    valores_monedas = resultado.get('valores_monedas', {})
    total_documentos = resultado.get('total_documentos', 0)
    
    # Organizar publicaciones por sección
    publicaciones_por_seccion = defaultdict(list)
    for pub in publicaciones:
        seccion = pub.get('seccion', 'Sin sección').upper()
        
        # Normalizar nombres de secciones
        if 'NORMAS GENERALES' in seccion:
            seccion = 'NORMAS GENERALES'
        elif 'NORMAS PARTICULARES' in seccion:
            seccion = 'NORMAS PARTICULARES'
        elif 'AVISOS' in seccion or 'DESTACADO' in seccion:
            seccion = 'AVISOS DESTACADOS'
        
        publicaciones_por_seccion[seccion].append(pub)
    
    # Definir orden de secciones
    orden_secciones = ['NORMAS GENERALES', 'NORMAS PARTICULARES', 'AVISOS DESTACADOS']
    
    # HTML template profesional tipo newsletter
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Informe Diario Oficial - {fecha}</title>
    <!--[if mso]>
    <noscript>
        <xml>
            <o:OfficeDocumentSettings>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
    <style>
        /* Reset Styles */
        body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
        table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
        img {{ -ms-interpolation-mode: bicubic; }}
        
        /* Remove default styling */
        img {{ border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
        table {{ border-collapse: collapse !important; }}
        body {{ height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }}
        
        /* Mobile Styles */
        @media screen and (max-width: 600px) {{
            .mobile-hide {{ display: none !important; }}
            .mobile-center {{ text-align: center !important; }}
            .container {{ width: 100% !important; max-width: 100% !important; }}
            .mobile-padding {{ padding: 20px !important; }}
            .stat-container {{ width: 100% !important; display: block !important; }}
            .stat-box {{ margin-bottom: 20px !important; }}
        }}
        
        /* Dark Mode Support */
        @media (prefers-color-scheme: dark) {{
            .dark-mode-bg {{ background-color: #1a1a1a !important; }}
            .dark-mode-text {{ color: #ffffff !important; }}
        }}
    </style>
</head>
<body style="margin: 0 !important; padding: 0 !important; background-color: #f4f4f4;">
    
    <!-- Hidden Preheader Text -->
    <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
        Resumen del Diario Oficial - {fecha}: {len(publicaciones)} publicaciones relevantes
    </div>
    
    <!-- Email Container -->
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td align="center" style="padding: 40px 0;">
                
                <!-- Email Content Container -->
                <table class="container" align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td align="center" style="padding: 40px 20px; background-color: #1e293b; border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 28px; font-weight: 300; color: #ffffff; letter-spacing: -0.5px;">
                                Informe Diario Oficial
                            </h1>
                            <p style="margin: 10px 0 0 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 16px; color: #94a3b8;">
                                {formatear_fecha_espanol(fecha)}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Stats Section -->
                    <tr>
                        <td style="padding: 30px 20px; background-color: #f8fafc; border-bottom: 1px solid #e2e8f0;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td class="stat-container" width="50%" style="text-align: center;">
                                        <div class="stat-box">
                                            <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 32px; font-weight: 700; color: #1e293b;">
                                                {total_documentos}
                                            </p>
                                            <p style="margin: 5px 0 0 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 14px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">
                                                Documentos Analizados
                                            </p>
                                        </div>
                                    </td>
                                    <td class="stat-container" width="50%" style="text-align: center;">
                                        <div class="stat-box">
                                            <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 32px; font-weight: 700; color: #1e293b;">
                                                {len(publicaciones)}
                                            </p>
                                            <p style="margin: 5px 0 0 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 14px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">
                                                Publicaciones Relevantes
                                            </p>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
"""
    
    # Si no hay publicaciones
    if not publicaciones:
        html += """
                    <!-- Empty State -->
                    <tr>
                        <td align="center" style="padding: 60px 20px;">
                            <p style="margin: 0 0 10px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 48px;">
                                📄
                            </p>
                            <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 18px; color: #64748b;">
                                No se encontraron publicaciones relevantes para esta fecha.
                            </p>
                        </td>
                    </tr>
"""
    else:
        # Agregar publicaciones por sección
        for seccion in orden_secciones:
            if seccion in publicaciones_por_seccion and publicaciones_por_seccion[seccion]:
                pubs = publicaciones_por_seccion[seccion]
                
                # Header de sección
                html += f"""
                    <!-- Section: {seccion} -->
                    <tr>
                        <td style="padding: 30px 20px 20px 20px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">
                                        <h2 style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 20px; font-weight: 600; color: #1e293b; float: left;">
                                            {seccion.title()}
                                        </h2>
                                        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 14px; color: #94a3b8; float: right;">
                                            {len(pubs)} publicacion{'es' if len(pubs) != 1 else ''}
                                        </span>
                                        <div style="clear: both;"></div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
"""
                
                # Publicaciones de la sección
                for i, pub in enumerate(pubs):
                    es_licitacion = 'licitación' in pub.get('titulo', '').lower()
                    es_ultima = (i == len(pubs) - 1)
                    
                    html += f"""
                    <!-- Publication -->
                    <tr>
                        <td style="padding: 0 20px {20 if not es_ultima else 30}px 20px;">
                            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8fafc; border-radius: 6px;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <h3 style="margin: 0 0 12px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                            {pub.get('titulo', 'Sin título')}
                                            {f'<span style="display: inline-block; margin-left: 10px; padding: 3px 8px; background-color: #3b82f6; color: #ffffff; font-size: 11px; font-weight: 600; border-radius: 3px; text-transform: uppercase; vertical-align: middle;">Licitación</span>' if es_licitacion else ''}
                                        </h3>
                                        <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 14px; color: #64748b; line-height: 1.6;">
                                            {pub.get('resumen') if pub.get('resumen') and pub.get('resumen') != 'No se pudo generar un resumen relevante.' else 'Resumen no disponible.'}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
"""
    
    # Agregar valores de monedas
    if valores_monedas:
        html += f"""
                    <!-- Currency Values -->
                    <tr>
                        <td style="padding: 30px 20px; background-color: #1e293b;">
                            <h2 style="margin: 0 0 20px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 600; color: #ffffff; text-align: center;">
                                Valores de Referencia del Día
                            </h2>
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td width="50%" style="text-align: center; padding: 0 10px;">
                                        <p style="margin: 0 0 5px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">
                                            Dólar Observado
                                        </p>
                                        <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 24px; font-weight: 700; color: #ffffff;">
                                            ${valores_monedas.get('dolar', 'N/A')}
                                        </p>
                                    </td>
                                    <td width="50%" style="text-align: center; padding: 0 10px;">
                                        <p style="margin: 0 0 5px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">
                                            Euro
                                        </p>
                                        <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 24px; font-weight: 700; color: #ffffff;">
                                            ${valores_monedas.get('euro', 'N/A')}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
"""
    
    html += """
                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding: 30px 20px; background-color: #f8fafc; border-radius: 0 0 8px 8px;">
                            <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 13px; color: #94a3b8; line-height: 1.5;">
                                Información obtenida directamente del sitio diariooficial.interior.gob.cl
                            </p>
                        </td>
                    </tr>
                    
                </table>
                <!-- End Email Content Container -->
                
            </td>
        </tr>
    </table>
    <!-- End Email Container -->
    
</body>
</html>
"""
    
    return html

# Ejecutar
if __name__ == "__main__":
    import sys
    
    # Permitir especificar fecha como argumento
    if len(sys.argv) > 1:
        fecha_hoy = sys.argv[1]
    else:
        fecha_hoy = "18-07-2025"
    
    html = generar_informe_html(fecha_hoy)
    
    # Guardar el HTML
    filename = f"informe_profesional_{fecha_hoy.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nInforme generado: {filename}")
    print(f"Diseño profesional tipo newsletter con:")
    print("- Compatibilidad total con clientes de email")
    print("- Diseño responsive para móviles")
    print("- Tablas HTML para máxima compatibilidad")
    print("- Estilos inline para renderizado correcto")
    print("- Dark mode support")