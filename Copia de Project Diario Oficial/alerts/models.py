from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class PerfilUsuario(models.Model):
    """
    Extiende el modelo de usuario para añadir el plan de suscripción.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    suscripciones = models.ManyToManyField('Empresa', blank=True, related_name='perfiles_suscritos')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Asegura que cada usuario tenga un perfil.
    """
    if created:
        PerfilUsuario.objects.create(user=instance)
    
    # Esto puede ser redundante si el perfil se crea y guarda, pero asegura que exista.
    if not hasattr(instance, 'perfil'):
         PerfilUsuario.objects.create(user=instance)
    instance.perfil.save()

class Empresa(models.Model):
    """
    Representa una empresa emisora de Hechos Esenciales.
    """
    nombre = models.CharField(max_length=255, unique=True)
    rut = models.CharField(max_length=20, blank=True, null=True, unique=True)
    rubro = models.CharField(max_length=100, blank=True, null=True, help_text="Rubro o industria de la empresa.")
    es_ipsa = models.BooleanField(default=False, help_text="Indica si la empresa forma parte del índice IPSA.")
    notificacion_enviada = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']

class HechoEsencial(models.Model):
    """
    Representa un Hecho Esencial publicado por una empresa.
    """
    RELEVANCIA_CHOICES = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='hechos_esenciales')
    titulo = models.CharField(max_length=500)
    url = models.URLField(max_length=500, unique=True)
    fecha_publicacion = models.DateTimeField()
    resumen = models.TextField(blank=True, null=True, help_text="Resumen del hecho esencial generado por IA.")
    relevancia = models.IntegerField(choices=RELEVANCIA_CHOICES, blank=True, null=True, help_text="Nivel de relevancia determinado por IA.")
    notificacion_enviada = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return f"{self.empresa.nombre} - {self.fecha_publicacion}"

class Alerta(models.Model):
    """
    Representa un Hecho Esencial publicado por una empresa.
    """
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='alertas')
    fecha_publicacion = models.DateTimeField()
    numero_documento = models.CharField(max_length=50, unique=True)
    url_documento = models.URLField(max_length=500)
    contenido = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Alerta de {self.empresa.nombre} - {self.numero_documento}"

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
        ordering = ['-fecha_publicacion']

class Suscripcion(models.Model):
    """
    DEPRECATED: Este modelo ha sido reemplazado por la relación ManyToMany en PerfilUsuario.
    Se mantiene temporalmente para evitar errores de migración, pero no se utiliza en la lógica nueva.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    activa = models.BooleanField(default=True)

    class Meta:
        # unique_together = ('usuario', 'empresa') # Comentado para evitar conflictos
        pass

class NotificacionEnviada(models.Model):
    """
    Registra cada notificación de Hecho Esencial que se ha enviado a un usuario.
    Esto es crucial para respetar los límites del plan de suscripción.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    hecho_esencial = models.ForeignKey(HechoEsencial, on_delete=models.CASCADE)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'hecho_esencial')

    def __str__(self):
        return f"Notificación para {self.usuario.username} sobre {self.hecho_esencial.empresa.nombre} el {self.fecha_envio.strftime('%Y-%m-%d')}"

class Organizacion(models.Model):
    nombre = models.CharField(max_length=200)
    dominio = models.CharField(max_length=80, help_text="Ej: empresa.com")
    fecha_pago = models.DateTimeField(null=True, blank=True)
    suscripcion_activa = models.BooleanField(default=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizaciones')
    PLAN_CHOICES = [
        ('gratis', 'Gratis'),
        ('premium', 'Premium'),
    ]
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='gratis')

    def __str__(self):
        return f"{self.nombre} ({self.dominio})"

class Destinatario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True, null=True)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, related_name='destinatarios')

    def __str__(self):
        return f"{self.nombre} <{self.email}>"

class RegistroPago(models.Model):
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=30, choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado'), ('fallido', 'Fallido')], default='pendiente')

    def __str__(self):
        return f"Pago {self.monto} - {self.organizacion.nombre} ({self.estado})"

class SuscripcionLanding(models.Model):
    email = models.EmailField()
    organizacion = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} ({self.organizacion})"

class InformeEnviado(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    destinatarios = models.TextField()
    enlace_html = models.CharField(max_length=255, blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Informe {self.empresa.nombre} - {self.fecha_envio.date()}"


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