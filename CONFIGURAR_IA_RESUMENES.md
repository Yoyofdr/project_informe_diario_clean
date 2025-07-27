# 🤖 Configuración de IA para Resúmenes

## ⚠️ IMPORTANTE: Sin API de IA, no se generan resúmenes

El sistema necesita al menos una API de IA configurada para generar resúmenes del Diario Oficial, CMF y SII.

## 🚀 Opción 1: Groq (RECOMENDADO - GRATIS)

### Pasos:
1. Ve a https://console.groq.com/
2. Crea una cuenta gratuita
3. Ve a "API Keys" → "Create API Key"
4. Copia la API key

### Configurar localmente:
Agrega a tu archivo `.env`:
```
GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXX
```

### Configurar en GitHub Actions:
1. Ve a tu repositorio → Settings → Secrets → Actions
2. New repository secret:
   - Name: `GROQ_API_KEY`
   - Secret: [tu API key de Groq]

## 🌟 Opción 2: Google Gemini (GRATIS)

### Pasos:
1. Ve a https://makersuite.google.com/app/apikey
2. Crea una API key
3. Copia la key

### Configurar:
```
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXX
```

## 💎 Opción 3: DeepSeek (MUY BARATO)

### Pasos:
1. Ve a https://platform.deepseek.com/
2. Registrarse y agregar $1 USD de crédito
3. Crear API key

### Configurar:
```
DEEPSEEK_API_KEY=sk-XXXXXXXXXXXXXXXX
```

## 📋 Verificar configuración

Una vez configurada la API:

### Local:
```bash
cd /Users/rodrigofernandezdelrio/Desktop/Project\ Diario\ Oficial/repo_clean
python scripts/config/configurar_groq.py
```

### GitHub Actions:
El workflow ya está configurado para usar las API keys desde los secrets.

## 🎯 Resultado esperado

Con la API configurada, los informes incluirán:
- **Diario Oficial**: Resúmenes de cada publicación relevante
- **CMF**: Análisis del impacto para inversionistas
- **SII**: Resúmenes de circulares y resoluciones

Sin API, solo verás títulos sin contexto adicional.