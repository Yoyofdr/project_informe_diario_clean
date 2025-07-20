#!/usr/bin/env python3
"""
Script para generar y enviar múltiples informes con el nuevo formato
"""
import os
import sys
import django
from datetime import datetime
import logging
import time

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
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar la función generar_informe_email desde enviar_informe_diario.py
from enviar_informe_diario import generar_informe_email

def enviar_informes_rango(fechas, destinatario='rfernandezdelrio@uc.cl'):
    """Genera y envía informes para un rango de fechas"""
    
    informes_enviados = []
    errores = []
    
    for fecha in fechas:
        try:
            logger.info(f"\n{'='*50}")
            logger.info(f"Procesando informe del {fecha}")
            
            # Generar el informe
            html_content = generar_informe_email(fecha)
            
            # Guardar copia local
            filename = f"informe_historico_{fecha.replace('-', '_')}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info(f"Informe guardado: {filename}")
            
            # Enviar por email
            subject = f'Informe Diario Oficial - {fecha}'
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
            
            logger.info(f"✓ Enviado: {fecha}")
            informes_enviados.append(fecha)
            
            # Esperar un poco entre envíos para no saturar
            time.sleep(2)
            
        except Exception as e:
            error_msg = f"Error con fecha {fecha}: {str(e)}"
            logger.error(error_msg)
            errores.append(error_msg)
            continue
    
    # Resumen final
    logger.info(f"\n{'='*50}")
    logger.info("RESUMEN FINAL")
    logger.info(f"Informes enviados: {len(informes_enviados)}/{len(fechas)}")
    if informes_enviados:
        logger.info(f"Fechas exitosas: {', '.join(informes_enviados)}")
    if errores:
        logger.error(f"Errores encontrados: {len(errores)}")
        for error in errores:
            logger.error(f"  - {error}")
    
    return informes_enviados, errores

if __name__ == "__main__":
    # Fechas del 11 al 19 de julio
    fechas = [
        "11-07-2025",
        "12-07-2025",
        "13-07-2025",  # Sábado - podría no haber edición
        "14-07-2025",
        "15-07-2025",
        "16-07-2025",
        "17-07-2025",
        "18-07-2025",
        "19-07-2025"
    ]
    
    logger.info("=== INICIANDO GENERACIÓN DE INFORMES HISTÓRICOS ===")
    logger.info(f"Fechas a procesar: {', '.join(fechas)}")
    logger.info(f"Destinatario: rfernandezdelrio@uc.cl")
    
    enviados, errores = enviar_informes_rango(fechas)
    
    logger.info("\n=== PROCESO COMPLETADO ===")
    sys.exit(0 if not errores else 1)