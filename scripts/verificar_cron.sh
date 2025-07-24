#!/bin/bash
# Script para verificar el estado del sistema de envío automático

echo "=== VERIFICACIÓN DEL SISTEMA DE ENVÍO AUTOMÁTICO ==="
echo ""

# 1. Verificar cron
echo "1. CONFIGURACIÓN DEL CRON:"
echo "--------------------------"
crontab -l | grep informe_diario_oficial
echo ""

# 2. Verificar si el scheduler está corriendo
echo "2. ESTADO DEL SCHEDULER:"
echo "-----------------------"
if pgrep -f "run_scheduler" > /dev/null; then
    echo "✓ El scheduler está ejecutándose"
    ps aux | grep run_scheduler | grep -v grep
else
    echo "✗ El scheduler NO está ejecutándose"
fi
echo ""

# 3. Verificar últimos logs
echo "3. ÚLTIMAS ENTRADAS DEL LOG DE CRON:"
echo "-----------------------------------"
if [ -f "/Users/rodrigofernandezdelrio/Desktop/Project Diario Oficial/cron_informe.log" ]; then
    tail -n 10 "/Users/rodrigofernandezdelrio/Desktop/Project Diario Oficial/cron_informe.log"
else
    echo "No se encontró el archivo de log"
fi
echo ""

# 4. Verificar próxima ejecución
echo "4. PRÓXIMA EJECUCIÓN PROGRAMADA:"
echo "--------------------------------"
echo "El informe se enviará a las 8:00 AM todos los días"
echo "Hora actual: $(date)"
echo ""

# 5. Test de envío
echo "5. PARA HACER UN TEST MANUAL:"
echo "-----------------------------"
echo "cd /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial"
echo "python manage.py informe_diario_oficial"
echo ""