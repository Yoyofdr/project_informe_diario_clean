from django.core.management.base import BaseCommand
from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

class Command(BaseCommand):
    help = 'Scrapea el sumario del Diario Oficial de hoy y lo muestra por consola.'

    def handle(self, *args, **kwargs):
        sumario = obtener_sumario_diario_oficial()
        for entrada in sumario:
            self.stdout.write(f"Título: {entrada['titulo']}")
            self.stdout.write(f"PDF: {entrada['url_pdf']}")
            self.stdout.write("-") 