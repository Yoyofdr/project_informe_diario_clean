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
            html = "<h1>Test de HTML</h1><p>Esto es una prueba de visualización.</p>"
            text = "Test de HTML: Esto es una prueba de visualización."
        else:
            resultados = obtener_sumario_diario_oficial(fecha)
            publicaciones = resultados["publicaciones"]
            valores_monedas = resultados["valores_monedas"]
            html = generar_informe_html(publicaciones, fecha, valores_monedas)
            text = f"Informe Diario Oficial {fecha or ''}: ver versión HTML."

        subject = f"Informe Diario Oficial - {fecha or datetime.now().strftime('%d-%m-%Y')}"
        # Agrupar destinatarios por organización
        orgs = {}
        for dest in Destinatario.objects.select_related('organizacion').all():
            org = dest.organizacion
            if org not in orgs:
                orgs[org] = []
            orgs[org].append(dest.email)
        
        # Pre-cargar todas las empresas para evitar múltiples consultas
        org_nombres = [org.nombre for org in orgs.keys()]
        empresas_dict = {}
        for empresa in Empresa.objects.filter(nombre__in=org_nombres):
            empresas_dict[empresa.nombre.lower()] = empresa
        
        for org, emails in orgs.items():
            # Buscar empresa asociada por nombre (si existe)
            empresa = empresas_dict.get(org.nombre.lower())
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