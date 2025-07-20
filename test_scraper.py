#!/usr/bin/env python
"""
Script de prueba para verificar el funcionamiento del scraper del Diario Oficial
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

def test_scraper():
    """Prueba el scraper con la fecha actual"""
    print("=== PRUEBA DEL SCRAPER DEL DIARIO OFICIAL ===\n")
    
    # Probar con fecha actual
    fecha_hoy = datetime.now().strftime("%d-%m-%Y")
    print(f"Probando con fecha: {fecha_hoy}")
    print("-" * 50)
    
    try:
        resultado = obtener_sumario_diario_oficial(fecha=fecha_hoy)
        
        if resultado:
            publicaciones = resultado.get('publicaciones', [])
            valores_monedas = resultado.get('valores_monedas', {})
            total_documentos = resultado.get('total_documentos', 0)
            
            print(f"\nTotal de documentos encontrados: {total_documentos}")
            print(f"Publicaciones relevantes: {len(publicaciones)}")
            
            if valores_monedas:
                print(f"\nValores de monedas:")
                print(f"  - Dólar: ${valores_monedas.get('dolar', 'No disponible')}")
                print(f"  - Euro: ${valores_monedas.get('euro', 'No disponible')}")
            
            if publicaciones:
                print(f"\n=== PUBLICACIONES ENCONTRADAS ===")
                for i, pub in enumerate(publicaciones, 1):
                    print(f"\n{i}. {pub['titulo']}")
                    print(f"   Sección: {pub.get('seccion', 'N/A')}")
                    print(f"   Relevante: {'Sí' if pub.get('relevante') else 'No'}")
                    print(f"   URL: {pub['url_pdf']}")
                    if pub.get('resumen'):
                        print(f"   Resumen: {pub['resumen'][:200]}...")
            else:
                print("\nNo se encontraron publicaciones relevantes.")
        else:
            print("\nERROR: No se obtuvo resultado del scraper")
            
    except Exception as e:
        print(f"\nERROR durante la ejecución del scraper: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n=== FIN DE LA PRUEBA ===")

if __name__ == "__main__":
    test_scraper()