# Instrucciones para el Envío Automático del Informe Diario

## Estado Actual ✅

He corregido el sistema de envío automático. Ahora el informe se enviará **todos los días a las 8:00 AM**.

### Cambios realizados:

1. **Corregí el horario del cron**: Cambié de 12:30 PM a 8:00 AM
2. **Creé scripts de respaldo**: Para asegurar que funcione correctamente
3. **Agregué herramientas de verificación**: Para monitorear el estado

## Cómo verificar que está funcionando

Ejecuta este comando en la terminal:
```bash
/Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial/verificar_cron.sh
```

## Opciones de configuración

### Opción 1: Cron (ACTUALMENTE ACTIVA) ✅
El sistema está configurado para ejecutarse automáticamente a las 8:00 AM usando cron.

### Opción 2: Scheduler Python (RESPALDO)
Si prefieres usar el scheduler de Python, ejecuta:
```bash
/Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial/iniciar_scheduler.sh
```

### Opción 3: LaunchAgent macOS (MÁS CONFIABLE)
Para instalar como servicio del sistema:
```bash
# Copiar el archivo plist
cp /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial/com.informediario.scheduler.plist ~/Library/LaunchAgents/

# Cargar el servicio
launchctl load ~/Library/LaunchAgents/com.informediario.scheduler.plist
```

## Solución de problemas

### Si el informe no se envía:

1. **Verifica el cron**:
   ```bash
   crontab -l
   ```
   Debe mostrar: `0 8 * * * cd /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial && ...`

2. **Revisa los logs**:
   ```bash
   tail -f /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial/cron_informe.log
   ```

3. **Prueba manual**:
   ```bash
   cd /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial
   python manage.py informe_diario_oficial
   ```

### Si hay errores de Selenium:

1. Asegúrate de que Chrome esté actualizado
2. Verifica que ChromeDriver esté instalado
3. Considera reiniciar el sistema

## Cambiar el horario de envío

Para cambiar la hora de envío (por ejemplo a las 9:00 AM):

```bash
# Editar cron
crontab -e

# Cambiar la línea a:
0 9 * * * cd /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial && ...
```

## Logs y monitoreo

- **Log del cron**: `/Users/rodrigofernandezdelrio/Desktop/Project Diario Oficial/cron_informe.log`
- **Log del scheduler**: `/Users/rodrigofernandezdelrio/Desktop/Project Diario Oficial/scheduler.log`
- **Correos enviados**: `/Users/rodrigofernandezdelrio/Desktop/Project Diario Oficial/sent_emails/`

## Notas importantes

1. El sistema necesita que la computadora esté encendida a las 8:00 AM
2. Si la computadora está dormida, el cron se ejecutará cuando despierte
3. Los fines de semana también se envía el informe
4. Si falla el envío, revisa que haya conexión a internet

## Contacto

Si tienes problemas, revisa:
1. Los logs mencionados arriba
2. Ejecuta el script de verificación
3. Prueba el envío manual

¡El sistema ahora debería funcionar correctamente todos los días a las 8:00 AM!