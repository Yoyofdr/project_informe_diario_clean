#!/usr/bin/env python3
"""
Script para arreglar usuarios existentes sin organización
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from django.contrib.auth.models import User
from alerts.models import Organizacion, Destinatario

print("🔧 Arreglando usuarios sin organización...")

# Buscar usuarios sin organización
usuarios_sin_org = []
for user in User.objects.filter(is_active=True):
    if not Organizacion.objects.filter(admin=user).exists():
        usuarios_sin_org.append(user)

print(f"\n📊 Usuarios sin organización: {len(usuarios_sin_org)}")

for user in usuarios_sin_org:
    print(f"\n👤 Procesando: {user.username} ({user.email})")
    
    # Extraer dominio del email
    email_domain = user.email.split('@')[1] if '@' in user.email else 'personal.cl'
    
    # Crear nombre de organización
    if user.first_name and user.last_name:
        org_name = f"{user.first_name} {user.last_name}"
    elif user.first_name:
        org_name = user.first_name
    else:
        org_name = user.email.split('@')[0]
    
    # Crear la organización
    org = Organizacion.objects.create(
        nombre=org_name,
        dominio=email_domain,
        admin=user,
        plan='gratis',
        suscripcion_activa=True
    )
    print(f"   ✅ Organización creada: {org_name}")
    
    # Agregar como destinatario
    if not Destinatario.objects.filter(email=user.email, organizacion=org).exists():
        Destinatario.objects.create(
            nombre=user.get_full_name() or user.username,
            email=user.email,
            organizacion=org
        )
        print(f"   ✅ Agregado como destinatario")

print("\n✅ ¡Proceso completado!")

# Mostrar resumen
print("\n📊 Resumen final:")
print(f"   Total usuarios: {User.objects.filter(is_active=True).count()}")
print(f"   Organizaciones: {Organizacion.objects.count()}")
print(f"   Destinatarios: {Destinatario.objects.count()}")