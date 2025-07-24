#!/usr/bin/env python
"""
Genera y envía el informe REAL del 21 de julio con la edición correcta
"""
import os
import sys
import django
from datetime import datetime
from bs4 import BeautifulSoup

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

def obtener_todas_las_publicaciones():
    """Extrae TODAS las publicaciones del HTML guardado"""
    
    with open('edicion_correcta_21_julio.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    publicaciones = []
    
    # Obtener todas las publicaciones
    content_rows = soup.find_all('tr', class_='content')
    
    for tr in content_rows:
        tds = tr.find_all('td')
        if len(tds) >= 2:
            titulo = tds[0].get_text(strip=True)
            link = tds[1].find('a', href=True)
            pdf_url = link['href'] if link else ""
            
            if pdf_url and not pdf_url.startswith('http'):
                pdf_url = f"https://www.diariooficial.interior.gob.cl{pdf_url}"
            
            # Determinar sección basándose en el título
            seccion = "NORMAS GENERALES"
            if "decreto" in titulo.lower():
                seccion = "DECRETOS"
            elif "resolución" in titulo.lower():
                seccion = "RESOLUCIONES"
            elif "ley" in titulo.lower():
                seccion = "LEYES"
            
            # Determinar si es relevante (basado en palabras clave)
            relevante = any(palabra in titulo.lower() for palabra in [
                'modifica', 'aprueba', 'establece', 'fija', 'reglamenta', 
                'dispone', 'tarifas', 'regulaciones'
            ])
            
            publicacion = {
                'titulo': titulo,
                'url_pdf': pdf_url,
                'seccion': seccion,
                'relevante': relevante,
                'resumen': f"Publicación oficial del Diario Oficial que {titulo.lower()[:100]}..."
            }
            publicaciones.append(publicacion)
    
    return publicaciones

def generar_html_informe(publicaciones):
    """Genera el HTML del informe con el diseño correcto"""
    
    fecha = "21 de Julio, 2025"
    edicion = "44.203"
    total_docs = len(publicaciones)
    relevantes = sum(1 for p in publicaciones if p.get('relevante', False))
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Diario Oficial - {fecha}</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; background-color: #f6f8fb;">
    <table cellpadding="0" cellspacing="0" width="100%" style="background-color: #f6f8fb;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                <table cellpadding="0" cellspacing="0" width="600" style="background-color: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(90deg, #2563eb 0%, #6366f1 100%); padding: 32px 40px;">
                            <h1 style="margin: 0 0 8px 0; color: white; font-size: 28px;">Informe Diario Oficial</h1>
                            <p style="margin: 0; color: white; font-size: 16px; opacity: 0.9;">{fecha} - Edición N° {edicion}</p>
                            
                            <!-- Estadísticas -->
                            <table cellpadding="0" cellspacing="0" style="margin-top: 20px;">
                                <tr>
                                    <td style="background: rgba(255,255,255,0.1); padding: 12px 20px; border-radius: 8px; margin-right: 24px;">
                                        <div style="font-size: 24px; font-weight: bold; color: white;">{total_docs}</div>
                                        <div style="font-size: 14px; color: white; opacity: 0.9;">Documentos totales</div>
                                    </td>
                                    <td width="24"></td>
                                    <td style="background: rgba(255,255,255,0.1); padding: 12px 20px; border-radius: 8px;">
                                        <div style="font-size: 24px; font-weight: bold; color: white;">{relevantes}</div>
                                        <div style="font-size: 14px; color: white; opacity: 0.9;">Publicaciones relevantes</div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 32px 40px;">
                            <h2 style="color: #334155; font-size: 20px; margin: 0 0 16px 0;">📋 Publicaciones Destacadas</h2>
"""
    
    # Agregar publicaciones
    for pub in publicaciones:
        relevante_style = "border-left: 4px solid #3b82f6;" if pub.get('relevante') else ""
        
        html += f"""
                            <table cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 16px;">
                                <tr>
                                    <td style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; {relevante_style}">
                                        <h3 style="margin: 0 0 8px 0; color: #1e293b; font-size: 16px; font-weight: 600;">
                                            {pub['titulo']}
                                        </h3>
                                        <p style="margin: 0 0 12px 0; color: #64748b; line-height: 1.5; font-size: 14px;">
                                            {pub['resumen']}
                                        </p>
                                        <table cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td style="background: #e0e7ff; color: #4338ca; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 500;">
                                                    {pub['seccion']}
                                                </td>
                                                <td width="12"></td>
                                                <td>
                                                    <a href="{pub['url_pdf']}" style="background: #2563eb; color: white; text-decoration: none; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: 500; display: inline-block;">
                                                        Ver Documento Oficial
                                                    </a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
"""
    
    html += """
                            <!-- Footer -->
                            <table cellpadding="0" cellspacing="0" width="100%" style="margin-top: 32px;">
                                <tr>
                                    <td style="text-align: center; padding-top: 24px; border-top: 1px solid #e2e8f0;">
                                        <p style="margin: 0; color: #94a3b8; font-size: 14px;">
                                            Este informe fue generado automáticamente<br>
                                            Fuente: Diario Oficial de la República de Chile
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    
    return html

def enviar_informe(html_content):
    """Envía el informe por email"""
    
    from django.core.mail import EmailMessage
    
    email = EmailMessage(
        subject="Informe Diario Oficial - 21 de Julio 2025 (Edición 44.203)",
        body=html_content,
        from_email="fernandezcamilog@gmail.com",
        to=["ifernaandeez@gmail.com"],
    )
    email.content_subtype = "html"
    
    try:
        email.send()
        print("✅ Email enviado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error al enviar email: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== GENERANDO INFORME REAL DEL 21 DE JULIO ===\n")
    
    # Obtener todas las publicaciones
    print("Obteniendo publicaciones...")
    publicaciones = obtener_todas_las_publicaciones()
    print(f"✅ {len(publicaciones)} publicaciones encontradas")
    
    # Generar HTML
    print("\nGenerando HTML del informe...")
    html = generar_html_informe(publicaciones)
    
    # Guardar copia local
    filename = "informe_real_21_julio_2025.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 Informe guardado en: {filename}")
    
    # Enviar por email
    print("\n📧 Enviando informe por email...")
    if enviar_informe(html):
        print("\n✅ Proceso completado exitosamente")
        print("📋 Resumen del informe:")
        print(f"   - Total de publicaciones: {len(publicaciones)}")
        print(f"   - Edición correcta: 44.203")
        print(f"   - Fecha: 21 de Julio, 2025")
    else:
        print("\n⚠️  El informe fue generado pero no se pudo enviar por email")