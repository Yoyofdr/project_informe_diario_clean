"""
Configuración centralizada de email para Informe Diario
Actualizar con las credenciales correctas del proveedor de email
"""
import os
from pathlib import Path

# Intentar cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # Si python-dotenv no está instalado, usar las variables del sistema
    pass

# Configuración de email principal - HOSTINGER
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.hostinger.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'use_tls': True,
    'sender_email': os.getenv('EMAIL_FROM', 'contacto@informediariochile.cl'),
    'sender_name': os.getenv('EMAIL_FROM_NAME', 'Informe Diario Chile'),
    'sender_password': os.getenv('HOSTINGER_EMAIL_PASSWORD', ''),  # Ahora viene del .env
    
    # Email por defecto para pruebas
    'default_recipient': os.getenv('DEFAULT_TO_EMAIL', 'rfernandezdelrio@uc.cl')
}

# Configuraciones por proveedor (ejemplos)
PROVIDER_CONFIGS = {
    'hostinger': {
        'smtp_server': 'smtp.hostinger.com',
        'smtp_port': 587,
        'use_tls': True,
        'notes': 'Usar la contraseña del email creada en hPanel. Puerto alternativo: 465 con SSL'
    },
    'gmail': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'use_tls': True,
        'notes': 'Requiere contraseña de aplicación si tienes 2FA activado'
    },
    'outlook': {
        'smtp_server': 'smtp-mail.outlook.com',
        'smtp_port': 587,
        'use_tls': True,
        'notes': 'Usar email completo como usuario'
    },
    'office365': {
        'smtp_server': 'smtp.office365.com',
        'smtp_port': 587,
        'use_tls': True,
        'notes': 'Para cuentas empresariales de Microsoft'
    },
    'zoho': {
        'smtp_server': 'smtp.zoho.com',
        'smtp_port': 587,
        'use_tls': True,
        'notes': 'Verificar que el dominio esté configurado'
    }
}

# Función helper para obtener configuración
def get_email_config():
    """Retorna la configuración de email actual"""
    return EMAIL_CONFIG

# Instrucciones de configuración
"""
PASOS PARA CONFIGURAR:

1. Identifica tu proveedor de email
2. Actualiza EMAIL_CONFIG con los datos correctos:
   - smtp_server: Servidor SMTP de tu proveedor
   - smtp_port: Puerto (generalmente 587 para TLS o 465 para SSL)
   - sender_password: Tu contraseña o contraseña de aplicación

3. Si usas Gmail con 2FA:
   - Ve a https://myaccount.google.com/apppasswords
   - Genera una contraseña de aplicación
   - Usa esa contraseña en lugar de tu contraseña normal

4. Para otros proveedores, consulta su documentación SMTP

5. SEGURIDAD: Nunca subas las credenciales reales a Git
   Considera usar variables de entorno:
   
   import os
   EMAIL_CONFIG['sender_password'] = os.environ.get('EMAIL_PASSWORD', '')
"""