# Integración Chennai - Mejoras Implementadas

## Resumen de Cambios

Se han integrado todas las mejoras de la rama Khartoum al repositorio Chennai, manteniendo un código limpio y organizado.

### 1. Integración con SII (Servicio de Impuestos Internos)

#### Archivos Principales:
- `alerts/scraper_sii.py`: Scraper completo para obtener circulares y resoluciones del SII
- `alerts/models.py`: Nuevo modelo DocumentoSII para almacenar documentos tributarios

#### Funcionalidades:
- Obtención automática de circulares y resoluciones exentas del SII
- Filtrado por fecha específica (día anterior)
- Mejora automática de descripciones tributarias para claridad
- Manejo robusto de errores y rate limiting

### 2. Integración con CMF (Comisión para el Mercado Financiero)

#### Archivos Principales:
- `alerts/management/commands/scrape_hechos.py`: Comando completamente reescrito con criterios profesionales
- `alerts/models.py`: Actualización del modelo HechoEsencial con campos profesionales

#### Mejoras Implementadas:
- Criterios de relevancia tipo Bloomberg/Refinitiv
- Categorización automática (CRÍTICO, IMPORTANTE, MODERADO, RUTINARIO)
- Detección de empresas IPSA
- Scoring de relevancia profesional (1-10)
- Integración con OpenAI para resúmenes inteligentes

### 3. Sistema de Informes Integrados

#### Archivos Principales:
- `generar_informe_oficial_integrado.py`: Script principal para informes combinados
- `alerts/management/commands/generar_informe_integrado.py`: Comando Django equivalente
- `templates/informe_diario_oficial_plantilla.html`: Plantilla actualizada con secciones SII y CMF

#### Características:
- Combina información del Diario Oficial, SII y CMF en un solo informe
- Secciones codificadas por color (rojo para SII, púrpura para CMF)
- Indicadores visuales de relevancia con emojis
- Formato HTML profesional y responsive

### 4. Actualización de Criterios de Relevancia

#### Archivo:
- `alerts/evaluador_relevancia.py`

#### Nuevos Criterios Agregados:
- **SII**: Siempre relevante (circulares, resoluciones, normativa tributaria)
- **CMF**: Siempre relevante (hechos esenciales, normativa financiera)
- **Ambientales**: Regulaciones ambientales, cambio climático, emisiones

## Uso del Sistema

### Generar Informe Integrado:
```bash
# Para hoy
python generar_informe_oficial_integrado.py

# Para fecha específica
python generar_informe_oficial_integrado.py "21-07-2025"

# Sin enviar email (solo generar HTML)
python generar_informe_oficial_integrado.py "21-07-2025" --no-enviar
```

### Actualizar Hechos CMF:
```bash
python manage.py scrape_hechos
```

## Estructura de Archivos

```
chennai/
├── alerts/
│   ├── management/commands/
│   │   ├── scrape_hechos.py         # CMF scraper mejorado
│   │   └── generar_informe_integrado.py
│   ├── models.py                     # Modelos actualizados
│   ├── evaluador_relevancia.py       # Criterios ampliados
│   ├── scraper_diario_oficial.py
│   └── scraper_sii.py                # Nuevo scraper SII
├── templates/
│   └── informe_diario_oficial_plantilla.html  # Plantilla actualizada
├── generar_informe_oficial_integrado.py       # Script standalone
└── CLAUDE.md                         # Instrucciones importantes
```

## Base de Datos

### Migraciones Aplicadas:
- `0004_add_criterios_profesionales_y_sii.py`: Añade campos profesionales y modelo DocumentoSII

### Nuevos Campos en HechoEsencial:
- `categoria`: Clasificación profesional del hecho
- `relevancia_profesional`: Score numérico de relevancia
- `es_empresa_ipsa`: Indicador de empresa IPSA
- `materia`: Contexto adicional del hecho

### Nuevo Modelo DocumentoSII:
- Almacena circulares, resoluciones y jurisprudencia del SII
- Campos para título, URL, contenido, resumen IA y relevancia

## Notas Importantes

1. **Compatibilidad**: Todos los cambios son retrocompatibles con el código existente
2. **Performance**: Se mantienen las optimizaciones de caché y rate limiting
3. **Configuración**: No se requieren cambios en settings.py
4. **Dependencias**: Ya incluidas en requirements.txt (OpenAI, etc)

## Próximos Pasos Sugeridos

1. Implementar scraping de jurisprudencia SII (requiere Selenium)
2. Añadir más fuentes de información financiera
3. Crear dashboard web para visualización de informes
4. Implementar sistema de alertas personalizadas