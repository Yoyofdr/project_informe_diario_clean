"""
Vista del dashboard de métricas del sistema de scraping
"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Sum, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from alerts.models import ScrapingMetric, PDFProcessingMetric, APICallMetric
import json


@staff_member_required
def dashboard_metrics(request):
    """Vista principal del dashboard de métricas"""
    
    # Obtener rango de fechas de los últimos 30 días
    fecha_fin = timezone.now()
    fecha_inicio = fecha_fin - timedelta(days=30)
    
    # Métricas generales
    metricas_generales = ScrapingMetric.objects.filter(
        fecha_ejecucion__range=[fecha_inicio, fecha_fin]
    ).aggregate(
        total_ejecuciones=Count('id'),
        ejecuciones_exitosas=Count('id', filter=Q(exitoso=True)),
        promedio_duracion=Avg('duracion_segundos'),
        total_publicaciones=Sum('total_publicaciones'),
        total_relevantes=Sum('publicaciones_relevantes'),
        promedio_pdfs_cache=Avg(F('pdfs_desde_cache') * 100.0 / (F('pdfs_descargados') + F('pdfs_desde_cache')))
    )
    
    # Calcular tasa de éxito
    if metricas_generales['total_ejecuciones'] > 0:
        metricas_generales['tasa_exito'] = (
            metricas_generales['ejecuciones_exitosas'] / metricas_generales['total_ejecuciones'] * 100
        )
    else:
        metricas_generales['tasa_exito'] = 0
    
    # Últimas ejecuciones
    ultimas_ejecuciones = ScrapingMetric.objects.order_by('-fecha_ejecucion')[:10]
    
    # Estadísticas de PDFs por método de extracción
    metodos_extraccion = PDFProcessingMetric.objects.filter(
        scraping_metric__fecha_ejecucion__range=[fecha_inicio, fecha_fin]
    ).values('metodo_extraccion').annotate(
        cantidad=Count('id'),
        tiempo_promedio=Avg('tiempo_extraccion')
    ).order_by('-cantidad')
    
    # Uso de APIs
    apis_stats = APICallMetric.objects.filter(
        fecha_llamada__range=[fecha_inicio, fecha_fin]
    ).values('api_name').annotate(
        total_llamadas=Count('id'),
        llamadas_exitosas=Count('id', filter=Q(exitoso=True)),
        tiempo_promedio=Avg('duracion_segundos'),
        costo_total=Sum('costo_estimado')
    )
    
    # Preparar datos para gráficos
    # Gráfico de publicaciones por día
    publicaciones_por_dia = list(
        ScrapingMetric.objects.filter(
            fecha_ejecucion__range=[fecha_inicio, fecha_fin],
            exitoso=True
        ).values('fecha_scraping').annotate(
            total=Sum('total_publicaciones'),
            relevantes=Sum('publicaciones_relevantes')
        ).order_by('fecha_scraping')
    )
    
    # Convertir fechas a strings para JSON
    for item in publicaciones_por_dia:
        item['fecha_scraping'] = item['fecha_scraping'].strftime('%Y-%m-%d')
    
    # Gráfico de rendimiento (tiempo de ejecución)
    rendimiento_temporal = list(
        ScrapingMetric.objects.filter(
            fecha_ejecucion__range=[fecha_inicio, fecha_fin]
        ).order_by('fecha_ejecucion').values(
            'fecha_ejecucion', 'duracion_segundos', 'exitoso'
        )[:50]  # Últimas 50 ejecuciones
    )
    
    for item in rendimiento_temporal:
        item['fecha_ejecucion'] = item['fecha_ejecucion'].strftime('%Y-%m-%d %H:%M')
    
    # Errores recientes
    errores_recientes = ScrapingMetric.objects.filter(
        exitoso=False,
        fecha_ejecucion__range=[fecha_inicio, fecha_fin]
    ).order_by('-fecha_ejecucion')[:5]
    
    # Estadísticas de caché
    cache_stats = {
        'total_pdfs': PDFProcessingMetric.objects.filter(
            scraping_metric__fecha_ejecucion__range=[fecha_inicio, fecha_fin]
        ).count(),
        'desde_cache': PDFProcessingMetric.objects.filter(
            scraping_metric__fecha_ejecucion__range=[fecha_inicio, fecha_fin],
            desde_cache=True
        ).count()
    }
    
    if cache_stats['total_pdfs'] > 0:
        cache_stats['porcentaje'] = (cache_stats['desde_cache'] / cache_stats['total_pdfs']) * 100
    else:
        cache_stats['porcentaje'] = 0
    
    context = {
        'metricas_generales': metricas_generales,
        'ultimas_ejecuciones': ultimas_ejecuciones,
        'metodos_extraccion': metodos_extraccion,
        'apis_stats': apis_stats,
        'publicaciones_por_dia': json.dumps(publicaciones_por_dia),
        'rendimiento_temporal': json.dumps(rendimiento_temporal),
        'errores_recientes': errores_recientes,
        'cache_stats': cache_stats,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    return render(request, 'alerts/dashboard_metrics.html', context)


@staff_member_required
def detalle_ejecucion(request, metric_id):
    """Vista detallada de una ejecución específica"""
    
    metric = ScrapingMetric.objects.prefetch_related('pdf_metrics').get(pk=metric_id)
    pdf_metrics = metric.pdf_metrics.all().order_by('-tiempo_total')
    
    # Estadísticas de esta ejecución
    stats = pdf_metrics.aggregate(
        total_pdfs=Count('id'),
        pdfs_exitosos=Count('id', filter=Q(exitoso=True)),
        tiempo_total_descarga=Sum('tiempo_descarga'),
        tiempo_total_extraccion=Sum('tiempo_extraccion'),
        tiempo_total_analisis=Sum('tiempo_analisis'),
        tamano_total_mb=Sum('tamano_bytes') / (1024 * 1024) if pdf_metrics.exists() else 0
    )
    
    # PDFs más lentos
    pdfs_lentos = pdf_metrics.order_by('-tiempo_total')[:10]
    
    # PDFs con errores
    pdfs_con_errores = pdf_metrics.filter(exitoso=False)
    
    context = {
        'metric': metric,
        'pdf_metrics': pdf_metrics,
        'stats': stats,
        'pdfs_lentos': pdfs_lentos,
        'pdfs_con_errores': pdfs_con_errores,
    }
    
    return render(request, 'alerts/detalle_ejecucion.html', context)