# 🖥️ Preview de la Plataforma - Diario Oficial Mejorado

## 1. Dashboard Principal de Métricas

```
┌──────────────────────────────────────────────────────────────────────────┐
│ 🏛️ Sistema de Monitoreo Diario Oficial          [Admin] [Cerrar Sesión] │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Dashboard de Métricas - Últimos 30 días                                │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ EJECUCIONES │  │ TASA ÉXITO  │  │ DOCUMENTOS  │  │ USO CACHÉ   │   │
│  │    156      │  │   98.5%     │  │   4,521     │  │   87.3%     │   │
│  │ ↑ 12%       │  │ ↑ 2.3%      │  │ ↑ 145       │  │ ↑ 15.2%     │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ 📊 Publicaciones por Día                                       │    │
│  │                                                                │    │
│  │  250 ┤ ╭─╮                                                    │    │
│  │  200 ┤╭╯ ╰╮    ╭─╮                                           │    │
│  │  150 ┤│   ╰─╮╭─╯ ╰╮  ╭──╮                                   │    │
│  │  100 ┤│     ╰╯    ╰──╯  ╰─╮  ╭─╮                           │    │
│  │   50 ┤│                    ╰──╯ ╰─                          │    │
│  │    0 └┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘    │
│  │      1  5  10  15  20  25  30 (días)                          │    │
│  │                                                                │    │
│  │  ─── Total Publicaciones  ─── Publicaciones Relevantes        │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌────────────────────────────────┐  ┌────────────────────────────┐    │
│  │ 🔄 Métodos de Extracción       │  │ ⚡ Rendimiento por Hora     │    │
│  │                                │  │                            │    │
│  │ PyPDF2     ████████████ 65%   │  │ 00-06h  ██████ 2.3s       │    │
│  │ PDFMiner   ██████ 25%         │  │ 06-12h  ████████ 3.1s     │    │
│  │ OCR        ██ 8%              │  │ 12-18h  ██████████ 3.8s   │    │
│  │ OCR Mej.   █ 2%               │  │ 18-24h  ███████ 2.7s      │    │
│  └────────────────────────────────┘  └────────────────────────────┘    │
│                                                                          │
│  [Ver Detalles] [Exportar CSV] [Configurar Alertas]                    │
└──────────────────────────────────────────────────────────────────────────┘
```

## 2. Vista de Ejecución en Tiempo Real

```
┌──────────────────────────────────────────────────────────────────────────┐
│ 🔄 Scraping en Progreso - 07 Enero 2024                                 │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Estado: PROCESANDO                          Tiempo: 02:34              │
│  ████████████████████░░░░░░░░░  73%         ETA: 00:52                │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ 📋 Log en Vivo                                                  │    │
│  │                                                                 │    │
│  │ [10:32:15] ✓ Conectando al Diario Oficial...                  │    │
│  │ [10:32:16] ✓ Página cargada exitosamente                      │    │
│  │ [10:32:17] ℹ️ Encontradas 156 publicaciones                    │    │
│  │ [10:32:18] ⚡ 45 PDFs en caché, descargando 111               │    │
│  │ [10:32:45] ✓ PDF 1/111: "Decreto 1234" - PyPDF2 OK           │    │
│  │ [10:32:47] ⚠️ PDF 2/111: "Ley 5678" - Fallback a OCR          │    │
│  │ [10:32:52] ✓ PDF 2/111: "Ley 5678" - OCR exitoso             │    │
│  │ [10:33:01] 🚦 Rate limit: esperando 3s...                     │    │
│  │ [10:33:04] ✓ Continuando descargas...                         │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │
│  │ PROCESADOS      │  │ DESDE CACHÉ     │  │ ERRORES         │        │
│  │ 114/156         │  │ 45 (39.5%)      │  │ 0               │        │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘        │
│                                                                          │
│  [Pausar] [Cancelar] [Ver Detalles]                                    │
└──────────────────────────────────────────────────────────────────────────┘
```

## 3. Detalle de Métricas por Ejecución

```
┌──────────────────────────────────────────────────────────────────────────┐
│ 📊 Detalle de Ejecución - 07 Enero 2024 10:30:00                       │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Información General                                                     │
│  ├─ Estado: ✅ Exitoso                                                  │
│  ├─ Duración: 3m 45s                                                   │
│  ├─ Publicaciones: 156 (32 relevantes)                                  │
│  └─ Memoria usada: 127 MB                                              │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ PDFs Procesados - Top 10 más lentos                           │    │
│  ├────────────────────────────────────────────────────────────────┤    │
│  │ # │ Título                    │ Método   │ Tiempo │ Tamaño   │    │
│  ├───┼───────────────────────────┼──────────┼────────┼──────────┤    │
│  │ 1 │ Decreto Supremo 1234/2024 │ OCR      │ 8.2s   │ 15.3 MB  │    │
│  │ 2 │ Ley 5678 Modificación...  │ OCR      │ 7.5s   │ 12.1 MB  │    │
│  │ 3 │ Resolución Exenta 910     │ PDFMiner │ 4.3s   │ 8.7 MB   │    │
│  │ 4 │ Circular 111/2024         │ PyPDF2   │ 2.1s   │ 3.2 MB   │    │
│  │ 5 │ Decreto Alcaldicio 222    │ Cache    │ 0.1s   │ 2.1 MB   │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌────────────────────────────┐  ┌────────────────────────────────┐    │
│  │ Distribución de Tiempos   │  │ Uso de APIs                   │    │
│  │                           │  │                               │    │
│  │ Descarga    ███ 35%      │  │ Gemini AI                     │    │
│  │ Extracción  █████ 45%    │  │ ├─ Llamadas: 32              │    │
│  │ Análisis    ██ 20%       │  │ ├─ Exitosas: 31 (96.9%)      │    │
│  │                           │  │ ├─ Tiempo promedio: 1.2s     │    │
│  │ Total: 3m 45s            │  │ └─ Costo estimado: $0.08     │    │
│  └────────────────────────────┘  └────────────────────────────────┘    │
│                                                                          │
│  [← Volver] [Exportar Reporte] [Ver Logs Completos]                    │
└──────────────────────────────────────────────────────────────────────────┘
```

