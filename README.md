# 📰 Informe Diario - Resumen del Diario Oficial

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-blue?style=flat-square&logo=github)](https://yoyofdr.github.io/informediario/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2+-green?style=flat-square&logo=django)](https://djangoproject.com)

> El resumen diario del Diario Oficial de Chile, explicado en simple y directo a tu correo.

## 🚀 Demo en Vivo

**Visita la demo:** [https://yoyofdr.github.io/informediario/](https://yoyofdr.github.io/informediario/)

## 📋 ¿Qué es Informe Diario?

Informe Diario es un servicio que:

- 📖 **Lee el Diario Oficial** automáticamente cada día
- 🧠 **Analiza con IA** las publicaciones más relevantes
- 📧 **Envía un resumen** directo a tu correo
- ⏰ **Ahorra tiempo** - solo lees lo importante en 5 minutos
- 🎯 **Filtra contenido** - solo lo que realmente te afecta

## ✨ Características

- **Análisis Inteligente**: Usa IA para identificar publicaciones relevantes
- **Resúmenes Claros**: Explicado en lenguaje simple, sin tecnicismos
- **Entrega Diaria**: Recibe el informe cada mañana en tu correo
- **Categorización**: Organizado por secciones (Normas Generales, Avisos, etc.)
- **Enlaces Directos**: Acceso directo a los documentos oficiales

## 🛠️ Tecnologías

- **Backend**: Django 5.2, Python 3.8+
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **IA**: OpenAI GPT para análisis de relevancia
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Despliegue**: GitHub Pages (demo) / VPS (producción)

## 📁 Estructura del Proyecto

```
informediario/
├── alerts/                 # App principal de Django
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas y lógica de negocio
│   ├── services/          # Servicios (scraping, IA, email)
│   └── templates/         # Templates HTML
├── market_sniper/         # Configuración de Django
├── templates/             # Templates globales
├── static/               # Archivos estáticos
├── manage.py             # Comando de Django
└── index.html            # Demo para GitHub Pages
```

## 🚀 Instalación Local

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/Yoyofdr/informediario.git
   cd informediario
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**
   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales
   ```

5. **Ejecuta las migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Inicia el servidor**
   ```bash
   python manage.py runserver
   ```

7. **Visita** http://localhost:8000

## 📧 Configuración de Email

El proyecto soporta dos modos de envío de emails:

### Modo Desarrollo (Archivos)
```bash
EMAIL_MODE=filebased
```
Los emails se guardan en la carpeta `sent_emails/`

### Modo Producción (SMTP)
```bash
EMAIL_MODE=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu@email.com
EMAIL_HOST_PASSWORD=tu_contraseña
```

## 🤖 Configuración de IA

Para usar el análisis con IA, configura tu API key de OpenAI:

```bash
OPENAI_API_KEY=tu_api_key_aqui
```

## 📊 Comandos Útiles

### Generar informe manual
```bash
python manage.py informe_diario_oficial
```

### Importar empresas
```bash
python manage.py importar_empresas
```

### Clasificar empresas
```bash
python manage.py clasificar_empresas
```

## 🌐 Despliegue

### GitHub Pages (Demo)
El sitio demo está desplegado automáticamente en GitHub Pages desde la rama `main`.

### Producción
Para desplegar en producción:

1. Configura un servidor VPS
2. Instala nginx y gunicorn
3. Configura SSL con Let's Encrypt
4. Usa PostgreSQL como base de datos
5. Configura un cron job para el informe diario

## 📈 Roadmap

- [ ] App móvil nativa
- [ ] Notificaciones push
- [ ] Personalización de filtros
- [ ] API pública
- [ ] Integración con WhatsApp
- [ ] Dashboard de analytics

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

- **Sitio web**: [informediario.cl](https://informediario.cl)
- **Email**: rodrigo@carvuk.com
- **GitHub**: [@Yoyofdr](https://github.com/Yoyofdr)

---

⭐ **Si te gusta este proyecto, ¡dale una estrella en GitHub!** 