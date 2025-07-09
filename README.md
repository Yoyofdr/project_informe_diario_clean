# Informe Diario – Backend robusto y escalable

## Descripción
Plataforma Django para el procesamiento, análisis y entrega de información relevante del Diario Oficial y Hechos Esenciales, con enfoque en robustez, eficiencia y escalabilidad.

---

## Servicios y utilidades integradas

### 1. **Sistema de Caché (Redis/Django cache)**
- **Ubicación:** `alerts/services/cache_service.py`
- **Uso:** Cachea PDFs, resultados de scraping y respuestas de API para evitar descargas y procesamiento repetido.
- **Ejemplo:**
```python
from alerts.services.cache_service import cache_service
pdf_bytes = cache_service.get_pdf_content(url_pdf)
```

### 2. **Extractor de PDFs robusto**
- **Ubicación:** `alerts/services/pdf_extractor.py`
- **Uso:** Extrae texto de PDFs usando PyPDF2, PDFMiner y OCR con fallback automático.
- **Ejemplo:**
```python
from alerts.services.pdf_extractor import PDFExtractor
extractor = PDFExtractor()
texto, metodo = extractor.extract_text(pdf_bytes)
```

### 3. **Reintentos automáticos (retry)**
- **Ubicación:** `alerts/utils/retry_utils.py`
- **Uso:** Decorador para funciones críticas que pueden fallar (descarga de PDFs, requests externos).
- **Ejemplo:**
```python
from alerts.utils.retry_utils import retry
@retry(max_attempts=3, backoff_base=2)
def funcion_critica(): ...
```

### 4. **Rate Limiting inteligente**
- **Ubicación:** `alerts/utils/rate_limiter.py`
- **Uso:** Limita la cantidad de requests por dominio para evitar bloqueos.
- **Ejemplo:**
```python
from alerts.utils.rate_limiter import rate_limited
@rate_limited
def funcion_con_request(url): ...
```

### 5. **Optimización de queries Django**
- **Ubicación:** `alerts/utils/db_optimizations.py`
- **Uso:** Utilidades y helpers para aplicar `select_related`, `prefetch_related` y anotaciones en queries complejas.
- **Ejemplo:**
```python
from alerts.utils.db_optimizations import optimize_empresa_queries
empresas = optimize_empresa_queries(Empresa.objects.all())
```

---

## Buenas prácticas
- Siempre usar los servicios de caché y extractor robusto en scraping y análisis de PDFs.
- Decorar funciones de requests externos con `@retry` y `@rate_limited`.
- Optimizar queries en vistas y comandos usando los helpers de `db_optimizations`.
- Mantener los tests actualizados (`alerts/tests/`).

---

## Configuración y despliegue rápido
1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configurar Redis** (opcional pero recomendado para caché eficiente).
3. **Variables de entorno:**
   - `GEMINI_API_KEY` y `HF_API_TOKEN` para IA.
4. **Migrar la base de datos:**
   ```bash
   python manage.py migrate
   ```
5. **Correr los tests:**
   ```bash
   python manage.py test alerts.tests
   ```
6. **Ejecutar el servidor:**
   ```bash
   python manage.py runserver
   ```

---

## Contacto y soporte
Para dudas técnicas, contacta al equipo de desarrollo.

---

## Monitoreo y métricas

### Servicio interno de métricas
- **Ubicación:** `alerts/services/metrics_service.py`
- **Uso:** Permite trackear duración, éxito, errores y detalles de scraping, descargas de PDF y llamadas a APIs.
- **Ejemplo básico:**
```python
from alerts.services.metrics_service import metrics_collector
from datetime import datetime

# Iniciar sesión de scraping
metric = metrics_collector.start_scraping(datetime.now())

# Trackear procesamiento de un PDF
with metrics_collector.track_pdf_processing(url_pdf, titulo) as pdf_metric:
    # ... procesamiento ...
    metrics_collector.record_pdf_extraction(pdf_metric, metodo, tiempo)

# Finalizar sesión
metrics_collector.end_scraping(exitoso=True)
```
- Los datos quedan en la base de datos y pueden consultarse vía Django Admin o scripts.

### Sugerencias de integración externa
- Puedes conectar con Sentry, Prometheus, Grafana, etc. usando señales de Django o hooks en los métodos del servicio.
- Para alertas en tiempo real, puedes agregar notificaciones en los métodos `end_scraping` o `track_api_call`. 