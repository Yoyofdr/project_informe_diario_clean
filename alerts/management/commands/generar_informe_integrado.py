"""
Comando para generar informe integrado con contenido del Diario Oficial, SII y CMF
"""
import os
import sys
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Importar scrapers
from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
from alerts.scraper_sii import obtener_novedades_tributarias_sii
from alerts.models import HechoEsencial, DocumentoSII

class Command(BaseCommand):
    help = 'Genera un informe integrado con contenido del Diario Oficial, SII y CMF'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fecha',
            type=str,
            help='Fecha del informe en formato DD-MM-YYYY (por defecto: hoy)'
        )
        parser.add_argument(
            '--no-enviar',
            action='store_true',
            help='No enviar el email, solo generar el HTML'
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Modo debug con más información'
        )

    def handle(self, *args, **options):
        # Configurar fecha
        if options['fecha']:
            fecha = options['fecha']
        else:
            fecha = datetime.now().strftime("%d-%m-%Y")
            
        self.debug = options.get('debug', False)
        no_enviar = options.get('no_enviar', False)
        
        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        self.stdout.write(self.style.SUCCESS(f'GENERANDO INFORME INTEGRADO - {fecha}'))
        self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))
        
        # 1. OBTENER DATOS DEL DIARIO OFICIAL
        self.stdout.write('1. Obteniendo datos del Diario Oficial...')
        resultado_dof = obtener_sumario_diario_oficial(fecha)
        
        if not resultado_dof:
            self.stdout.write(self.style.ERROR('Error: No se obtuvieron resultados del Diario Oficial'))
            return
            
        publicaciones_dof = resultado_dof.get('publicaciones', [])
        valores_monedas = resultado_dof.get('valores_monedas', {})
        total_documentos = resultado_dof.get('total_documentos', 0)
        
        self.stdout.write(self.style.SUCCESS(f'   ✓ {len(publicaciones_dof)} publicaciones relevantes'))
        
        # 2. OBTENER DATOS DEL SII
        self.stdout.write('\n2. Obteniendo novedades del SII...')
        try:
            resultado_sii = obtener_novedades_tributarias_sii(fecha)
            circulares_sii = resultado_sii.get('circulares', [])
            resoluciones_sii = resultado_sii.get('resoluciones', [])
            self.stdout.write(self.style.SUCCESS(f'   ✓ {len(circulares_sii)} circulares, {len(resoluciones_sii)} resoluciones'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'   ✗ Error obteniendo datos SII: {str(e)}'))
            circulares_sii = []
            resoluciones_sii = []
        
        # 3. OBTENER HECHOS ESENCIALES CMF
        self.stdout.write('\n3. Obteniendo hechos esenciales CMF...')
        hechos_cmf = self.obtener_hechos_cmf_dia_anterior(fecha)
        self.stdout.write(self.style.SUCCESS(f'   ✓ {len(hechos_cmf)} hechos relevantes'))
        
        # 4. ORGANIZAR CONTENIDO POR SECCIONES
        self.stdout.write('\n4. Organizando contenido...')
        
        # Secciones del Diario Oficial
        secciones_dof = self.organizar_secciones_dof(publicaciones_dof)
        
        # 5. GENERAR HTML
        self.stdout.write('\n5. Generando HTML...')
        
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
        try:
            html = render_to_string('informe_diario_oficial_plantilla.html', context)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error renderizando plantilla: {str(e)}'))
            # Fallback: leer plantilla directamente
            template_path = os.path.join(settings.BASE_DIR, 'templates', 'informe_diario_oficial_plantilla.html')
            with open(template_path, 'r', encoding='utf-8') as f:
                from django.template import Template, Context
                template = Template(f.read())
                html = template.render(Context(context))
        
        # Guardar archivo
        filename = f"informe_integrado_{fecha.replace('-', '_')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        self.stdout.write(self.style.SUCCESS(f'   ✓ Archivo guardado: {filename}'))
        
        # 6. ENVIAR EMAIL
        if not no_enviar:
            self.stdout.write('\n6. Enviando email...')
            self.enviar_email(html, fecha_formato, edicion)
        else:
            self.stdout.write(self.style.WARNING('\n6. Email NO enviado (--no-enviar activado)'))
            
        self.stdout.write(self.style.SUCCESS('\n✅ PROCESO COMPLETADO'))

    def obtener_hechos_cmf_dia_anterior(self, fecha):
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
            
            # Contar por categoría para debug
            if self.debug:
                criticos = hechos.filter(categoria='CRITICO').count()
                importantes = hechos.filter(categoria='IMPORTANTE').count()
                moderados = hechos.filter(categoria='MODERADO').count()
                self.stdout.write(f'   CMF: {criticos} críticos, {importantes} importantes, {moderados} moderados')
            
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
            self.stdout.write(self.style.WARNING(f'Error obteniendo hechos CMF: {str(e)}'))
            return []

    def organizar_secciones_dof(self, publicaciones):
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

    def enviar_email(self, html, fecha_formato, edicion):
        """Envía el informe por email"""
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
            
            self.stdout.write(self.style.SUCCESS('   ✓ Email enviado exitosamente'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Error enviando email: {str(e)}'))