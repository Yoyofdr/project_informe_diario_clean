#!/usr/bin/env python3
"""
Script para actualizar todas las configuraciones de email en el proyecto
"""
import os
import re
import sys

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.email_settings import EMAIL_CONFIG

def actualizar_archivo(filepath, dry_run=True):
    """Actualiza un archivo con la nueva configuración de email"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        cambios = []
        
        # Patrones a buscar y reemplazar
        patterns = [
            # Email remitente
            (r'de_email\s*=\s*["\']rodrigo@carvuk\.com["\']', 
             f'de_email = "{EMAIL_CONFIG["sender_email"]}"'),
            (r'["\']rodrigo@carvuk\.com["\']', 
             f'"{EMAIL_CONFIG["sender_email"]}"'),
            
            # Password
            (r'password\s*=\s*["\']swqjlcwjaoooyzcb["\']',
             f'password = "{EMAIL_CONFIG["sender_password"]}"'),
            
            # SMTP settings en Django settings
            (r'EMAIL_HOST_USER\s*=\s*["\']rodrigo@carvuk\.com["\']',
             f'EMAIL_HOST_USER = "{EMAIL_CONFIG["sender_email"]}"'),
            (r'DEFAULT_FROM_EMAIL\s*=\s*["\']rodrigo@carvuk\.com["\']',
             f'DEFAULT_FROM_EMAIL = "{EMAIL_CONFIG["sender_email"]}"'),
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                cambios.append(f"  - Actualizado: {pattern}")
        
        if content != original_content:
            print(f"\n📄 {filepath}")
            for cambio in cambios:
                print(cambio)
            
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("  ✅ Archivo actualizado")
            else:
                print("  ⚠️  Modo dry-run: no se guardaron cambios")
            
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error procesando {filepath}: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 Actualizando configuraciones de email en el proyecto")
    print(f"📧 Nuevo email: {EMAIL_CONFIG['sender_email']}")
    print("-" * 60)
    
    # Determinar si es dry-run
    dry_run = '--apply' not in sys.argv
    if dry_run:
        print("⚠️  MODO DRY-RUN: Mostrando cambios sin aplicarlos")
        print("   Usa --apply para aplicar los cambios")
        print("-" * 60)
    
    # Directorio base
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Archivos a actualizar
    archivos = [
        'generar_informe_oficial_integrado_mejorado.py',
        'market_sniper/settings.py',
        'market_sniper/settings_prod.py',
        'alerts/scraper_diario_oficial.py',
    ]
    
    # Archivos en scripts/email/
    email_scripts = [
        'enviar_informe_direccion_correcta_final.py',
        'enviar_informe_smtp_directo.py',
        'enviar_informe_completo_final.py',
        'enviar_informe_final_correcto.py',
        'enviar_informe_21_julio_oficial.py',
        'enviar_informe_diseño_correcto.py',
        'enviar_informe_bolt_final.py',
        'enviar_informe_21_julio_email.py',
        'enviar_informe_moderno_smtp.py',
        'enviar_informe_final_21_julio.py',
        'reenviar_informe_direcciones_correctas.py',
    ]
    
    # Agregar scripts de email a la lista
    for script in email_scripts:
        archivos.append(f'scripts/email/{script}')
    
    # Procesar archivos
    actualizados = 0
    for archivo in archivos:
        filepath = os.path.join(base_dir, archivo)
        if os.path.exists(filepath):
            if actualizar_archivo(filepath, dry_run):
                actualizados += 1
        else:
            print(f"⚠️  No encontrado: {archivo}")
    
    print("\n" + "-" * 60)
    print(f"📊 Resumen: {actualizados} archivos con cambios detectados")
    
    if dry_run and actualizados > 0:
        print("\n✨ Para aplicar los cambios, ejecuta:")
        print(f"   python {sys.argv[0]} --apply")
    elif not dry_run:
        print("\n✅ Cambios aplicados exitosamente")
        print("\n⚠️  IMPORTANTE:")
        print(f"   1. Actualiza la contraseña en config/email_settings.py")
        print(f"   2. Verifica la configuración SMTP de tu proveedor")
        print(f"   3. Considera usar variables de entorno para la contraseña")

if __name__ == "__main__":
    main()