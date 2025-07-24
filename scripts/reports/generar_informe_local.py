#!/usr/bin/env python
"""
Script para generar el informe del Diario Oficial localmente en HTML
sin depender del sistema de email
"""

import os
import sys
import django
from datetime import datetime

# Configurar el entorno Django
sys.path.append('/Users/rodrigofernandezdelrio/Desktop/Project Diario Oficial')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.management.commands.informe_diario_oficial import Command as InformeCommand
from alerts.informe_diario import InformeDiario

def generar_informe_local():
    """Genera el informe del Diario Oficial y lo guarda como archivo HTML"""
    
    print("=== GENERADOR DE INFORME DIARIO OFICIAL ===")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    try:
        # Crear instancia del comando
        comando = InformeCommand()
        
        # Ejecutar el scraping
        print("1. Ejecutando scraping del Diario Oficial...")
        avisos = comando.scrapear_diario_oficial()
        
        if not avisos:
            print("⚠️  No se encontraron avisos en el Diario Oficial de hoy")
            return
        
        print(f"✅ Se encontraron {len(avisos)} avisos")
        
        # Generar el informe
        print("\n2. Generando informe HTML...")
        informe = InformeDiario()
        contenido_html = informe.generar_informe_diario_oficial(avisos)
        
        # Guardar el informe
        fecha_str = datetime.now().strftime('%Y-%m-%d')
        nombre_archivo = f"informe_diario_oficial_{fecha_str}.html"
        ruta_archivo = os.path.join('/Users/rodrigofernandezdelrio/Desktop/Project Diario Oficial', nombre_archivo)
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_html)
        
        print(f"\n✅ INFORME GENERADO EXITOSAMENTE")
        print(f"📄 Archivo guardado en: {ruta_archivo}")
        print(f"\n🌐 Para ver el informe, abre el archivo en tu navegador:")
        print(f"   file://{ruta_archivo}")
        
        # Mostrar resumen del contenido
        print(f"\n📊 RESUMEN DEL INFORME:")
        print(f"   - Total de avisos: {len(avisos)}")
        
        # Contar avisos por categoría si es posible
        categorias = {}
        for aviso in avisos:
            cat = aviso.get('categoria', 'Sin categoría')
            categorias[cat] = categorias.get(cat, 0) + 1
        
        if categorias:
            print("   - Avisos por categoría:")
            for cat, count in sorted(categorias.items()):
                print(f"     • {cat}: {count}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        print("\nDetalles del error:")
        import traceback
        traceback.print_exc()
        
        print("\n💡 Sugerencias:")
        print("1. Verifica que el scraper esté funcionando correctamente")
        print("2. Asegúrate de tener conexión a internet")
        print("3. Verifica que ChromeDriver esté instalado y actualizado")

def mostrar_opciones_adicionales():
    """Muestra opciones adicionales para el usuario"""
    print("\n" + "=" * 50)
    print("OPCIONES ADICIONALES:")
    print("1. Para probar el envío por email, ejecuta: python test_email_config.py")
    print("2. Para enviar el informe manualmente, ejecuta: python enviar_informe_hoy.py")
    print("3. Para configurar el envío automático, revisa: INSTRUCCIONES_ENVIO_AUTOMATICO.md")

if __name__ == "__main__":
    generar_informe_local()
    mostrar_opciones_adicionales()