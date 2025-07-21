#!/usr/bin/env python
"""
Verificar qué ediciones existen alrededor del 21 de julio
"""
import requests
from datetime import datetime, timedelta

def verificar_ediciones():
    """Verifica las ediciones disponibles del 19 al 23 de julio"""
    
    print("=== VERIFICANDO EDICIONES DE JULIO 2025 ===\n")
    
    # Fecha central: 21 de julio
    fecha_central = datetime(2025, 7, 21)
    
    # Revisar del 19 al 23 de julio
    for i in range(-2, 3):  # -2, -1, 0, 1, 2 días
        fecha = fecha_central + timedelta(days=i)
        fecha_str = fecha.strftime("%d-%m-%Y")
        
        # Estimar número de edición (aproximado)
        edicion = 44204 + i  # Asumiendo ediciones consecutivas
        
        url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha_str}&edition={edicion}"
        
        print(f"\n{'='*60}")
        print(f"Fecha: {fecha.strftime('%A %d de julio, %Y')} ({fecha_str})")
        print(f"Edición estimada: {edicion}")
        print(f"URL: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            # Buscar indicadores en el HTML
            if "No existen publicaciones" in response.text:
                print("❌ Sin publicaciones")
            elif "TSPD" in response.text and len(response.text) < 6000:
                print("🛡️ Protección anti-bot")
            elif "Normas Generales" in response.text:
                print("✅ CON PUBLICACIONES")
                # Contar publicaciones aproximadas
                count = response.text.count('class="content"')
                if count > 0:
                    print(f"   Posibles publicaciones: {count}")
            else:
                print("❓ Estado desconocido")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n{'='*60}")
    print("FIN DE LA VERIFICACIÓN")

if __name__ == "__main__":
    verificar_ediciones()