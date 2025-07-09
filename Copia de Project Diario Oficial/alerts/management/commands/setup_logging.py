"""
Comando para configurar el sistema de logging estructurado
"""
from django.core.management.base import BaseCommand
from alerts.utils.logging_config import setup_logging
import os


class Command(BaseCommand):
    help = 'Configura el sistema de logging estructurado'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--level',
            type=str,
            default='INFO',
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            help='Nivel de logging'
        )
        parser.add_argument(
            '--structured',
            action='store_true',
            default=True,
            help='Usar formato JSON estructurado'
        )
        parser.add_argument(
            '--traditional',
            action='store_true',
            help='Usar formato tradicional de texto'
        )
        parser.add_argument(
            '--log-dir',
            type=str,
            default='logs',
            help='Directorio para guardar los logs'
        )
    
    def handle(self, *args, **options):
        # Determinar formato
        structured = not options['traditional']
        
        # Configurar logging
        setup_logging(
            log_level=options['level'],
            log_dir=options['log_dir'],
            structured=structured
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Sistema de logging configurado:\n"
                f"- Nivel: {options['level']}\n"
                f"- Formato: {'JSON estructurado' if structured else 'Tradicional'}\n"
                f"- Directorio: {options['log_dir']}"
            )
        )
        
        # Crear ejemplo de uso
        import logging
        logger = logging.getLogger('alerts.test')
        
        logger.debug("Mensaje de debug")
        logger.info("Mensaje informativo", extra={'user': 'admin', 'action': 'setup_logging'})
        logger.warning("Mensaje de advertencia")
        
        self.stdout.write(
            self.style.SUCCESS(
                "\nPrueba de logging realizada. Revisa los archivos en el directorio de logs."
            )
        )