"""
Versión mejorada del scraper con mejor manejo de ediciones
"""
import os
import json
from datetime import datetime, timedelta

def estimar_edicion_por_dias_habiles_mejorado(fecha):
    """
    Estima el número de edición basándose en días hábiles con validaciones mejoradas.
    """
    try:
        # Cargar el caché
        cache_file = os.path.join(os.path.dirname(__file__), '..', 'edition_cache.json')
        cache = {}
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache = json.load(f)
        
        fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
        
        # Buscar la referencia más cercana ANTERIOR a la fecha solicitada
        mejor_ref = None
        fecha_ref_mas_cercana = None
        
        for fecha_cache, edicion_cache in cache.items():
            fecha_cache_obj = datetime.strptime(fecha_cache, "%d-%m-%Y")
            
            # Solo considerar fechas anteriores o iguales
            if fecha_cache_obj <= fecha_obj:
                if mejor_ref is None or fecha_cache_obj > fecha_ref_mas_cercana:
                    fecha_ref_mas_cercana = fecha_cache_obj
                    mejor_ref = (fecha_cache, int(edicion_cache))
        
        if mejor_ref:
            fecha_ref, edicion_ref = mejor_ref
            fecha_ref_obj = datetime.strptime(fecha_ref, "%d-%m-%Y")
            
            # Contar días hábiles entre las dos fechas
            dias_habiles = contar_dias_habiles(fecha_ref_obj, fecha_obj)
            
            # Calcular la edición estimada
            edicion_estimada = edicion_ref + dias_habiles
            
            print(f"[EDITION] Estimación mejorada:")
            print(f"  - Fecha referencia: {fecha_ref} (edición {edicion_ref})")
            print(f"  - Fecha objetivo: {fecha}")
            print(f"  - Días hábiles de diferencia: {dias_habiles}")
            print(f"  - Edición estimada: {edicion_estimada}")
            
            # Validar que no exista ya esa edición en otra fecha
            for f, e in cache.items():
                if int(e) == edicion_estimada and f != fecha:
                    print(f"[ALERTA] La edición {edicion_estimada} ya está asignada a {f}")
                    print(f"[ALERTA] Ajustando edición para evitar duplicados...")
                    # Buscar la siguiente edición disponible
                    edicion_estimada = encontrar_siguiente_edicion_disponible(cache, edicion_estimada)
                    print(f"[ALERTA] Nueva edición asignada: {edicion_estimada}")
                    break
            
            return str(edicion_estimada)
        else:
            print("[EDITION] No se encontraron referencias en el caché")
            return None
            
    except Exception as e:
        print(f"[EDITION] Error en estimación mejorada: {e}")
        return None

def contar_dias_habiles(fecha_inicio, fecha_fin):
    """
    Cuenta los días hábiles entre dos fechas (excluyendo fecha_inicio, incluyendo fecha_fin)
    """
    dias_habiles = 0
    fecha_actual = fecha_inicio + timedelta(days=1)
    
    while fecha_actual <= fecha_fin:
        # Si es lunes a viernes (0-4), es día hábil
        if fecha_actual.weekday() < 5:
            dias_habiles += 1
        fecha_actual += timedelta(days=1)
    
    return dias_habiles

def encontrar_siguiente_edicion_disponible(cache, edicion_inicial):
    """
    Encuentra la siguiente edición disponible que no esté en el caché
    """
    ediciones_usadas = set(int(e) for e in cache.values())
    edicion = edicion_inicial
    
    while edicion in ediciones_usadas:
        edicion += 1
    
    return edicion

def validar_y_actualizar_cache(fecha, edicion_estimada):
    """
    Valida y actualiza el caché con controles adicionales
    """
    try:
        cache_file = os.path.join(os.path.dirname(__file__), '..', 'edition_cache.json')
        cache = {}
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache = json.load(f)
        
        # Verificar duplicados
        for f, e in cache.items():
            if int(e) == int(edicion_estimada) and f != fecha:
                print(f"[ALERTA] Intento de asignar edición duplicada {edicion_estimada}")
                print(f"[ALERTA] Ya está asignada a {f}")
                return False
        
        # Actualizar caché
        cache[fecha] = str(edicion_estimada)
        
        # Ordenar por fecha
        cache_ordenado = dict(sorted(cache.items(), key=lambda x: datetime.strptime(x[0], "%d-%m-%Y")))
        
        with open(cache_file, 'w') as f:
            json.dump(cache_ordenado, f, indent=2)
        
        print(f"[EDITION] Caché actualizado: {fecha} -> {edicion_estimada}")
        return True
        
    except Exception as e:
        print(f"[EDITION] Error actualizando caché: {e}")
        return False

def obtener_numero_edicion_mejorado(fecha, driver=None):
    """
    Versión mejorada de obtener_numero_edicion con validaciones adicionales
    """
    try:
        # 1. Verificar caché primero
        cache_file = os.path.join(os.path.dirname(__file__), '..', 'edition_cache.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache = json.load(f)
                if fecha in cache:
                    print(f"[EDITION] Número de edición encontrado en caché: {cache[fecha]}")
                    return cache[fecha]
        
        # 2. Intentar obtener del sitio web (código existente)
        # ... (aquí iría el código de selenium)
        
        # 3. Si falla, usar estimación mejorada
        edicion_estimada = estimar_edicion_por_dias_habiles_mejorado(fecha)
        
        if edicion_estimada:
            # Actualizar el caché solo si es válido
            if validar_y_actualizar_cache(fecha, edicion_estimada):
                return edicion_estimada
        
        # 4. Como último recurso, avisar del problema
        print(f"[ERROR] No se pudo determinar la edición para {fecha}")
        print("[ERROR] Se requiere intervención manual")
        
        return None
        
    except Exception as e:
        print(f"[ERROR] Error crítico obteniendo edición: {e}")
        return None

# Función para auditar el caché actual
def auditar_cache():
    """
    Audita el caché buscando problemas como ediciones duplicadas o saltos
    """
    try:
        cache_file = os.path.join(os.path.dirname(__file__), '..', 'edition_cache.json')
        if not os.path.exists(cache_file):
            print("[AUDIT] No existe archivo de caché")
            return
        
        with open(cache_file, 'r') as f:
            cache = json.load(f)
        
        print("\n=== AUDITORÍA DE CACHÉ ===")
        
        # Verificar duplicados
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
            print("\n✅ No se encontraron ediciones duplicadas")
        
        # Verificar secuencia
        fechas_ordenadas = sorted(cache.items(), key=lambda x: datetime.strptime(x[0], "%d-%m-%Y"))
        
        print("\n📅 SECUENCIA DE EDICIONES:")
        edicion_anterior = None
        fecha_anterior = None
        
        for fecha, edicion in fechas_ordenadas:
            fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
            dia_semana = fecha_obj.strftime("%A")
            
            if edicion_anterior:
                dias_habiles = contar_dias_habiles(
                    datetime.strptime(fecha_anterior, "%d-%m-%Y"),
                    fecha_obj
                )
                diferencia_edicion = int(edicion) - int(edicion_anterior)
                
                simbolo = "✅" if diferencia_edicion == dias_habiles else "⚠️"
                print(f"   {simbolo} {fecha} ({dia_semana[:3]}): {edicion} "
                      f"(+{diferencia_edicion} ediciones, {dias_habiles} días hábiles)")
            else:
                print(f"   📍 {fecha} ({dia_semana[:3]}): {edicion} (referencia inicial)")
            
            edicion_anterior = edicion
            fecha_anterior = fecha
        
        print("\n=========================")
        
    except Exception as e:
        print(f"[AUDIT] Error en auditoría: {e}")