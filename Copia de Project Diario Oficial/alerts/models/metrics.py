"""
Modelos para almacenar métricas del sistema de scraping
"""
from django.db import models
from django.utils import timezone


class ScrapingMetric(models.Model):
    """Métricas de cada ejecución del scraping"""
    
    fecha_scraping = models.DateField(help_text="Fecha del diario oficial scrapeado")
    fecha_ejecucion = models.DateTimeField(default=timezone.now, help_text="Momento de ejecución")
    duracion_segundos = models.FloatField(help_text="Duración total del scraping en segundos")
    
    # Contadores
    total_publicaciones = models.IntegerField(default=0)
    publicaciones_relevantes = models.IntegerField(default=0)
    pdfs_descargados = models.IntegerField(default=0)
    pdfs_desde_cache = models.IntegerField(default=0)
    
    # Estados
    exitoso = models.BooleanField(default=True)
    mensaje_error = models.TextField(blank=True, null=True)
    
    # Métricas de rendimiento
    tiempo_descarga_promedio = models.FloatField(null=True, blank=True, help_text="Tiempo promedio de descarga de PDF en segundos")
    tiempo_procesamiento_promedio = models.FloatField(null=True, blank=True, help_text="Tiempo promedio de procesamiento de PDF en segundos")
    
    # Uso de recursos
    memoria_usada_mb = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_ejecucion']
        indexes = [
            models.Index(fields=['-fecha_ejecucion']),
            models.Index(fields=['fecha_scraping']),
            models.Index(fields=['exitoso']),
        ]
        verbose_name = "Métrica de Scraping"
        verbose_name_plural = "Métricas de Scraping"
    
    def __str__(self):
        return f"Scraping {self.fecha_scraping} - {'Exitoso' if self.exitoso else 'Fallido'}"
    
    @property
    def tasa_cache(self):
        """Porcentaje de PDFs obtenidos desde caché"""
        total = self.pdfs_descargados + self.pdfs_desde_cache
        if total == 0:
            return 0
        return (self.pdfs_desde_cache / total) * 100
    
    @property
    def tasa_relevancia(self):
        """Porcentaje de publicaciones relevantes"""
        if self.total_publicaciones == 0:
            return 0
        return (self.publicaciones_relevantes / self.total_publicaciones) * 100


class PDFProcessingMetric(models.Model):
    """Métricas detalladas del procesamiento de PDFs"""
    
    scraping_metric = models.ForeignKey(ScrapingMetric, on_delete=models.CASCADE, related_name='pdf_metrics')
    url_pdf = models.URLField()
    titulo = models.CharField(max_length=500)
    
    # Tiempos
    tiempo_descarga = models.FloatField(null=True, blank=True, help_text="Segundos")
    tiempo_extraccion = models.FloatField(null=True, blank=True, help_text="Segundos")
    tiempo_analisis = models.FloatField(null=True, blank=True, help_text="Segundos para generar resumen")
    
    # Estados
    desde_cache = models.BooleanField(default=False)
    metodo_extraccion = models.CharField(
        max_length=20,
        choices=[
            ('pypdf2', 'PyPDF2'),
            ('pdfminer', 'PDFMiner'),
            ('ocr', 'OCR'),
            ('failed', 'Falló'),
        ],
        null=True,
        blank=True
    )
    
    exitoso = models.BooleanField(default=True)
    mensaje_error = models.TextField(blank=True, null=True)
    
    # Características del PDF
    num_paginas = models.IntegerField(null=True, blank=True)
    tamano_bytes = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Métrica de Procesamiento PDF"
        verbose_name_plural = "Métricas de Procesamiento PDF"
    
    def __str__(self):
        return f"PDF: {self.titulo[:50]}..."
    
    @property
    def tiempo_total(self):
        """Tiempo total de procesamiento"""
        total = 0
        if self.tiempo_descarga:
            total += self.tiempo_descarga
        if self.tiempo_extraccion:
            total += self.tiempo_extraccion
        if self.tiempo_analisis:
            total += self.tiempo_analisis
        return total


class APICallMetric(models.Model):
    """Métricas de llamadas a APIs externas"""
    
    api_name = models.CharField(
        max_length=50,
        choices=[
            ('gemini', 'Google Gemini'),
            ('huggingface', 'HuggingFace'),
            ('twilio', 'Twilio WhatsApp'),
        ]
    )
    
    fecha_llamada = models.DateTimeField(default=timezone.now)
    duracion_segundos = models.FloatField()
    exitoso = models.BooleanField(default=True)
    mensaje_error = models.TextField(blank=True, null=True)
    
    # Detalles adicionales
    endpoint = models.CharField(max_length=200, blank=True)
    tokens_usados = models.IntegerField(null=True, blank=True)
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_llamada']
        indexes = [
            models.Index(fields=['-fecha_llamada']),
            models.Index(fields=['api_name']),
            models.Index(fields=['exitoso']),
        ]
        verbose_name = "Métrica de Llamada API"
        verbose_name_plural = "Métricas de Llamadas API"
    
    def __str__(self):
        return f"{self.api_name} - {self.fecha_llamada.strftime('%Y-%m-%d %H:%M')}"