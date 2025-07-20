#!/usr/bin/env python
"""
Script para probar los resúmenes mejorados
"""
import os
from dotenv import load_dotenv
from alerts.scraper_diario_oficial import resumen_con_gemini

# Ejemplos de textos del Diario Oficial para probar
ejemplos = [
    {
        "titulo": "Llamado a Licitación Pública para la Concesión del Uso de las Vías",
        "texto": """La Municipalidad de Santiago convoca a licitación pública para la concesión 
del uso de las vías públicas en el sector centro de la comuna, específicamente en las 
calles Ahumada, Huérfanos y Estado. El período de concesión será de 5 años a partir 
del 1 de agosto de 2025. Los interesados deberán presentar una garantía de seriedad 
de la oferta por $50.000.000 (cincuenta millones de pesos). Las bases estarán 
disponibles desde el 15 de julio de 2025 en las oficinas municipales. El plazo para 
presentar ofertas vence el 31 de julio de 2025 a las 15:00 horas. Los oferentes 
deberán acreditar experiencia mínima de 3 años en administración de espacios públicos 
y contar con capital de trabajo no inferior a $200.000.000."""
    },
    {
        "titulo": "Decreto que establece medidas de emergencia por déficit hídrico",
        "texto": """Se declara emergencia hídrica en las comunas de Petorca, La Ligua y 
Cabildo de la Región de Valparaíso, debido al déficit de precipitaciones que alcanza 
un 70% bajo el promedio histórico. La medida regirá desde el 15 de julio hasta el 
31 de diciembre de 2025. Se autoriza a la Dirección General de Aguas para adoptar 
medidas excepcionales como la redistribución de caudales y restricción del uso del 
agua para riego en un 30%. Los agricultores afectados podrán postular a subsidios 
especiales por un monto total de $5.000.000.000. Las solicitudes se recibirán en 
las oficinas de INDAP entre el 20 de julio y el 20 de agosto de 2025."""
    },
    {
        "titulo": "Aprueba nuevo reglamento de transporte escolar",
        "texto": """Se aprueba el nuevo reglamento que establece requisitos adicionales para 
el transporte escolar en todo el territorio nacional. Los vehículos deberán contar con 
cinturones de seguridad de tres puntos en todos los asientos, cámaras de seguridad 
interiores y GPS con monitoreo en tiempo real. Los conductores deberán aprobar un 
curso especializado de 40 horas impartido por instituciones acreditadas. El plazo 
para adecuarse a la nueva normativa es de 6 meses a contar de la publicación. Las 
multas por incumplimiento van desde 5 a 50 UTM. Se estima que la medida beneficiará 
a más de 800.000 estudiantes que utilizan transporte escolar diariamente."""
    }
]

def probar_resumenes():
    """Prueba los resúmenes con diferentes tipos de documentos"""
    load_dotenv()
    
    print("=== PROBANDO RESÚMENES MEJORADOS ===\n")
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n{'='*60}")
        print(f"EJEMPLO {i}: {ejemplo['titulo']}")
        print(f"{'='*60}")
        
        print(f"\nTEXTO ORIGINAL (primeras 200 palabras):")
        print(f"{ejemplo['texto'][:400]}...")
        
        # Generar resumen
        resumen = resumen_con_gemini(ejemplo['texto'], ejemplo['titulo'])
        
        print(f"\nRESUMEN GENERADO:")
        if resumen:
            print(resumen)
            
            # Verificar que incluye elementos clave
            print(f"\n✓ VERIFICACIÓN DE ELEMENTOS CLAVE:")
            elementos = {
                "Ubicación": any(word in resumen.lower() for word in ["santiago", "petorca", "valparaíso", "comuna", "región", "nacional"]),
                "Fechas": any(word in resumen.lower() for word in ["julio", "agosto", "diciembre", "2025", "plazo", "meses"]),
                "Montos": "$" in resumen or "pesos" in resumen.lower() or "utm" in resumen.lower(),
                "Requisitos": any(word in resumen.lower() for word in ["requisito", "experiencia", "acreditar", "deberán", "curso"]),
                "Entidades": any(word in resumen.lower() for word in ["municipalidad", "indap", "dirección general"]),
            }
            
            for elemento, presente in elementos.items():
                estado = "✅" if presente else "❌"
                print(f"  {estado} {elemento}")
            
            # Contar caracteres
            print(f"\n📏 Longitud del resumen: {len(resumen)} caracteres")
        else:
            print("❌ No se pudo generar resumen")
    
    print(f"\n{'='*60}")
    print("PRUEBA COMPLETADA")
    print(f"{'='*60}")

if __name__ == "__main__":
    probar_resumenes()