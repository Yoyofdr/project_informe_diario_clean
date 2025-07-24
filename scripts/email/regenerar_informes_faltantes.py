#!/usr/bin/env python3
"""
Script para regenerar informes con problemas
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
from enviar_informe_diario import generar_informe_email

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def regenerar_y_enviar(fechas, destinatario='rfernandezdelrio@uc.cl'):
    """Regenera y envía informes específicos"""
    
    for fecha in fechas:
        try:
            logger.info(f"\n{'='*50}")
            logger.info(f"Regenerando informe del {fecha} con force_refresh=True")
            
            # Primero, obtener datos frescos del scraper
            resultado = obtener_sumario_diario_oficial(fecha, force_refresh=True)
            
            logger.info(f"Resultados del scraper:")
            logger.info(f"  - Total documentos: {resultado.get('total_documentos', 0)}")
            logger.info(f"  - Publicaciones relevantes: {len(resultado.get('publicaciones', []))}")
            
            # Generar el informe HTML
            html_content = generar_informe_email(fecha)
            
            # Guardar copia local
            filename = f"informe_corregido_{fecha.replace('-', '_')}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info(f"Informe guardado: {filename}")
            
            # Enviar por email
            subject = f'Informe Diario Oficial - {fecha} (CORREGIDO)'
            from_email = settings.DEFAULT_FROM_EMAIL
            
            msg = EmailMessage(
                subject,
                '',
                from_email,
                [destinatario]
            )
            msg.content_subtype = 'html'
            msg.body = html_content
            msg.send()
            
            logger.info(f"✓ Enviado informe corregido del {fecha}")
            
        except Exception as e:
            logger.error(f"Error con fecha {fecha}: {str(e)}")
            continue

if __name__ == "__main__":
    # Fechas problemáticas
    fechas = ["12-07-2025", "14-07-2025", "15-07-2025"]
    
    logger.info("=== REGENERANDO INFORMES CON PROBLEMAS ===")
    regenerar_y_enviar(fechas)
    logger.info("\n=== PROCESO COMPLETADO ===")