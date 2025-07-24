# POLÍTICA DE CONTENIDO - INFORME DIARIO OFICIAL

## REGLA FUNDAMENTAL
**NUNCA INVENTAR CONTENIDO DEL DIARIO OFICIAL**

## Principios

1. **Solo datos reales**: Todos los datos deben provenir del scraping real del sitio diariooficial.interior.gob.cl
2. **Sin contenido ficticio**: No crear publicaciones, leyes, decretos o valores de monedas inventados
3. **Transparencia total**: Si no hay datos, informar claramente al usuario

## Qué hacer cuando no hay datos

### Si el scraper falla:
```
ERROR: No se pudo acceder al Diario Oficial del [fecha]
Razón: [descripción del error]

Posibles soluciones:
1. Intentar más tarde
2. Verificar conexión
3. Revisar si el sitio está disponible
```

### Si no hay publicaciones:
```
No se encontraron publicaciones relevantes para el [fecha]

Esto puede ocurrir porque:
- No hubo publicaciones ese día
- Es fin de semana o feriado
- Aún no se han publicado los documentos del día
```

## Implementación en código

```python
# CORRECTO
if not publicaciones:
    return {
        'error': True,
        'mensaje': 'No se encontraron publicaciones para esta fecha',
        'publicaciones': [],
        'total_documentos': 0
    }

# INCORRECTO - NUNCA HACER ESTO
if not publicaciones:
    publicaciones = [
        {"titulo": "LEY INVENTADA", "resumen": "Contenido falso"}
    ]
```

## Consecuencias de inventar contenido

1. **Pérdida de confianza**: El usuario no puede confiar en la información
2. **Información falsa oficial**: Es especialmente grave con documentos legales
3. **Decisiones incorrectas**: Usuarios pueden tomar decisiones basadas en información falsa

## Recordatorio

El Diario Oficial contiene:
- Leyes reales
- Decretos oficiales
- Resoluciones gubernamentales
- Licitaciones públicas
- Valores económicos oficiales

**TODA esta información debe ser 100% real y verificable**

---
Creado: 21 de julio de 2025
Razón: Prevenir futuros casos de contenido inventado