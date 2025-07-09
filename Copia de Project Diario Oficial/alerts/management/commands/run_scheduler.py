import time
from django.core.management.base import BaseCommand
from django.core.management import call_command
import schedule
import datetime

def job(task_name, command_name):
    """Ejecuta un comando de Django y registra la hora."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Iniciando tarea: '{task_name}'...")
    try:
        call_command(command_name)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Tarea '{task_name}' finalizada exitosamente.")
    except Exception as e:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Error al ejecutar la tarea '{task_name}': {e}")


class Command(BaseCommand):
    help = 'Inicia el programador de tareas para buscar y notificar hechos esenciales.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando el programador...'))

        # Programar las tareas
        schedule.every(30).minutes.do(job, task_name="Scraping de Hechos Esenciales", command_name='scrape_hechos')
        schedule.every(30).minutes.do(job, task_name="Envío de Notificaciones", command_name='send_notifications')

        self.stdout.write(self.style.SUCCESS('Tareas programadas para ejecutarse cada 30 minutos (MODO DE PRUEBA).'))
        self.stdout.write(self.style.SUCCESS('Presiona CTRL+C para detener el programador.'))

        while True:
            schedule.run_pending()
            time.sleep(1) 