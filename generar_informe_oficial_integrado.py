#!/usr/bin/env python
"""
Script para generar informe integrado con contenido del Diario Oficial, SII y CMF
Uso: python generar_informe_oficial_integrado.py [fecha]
"""
import os
import sys
import django
from datetime import datetime, timedelta
import argparse

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from django.utils import timezone
from django.template import engines
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Importar scrapers
from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
from alerts.scraper_sii import obtener_novedades_tributarias_sii
from alerts.models import HechoEsencial, DocumentoSII

def obtener_hechos_cmf_dia_anterior(fecha):
    """Obtiene los hechos esenciales CMF del día anterior"""
    try:
        # Convertir fecha string a datetime
        fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
        # CMF muestra hechos del día anterior (T-1)
        fecha_anterior = fecha_obj - timedelta(days=1)
        
        # Obtener hechos de esa fecha
        hechos = HechoEsencial.objects.filter(
            fecha_publicacion__date=fecha_anterior.date(),
            resumen__isnull=False  # Solo con resumen
        ).exclude(
            categoria='RUTINARIO'  # Excluir rutinarios
        ).select_related('empresa').order_by(
            '-relevancia_profesional',  # Ordenar por relevancia
            '-fecha_publicacion'
        )[:12]  # Máximo 12 hechos
        
        # Formatear para la plantilla
        hechos_formateados = []
        for hecho in hechos:
            # Emoji según categoría
            emoji_map = {
                'CRITICO': '🔴',
                'IMPORTANTE': '🟡',
                'MODERADO': '🟢'
            }
            emoji = emoji_map.get(hecho.categoria, '')
            
            hechos_formateados.append({
                'empresa': hecho.empresa.nombre,
                'titulo': hecho.titulo,
                'resumen': hecho.resumen,
                'url': hecho.url,
                'categoria': hecho.categoria,
                'categoria_emoji': emoji,
                'relevancia': hecho.relevancia_profesional,
                'es_ipsa': hecho.es_empresa_ipsa
            })
            
        return hechos_formateados
        
    except Exception as e:
        print(f'[WARNING] Error obteniendo hechos CMF: {str(e)}')
        return []

def organizar_secciones_dof(publicaciones):
    """Organiza las publicaciones del Diario Oficial por secciones"""
    secciones_dict = {
        'NORMAS GENERALES': {
            'nombre': 'NORMAS GENERALES',
            'descripcion': 'Leyes, decretos supremos y resoluciones de alcance general',
            'publicaciones': []
        },
        'NORMAS PARTICULARES': {
            'nombre': 'NORMAS PARTICULARES', 
            'descripcion': 'Resoluciones específicas, nombramientos y concesiones',
            'publicaciones': []
        },
        'AVISOS DESTACADOS': {
            'nombre': 'AVISOS DESTACADOS',
            'descripcion': 'Licitaciones, concursos públicos y avisos importantes',
            'publicaciones': []
        }
    }
    
    for pub in publicaciones:
        seccion = pub.get('seccion', 'NORMAS GENERALES').upper()
        if seccion in secciones_dict:
            secciones_dict[seccion]['publicaciones'].append(pub)
    
    # Retornar solo secciones con contenido
    return [s for s in secciones_dict.values() if s['publicaciones']]

