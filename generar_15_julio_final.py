#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
from dotenv import load_dotenv
load_dotenv()
django.setup()

from django.core.mail import EmailMessage
from django.conf import settings
from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
from enviar_informe_diario import generar_informe_email

# Fecha objetivo
fecha = "15-07-2025"
print(f"Generando informe FINAL para {fecha}...")

# Intentar obtener datos del caché primero
resultado = obtener_sumario_diario_oficial(fecha, force_refresh=False)
print(f"Total documentos: {resultado.get('total_documentos', 0)}")
print(f"Publicaciones relevantes: {len(resultado.get('publicaciones', []))}")

# Si no hay datos, forzar actualización
if resultado.get('total_documentos', 0) == 0:
    print("Sin datos en caché, forzando actualización...")
    resultado = obtener_sumario_diario_oficial(fecha, force_refresh=True)

# Generar HTML
html_content = generar_informe_email(fecha)

# Guardar localmente
filename = f"informe_final_15_07_2025.html"
with open(filename, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Informe guardado: {filename}")

# Enviar por email
subject = f'Informe Diario Oficial - {fecha} (FINAL)'
from_email = settings.DEFAULT_FROM_EMAIL

msg = EmailMessage(
    subject,
    '',
    from_email,
    ['rfernandezdelrio@uc.cl']
)
msg.content_subtype = 'html'
msg.body = html_content
msg.send()

print(f"✓ Informe del {fecha} enviado exitosamente")