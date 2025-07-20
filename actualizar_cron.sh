#!/bin/bash

# Script para actualizar el cron y usar el nuevo script de envío

echo "=== Actualizando configuración de cron para envío diario ==="

# Crear respaldo del cron actual
echo "Respaldando cron actual..."
crontab -l > cron_backup_$(date +%Y%m%d_%H%M%S).txt

# Crear nuevo archivo de cron
cat > cron_actualizado.txt << 'EOF'
# Envío diario del Informe Diario Oficial a las 8:00 AM
0 8 * * * cd /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial && /Users/rodrigofernandezdelrio/.pyenv/shims/python3 enviar_informe_diario.py >> /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial/informe_diario.log 2>&1
EOF

echo "Nuevo cron creado:"
cat cron_actualizado.txt

# Preguntar confirmación
echo ""
echo "¿Deseas aplicar esta configuración? (s/n)"
read -r respuesta

if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
    # Aplicar el nuevo cron
    crontab cron_actualizado.txt
    echo "✅ Cron actualizado exitosamente"
    
    # Verificar
    echo ""
    echo "Verificando nueva configuración:"
    crontab -l
    
    # Limpiar
    rm cron_actualizado.txt
    
    echo ""
    echo "=== IMPORTANTE ==="
    echo "El informe ahora se enviará diariamente a las 8:00 AM usando el script mejorado."
    echo "Los logs se guardarán en: informe_diario.log"
    echo ""
    echo "Para probar el envío manualmente, ejecuta:"
    echo "cd /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial && python3 enviar_informe_diario.py"
else
    echo "Actualización cancelada. El cron no fue modificado."
    rm cron_actualizado.txt
fi