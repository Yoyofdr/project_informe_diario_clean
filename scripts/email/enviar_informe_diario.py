#!/usr/bin/env python
"""
Script principal para envío diario del informe del Diario Oficial
Versión mejorada con el diseño Bolt refinado y resúmenes cortos
"""
import os
import sys
import django
from datetime import datetime
import logging

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')

# Cargar variables del .env
from dotenv import load_dotenv
load_dotenv()

django.setup()

from django.core.mail import EmailMessage
from django.conf import settings
from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
from utils_fecha import formatear_fecha_espanol
from collections import defaultdict

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('informe_diario.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def generar_informe_email(fecha):
    """Genera el informe en formato HTML con estilos inline para email"""
    
    logger.info(f"Generando informe para: {fecha}")
    
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
                                                    <p style="margin: 0 0 16px 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        {pub.get('resumen', 'Resumen no disponible.')}
                                                    </p>
                                                    <a href="{pub.get('url_pdf', '#')}" style="display: inline-flex; align-items: center; padding: 8px 16px; background-color: #3b82f6; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500; border-radius: 6px; transition: background-color 0.2s;">
                                                        <svg style="width: 16px; height: 16px; margin-right: 8px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                                        </svg>
                                                        Ver documento oficial
                                                    </a>
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

def main():
    """Función principal para envío diario"""
    try:
        # Obtener fecha de hoy
        fecha = datetime.now().strftime("%d-%m-%Y")
        logger.info(f"=== INICIANDO ENVÍO DIARIO DEL {fecha} ===")
        
        # Generar el informe
        html_content = generar_informe_email(fecha)
        
        # Guardar copia local
        filename = f"informe_{fecha.replace('-', '_')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info(f"Informe guardado localmente: {filename}")
        
        # Configurar el email
        subject = f'Informe Diario Oficial - {fecha}'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Lista de destinatarios desde la base de datos
        from alerts.models import Destinatario
        destinatarios = list(Destinatario.objects.values_list('email', flat=True))
        
        if not destinatarios:
            logger.warning("No hay destinatarios registrados en la base de datos")
            destinatarios = ['rfernandezdelrio@uc.cl']  # Fallback
        
        # Enviar a cada destinatario
        enviados = 0
        errores = []
        
        for email in destinatarios:
            try:
                msg = EmailMessage(
                    subject,
                    '',
                    from_email,
                    [email]
                )
                msg.content_subtype = 'html'
                msg.body = html_content
                msg.send()
                logger.info(f"✓ Enviado a: {email}")
                enviados += 1
            except Exception as e:
                error_msg = f"Error enviando a {email}: {str(e)}"
                logger.error(error_msg)
                errores.append(error_msg)
        
        # Resumen
        logger.info(f"=== RESUMEN ===")
        logger.info(f"Enviados: {enviados}/{len(destinatarios)}")
        if errores:
            logger.error(f"Errores: {len(errores)}")
            for error in errores:
                logger.error(f"  - {error}")
        
        logger.info(f"=== ENVÍO COMPLETADO ===\n")
        
        # Retornar estado para scripts externos
        return 0 if not errores else 1
        
    except Exception as e:
        logger.error(f"ERROR CRÍTICO: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())