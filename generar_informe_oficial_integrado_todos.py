#!/usr/bin/env python3
"""
Generador de informe oficial integrado para TODOS los suscriptores
Basado en generar_informe_oficial_integrado_mejorado.py
"""

import json
import os
import sys
import django
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import logging
from pathlib import Path

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

# Importar modelos Django
from django.contrib.auth.models import User
from alerts.models import Destinatario, Organizacion, InformeEnviado

# Importar scrapers
from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
from scraper_cmf_mejorado import ScraperCMFMejorado
from alerts.cmf_criterios_profesionales import filtrar_hechos_profesional, get_icono_categoria
from alerts.scraper_sii import obtener_circulares_sii, obtener_resoluciones_exentas_sii, obtener_jurisprudencia_administrativa_sii
from alerts.cmf_resumenes_ai import generar_resumen_cmf

# Importar funciones originales
from generar_informe_oficial_integrado_mejorado import (
    obtener_publicaciones_sii_dia,
    obtener_hechos_cmf_dia,
    generar_html_informe
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def obtener_destinatarios_activos():
    """
    Obtiene todos los destinatarios activos para el informe diario
    """
    destinatarios = []
    
    # 1. Usuarios registrados con email verificado
    usuarios_activos = User.objects.filter(
        is_active=True,
        email__isnull=False
    ).exclude(email='')
    
    for usuario in usuarios_activos:
        destinatarios.append({
            'nombre': f"{usuario.first_name} {usuario.last_name}".strip() or usuario.username,
            'email': usuario.email,
            'tipo': 'usuario_registrado'
        })
    
    # 2. Destinatarios de organizaciones con suscripción activa
    organizaciones_activas = Organizacion.objects.filter(suscripcion_activa=True)
    
    for org in organizaciones_activas:
        for dest in org.destinatarios.all():
            destinatarios.append({
                'nombre': dest.nombre,
                'email': dest.email,
                'tipo': 'organizacion',
                'organizacion': org.nombre
            })
    
    # Eliminar duplicados por email
    emails_unicos = {}
    for dest in destinatarios:
        if dest['email'] not in emails_unicos:
            emails_unicos[dest['email']] = dest
    
    return list(emails_unicos.values())

def enviar_informe_email_masivo(html, fecha, destinatarios):
    """
    Envía el informe por email a múltiples destinatarios
    """
    # Configuración desde variables de entorno
    de_email = os.getenv('EMAIL_FROM', 'contacto@informediariochile.cl')
    de_nombre = os.getenv('EMAIL_FROM_NAME', 'Informe Diario Chile')
    password = os.getenv('HOSTINGER_EMAIL_PASSWORD', '')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.hostinger.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    
    # Verificar que tenemos la contraseña
    if not password:
        logger.error("❌ Error: No se encontró la contraseña del email")
        logger.error("   Asegúrate de tener el archivo .env con HOSTINGER_EMAIL_PASSWORD")
        return
    
    # Formatear fecha para el asunto
    fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_formato = f"{fecha_obj.day} de {meses[fecha_obj.month]}, {fecha_obj.year}"
    
    # Conectar al servidor SMTP una sola vez
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(de_email, password)
        logger.info("✅ Conectado al servidor SMTP")
    except Exception as e:
        logger.error(f"❌ Error conectando al servidor SMTP: {str(e)}")
        return
    
    # Estadísticas
    enviados = 0
    errores = 0
    
    # Enviar a cada destinatario
    for dest in destinatarios:
        try:
            # Crear mensaje personalizado
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{de_nombre} <{de_email}>"
            msg['To'] = dest['email']
            msg['Subject'] = f"Informe Diario • {fecha_formato}"
            
            # Personalizar HTML con link de desuscripción
            html_personalizado = html
            
            # Agregar footer personalizado antes del cierre del body
            footer_personalizado = f"""
                <div style="text-align: center; padding: 20px; font-size: 12px; color: #666;">
                    <p>Este informe fue enviado a {dest['email']}</p>
                    <p><a href="https://informediariochile.cl/unsubscribe?email={dest['email']}" 
                          style="color: #666; text-decoration: underline;">Cancelar suscripción</a></p>
                </div>
            """
            html_personalizado = html_personalizado.replace('</body>', footer_personalizado + '</body>')
            
            # Adjuntar HTML
            html_part = MIMEText(html_personalizado, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar
            server.send_message(msg)
            enviados += 1
            logger.info(f"✅ Enviado a {dest['nombre']} <{dest['email']}>")
            
        except Exception as e:
            errores += 1
            logger.error(f"❌ Error enviando a {dest['email']}: {str(e)}")
    
    # Cerrar conexión
    try:
        server.quit()
    except:
        pass
    
    # Resumen
    logger.info(f"\n📊 Resumen de envío:")
    logger.info(f"   ✅ Enviados: {enviados}")
    logger.info(f"   ❌ Errores: {errores}")
    logger.info(f"   📧 Total destinatarios: {len(destinatarios)}")
    
    # Registrar en base de datos
    if enviados > 0:
        try:
            # Buscar o crear empresa "Informe Diario"
            from alerts.models import Empresa
            empresa, created = Empresa.objects.get_or_create(
                nombre="Informe Diario Oficial",
                defaults={'rut': '00000000-0'}
            )
            
            # Registrar envío
            InformeEnviado.objects.create(
                empresa=empresa,
                destinatarios=f"{enviados} destinatarios",
                resumen=f"Informe del {fecha_formato} enviado a {enviados} destinatarios"
            )
        except Exception as e:
            logger.error(f"Error registrando envío: {e}")

def generar_informe_oficial_masivo(fecha=None):
    """
    Genera y envía el informe oficial a TODOS los suscriptores
    """
    if not fecha:
        fecha = datetime.now().strftime("%d-%m-%Y")
    
    logger.info(f"🚀 Generando informe masivo para {fecha}")
    
    # 1. Obtener destinatarios
    destinatarios = obtener_destinatarios_activos()
    
    if not destinatarios:
        logger.warning("⚠️  No hay destinatarios activos")
        return False
    
    logger.info(f"📧 Destinatarios encontrados: {len(destinatarios)}")
    
    # 2. Obtener datos del Diario Oficial
    logger.info("Obteniendo datos del Diario Oficial...")
    resultado_diario = obtener_sumario_diario_oficial(fecha)
    
    # 3. Obtener hechos CMF
    logger.info("Obteniendo hechos CMF...")
    hechos_cmf = obtener_hechos_cmf_dia(fecha)
    
    # 4. Obtener publicaciones del SII
    logger.info("Obteniendo publicaciones del SII...")
    try:
        publicaciones_sii = obtener_publicaciones_sii_dia(fecha)
    except Exception as e:
        logger.error(f"Error obteniendo SII: {e}")
        publicaciones_sii = []
    
    # 5. Generar HTML del informe
    html = generar_html_informe(fecha, resultado_diario, hechos_cmf, publicaciones_sii)
    
    # 6. Guardar copia local
    filename = f"informe_diario_masivo_{fecha.replace('-', '_')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    logger.info(f"Informe guardado en: {filename}")
    
    # 7. Enviar a todos los destinatarios
    enviar_informe_email_masivo(html, fecha, destinatarios)
    
    return True

if __name__ == "__main__":
    import sys
    
    # Verificar si es domingo
    if datetime.now().weekday() == 6:
        logger.info("🚫 Es domingo - no se envían informes")
        sys.exit(0)
    
    if len(sys.argv) > 1:
        fecha = sys.argv[1]  # Formato: DD-MM-YYYY
        generar_informe_oficial_masivo(fecha)
    else:
        generar_informe_oficial_masivo()