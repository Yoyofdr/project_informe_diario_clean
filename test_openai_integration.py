#!/usr/bin/env python
"""
Script para probar la integración con OpenAI API
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.evaluador_relevancia import EvaluadorRelevancia
from alerts.scraper_diario_oficial import generar_resumen_desde_texto

def test_evaluador_relevancia():
    """Prueba el evaluador de relevancia con OpenAI"""
    print("=== PROBANDO EVALUADOR DE RELEVANCIA CON OPENAI ===\n")
    
    evaluador = EvaluadorRelevancia()
    
    # Casos de prueba
    casos = [
        {
            "titulo": "LEY NÚM. 21.789 - MODIFICA EL CÓDIGO DEL TRABAJO EN MATERIA DE TELETRABAJO",
            "esperado": True
        },
        {
            "titulo": "NOMBRA A DON JUAN PÉREZ COMO DIRECTOR DE SERVICIO",
            "esperado": False
        },
        {
            "titulo": "FIJA TARIFAS ELÉCTRICAS PARA EL SISTEMA INTERCONECTADO CENTRAL",
            "esperado": True
        },
        {
            "titulo": "CONCURSO PÚBLICO PARA PROVEER CARGO DE TERCER NIVEL JERÁRQUICO",
            "esperado": False
        },
        {
            "titulo": "LLAMA A CONCURSO PÚBLICO PARA LA ASIGNACIÓN DEL PROYECTO HABILITACIÓN DE SERVICIOS DE TELECOMUNICACIONES",
            "esperado": True
        }
    ]
    
    for caso in casos:
        titulo = caso["titulo"]
        esperado = caso["esperado"]
        
        print(f"Evaluando: {titulo}")
        es_relevante, razon = evaluador.evaluar_relevancia(titulo)
        
        estado = "✓" if es_relevante == esperado else "✗"
        print(f"{estado} Resultado: {'RELEVANTE' if es_relevante else 'NO RELEVANTE'}")
        print(f"  Razón: {razon}")
        print(f"  Esperado: {'RELEVANTE' if esperado else 'NO RELEVANTE'}")
        print()

def test_generacion_resumenes():
    """Prueba la generación de resúmenes con OpenAI"""
    print("\n=== PROBANDO GENERACIÓN DE RESÚMENES CON OPENAI ===\n")
    
    texto_prueba = """EXTRACTO
    MINISTERIO DE VIVIENDA Y URBANISMO
    SUBSECRETARÍA DE VIVIENDA Y URBANISMO
    
    APRUEBA LLAMADO A POSTULACIÓN EN CONDICIONES ESPECIALES PARA EL DESARROLLO 
    DE PROYECTOS DEL PROGRAMA DE HABITABILIDAD RURAL, PARA LAS REGIONES DE 
    COQUIMBO Y LOS LAGOS
    
    (Resolución)
    
    Núm. 1.234 exenta.- Santiago, 15 de julio de 2025.
    
    Considerando:
    
    a) Que el Programa de Habitabilidad Rural tiene por objetivo mejorar las 
    condiciones de habitabilidad de las familias que residen en zonas rurales 
    y localidades urbanas de hasta 5.000 habitantes.
    
    b) Que se requiere un llamado especial para las regiones de Coquimbo y 
    Los Lagos debido a las particulares condiciones climáticas y geográficas 
    de dichas zonas.
    
    Resuelvo:
    
    1. Apruébase el llamado a postulación en condiciones especiales para el 
    desarrollo de proyectos del Programa de Habitabilidad Rural, destinado a 
    las regiones de Coquimbo y Los Lagos.
    
    2. El presente llamado contempla recursos por un total de 5.000 UF, 
    distribuidos equitativamente entre ambas regiones.
    
    3. Podrán postular personas naturales o jurídicas que cumplan con los 
    requisitos establecidos en el DS N° 10 (V. y U.) de 2015 y que presenten 
    proyectos de mejoramiento de viviendas rurales existentes.
    
    4. El plazo de postulación se extenderá desde el 1 de agosto hasta el 
    30 de septiembre de 2025.
    
    5. Los proyectos deberán considerar soluciones constructivas apropiadas 
    para las condiciones climáticas de cada región, priorizando la eficiencia 
    energética y el uso de materiales locales."""
    
    titulo = "APRUEBA LLAMADO A POSTULACIÓN PROGRAMA DE HABITABILIDAD RURAL PARA COQUIMBO Y LOS LAGOS"
    
    print(f"Generando resumen para: {titulo}")
    print("-" * 50)
    
    resumen = generar_resumen_desde_texto(texto_prueba, titulo)
    
    print(f"Resumen generado:\n{resumen}")
    print("-" * 50)

if __name__ == "__main__":
    print("PRUEBA DE INTEGRACIÓN CON OPENAI API")
    print("=" * 50)
    
    # Verificar que existe la API key
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.environ.get('OPENAI_API_KEY'):
        print("ERROR: No se encontró OPENAI_API_KEY en las variables de entorno")
        sys.exit(1)
    
    print("✓ API Key de OpenAI configurada correctamente")
    print()
    
    # Ejecutar pruebas
    test_evaluador_relevancia()
    test_generacion_resumenes()
    
    print("\n✓ Pruebas completadas")