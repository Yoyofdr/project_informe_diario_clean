from datetime import datetime

def generar_informe_html(publicaciones, fecha=None, valores_monedas=None):
    """
    Genera un informe HTML elegante y sobrio con las publicaciones relevantes y su resumen, usando solo estilos inline para máxima compatibilidad con Gmail.
    Si se entregan valores de dólar y euro, los muestra al final.
    """
    if fecha is None:
        fecha = datetime.now().strftime('%d-%m-%Y')
    html = f"""
    <html>
    <body style='font-family: Segoe UI, Arial, sans-serif; background: #fff;'>
        <h1 style='margin-bottom: 0.5em;'>Informe Diario Oficial</h1>
        <div style='color:#111; font-size:1.3em; margin-bottom:18px;'>Edición del {fecha}</div>
        <div style='height:18px;'></div>
        <table width='100%' cellpadding='0' cellspacing='0' style='border-collapse: separate; border-spacing: 0; width: 100%; margin: 24px 0 32px 0; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #0001; overflow: hidden;'>
            <tr>
                <th style='background: #f4f4f7; color: #222; font-size: 1.08em; font-weight: 700; border-bottom: 2px solid #e0e0e0; padding: 14px 18px; text-align: left;'>Sección</th>
                <th style='background: #f4f4f7; color: #222; font-size: 1.08em; font-weight: 700; border-bottom: 2px solid #e0e0e0; padding: 14px 18px; text-align: left;'>Título</th>
                <th style='background: #f4f4f7; color: #222; font-size: 1.08em; font-weight: 700; border-bottom: 2px solid #e0e0e0; padding: 14px 18px; text-align: left;'>Resumen</th>
            </tr>
    """
    if not publicaciones:
        html += "<tr><td colspan='3' style='padding: 18px; color: #555; border-bottom: 1px solid #ececec; font-size: 1em;'>No hay publicaciones relevantes hoy.</td></tr>"
    else:
        pub = publicaciones[0]  # Solo la primera publicación relevante
        url = pub['url_pdf']
        if url.startswith('http'):
            url_final = url
        else:
            url_final = f'https://www.diariooficial.interior.gob.cl{url}'
        html += f"""
            <tr>
                <td style='border-bottom: 1px solid #ececec; vertical-align: top; color: #222; font-size: 1em; padding: 14px 18px;'>{pub['seccion'].title()}</td>
                <td style='border-bottom: 1px solid #ececec; vertical-align: top; color: #222; font-size: 1em; padding: 14px 18px;'><a href='{url_final}' target='_blank' style='color: #1a3c7b; text-decoration: underline;'>{pub['titulo']}</a></td>
                <td style='border-bottom: 1px solid #ececec; vertical-align: top; color: #222; font-size: 1em; padding: 14px 18px;'>{pub['resumen']}</td>
            </tr>
        """
    html += """
        </table>
    """
    # Agregar sección de valores de monedas si existen
    if valores_monedas and (valores_monedas.get('dolar') or valores_monedas.get('euro')):
        html += "<div style='margin-top:32px; padding:18px; background:#f8f9fa; border-radius:8px; border:1px solid #e0e0e0; color:#222; font-size:1.08em;'>"
        html += "<strong>Valores de referencia publicados por el Banco Central de Chile:</strong><br>"
        if valores_monedas.get('dolar'):
            html += f"Dólar observado: <b>${valores_monedas['dolar']}</b><br>"
        if valores_monedas.get('euro'):
            html += f"Euro: <b>${valores_monedas['euro']}</b><br>"
        html += "</div>"
    else:
        html += "<div style='margin-top:32px; padding:18px; background:#f8f9fa; border-radius:8px; border:1px solid #e0e0e0; color:#222; font-size:1.08em;'>"
        html += "<strong>Valores de dólar y euro:</strong> No publicados en la edición de hoy." 
        html += "</div>"
    html += """
    </body>
    </html>
    """
    return html 