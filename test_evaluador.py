#!/usr/bin/env python
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alerts.evaluador_relevancia import EvaluadorRelevancia

def test_evaluador():
    """Prueba el evaluador de relevancia con títulos reales"""
    
    evaluador = EvaluadorRelevancia()
    
    # Títulos de prueba del 11-07-2025
    titulos = [
        # Licitaciones
        "Extracto de resolución número 2, de 2025.- Aprueba Bases de Licitación y sus Anexos para la Concesión del Uso de las Vías",
        "Resolución exenta número P-319, de 2025.- Modifica bases y llamado a concurso para proveer cargo de tercer nivel directivo",
        
        # Deberían ser relevantes
        "Decreto número 57, de 2024.- Fija fórmulas tarifarias de los servicios de producción y distribución de agua potable",
        "Resolución exenta número 4.945, de 2025.- Establece medidas sanitarias aplicadas a productos por brote de influenza aviar",
        "Resolución exenta número 5.040, de 2025.- Establece requisitos fitosanitarios para la importación de frutos frescos",
        "Certificado Tipos de cambio y paridades de monedas extranjeras para efectos que señala",
        "Decreto número 19, de 2025.- Modifica decreto Nº 460, de 2011, que crea un establecimiento penitenciario",
        "Resolución exenta número 1.777, de 2025.- Aprueba proyecto de Ciclovía Av. Guillermo Mann",
        
        # NO deberían ser relevantes
        "Decreto número 48, de 2025.- Nombra a doña Verónica Isabel Encina Vera en el cargo de Defensora Nacional",
        "Extracto de resolución exenta número 73, de 2025.- Complementa lista anexa de resolución N° 8 exenta",
        "Extracto de resolución exenta número 81, de 2025.- Modifica fecha de entrada en vigencia de resolución",
        "Resolución exenta número 5.041, de 2025.- Reconoce al Centro de Producción Koppert B.V.",
        
        # Ejemplos de otros días (deberían ser relevantes)
        "Resolución exenta número 283, de 2025.- Extiende vigencia de declaración de emergencia agrícola por déficit hídrico",
        "Resolución exenta número 3.874, de 2025.- Aprueba Manual de procedimientos para la evaluación de solicitudes de creación de comunas",
        "Resolución exenta número 1.453, de 2025.- Somete a consulta ciudadana la propuesta de anteproyecto de la Estrategia",
        "Decreto exento número 211, de 2025.- Reajusta en 2,2% las tasas fijas de impuesto de Timbres y Estampillas"
    ]
    
    print("="*80)
    print("EVALUACIÓN DE RELEVANCIA DE PUBLICACIONES")
    print("="*80)
    
    relevantes = []
    no_relevantes = []
    
    for titulo in titulos:
        es_relevante, razon = evaluador._evaluar_con_reglas(titulo)  # Usar reglas directamente
        
        if es_relevante:
            relevantes.append((titulo, razon))
        else:
            no_relevantes.append((titulo, razon))
        
        print(f"\n{'✓' if es_relevante else '✗'} {titulo}")
        print(f"   → {razon}")
    
    print(f"\n{'='*80}")
    print(f"RESUMEN: {len(relevantes)} relevantes, {len(no_relevantes)} no relevantes")
    print("="*80)
    
    # Verificar casos específicos
    print("\nVERIFICACIONES IMPORTANTES:")
    
    # Verificar que las licitaciones sean detectadas
    licitaciones = [t for t, r in relevantes if "licitación" in t.lower()]
    print(f"✓ Licitaciones detectadas: {len(licitaciones)}")
    
    # Verificar que los nombramientos sean excluidos (excepto Defensor Nacional)
    nombramientos_incluidos = [t for t, r in relevantes if "nombra" in t.lower()]
    print(f"✓ Nombramientos de alto nivel incluidos: {len(nombramientos_incluidos)}")
    
    # Verificar emergencias y consultas ciudadanas
    emergencias = [t for t, r in relevantes if "emergencia" in t.lower() or "consulta ciudadana" in t.lower()]
    print(f"✓ Emergencias y consultas detectadas: {len(emergencias)}")

if __name__ == "__main__":
    test_evaluador()