#!/usr/bin/env python
"""
Utilidades para manejo de fechas en español
"""
from datetime import datetime

def formatear_fecha_espanol(fecha_str):
    """
    Convierte una fecha en formato dd-mm-yyyy a formato largo en español
    Ej: "18-07-2025" -> "18 de julio de 2025"
    """
    meses_espanol = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    
    fecha_obj = datetime.strptime(fecha_str, '%d-%m-%Y')
    mes_espanol = meses_espanol[fecha_obj.month]
    
    return f"{fecha_obj.day} de {mes_espanol} de {fecha_obj.year}"

def dia_semana_espanol(fecha_str):
    """
    Obtiene el día de la semana en español
    """
    dias_espanol = {
        0: 'lunes', 1: 'martes', 2: 'miércoles', 3: 'jueves',
        4: 'viernes', 5: 'sábado', 6: 'domingo'
    }
    
    fecha_obj = datetime.strptime(fecha_str, '%d-%m-%Y')
    dia_espanol = dias_espanol[fecha_obj.weekday()]
    
    return dia_espanol.capitalize()

def fecha_completa_espanol(fecha_str):
    """
    Retorna fecha completa con día de la semana
    Ej: "Viernes, 18 de julio de 2025"
    """
    dia = dia_semana_espanol(fecha_str)
    fecha = formatear_fecha_espanol(fecha_str)
    return f"{dia}, {fecha}"