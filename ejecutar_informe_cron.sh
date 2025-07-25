#!/bin/bash

# Script wrapper para ejecutar el informe desde cron
# Configurar pyenv
export PATH="/Users/rodrigofernandezdelrio/.pyenv/shims:$PATH"
export PYENV_ROOT="$HOME/.pyenv"

# Configurar Django
export DJANGO_SETTINGS_MODULE="market_sniper.settings"

# Cambiar al directorio correcto
cd /Users/rodrigofernandezdelrio/conductor/repo/informediario/chennai

# Ejecutar el script Python
/Users/rodrigofernandezdelrio/.pyenv/shims/python3 generar_informe_oficial_integrado_mejorado.py