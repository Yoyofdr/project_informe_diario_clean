from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
from alerts.informe_diario import generar_informe_html
from datetime import datetime
from django.conf import settings
from alerts.models import Destinatario, Organizacion, Empresa, InformeEnviado

class Command(BaseCommand):
    help = 'Genera el informe diario del Diario Oficial y lo envía por correo a todos los destinatarios.'

    def add_arguments(self, parser):
        parser.add_argument('--fecha', type=str, help='Fecha en formato dd-mm-aaaa (opcional)')
        parser.add_argument('--test', action='store_true', help='Enviar un HTML mínimo de prueba')

    def handle(self, *args, **options):
        fecha = options.get('fecha')
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@carvuk.com')
        destinatarios = Destinatario.objects.values_list('email', flat=True)
        if not destinatarios:
            self.stdout.write(self.style.WARNING('No hay destinatarios registrados.'))
            return

        if options.get('test'):
            # Datos de ejemplo para el test visual
            publicaciones = [
                {
                    'titulo': 'Ejemplo de hecho relevante',
                    'resumen': 'Este es un resumen de ejemplo para mostrar el diseño del informe diario.',
                    'url_pdf': 'https://www.diariooficial.interior.gob.cl/documento/ejemplo.pdf',
                    'categoria': 'otros',
                }
            ]
            valores_monedas = {'dolar': '950,00', 'euro': '1050,00'}
            total_documentos = 1
            html = generar_informe_html(publicaciones, fecha, valores_monedas, documentos_analizados=total_documentos)
            text = "Informe Diario Oficial (prueba): ver versión HTML."
        else:
            resultados = obtener_sumario_diario_oficial(fecha)
            publicaciones = resultados["publicaciones"]
            valores_monedas = resultados["valores_monedas"]
            total_documentos = resultados.get("total_documentos", None)
            if total_documentos is None:
                # Fallback: usar publicaciones si no está implementado en el scraper
                total_documentos = len(publicaciones)
            print("[DEBUG] total_documentos:", total_documentos)
            # Si el scraping falla (no hay publicaciones y total_documentos es 0), NO enviar correo al cliente
            if not publicaciones and (total_documentos == 0 or total_documentos is None):
                print("[INFO] Scraping falló o no hay contenido. No se enviará correo al cliente.")
                return  # Salir sin enviar nada
            html = generar_informe_html(publicaciones, fecha, valores_monedas, documentos_analizados=total_documentos)
            print("[DEBUG] HTML generado:\n", html[:1000], "...\n[fin HTML]")
            text = f"Informe Diario Oficial {fecha or ''}: ver versión HTML."

        subject = f"Informe Diario Oficial - {fecha or datetime.now().strftime('%d-%m-%Y')}"
        # Agrupar destinatarios por organización
        orgs = {}
        for dest in Destinatario.objects.select_related('organizacion').all():
            org = dest.organizacion
            if org not in orgs:
                orgs[org] = []
            orgs[org].append(dest.email)
        for org, emails in orgs.items():
            # Buscar empresa asociada por nombre (si existe)
            empresa = Empresa.objects.filter(nombre__iexact=org.nombre).first()
            if not empresa:
                continue  # Si no hay empresa asociada, omitir
            for email in emails:
                msg = EmailMultiAlternatives(subject, text, from_email, [email])
                msg.attach_alternative(html, "text/html")
                msg.send()
                self.stdout.write(self.style.SUCCESS(f"Correo enviado a {email} (from: {from_email})"))
            # Guardar registro en InformeEnviado (un registro por organización/empresa)
            InformeEnviado.objects.create(
                empresa=empresa,
                destinatarios=", ".join(emails),
                enlace_html="",  # Si guardas el HTML en disco, pon la ruta aquí
                resumen=text
            ) 