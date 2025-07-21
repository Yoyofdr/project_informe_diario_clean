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
**SIEMPRE USAR**: `generar_informe_oficial.py`
- Contiene todo el proceso correcto
- Usa el scraper oficial
- Usa la plantilla oficial
- Usa las direcciones correctas

Ejemplo de uso:
```bash
python generar_informe_oficial.py                    # Para hoy
python generar_informe_oficial.py "21-07-2025"      # Para fecha específica
```