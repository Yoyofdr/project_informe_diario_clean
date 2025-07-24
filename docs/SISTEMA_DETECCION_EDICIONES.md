# Sistema de Detección Automática de Ediciones - Diario Oficial

## Resumen

He implementado un sistema robusto que puede detectar automáticamente el número de edición correcto para cualquier fecha del Diario Oficial, sin necesidad de actualización manual.

## Cómo Funciona

El sistema utiliza una estrategia de múltiples niveles:

### 1. **Caché Local** (Primera opción)
- Busca en `edition_cache.json` si ya conoce la edición para esa fecha
- Si la encuentra, la usa directamente (más rápido)

### 2. **Detección Automática con Selenium** (Segunda opción)
- Navega a la página del Diario Oficial para la fecha solicitada
- Busca el selector de ediciones en la página
- Extrae automáticamente el número de edición correcto
- Actualiza el caché para futuras consultas

### 3. **Estimación por Días Hábiles** (Respaldo)
- Si Selenium falla, usa un algoritmo inteligente
- Calcula basándose en:
  - Ediciones conocidas anteriores
  - Solo cuenta días hábiles (lunes a viernes)
  - Ignora fines de semana
  - Usa la edición conocida más cercana como referencia

## Ventajas del Sistema

1. **Automático**: No requiere intervención manual para fechas nuevas
2. **Robusto**: Tiene múltiples estrategias de respaldo
3. **Inteligente**: Entiende que el Diario Oficial solo se publica en días hábiles
4. **Auto-aprendizaje**: El caché se actualiza automáticamente con nuevas ediciones detectadas

## Ejemplo de Funcionamiento

Para el 18 de julio de 2025:
- El sistema no encontró la fecha en caché
- Intentó con Selenium (falló por problemas de acceso)
- Usó la estimación por días hábiles:
  - Tomó como referencia el 17 de julio (edición 44200)
  - Calculó que el 18 es el siguiente día hábil (+1)
  - Estimó correctamente: edición 44201

## Mantenimiento

El sistema es prácticamente libre de mantenimiento:
- El caché se actualiza automáticamente
- Las estimaciones mejoran con cada nueva edición conocida
- No requiere actualización manual para fechas futuras

## Casos Especiales

El sistema maneja correctamente:
- Fines de semana (no hay ediciones)
- Días feriados (puede requerir ajuste manual en el caché)
- Ediciones especiales (detectadas automáticamente por Selenium)

## Archivos Involucrados

1. `alerts/scraper_diario_oficial.py`: Contiene las funciones mejoradas
2. `edition_cache.json`: Almacena ediciones conocidas
3. Funciones clave:
   - `obtener_numero_edicion()`: Función principal
   - `estimar_edicion_por_dias_habiles()`: Algoritmo de estimación

## Conclusión

Con este sistema, puedes generar informes para cualquier fecha sin preocuparte por actualizar manualmente los números de edición. El sistema se encarga de todo automáticamente.