#!/usr/bin/env python3
"""
Script para verificar que las variables de entorno estén configuradas correctamente
"""
import os
from pathlib import Path

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(verbose=True)
        print("✅ Archivo .env cargado exitosamente\n")
    else:
        print("⚠️  No se encontró archivo .env\n")
except ImportError:
    print("⚠️  python-dotenv no está instalado. Usando variables del sistema.\n")

# Variables a verificar
variables = [
    ('HOSTINGER_EMAIL_PASSWORD', True),  # (nombre, es_sensible)
    ('EMAIL_FROM', False),
    ('EMAIL_FROM_NAME', False),
    ('SMTP_SERVER', False),
    ('SMTP_PORT', False),
    ('DEFAULT_TO_EMAIL', False),
]

print("🔍 Verificando variables de entorno:\n")
print("-" * 50)

todas_configuradas = True

for var_name, es_sensible in variables:
    valor = os.getenv(var_name)
    
    if valor:
        if es_sensible:
            # Ocultar parte del valor sensible
            display = valor[:3] + '*' * (len(valor) - 3)
        else:
            display = valor
        print(f"✅ {var_name}: {display}")
    else:
        print(f"❌ {var_name}: No configurada")
        todas_configuradas = False

print("-" * 50)

if todas_configuradas:
    print("\n✨ ¡Todas las variables están configuradas!")
    print("\n🧪 Probando configuración de email...")
    
    # Probar importación de configuración
    try:
        from config.email_settings import EMAIL_CONFIG
        print("\n📧 Configuración de email cargada:")
        print(f"   Servidor: {EMAIL_CONFIG['smtp_server']}")
        print(f"   Puerto: {EMAIL_CONFIG['smtp_port']}")
        print(f"   Remitente: {EMAIL_CONFIG['sender_email']}")
        print(f"   Contraseña: {'✅ Configurada' if EMAIL_CONFIG['sender_password'] else '❌ No configurada'}")
    except Exception as e:
        print(f"\n❌ Error al cargar configuración: {e}")
else:
    print("\n⚠️  Algunas variables no están configuradas.")
    print("\n📝 Para configurarlas:")
    print("   1. Copia .env.example como .env")
    print("   2. Actualiza los valores en .env")
    print("   3. Ejecuta este script nuevamente")