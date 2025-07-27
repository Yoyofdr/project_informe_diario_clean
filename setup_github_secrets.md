# Configuración de GitHub Secrets para Automatización

## 🔐 Secrets necesarios

Ve a tu repositorio en GitHub → Settings → Secrets and variables → Actions → New repository secret

Agrega los siguientes secrets:

### 1. HOSTINGER_EMAIL_PASSWORD
```
Rfdr1729!
```

### 2. OPENAI_API_KEY (Opcional)
```
[Si tienes una API key de OpenAI, agrégala aquí]
```
Nota: El sistema puede funcionar sin OpenAI usando alternativas gratuitas.

## 🚀 Cómo agregar cada secret:

1. Click en "New repository secret"
2. Name: [Nombre del secret]
3. Secret: [Valor del secret]
4. Click "Add secret"

## ✅ Verificación

Una vez agregados todos los secrets:
1. Ve a Actions en tu repositorio
2. Busca "Envío Diario de Informes"
3. Click en "Run workflow" → "Run workflow" para probar

## 📅 Horario

El envío se ejecutará automáticamente:
- **Hora**: 9:00 AM hora de Chile
- **Días**: Lunes a Sábado (no domingos)
- **Manual**: Puedes ejecutarlo manualmente cuando quieras