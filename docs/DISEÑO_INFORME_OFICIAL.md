# Diseño Oficial del Informe Diario Oficial

## Descripción General
Este documento describe el diseño oficial aprobado para los informes del Diario Oficial que se envían por email.

## Estructura del Informe

### 1. Header
- **Fondo**: Gradiente de gris oscuro (`linear-gradient(135deg, #1e293b 0%, #334155 100%)`)
- **Título**: "Diario Oficial" en blanco, 28px, font-weight 700
- **Fecha**: Formato completo (ej: "Lunes 21 de julio de 2025")
- **Padding**: 48px vertical, 32px horizontal

### 2. Estadísticas
- **Fondo**: Gradiente azul claro (`linear-gradient(90deg, #eff6ff 0%, #eef2ff 100%)`)
- **Dos columnas**:
  - Total Documentos (color azul #1d4ed8)
  - Publicaciones Relevantes (color verde #059669)
- **Números grandes**: 32px
- **Labels**: Mayúsculas, 11px, espaciado de letras

### 3. Secciones de Contenido
Tres secciones principales:
1. **Normas Generales** - Normativas de aplicación general
2. **Normas Particulares** - Resoluciones y normativas específicas  
3. **Avisos Destacados** - Avisos de interés público y licitaciones

### 4. Publicaciones
- **Tarjeta**: Borde gris (#e2e8f0), radio 12px
- **Borde superior**: 3px sólido azul (#3b82f6)
- **Padding interno**: 24px
- **Título**: 16px, font-weight 600
- **Resumen**: 14px, color gris (#64748b)
- **Botón PDF**: 
  - Fondo azul (#3b82f6)
  - Texto blanco
  - Padding: 10px 20px
  - Sin emojis
  - Texto: "Ver documento oficial"

### 5. Badge de Licitación
- **Cuando aplica**: Para publicaciones que son licitaciones
- **Estilo**: Fondo azul claro (#dbeafe), texto azul oscuro (#1e40af)
- **Tamaño**: 11px, mayúsculas

### 6. Footer
- **Fondo**: Gris claro (#f8fafc)
- **Texto principal**: "Información obtenida directamente del sitio diariooficial.interior.gob.cl"
- **Texto secundario**: Estadísticas del informe

## Características Técnicas

### Compatibilidad Email
- Diseño basado en tablas HTML para máxima compatibilidad
- Estilos inline para clientes de correo
- Ancho fijo de 672px
- Sin JavaScript
- Sin CSS externo

### Colores Principales
- Azul principal: #3b82f6
- Gris oscuro header: #1e293b → #334155
- Azul claro fondo: #eff6ff → #eef2ff
- Verde estadísticas: #059669
- Gris texto: #64748b

### Tipografía
- Font stack: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif
- Tamaños: 28px (título), 18px (secciones), 16px (publicaciones), 14px (texto), 11px (labels)

## Archivos Relacionados

1. **Plantilla HTML**: `/templates/informe_diario_oficial_plantilla.html`
2. **Script de generación**: `generar_informe_plantilla.py`
3. **Ejemplo de referencia**: `informe_email_12_07_2025.html`

## Uso

Para generar un informe con este diseño:

```python
python generar_informe_plantilla.py [fecha-opcional]
```

Sin fecha, genera el informe de hoy. Con fecha, usar formato DD-MM-AAAA.

## Notas Importantes

- NO usar emojis en los botones de descarga
- Incluir siempre los enlaces a los PDFs oficiales
- Mantener el diseño de tabla para compatibilidad con clientes de email
- Los valores de monedas solo se muestran si están disponibles
- El badge "Licitación" solo aparece en publicaciones marcadas como licitación

---
Última actualización: 21 de julio de 2025