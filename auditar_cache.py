#!/usr/bin/env python
"""
Script para auditar el caché de ediciones y detectar problemas
"""
import json
import os
from datetime import datetime, timedelta

def contar_dias_habiles(fecha_inicio, fecha_fin):
    """Cuenta los días hábiles entre dos fechas"""
    dias_habiles = 0
    fecha_actual = fecha_inicio + timedelta(days=1)
    
    while fecha_actual <= fecha_fin:
        if fecha_actual.weekday() < 5:  # 0=lunes, 4=viernes
            dias_habiles += 1
        fecha_actual += timedelta(days=1)
    
    return dias_habiles

def auditar_cache():
    """Audita el caché buscando problemas"""
    try:
        cache_file = 'edition_cache.json'
        if not os.path.exists(cache_file):
            print("[AUDIT] No existe archivo de caché")
            return
        
        with open(cache_file, 'r') as f:
            cache = json.load(f)
        
        print("\n" + "="*60)
        print("AUDITORÍA DE CACHÉ DE EDICIONES")
        print("="*60)
        
        # 1. Verificar duplicados
        print("\n📋 VERIFICANDO DUPLICADOS...")
        ediciones_vistas = {}
        duplicados = []
        
        for fecha, edicion in cache.items():
            if edicion in ediciones_vistas:
                duplicados.append((fecha, edicion, ediciones_vistas[edicion]))
            else:
                ediciones_vistas[edicion] = fecha
        
        if duplicados:
            print("\n❌ EDICIONES DUPLICADAS ENCONTRADAS:")
            for fecha, edicion, fecha_original in duplicados:
                print(f"   Edición {edicion}: {fecha_original} y {fecha}")
        else:
            print("✅ No se encontraron ediciones duplicadas")
        
        # 2. Verificar secuencia y coherencia
        print("\n📅 SECUENCIA DE EDICIONES:")
        print("-"*60)
        
        fechas_ordenadas = sorted(cache.items(), key=lambda x: datetime.strptime(x[0], "%d-%m-%Y"))
        
        edicion_anterior = None
        fecha_anterior = None
        problemas = []
        
        for fecha, edicion in fechas_ordenadas:
            fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
            dia_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"][fecha_obj.weekday()]
            
            if edicion_anterior:
                fecha_anterior_obj = datetime.strptime(fecha_anterior, "%d-%m-%Y")
                dias_habiles = contar_dias_habiles(fecha_anterior_obj, fecha_obj)
                diferencia_edicion = int(edicion) - int(edicion_anterior)
                
                if diferencia_edicion == dias_habiles:
                    simbolo = "✅"
                    estado = "OK"
                else:
                    simbolo = "⚠️"
                    estado = f"ESPERADO: +{dias_habiles}, REAL: +{diferencia_edicion}"
                    problemas.append((fecha, estado))
                
                print(f"   {simbolo} {fecha} ({dia_semana}): Ed.{edicion} "
                      f"[+{diferencia_edicion} ed, {dias_habiles} días háb] {estado}")
            else:
                print(f"   📍 {fecha} ({dia_semana}): Ed.{edicion} (INICIO)")
            
            edicion_anterior = edicion
            fecha_anterior = fecha
        
        # 3. Resumen
        print("\n" + "="*60)
        print("RESUMEN:")
        print(f"  - Total de fechas en caché: {len(cache)}")
        print(f"  - Rango: {fechas_ordenadas[0][0]} a {fechas_ordenadas[-1][0]}")
        print(f"  - Ediciones: {fechas_ordenadas[0][1]} a {fechas_ordenadas[-1][1]}")
        
        if problemas:
            print(f"\n⚠️  Se encontraron {len(problemas)} inconsistencias:")
            for fecha, problema in problemas:
                print(f"     - {fecha}: {problema}")
        else:
            print("\n✅ El caché está en perfecto estado")
        
        # 4. Recomendaciones
        if duplicados or problemas:
            print("\n💡 RECOMENDACIONES:")
            if duplicados:
                print("   - Corregir las ediciones duplicadas manualmente")
            if problemas:
                print("   - Verificar las fechas con inconsistencias")
                print("   - El sistema ahora previene duplicados automáticamente")
        
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"[ERROR] Error en auditoría: {e}")

if __name__ == "__main__":
    auditar_cache()