## 4. Panel de Configuración y Alertas

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ⚙️ Configuración del Sistema                                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  🚦 Rate Limiting                                                       │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ Dominio                              │ Max Req │ Ventana      │    │
│  ├──────────────────────────────────────┼─────────┼──────────────┤    │
│  │ diariooficial.interior.gob.cl        │ 5       │ 60s          │    │
│  │ api.gemini.google.com                │ 60      │ 60s          │    │
│  │ api.huggingface.co                   │ 30      │ 60s          │    │
│  │ [+ Agregar dominio]                  │         │              │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  🔔 Alertas Configuradas                                                │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ☑️ Tasa de éxito < 90%              → Email a admin@empresa.cl │    │
│  │ ☑️ Tiempo promedio > 5 min          → SMS a +56 9 1234 5678   │    │
│  │ ☑️ Errores consecutivos > 3         → Slack #ops-alerts       │    │
│  │ ☐ Uso de caché < 50%               → Dashboard notification   │    │
│  │ [+ Nueva alerta]                                               │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  💾 Caché Redis                         📝 Logging                      │
│  ├─ Estado: 🟢 Conectado               ├─ Nivel: INFO                  │
│  ├─ Uso: 2.3 GB / 8 GB                 ├─ Formato: JSON               │
│  ├─ Hit Rate: 87.3%                    ├─ Rotación: Diaria            │
│  └─ TTL PDFs: 7 días                   └─ Retención: 30 días          │
│                                                                          │
│  [Guardar Cambios] [Limpiar Caché] [Exportar Configuración]            │
└──────────────────────────────────────────────────────────────────────────┘
```

## 5. Vista de Logs Estructurados

```
┌──────────────────────────────────────────────────────────────────────────┐
│ 📝 Visor de Logs - Tiempo Real                                          │
├──────────────────────────────────────────────────────────────────────────┤
│ Filtros: [INFO ▼] [Últimas 24h ▼] [Todos los módulos ▼] 🔍 Buscar...  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ {                                                                        │
│   "timestamp": "2024-01-07T10:33:45.123Z",                             │
│   "level": "INFO",                                                      │
│   "logger": "alerts.scraper_diario_oficial",                           │
│   "message": "PDF procesado exitosamente",                             │
│   "module": "scraper_diario_oficial",                                  │
│   "function": "extraer_texto_pdf_mixto",                               │
│   "line": 89,                                                          │
│   "pdf_url": "https://www.diariooficial.interior.gob.cl/2024/01/07/decreto-1234.pdf", │
│   "extraction_method": "pypdf2",                                        │
│   "duration_seconds": 1.23,                                            │
│   "from_cache": false,                                                 │
│   "pdf_size_mb": 3.2,                                                  │
│   "pages_extracted": 2                                                 │
│ }                                                                       │
│ ─────────────────────────────────────────────────────────────────────   │
│ {                                                                        │
│   "timestamp": "2024-01-07T10:33:46.789Z",                             │
│   "level": "WARNING",                                                   │
│   "logger": "alerts.utils.rate_limiter",                               │
│   "message": "Rate limit alcanzado. Esperando 3.0 segundos...",        │
│   "domain": "diariooficial.interior.gob.cl",                           │
│   "requests_made": 5,                                                   │
│   "window_seconds": 60                                                 │
│ }                                                                       │
│                                                                          │
│ [Pausar] [Limpiar] [Exportar] [Configurar Filtros]                     │
└──────────────────────────────────────────────────────────────────────────┘
```

## Características Visuales Destacadas:

1. **Dashboard Responsivo**: Gráficos en tiempo real con Chart.js
2. **Indicadores KPI**: Métricas clave con comparación período anterior
3. **Logs Estructurados**: JSON formateado para fácil análisis
4. **Progress Bars**: Visualización del progreso en tiempo real
5. **Alertas Visuales**: Códigos de color para estados (✅ ⚠️ ❌)
6. **Interfaz Admin**: Integrada con Django Admin personalizado

La plataforma ahora ofrece visibilidad completa del sistema con métricas en tiempo real, logs estructurados y configuración flexible, todo en una interfaz moderna y profesional.