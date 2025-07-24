#!/usr/bin/env python
"""
Script para generar el informe del 21 de julio con el diseño original de Bolt (React convertido a HTML)
"""
from datetime import datetime

def generar_informe_original():
    """Genera el informe del 21 de julio con el diseño original que compartiste"""
    
    fecha = "Lunes 21 de julio, 2025"
    total_documentos = 47
    publicaciones_relevantes = 7
    
    # Publicaciones del día
    publicaciones = [
        {
            "title": "LEY NÚM. 21.791 - MODIFICA EL CÓDIGO DEL TRABAJO EN MATERIA DE INCLUSIÓN LABORAL",
            "summary": "Establece cuotas obligatorias de contratación de personas con discapacidad en empresas con 100 o más trabajadores, fijando un mínimo del 1% de la dotación.",
            "meta": "Sección I - Normas Generales"
        },
        {
            "title": "DECRETO SUPREMO Nº 147 - MINISTERIO DE HACIENDA - VALORES UF",
            "summary": "Actualiza los valores de la UF para el período del 10 de agosto al 9 de septiembre de 2025, considerando la variación del IPC de julio.",
            "meta": "Sección I - Normas Generales"
        },
        {
            "title": "DECRETO SUPREMO Nº 312 - PROTECCIÓN DE DATOS EN E-COMMERCE",
            "summary": "Establece normas obligatorias para el tratamiento de datos personales en plataformas de comercio electrónico, incluyendo consentimiento expreso.",
            "meta": "Sección I - Normas Generales"
        },
        {
            "title": "RESOLUCIÓN EXENTA Nº 4.231 - SERVICIO DE IMPUESTOS INTERNOS",
            "summary": "Actualiza los requisitos técnicos para la emisión de boletas y facturas electrónicas, incorporando nuevos campos para criptoactivos.",
            "meta": "Sección II - Normas Particulares"
        },
        {
            "title": "RESOLUCIÓN EXENTA Nº 892 - SUBSECRETARÍA DE TRANSPORTES",
            "summary": "Define restricción vehicular extraordinaria para vehículos sin sello verde los días 22 y 23 de julio en la Región Metropolitana.",
            "meta": "Sección II - Normas Particulares"
        },
        {
            "title": "BANCO CENTRAL - TIPOS DE CAMBIO Y PARIDADES",
            "summary": "Publica los tipos de cambio oficiales del dólar observado ($943.28) y euro ($1,026.45) para operaciones del 21 de julio de 2025.",
            "meta": "Sección III - Avisos Destacados"
        },
        {
            "title": "MUNICIPALIDAD DE SANTIAGO - LICITACIÓN PÚBLICA CICLOVÍAS",
            "summary": "Convoca a licitación pública ID 2397-45-LP25 para la construcción de 12 kilómetros de ciclovías, con presupuesto de $4.500 millones.",
            "meta": "Sección III - Avisos Destacados"
        }
    ]
    
    # Generar HTML con Tailwind CSS
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diario Oficial - 21 de julio, 2025</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Animaciones personalizadas */
        .hover-lift {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .hover-lift:hover {{
            transform: translateY(-4px);
        }}
        
        /* Línea superior animada */
        .top-line {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(to right, #3b82f6, #6366f1);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .group:hover .top-line {{
            transform: scaleX(1);
        }}
        
        /* Transiciones suaves */
        * {{
            transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
            transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
            transition-duration: 150ms;
        }}
    </style>
</head>
<body class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 p-5">
    <div class="max-w-2xl mx-auto bg-white shadow-2xl rounded-lg overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-br from-black via-gray-900 to-gray-700 px-8 py-12 text-center relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-r from-gray-700/30 to-black/20"></div>
            <div class="relative z-10">
                <h1 class="text-3xl font-bold text-white tracking-tight mb-2">
                    Diario Oficial
                </h1>
                <div class="flex items-center justify-center text-gray-200 text-sm font-medium">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    {fecha}
                </div>
            </div>
        </div>

        <!-- Stats -->
        <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-100">
            <div class="grid grid-cols-2 divide-x divide-blue-200">
                <div class="px-8 py-6 text-center">
                    <div class="flex items-center justify-center mb-2">
                        <svg class="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                        </svg>
                    </div>
                    <div class="text-3xl font-bold text-blue-900 mb-1">
                        {total_documentos}
                    </div>
                    <div class="text-xs font-semibold text-blue-600 uppercase tracking-wider">
                        Total Documentos
                    </div>
                </div>
                <div class="px-8 py-6 text-center">
                    <div class="flex items-center justify-center mb-2">
                        <svg class="w-6 h-6 text-emerald-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>
                        </svg>
                    </div>
                    <div class="text-3xl font-bold text-emerald-700 mb-1">
                        {publicaciones_relevantes}
                    </div>
                    <div class="text-xs font-semibold text-emerald-600 uppercase tracking-wider">
                        Relevantes
                    </div>
                </div>
            </div>
        </div>

        <!-- Content -->
        <div class="p-8">
            <div class="flex items-center mb-6 pb-4 border-b border-blue-100">
                <div class="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-lg mr-4">
                    <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                </div>
                <div class="flex-1">
                    <h2 class="text-lg font-semibold text-slate-900">
                        Publicaciones Destacadas
                    </h2>
                    <p class="text-sm text-blue-600">
                        Documentos de mayor relevancia e impacto
                    </p>
                </div>
                <div class="text-sm text-indigo-600 font-medium">
                    {len(publicaciones)} elementos
                </div>
            </div>

            <div class="space-y-4">
"""
    
    # Agregar cada publicación
    for i, pub in enumerate(publicaciones):
        html += f"""
                <div class="group bg-white border border-slate-200 rounded-xl p-6 transition-all duration-300 hover:border-blue-300 hover:shadow-xl hover:shadow-blue-100/50 hover:-translate-y-1 relative overflow-hidden hover-lift">
                    <div class="top-line"></div>
                    <h3 class="font-semibold text-slate-800 mb-3 leading-snug group-hover:text-blue-800 transition-colors">
                        {pub['title']}
                    </h3>
                    <p class="text-slate-600 text-sm leading-relaxed mb-4">
                        {pub['summary']}
                    </p>
                    <div class="pt-4 border-t border-blue-50 text-xs text-blue-600 flex items-center">
                        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"></path>
                        </svg>
                        {pub['meta']}
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    html = generar_informe_original()
    
    # Guardar el HTML
    filename = "informe_diario_oficial_21_07_2025_diseño_original.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Informe con diseño original generado: {filename}")