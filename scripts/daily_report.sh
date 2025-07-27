#!/bin/bash
# Script de ejecución diaria del informe

# Configurar variables de entorno
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
cd "$(dirname "$0")/.."

# Cargar variables de entorno
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Log file
LOG_DIR="logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/daily_report_$(date +%Y%m%d).log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando generación de informe diario" | tee -a "$LOG_FILE"

# Verificar día de la semana (0=domingo, 6=sábado)
DAY_OF_WEEK=$(date +%w)
if [ "$DAY_OF_WEEK" -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Es domingo - no se envía informe" | tee -a "$LOG_FILE"
    exit 0
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Ejecutar el script de generación masiva (para todos los suscriptores)
python3 generar_informe_oficial_integrado_todos.py 2>&1 | tee -a "$LOG_FILE"

# Verificar resultado
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Informe generado y enviado exitosamente" | tee -a "$LOG_FILE"
    
    # Enviar notificación de éxito (opcional)
    if [ ! -z "$NOTIFICATION_EMAIL" ]; then
        echo "Informe diario enviado exitosamente" | mail -s "✅ Informe Diario - OK" "$NOTIFICATION_EMAIL"
    fi
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Error al generar el informe" | tee -a "$LOG_FILE"
    
    # Enviar notificación de error
    if [ ! -z "$NOTIFICATION_EMAIL" ]; then
        tail -50 "$LOG_FILE" | mail -s "❌ Error - Informe Diario" "$NOTIFICATION_EMAIL"
    fi
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Proceso finalizado" | tee -a "$LOG_FILE"
