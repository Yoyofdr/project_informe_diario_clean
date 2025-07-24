# INSTRUCCIONES IMPORTANTES PARA CLAUDE

## ⚠️ LECTURA OBLIGATORIA ANTES DE GENERAR INFORMES

## 🚨 GENERACIÓN DE INFORMES DEL DIARIO OFICIAL

### SIEMPRE usar el sistema oficial existente:

1. **SCRAPER OFICIAL**: `alerts.scraper_diario_oficial.obtener_sumario_diario_oficial()`
   - Ya incluye evaluación de relevancia con IA
   - Ya genera resúmenes con IA (OpenAI)
   - Ya clasifica en las secciones oficiales
   - Ya extrae valores de monedas

2. **PLANTILLA OFICIAL**: `templates/informe_diario_oficial_plantilla.html`
   - Diseño aprobado de Bolt
   - Usa las 3 secciones oficiales: Normas Generales, Normas Particulares, Avisos Destacados
   - NO crear plantillas nuevas
   - NO modificar la estructura

3. **DIRECCIONES DE EMAIL**:
   - De: rodrigo@carvuk.com
   - Para: rfernandezdelrio@uc.cl

### ❌ NO HACER:
- NO crear nuevos scrapers desde cero
- NO crear nuevas plantillas HTML
- NO reclasificar publicaciones (usar las secciones del scraper)
- NO reimplementar evaluación de relevancia (ya está en el proyecto)
- NO reimplementar generación de resúmenes (ya está en el proyecto)

### ✅ PROCESO CORRECTO:

```python
# 1. Ejecutar el scraper oficial
from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
resultado = obtener_sumario_diario_oficial(fecha)

# 2. Usar la plantilla oficial
from django.template import engines
with open('templates/informe_diario_oficial_plantilla.html', 'r') as f:
    template_content = f.read()
template = engines['django'].from_string(template_content)
html = template.render(context)

# 3. Enviar con las direcciones correctas
msg['From'] = "rodrigo@carvuk.com"
msg['To'] = "rfernandezdelrio@uc.cl"
```

### 📝 NOTAS ADICIONALES:
- El número de edición correcto está en `edition_cache.json`
- Los criterios de relevancia incluyen regulaciones ambientales
- El pie del informe NO debe incluir estadísticas detalladas

### 🎯 SCRIPT DE REFERENCIA:
**SIEMPRE USAR**: `generar_informe_oficial_integrado_mejorado.py`
- Contiene todo el proceso correcto
- Usa el scraper oficial del Diario Oficial
- **IMPORTANTE**: Actualiza automáticamente los enlaces CMF con el formato correcto
- Usa las direcciones correctas
- Genera informes integrados con Diario Oficial + CMF

Ejemplo de uso:
```bash
python generar_informe_oficial_integrado_mejorado.py                    # Para hoy
python generar_informe_oficial_integrado_mejorado.py "21-07-2025"      # Para fecha específica
```

## 🔗 ENLACES CMF - INFORMACIÓN CRÍTICA

### ⚠️ FORMATO CORRECTO DE ENLACES CMF:
Los enlaces de hechos esenciales CMF DEBEN tener este formato:
```
https://www.cmfchile.cl/sitio/aplic/serdoc/ver_sgd.php?s567=[32_CARACTERES_HEX][CADENA_BASE64]&secuencia=-1&t=[TIMESTAMP]
```

Ejemplo correcto:
```
https://www.cmfchile.cl/sitio/aplic/serdoc/ver_sgd.php?s567=aca10a71d6390ef27ab35f494e6db994VFdwQmVVNVVRVE5OUkZWNFRtcFZNMDEzUFQwPQ==&secuencia=-1&t=1753329541
```

### ✅ SCRAPER CMF MEJORADO:
**USAR**: `scraper_cmf_mejorado.py`
- Obtiene automáticamente los enlaces correctos del día
- Actualiza el archivo `hechos_cmf_selenium_reales.json`
- Se ejecuta automáticamente al generar el informe

### ❌ NUNCA HACER:
- NO usar enlaces cortos o incompletos
- NO inventar tokens o IDs
- NO usar enlaces de búsqueda genéricos
- NO confiar en enlaces antiguos sin verificar