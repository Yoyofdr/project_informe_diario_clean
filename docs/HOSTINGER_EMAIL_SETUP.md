# Configuración de Email con Hostinger

## 📧 Configuración SMTP para contacto@informediariochile.cl

### Datos de conexión SMTP en Hostinger:

```
Servidor SMTP: smtp.hostinger.com
Puerto: 587 (TLS) o 465 (SSL)
Seguridad: STARTTLS (para puerto 587) o SSL/TLS (para puerto 465)
Usuario: contacto@informediariochile.cl (email completo)
Contraseña: La que configuraste en hPanel
```

## 🔧 Pasos para configurar en Hostinger:

### 1. Crear/Verificar el email en hPanel

1. Ingresa a tu cuenta de Hostinger
2. Ve a **hPanel** → **Emails** → **Cuentas de correo**
3. Si no existe, crea `contacto@informediariochile.cl`
4. Anota la contraseña (o crea una nueva)

### 2. Verificar configuración SMTP

En hPanel, busca **Configuración de correo** donde verás:
- Servidor entrante (IMAP): imap.hostinger.com
- Servidor saliente (SMTP): smtp.hostinger.com
- Puertos y tipo de seguridad

### 3. Actualizar la configuración en el proyecto

1. **Edita el archivo** `config/email_settings.py`:
   ```python
   EMAIL_CONFIG = {
       'smtp_server': 'smtp.hostinger.com',
       'smtp_port': 587,
       'use_tls': True,
       'sender_email': 'contacto@informediariochile.cl',
       'sender_name': 'Informe Diario Chile',
       'sender_password': 'TU_CONTRASEÑA_DE_HOSTINGER',  # <-- ACTUALIZAR AQUÍ
       'default_recipient': 'rfernandezdelrio@uc.cl'
   }
   ```

2. **Aplica los cambios** en todo el proyecto:
   ```bash
   cd /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial/repo_clean
   python scripts/actualizar_emails.py --apply
   ```

## 🧪 Script de prueba para Hostinger

Crea un archivo `test_hostinger_email.py`:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
EMAIL = "contacto@informediariochile.cl"
PASSWORD = "TU_CONTRASEÑA"  # Actualizar con tu contraseña

def test_email():
    try:
        # Conectar al servidor
        print(f"Conectando a {SMTP_SERVER}:{SMTP_PORT}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        
        print(f"Autenticando como {EMAIL}...")
        server.login(EMAIL, PASSWORD)
        
        # Crear mensaje de prueba
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = "rfernandezdelrio@uc.cl"
        msg['Subject'] = "Prueba - Informe Diario Chile"
        
        body = "Este es un email de prueba desde el nuevo dominio informediariochile.cl"
        msg.attach(MIMEText(body, 'plain'))
        
        # Enviar
        print("Enviando email de prueba...")
        server.send_message(msg)
        server.quit()
        
        print("✅ Email enviado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_email()
```

## 🚨 Troubleshooting Hostinger

### Error: "Authentication failed"
- Verifica que uses el email completo como usuario
- La contraseña es la del email, no la de tu cuenta Hostinger
- Puedes resetear la contraseña desde hPanel

### Error: "Connection timeout"
- Algunos ISP bloquean el puerto 587
- Prueba con puerto 465 y SSL:
  ```python
  'smtp_port': 465,
  'use_tls': False,  # Cambiar a False
  'use_ssl': True,   # Agregar esta línea
  ```

### Error: "Relay access denied"
- Verifica que el dominio esté activo en Hostinger
- Espera 24-48h si recién configuraste el dominio
- Revisa que el email exista en hPanel

## 📝 Verificación de DNS

Para mejor entrega de emails, verifica en hPanel:

1. **Registros MX**: Deben apuntar a Hostinger
2. **SPF Record**: Agrega si no existe:
   ```
   v=spf1 include:hostinger.com ~all
   ```
3. **DKIM**: Hostinger lo configura automáticamente

## 🔒 Seguridad

### Opción 1: Usar variables de entorno

1. Crea un archivo `.env` en la raíz del proyecto:
   ```
   HOSTINGER_EMAIL_PASSWORD=tu_contraseña_real
   ```

2. Actualiza `config/email_settings.py`:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   EMAIL_CONFIG = {
       ...
       'sender_password': os.getenv('HOSTINGER_EMAIL_PASSWORD', ''),
       ...
   }
   ```

### Opción 2: Usar Django settings

Si usas Django, puedes agregar en `settings.py`:
```python
# Email settings para Hostinger
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'contacto@informediariochile.cl'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'Informe Diario Chile <contacto@informediariochile.cl>'
```

## ✅ Checklist Final

- [ ] Email creado en hPanel de Hostinger
- [ ] Contraseña del email anotada
- [ ] `config/email_settings.py` actualizado con contraseña
- [ ] Script `actualizar_emails.py --apply` ejecutado
- [ ] Email de prueba enviado exitosamente
- [ ] DNS verificado (MX, SPF)
- [ ] Variables de entorno configuradas (opcional)

## 📞 Soporte Hostinger

Si necesitas ayuda:
- Chat en vivo 24/7 en tu cuenta Hostinger
- Base de conocimientos: https://support.hostinger.com/es/
- Ticket de soporte desde hPanel