def generar_informe_integrado(fecha=None, no_enviar=False):
    """
    Genera y envía el informe integrado
    
    Args:
        fecha (str): Fecha en formato DD-MM-YYYY. Si no se proporciona, usa hoy.
        no_enviar (bool): Si es True, no envía el email
    """
    
    if fecha is None:
        fecha = datetime.now().strftime("%d-%m-%Y")
    
    print(f"\n{'='*60}")
    print(f"GENERANDO INFORME INTEGRADO - {fecha}")
    print(f"{'='*60}\n")
    
    # 1. OBTENER DATOS DEL DIARIO OFICIAL
    print("1. Obteniendo datos del Diario Oficial...")
    resultado_dof = obtener_sumario_diario_oficial(fecha)
    
    if not resultado_dof:
        print("❌ Error: No se obtuvieron resultados del Diario Oficial")
        return False
        
    publicaciones_dof = resultado_dof.get('publicaciones', [])
    valores_monedas = resultado_dof.get('valores_monedas', {})
    total_documentos = resultado_dof.get('total_documentos', 0)
    
    print(f"   ✓ {len(publicaciones_dof)} publicaciones relevantes")
    
    # 2. OBTENER DATOS DEL SII
    print("\n2. Obteniendo novedades del SII...")
    try:
        resultado_sii = obtener_novedades_tributarias_sii(fecha)
        circulares_sii = resultado_sii.get('circulares', [])
        resoluciones_sii = resultado_sii.get('resoluciones', [])
        print(f"   ✓ {len(circulares_sii)} circulares, {len(resoluciones_sii)} resoluciones")
    except Exception as e:
        print(f"   ✗ Error obteniendo datos SII: {str(e)}")
        circulares_sii = []
        resoluciones_sii = []
    
    # 3. OBTENER HECHOS ESENCIALES CMF
    print("\n3. Obteniendo hechos esenciales CMF...")
    hechos_cmf = obtener_hechos_cmf_dia_anterior(fecha)
    print(f"   ✓ {len(hechos_cmf)} hechos relevantes")
    
    # 4. ORGANIZAR CONTENIDO POR SECCIONES
    print("\n4. Organizando contenido...")
    
    # Secciones del Diario Oficial
    secciones_dof = organizar_secciones_dof(publicaciones_dof)
    
    # 5. GENERAR HTML
    print("\n5. Generando HTML...")
    
    # Preparar contexto
    fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_formato = f"{fecha_obj.day} de {meses[fecha_obj.month]}, {fecha_obj.year}"
    
    # Obtener número de edición
    edicion = resultado_dof.get('edicion', 'N/A')
    
    context = {
        'fecha': fecha,
        'fecha_formato': fecha_formato,
        'edicion_numero': edicion,
        'total_documentos': total_documentos,
        'publicaciones_relevantes': len(publicaciones_dof),
        'secciones': secciones_dof,
        'valores_monedas': valores_monedas,
        # Contenido SII
        'circulares_sii': circulares_sii,
        'resoluciones_sii': resoluciones_sii,
        # Contenido CMF
        'hechos_cmf': hechos_cmf
    }
    
    # Renderizar plantilla
    with open('templates/informe_diario_oficial_plantilla.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    django_engine = engines['django']
    template = django_engine.from_string(template_content)
    html = template.render(context)
    
    # Guardar archivo
    filename = f"informe_integrado_{fecha.replace('-', '_')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"   ✓ Archivo guardado: {filename}")
    
    # 6. ENVIAR EMAIL
    if not no_enviar:
        print("\n6. Enviando email...")
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Informe Integrado - {fecha_formato} (Edición {edicion})"
            msg['From'] = "rodrigo@carvuk.com"
            msg['To'] = "rfernandezdelrio@uc.cl"
            
            html_part = MIMEText(html, 'html')
            msg.attach(html_part)
            
            # Enviar
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("rodrigo@carvuk.com", os.environ.get('EMAIL_PASSWORD', 'swqjlcwjaoooyzcb'))
            server.send_message(msg)
            server.quit()
            
            print("   ✓ Email enviado exitosamente")
            
        except Exception as e:
            print(f"   ✗ Error enviando email: {str(e)}")
    else:
        print("\n6. Email NO enviado (--no-enviar activado)")
        
    print("\n✅ PROCESO COMPLETADO")
    return True

if __name__ == "__main__":
    # Parser de argumentos
    parser = argparse.ArgumentParser(description='Genera informe integrado del Diario Oficial, SII y CMF')
    parser.add_argument('fecha', nargs='?', help='Fecha en formato DD-MM-YYYY (por defecto: hoy)')
    parser.add_argument('--no-enviar', action='store_true', help='No enviar el email, solo generar el HTML')
    
    args = parser.parse_args()
    
    generar_informe_integrado(args.fecha, args.no_enviar)