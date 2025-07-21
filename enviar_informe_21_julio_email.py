#!/usr/bin/env python
"""
Script para enviar el informe del 21 de julio por email
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from alerts.models import Destinatario

def enviar_informe_21_julio():
    """Envía el informe del 21 de julio por correo electrónico"""
    
    # Leer el informe HTML generado
    filename = "informe_diario_oficial_21_07_2025_completo.html"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Obtener destinatarios de la base de datos
        destinatarios = Destinatario.objects.all()
        
        if not destinatarios:
            # Si no hay destinatarios en BD, usar email por defecto
            emails = ['rfernandezdelrio@uc.cl']
            print("No se encontraron destinatarios en la base de datos. Enviando al email por defecto.")
        else:
            emails = [d.email for d in destinatarios]
            print(f"Enviando a {len(emails)} destinatarios de la base de datos")
        
        # Preparar el email
        asunto = "Informe Diario Oficial - 21 de julio de 2025 - Edición N° 44.204"
        
        # Crear versión de texto plano
        mensaje_texto = """
Informe Diario Oficial
Lunes 21 de julio de 2025
Edición N° 44.204

RESUMEN:
- 47 documentos publicados
- 5 publicaciones relevantes
- 1 licitación pública

PUBLICACIONES DESTACADAS:
1. Ley de inclusión laboral de personas con discapacidad
2. Actualización de valores UF
3. Reglamento de protección de datos en comercio electrónico
4. Modificación documentos tributarios electrónicos
5. Tipos de cambio del Banco Central

VALORES DEL DÍA:
- Dólar: $943.28
- Euro: $1,026.45
- UF: $38,073.52

Para ver el informe completo con todos los detalles, abra el archivo HTML adjunto.
"""
        
        # Enviar a cada destinatario
        enviados = 0
        errores = 0
        
        for email in emails:
            try:
                print(f"Enviando a: {email}")
                
                send_mail(
                    subject=asunto,
                    message=mensaje_texto,
                    from_email='rodrigo@carvuk.com',
                    recipient_list=[email],
                    html_message=html_content,
                    fail_silently=False
                )
                
                enviados += 1
                print(f"✓ Enviado exitosamente a {email}")
                
            except Exception as e:
                errores += 1
                print(f"✗ Error enviando a {email}: {str(e)}")
        
        # Resumen final
        print(f"\n{'='*50}")
        print(f"RESUMEN DE ENVÍO:")
        print(f"- Enviados exitosamente: {enviados}")
        print(f"- Errores: {errores}")
        print(f"- Total destinatarios: {len(emails)}")
        print(f"{'='*50}")
        
        return enviados > 0
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filename}")
        return False
    except Exception as e:
        print(f"Error general: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Iniciando envío del informe del 21 de julio de 2025...")
    exito = enviar_informe_21_julio()
    
    if exito:
        print("\n✓ Informe enviado exitosamente")
    else:
        print("\n✗ Error al enviar el informe")