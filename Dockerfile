# Dockerfile para Informe Diario (Django)
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev tesseract-ocr poppler-utils libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y código
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=market_sniper.settings

# Migraciones y collectstatic (opcional)
RUN python manage.py migrate --noinput || true
RUN python manage.py collectstatic --noinput || true

# Comando por defecto: gunicorn
CMD ["gunicorn", "market_sniper.wsgi:application", "--bind", "0.0.0.0:8000"] 