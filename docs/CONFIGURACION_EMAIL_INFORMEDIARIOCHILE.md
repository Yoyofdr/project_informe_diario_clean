# Configuración de Email - Informe Diario Chile

## 📧 Nuevo Email Corporativo

- **Dominio**: informediariochile.cl
- **Email de envío**: contacto@informediariochile.cl
- **Email de contacto**: contacto@informediariochile.cl

## 🔧 Configuración SMTP

### Paso 1: Identificar tu proveedor

El dominio `informediariochile.cl` puede estar configurado con diferentes proveedores:

1. **Google Workspace** (Gmail empresarial)
2. **Microsoft 365** (Outlook empresarial)
3. **Hosting propio** (del proveedor donde compraste el dominio)
4. **Otros** (Zoho, ProtonMail, etc.)

### Paso 2: Obtener credenciales SMTP

Según tu proveedor, necesitarás:

#### Para Google Workspace:
```python
smtp_server = 'smtp.gmail.com'
smtp_port = 587
use_tls = True
# Requiere contraseña de aplicación si tienes 2FA
```

#### Para Microsoft 365:
```python
smtp_server = 'smtp.office365.com'
smtp_port = 587
use_tls = True
```

#### Para hosting común (cPanel, etc):
```python
smtp_server = 'mail.informediariochile.cl'  # o el que te indique tu proveedor
smtp_port = 587  # o 465 para SSL
use_tls = True   # o False si usas SSL
```

### Paso 3: Actualizar configuración

1. **Editar archivo de configuración**:
   ```bash
   nano config/email_settings.py
   ```

2. **Actualizar estos valores**:
   ```python
   EMAIL_CONFIG = {
       'smtp_server': 'TU_SERVIDOR_SMTP',
       'smtp_port': 587,
       'use_tls': True,
       'sender_email': 'contacto@informediariochile.cl',
       'sender_name': 'Informe Diario Chile',
       'sender_password': 'TU_CONTRASEÑA',  # Ver sección de seguridad
   }
   ```

### Paso 4: Aplicar cambios en todo el proyecto

```bash
# Ver qué archivos se actualizarán (modo seguro)
python scripts/actualizar_emails.py

# Aplicar los cambios
python scripts/actualizar_emails.py --apply
```

## 🔒 Seguridad

### Opción 1: Contraseña de Aplicación (Recomendado)

Si tu proveedor lo soporta (Gmail, Outlook):
1. Activa autenticación de 2 factores
2. Genera una contraseña de aplicación específica
3. Usa esa contraseña en lugar de tu contraseña normal

### Opción 2: Variables de Entorno

En lugar de hardcodear la contraseña:

1. **En desarrollo** (.env):
   ```
   EMAIL_PASSWORD=tu_contraseña_aqui
   ```

2. **En producción** (Heroku, etc):
   ```bash
   heroku config:set EMAIL_PASSWORD=tu_contraseña_aqui
   ```

3. **En el código**:
   ```python
   import os
   EMAIL_CONFIG['sender_password'] = os.environ.get('EMAIL_PASSWORD', '')
   ```

## 🧪 Probar configuración

### Test simple de conexión:
```python
# test_email.py
from config.email_settings import EMAIL_CONFIG
import smtplib

try:
    server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
    if EMAIL_CONFIG['use_tls']:
        server.starttls()
    server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
    server.quit()
    print("✅ Conexión exitosa!")
except Exception as e:
    print(f"❌ Error: {e}")
```

### Test de envío:
```bash
# Enviar informe de prueba
python generar_informe_oficial_integrado_mejorado.py
```

## 📝 Checklist de Migración

- [ ] Obtener credenciales SMTP del proveedor
- [ ] Actualizar `config/email_settings.py`
- [ ] Ejecutar `scripts/actualizar_emails.py --apply`
- [ ] Configurar variables de entorno (si aplica)
- [ ] Probar conexión SMTP
- [ ] Enviar email de prueba
- [ ] Actualizar DNS si es necesario (SPF, DKIM)
- [ ] Notificar a usuarios del cambio de remitente

## 🆘 Troubleshooting

### Error: "Authentication failed"
- Verifica usuario y contraseña
- Algunos proveedores requieren el email completo como usuario
- Revisa si necesitas contraseña de aplicación

### Error: "Connection refused"
- Verifica servidor SMTP y puerto
- Algunos hostings bloquean puertos SMTP
- Prueba puerto 465 con SSL en lugar de 587 con TLS

### Error: "Relay access denied"
- El servidor no permite enviar desde esa dirección
- Verifica que el dominio esté configurado correctamente
- Contacta a tu proveedor de hosting

## 📞 Soporte

Si necesitas ayuda con la configuración, contacta a tu proveedor de:
- Dominio/Hosting donde compraste informediariochile.cl
- Servicio de email que estés usando (Google Workspace, etc.)

Ellos te pueden proporcionar:
- Servidor SMTP correcto
- Puerto y método de encriptación
- Requisitos especiales de autenticación