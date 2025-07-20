#!/bin/bash
# Script para iniciar el scheduler del informe diario

cd /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial

# Activar el entorno Python correcto
export PATH="/Users/rodrigofernandezdelrio/.pyenv/shims:$PATH"

# Ejecutar el scheduler
echo "Iniciando scheduler del informe diario..."
python manage.py run_scheduler