#!/usr/bin/env python3
"""
Script para verificar los suscriptores actuales del sistema
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from django.contrib.auth.models import User
from alerts.models import Destinatario, Organizacion, SuscripcionLanding

print("📊 VERIFICACIÓN DE SUSCRIPTORES")
print("=" * 50)

# 1. Usuarios registrados
usuarios = User.objects.filter(is_active=True, email__isnull=False).exclude(email='')
print(f"\n👥 Usuarios registrados activos: {usuarios.count()}")
for u in usuarios[:5]:  # Mostrar primeros 5
    print(f"   - {u.username}: {u.email}")
if usuarios.count() > 5:
    print(f"   ... y {usuarios.count() - 5} más")

# 2. Organizaciones
orgs = Organizacion.objects.all()
print(f"\n🏢 Organizaciones: {orgs.count()}")
for org in orgs:
    print(f"   - {org.nombre} ({org.plan})")
    print(f"     Suscripción activa: {'✅' if org.suscripcion_activa else '❌'}")
    print(f"     Destinatarios: {org.destinatarios.count()}")

# 3. Destinatarios totales
destinatarios = Destinatario.objects.all()
print(f"\n📧 Destinatarios totales: {destinatarios.count()}")

# 4. Suscripciones del landing
suscripciones_landing = SuscripcionLanding.objects.all()
print(f"\n🌐 Suscripciones del landing page: {suscripciones_landing.count()}")
for s in suscripciones_landing[:5]:
    print(f"   - {s.email} ({s.organizacion})")
if suscripciones_landing.count() > 5:
    print(f"   ... y {suscripciones_landing.count() - 5} más")

# Resumen
print("\n" + "=" * 50)
print("📋 RESUMEN:")
total_emails = set()

# Agregar emails de usuarios
for u in usuarios:
    if u.email:
        total_emails.add(u.email)

# Agregar emails de destinatarios
for d in destinatarios:
    total_emails.add(d.email)

print(f"📧 Total de emails únicos: {len(total_emails)}")
print(f"✅ Estos recibirán el informe diario automáticamente")