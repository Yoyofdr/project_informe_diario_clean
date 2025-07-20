#!/usr/bin/env python
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alerts.scraper_diario_oficial import es_relevante, PALABRAS_RELEVANTES, PALABRAS_NO_RELEVANTES

def test_relevancia():
    """Prueba qué publicaciones se consideran relevantes"""
    
    print("="*60)
    print("PRUEBA DE CRITERIOS DE RELEVANCIA")
    print("="*60)
    
    print("\nPALABRAS RELEVANTES:")
    for p in PALABRAS_RELEVANTES:
        print(f"  - {p}")
    
    print("\nPALABRAS NO RELEVANTES:")
    for p in PALABRAS_NO_RELEVANTES[:5]:  # Mostrar solo las primeras 5
        print(f"  - {p}")
    print("  ...")
    
    # Casos de prueba del 11-07-2025
    titulos = [
        "Decreto número 57, de 2024.- Fija fórmulas tarifarias de los servicios de producción y distribución de agua potable",
        "Decreto número 19, de 2025.- Modifica decreto Nº 460, de 2011, que crea un establecimiento penitenciario",
        "Decreto número 48, de 2025.- Nombra a doña Verónica Isabel Encina Vera en el cargo de Defensora Nacional",
        "Resolución exenta número 5.040, de 2025.- Establece requisitos fitosanitarios para la importación de frutos",
        "Resolución exenta número 81, de 2025.- Modifica fecha de entrada en vigencia de resolución Nº 41 exenta",
        "Certificado Tipos de cambio y paridades de monedas extranjeras para efectos que señala",
        "Extracto de resolución exenta número 73, de 2025.- Complementa lista anexa de resolución N° 8 exenta",
        "Resolución exenta número 4.945, de 2025.- Establece medidas sanitarias aplicadas a productos",
        "Resolución exenta número 1.777, de 2025.- Aprueba proyecto de Ciclovía Av. Guillermo Mann"
    ]
    
    print("\n\nRESULTADOS DE RELEVANCIA:")
    print("-"*60)
    
    relevantes = []
    no_relevantes = []
    
    for titulo in titulos:
        es_rel = es_relevante(titulo)
        if es_rel:
            relevantes.append(titulo)
        else:
            no_relevantes.append(titulo)
        
        print(f"\nTítulo: {titulo}")
        print(f"¿Es relevante? {'SÍ' if es_rel else 'NO'}")
        
        # Mostrar qué palabras coinciden
        titulo_upper = titulo.upper()
        palabras_rel = [p for p in PALABRAS_RELEVANTES if p in titulo_upper]
        palabras_no_rel = [p for p in PALABRAS_NO_RELEVANTES if p in titulo_upper]
        
        if palabras_rel:
            print(f"  Palabras relevantes encontradas: {', '.join(palabras_rel)}")
        if palabras_no_rel:
            print(f"  Palabras NO relevantes encontradas: {', '.join(palabras_no_rel)}")
    
    print(f"\n\nRESUMEN:")
    print(f"Publicaciones relevantes: {len(relevantes)}")
    print(f"Publicaciones no relevantes: {len(no_relevantes)}")

if __name__ == "__main__":
    test_relevancia()