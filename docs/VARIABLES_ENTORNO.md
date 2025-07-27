# Variables de Entorno - Informe Diario Chile

## 🔒 Configuración Segura con Variables de Entorno

El proyecto ahora usa variables de entorno para proteger información sensible como contraseñas.

## 📋 Variables Disponibles

### Email (Hostinger)
```bash
# Credenciales de email
HOSTINGER_EMAIL_PASSWORD=tu_contraseña_aqui

# Configuración SMTP (opcional, tiene valores por defecto)
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=587
EMAIL_FROM=contacto@informediariochile.cl
EMAIL_FROM_NAME=Informe Diario Chile

# Destinatario por defecto (opcional)
DEFAULT_TO_EMAIL=rfernandezdelrio@uc.cl
```

### Otras APIs (si las usas)
```bash
# OpenAI para resúmenes
OPENAI_API_KEY=tu_api_key_aqui

# Django
SECRET_KEY=tu_secret_key_django
DEBUG=False
```

## 🚀 Cómo Configurar

### 1. Desarrollo Local

1. **Crea el archivo `.env`** en la raíz del proyecto:
   ```bash
   cd /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial/repo_clean
   nano .env
   ```

2. **Agrega las variables**:
   ```
   HOSTINGER_EMAIL_PASSWORD=Rfdr1729!
   DEFAULT_TO_EMAIL=rfernandezdelrio@uc.cl
   ```

3. **Verifica que funcione**:
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅' if os.getenv('HOSTINGER_EMAIL_PASSWORD') else '❌')"
   ```

### 2. Producción (Heroku)

```bash
heroku config:set HOSTINGER_EMAIL_PASSWORD=tu_contraseña
heroku config:set EMAIL_FROM=contacto@informediariochile.cl
heroku config:set SMTP_SERVER=smtp.hostinger.com
```

### 3. Producción (Servidor Linux)

1. **Edita el archivo de entorno del sistema**:
   ```bash
   sudo nano /etc/environment
   ```

2. **Agrega las variables**:
   ```
   HOSTINGER_EMAIL_PASSWORD="tu_contraseña"
   EMAIL_FROM="contacto@informediariochile.cl"
   ```

3. **O usa systemd** (si usas servicios):
   ```ini
   [Service]
   Environment="HOSTINGER_EMAIL_PASSWORD=tu_contraseña"
   Environment="EMAIL_FROM=contacto@informediariochile.cl"
   ```

## 🔍 Verificar Variables

### Script de verificación:
```python
# check_env.py
import os
from dotenv import load_dotenv

load_dotenv()

variables = [
    'HOSTINGER_EMAIL_PASSWORD',
    'EMAIL_FROM',
    'SMTP_SERVER',
    'DEFAULT_TO_EMAIL'
]

print("🔍 Verificando variables de entorno:\n")
for var in variables:
    value = os.getenv(var)
    if value:
        # Ocultar parte de la contraseña
        if 'PASSWORD' in var:
            display = value[:3] + '*' * (len(value) - 3)
        else:
            display = value
        print(f"✅ {var}: {display}")
    else:
        print(f"❌ {var}: No configurada")
```

## 📁 Archivos que Usan Variables

1. **config/email_settings.py**
   - Lee todas las configuraciones de email del .env

2. **generar_informe_oficial_integrado_mejorado.py**
   - Usa las variables para enviar emails

3. **market_sniper/settings.py**
   - Puede usar SECRET_KEY y DEBUG del .env

## 🚨 Importante

### NO hacer:
- ❌ Subir `.env` a Git (ya está en .gitignore)
- ❌ Compartir las credenciales en código
- ❌ Hardcodear contraseñas en los archivos

### SÍ hacer:
- ✅ Usar diferentes `.env` para desarrollo y producción
- ✅ Documentar qué variables son necesarias
- ✅ Usar valores por defecto sensatos
- ✅ Rotar contraseñas periódicamente

## 🆘 Troubleshooting

### "No se encontró la contraseña del email"
```bash
# Verificar que el .env existe
ls -la .env

# Verificar el contenido (con cuidado)
cat .env | grep HOSTINGER

# Verificar que python-dotenv está instalado
pip install python-dotenv
```

### Variables no se cargan
```python
# Verificar la ruta del .env
from pathlib import Path
print(Path('.env').absolute())

# Cargar manualmente
from dotenv import load_dotenv
load_dotenv(verbose=True)  # Muestra información de debug
```

## 📝 Template .env.example

Crea un archivo `.env.example` para nuevos desarrolladores:

```bash
# Email Configuration
HOSTINGER_EMAIL_PASSWORD=your_password_here
EMAIL_FROM=contacto@informediariochile.cl
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=587
DEFAULT_TO_EMAIL=your_email@example.com

# API Keys (if needed)
OPENAI_API_KEY=your_openai_key_here

# Django
SECRET_KEY=your_secret_key_here
DEBUG=True
```

Este archivo SÍ se puede subir a Git como referencia.