#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial_mejorado import obtener_sumario_diario_oficial
from datetime import datetime

def test_scraper(fecha_str, force_refresh=True):
    """Prueba el scraper mejorado para una fecha específica"""
    print(f"\n{'='*60}")
    print(f"Probando scraper mejorado para fecha: {fecha_str}")
    print(f"{'='*60}\n")
    
    try:
        # Ejecutar scraping
        resultado = obtener_sumario_diario_oficial(fecha=fecha_str, force_refresh=force_refresh)
        
        if not resultado or not isinstance(resultado, dict):
            print("ERROR: No se obtuvo resultado del scraping")
            return
        
        publicaciones = resultado.get('publicaciones', [])
        valores_monedas = resultado.get('valores_monedas', {})
        total_documentos = resultado.get('total_documentos', 0)
        
        # Mostrar resumen
        print(f"\nTotal documentos en el Diario: {total_documentos}")
        print(f"Publicaciones relevantes encontradas: {len(publicaciones)}")
        
        # Contar y mostrar licitaciones
        licitaciones = []
        for p in publicaciones:
            titulo_lower = p['titulo'].lower()
            if (p.get('es_licitacion', False) or 
                any(kw in titulo_lower for kw in ['licitación', 'bases de licitación', 'concurso público', 'llamado a licitación'])):
                licitaciones.append(p)
        
        if licitaciones:
            print(f"\n{'¡'*5} LICITACIONES ENCONTRADAS: {len(licitaciones)} {'!'*5}")
            for i, lic in enumerate(licitaciones, 1):
                print(f"\n{i}. {lic['titulo']}")
                print(f"   Sección: {lic['seccion']}")
                print(f"   URL: {lic['url_pdf']}")
                if lic.get('resumen'):
                    print(f"   Resumen: {lic['resumen'][:200]}...")
        else:
            print("\n⚠️  NO SE ENCONTRARON LICITACIONES")
        
        # Mostrar valores de monedas
        if valores_monedas:
            dolar = valores_monedas.get('dolar')
            euro = valores_monedas.get('euro')
            if dolar or euro:
                print("\nValores de monedas:")
                if dolar:
                    print(f"  Dólar: ${dolar}")
                if euro:
                    print(f"  Euro: ${euro}")
        
        # Mostrar otras publicaciones relevantes
        print(f"\n{'='*60}")
        print("OTRAS PUBLICACIONES RELEVANTES:")
        print(f"{'='*60}")
        
        otras = [p for p in publicaciones if p not in licitaciones]
        for i, pub in enumerate(otras[:5], 1):  # Mostrar solo las primeras 5
            print(f"\n{i}. {pub['titulo']}")
            print(f"   Sección: {pub['seccion']}")
            if pub.get('resumen'):
                print(f"   Resumen: {pub['resumen'][:150]}...")
        
        if len(otras) > 5:
            print(f"\n... y {len(otras) - 5} publicaciones más")
        
    except Exception as e:
        print(f"\nERROR durante el scraping: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Probar con fecha del 11-07-2025 donde sabemos que hay licitación
    test_scraper("11-07-2025", force_refresh=True)
    
    # También probar con 12-07-2025
    print("\n\n")
    test_scraper("12-07-2025", force_refresh=True)