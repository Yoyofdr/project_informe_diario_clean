#!/usr/bin/env python3
"""
Script para probar el envío de informe con la nueva configuración de Hostinger
"""
import os
import sys
from datetime import datetime

# Agregar el directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🚀 Probando envío de informe con nueva configuración")
print("=" * 60)
print(f"📧 Remitente: contacto@informediariochile.cl")
print(f"📬 Destinatario: rfernandezdelrio@uc.cl")
print(f"🏢 Servidor: smtp.hostinger.com")
print(f"📅 Fecha: {datetime.now().strftime('%d-%m-%Y')}")
print("=" * 60)

# Ejecutar el script de informe
try:
    import subprocess
    result = subprocess.run(
        [sys.executable, "generar_informe_oficial_integrado_mejorado.py"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    print("\n📝 Salida del script:")
    print("-" * 60)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("⚠️ Errores:")
        print(result.stderr)
    
    if result.returncode == 0:
        print("\n✅ Proceso completado exitosamente")
    else:
        print(f"\n❌ Error: código de salida {result.returncode}")
        
except Exception as e:
    print(f"\n❌ Error ejecutando el script: {e}")

print("\n" + "=" * 60)
print("✨ Prueba finalizada")