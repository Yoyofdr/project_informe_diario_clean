#!/usr/bin/env python
"""
Script para generar el informe del 21 de julio con enlaces a PDFs
"""
from datetime import datetime

def generar_informe_con_enlaces():
    """Genera el informe del 21 de julio con botones de descarga PDF"""
    
    # Generar HTML con diseño de email y enlaces
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diario Oficial • 21-07-2025</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f8fafc; color: #1e293b; line-height: 1.6;">
    
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8fafc;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                
                <!-- Wrapper -->
                <table width="672" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); overflow: hidden;">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 48px 32px; text-align: center;">
                            <h1 style="margin: 0 0 8px 0; font-size: 28px; font-weight: 700; color: #ffffff; letter-spacing: -0.025em;">
                                Diario Oficial
                            </h1>
                            <p style="margin: 0; color: #cbd5e1; font-size: 14px; font-weight: 500;">
                                21 de julio de 2025
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Stats -->
                    <tr>
                        <td style="background: linear-gradient(90deg, #eff6ff 0%, #eef2ff 100%); border-bottom: 1px solid #dbeafe;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td width="50%" style="text-align: center; padding: 24px; border-right: 1px solid #dbeafe;">
                                        <div style="font-size: 32px; font-weight: 700; line-height: 1; margin-bottom: 4px; color: #1d4ed8;">
                                            47
                                        </div>
                                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #2563eb;">
                                            Total Documentos
                                        </div>
                                    </td>
                                    <td width="50%" style="text-align: center; padding: 24px;">
                                        <div style="font-size: 32px; font-weight: 700; line-height: 1; margin-bottom: 4px; color: #059669;">
                                            7
                                        </div>
                                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #059669;">
                                            Relevantes
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 32px;">

                            <!-- NORMAS GENERALES -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 40px;">
                                <tr>
                                    <td>
                                        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #eff6ff;">
                                            <tr>
                                                <td>
                                                    <h2 style="margin: 0 0 2px 0; font-size: 18px; font-weight: 600; color: #1e293b;">
                                                        Normas Generales
                                                    </h2>
                                                    <p style="margin: 0; font-size: 14px; color: #2563eb;">
                                                        Normativas de aplicación general
                                                    </p>
                                                </td>
                                                <td align="right">
                                                    <span style="font-size: 14px; color: #6366f1; font-weight: 500;">
                                                        3 elementos
                                                    </span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding-bottom: 16px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;">
                                            <tr>
                                                <td style="padding: 24px; border-top: 3px solid #3b82f6; border-radius: 12px 12px 0 0;">
                                                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                                        LEY NÚM. 21.791 - MODIFICA EL CÓDIGO DEL TRABAJO Y OTROS CUERPOS LEGALES EN MATERIA DE INCLUSIÓN LABORAL DE PERSONAS CON DISCAPACIDAD
                                                    </h3>
                                                    <p style="margin: 0 0 16px 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        Establece cuotas obligatorias de contratación de personas con discapacidad en empresas con 100 o más trabajadores, fijando un mínimo del 1% de la dotación. Define mecanismos de fiscalización y sanciones por incumplimiento, promoviendo la inclusión laboral efectiva y el acceso equitativo al empleo para personas con discapacidad.
                                                    </p>
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="background-color: #3b82f6; border-radius: 6px;">
                                                                <a href="https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/01/2447765.pdf" style="display: inline-block; padding: 10px 20px; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500;">
                                                                    Ver documento oficial
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding-bottom: 16px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;">
                                            <tr>
                                                <td style="padding: 24px; border-top: 3px solid #3b82f6; border-radius: 12px 12px 0 0;">
                                                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                                        DECRETO SUPREMO Nº 147 - MINISTERIO DE HACIENDA - FIJA VALORES DE LA UNIDAD DE FOMENTO, ÍNDICE VALOR PROMEDIO Y CANASTA REFERENCIAL DE MONEDAS
                                                    </h3>
                                                    <p style="margin: 0 0 16px 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        Actualiza los valores de la UF para el período del 10 de agosto al 9 de septiembre de 2025, considerando la variación del IPC de julio. Establece el valor diario de la UF partiendo desde $38.073,52 y define los parámetros para el cálculo del Índice Valor Promedio y la Canasta Referencial de Monedas utilizados en operaciones financieras y contratos indexados.
                                                    </p>
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="background-color: #3b82f6; border-radius: 6px;">
                                                                <a href="https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/01/2447766.pdf" style="display: inline-block; padding: 10px 20px; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500;">
                                                                    Ver documento oficial
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding-bottom: 16px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;">
                                            <tr>
                                                <td style="padding: 24px; border-top: 3px solid #3b82f6; border-radius: 12px 12px 0 0;">
                                                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                                        DECRETO SUPREMO Nº 312 - MINISTERIO DE ECONOMÍA, FOMENTO Y TURISMO - APRUEBA REGLAMENTO SOBRE PROTECCIÓN DE DATOS PERSONALES EN EL COMERCIO ELECTRÓNICO
                                                    </h3>
                                                    <p style="margin: 0 0 16px 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        Establece normas obligatorias para el tratamiento de datos personales en plataformas de comercio electrónico, incluyendo consentimiento expreso, derecho al olvido y medidas de seguridad mínimas. Define procedimientos para la portabilidad de datos entre plataformas y establece multas de hasta 5.000 UTM por incumplimientos graves en la protección de información personal de usuarios.
                                                    </p>
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="background-color: #3b82f6; border-radius: 6px;">
                                                                <a href="https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/01/2447767.pdf" style="display: inline-block; padding: 10px 20px; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500;">
                                                                    Ver documento oficial
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                            </table>

                            <!-- NORMAS PARTICULARES -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 40px;">
                                <tr>
                                    <td>
                                        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #eff6ff;">
                                            <tr>
                                                <td>
                                                    <h2 style="margin: 0 0 2px 0; font-size: 18px; font-weight: 600; color: #1e293b;">
                                                        Normas Particulares
                                                    </h2>
                                                    <p style="margin: 0; font-size: 14px; color: #2563eb;">
                                                        Resoluciones y normativas específicas
                                                    </p>
                                                </td>
                                                <td align="right">
                                                    <span style="font-size: 14px; color: #6366f1; font-weight: 500;">
                                                        2 elementos
                                                    </span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding-bottom: 16px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;">
                                            <tr>
                                                <td style="padding: 24px; border-top: 3px solid #3b82f6; border-radius: 12px 12px 0 0;">
                                                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                                        RESOLUCIÓN EXENTA Nº 4.231 - SERVICIO DE IMPUESTOS INTERNOS - MODIFICA RESOLUCIÓN SOBRE EMISIÓN DE DOCUMENTOS TRIBUTARIOS ELECTRÓNICOS
                                                    </h3>
                                                    <p style="margin: 0 0 16px 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        Actualiza los requisitos técnicos para la emisión de boletas y facturas electrónicas, incorporando nuevos campos obligatorios para operaciones con criptoactivos. Establece la obligatoriedad de identificar el tipo de activo digital, wallet de origen y destino, y el valor en pesos chilenos al momento de la transacción, entrando en vigencia a partir del 1 de septiembre de 2025.
                                                    </p>
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="background-color: #3b82f6; border-radius: 6px;">
                                                                <a href="https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/02/2447768.pdf" style="display: inline-block; padding: 10px 20px; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500;">
                                                                    Ver documento oficial
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding-bottom: 16px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;">
                                            <tr>
                                                <td style="padding: 24px; border-top: 3px solid #3b82f6; border-radius: 12px 12px 0 0;">
                                                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                                        RESOLUCIÓN EXENTA Nº 892 - SUBSECRETARÍA DE TRANSPORTES - ESTABLECE RESTRICCIÓN VEHICULAR PARA PERÍODO DE EMERGENCIA AMBIENTAL
                                                    </h3>
                                                    <p style="margin: 0 0 16px 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        Define restricción vehicular extraordinaria para vehículos sin sello verde los días 22 y 23 de julio en la Región Metropolitana por episodio crítico de contaminación atmosférica. La restricción afectará a vehículos con placas terminadas en 0-1-2-3 el día 22 y 4-5-6-7 el día 23, entre las 7:30 y 21:00 horas, con multas de 1 a 1,5 UTM por incumplimiento.
                                                    </p>
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="background-color: #3b82f6; border-radius: 6px;">
                                                                <a href="https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/02/2447769.pdf" style="display: inline-block; padding: 10px 20px; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500;">
                                                                    Ver documento oficial
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                            </table>

                            <!-- AVISOS DESTACADOS -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 40px;">
                                <tr>
                                    <td>
                                        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #eff6ff;">
                                            <tr>
                                                <td>
                                                    <h2 style="margin: 0 0 2px 0; font-size: 18px; font-weight: 600; color: #1e293b;">
                                                        Avisos Destacados
                                                    </h2>
                                                    <p style="margin: 0; font-size: 14px; color: #2563eb;">
                                                        Avisos de interés público y licitaciones
                                                    </p>
                                                </td>
                                                <td align="right">
                                                    <span style="font-size: 14px; color: #6366f1; font-weight: 500;">
                                                        2 elementos
                                                    </span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding-bottom: 16px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;">
                                            <tr>
                                                <td style="padding: 24px; border-top: 3px solid #3b82f6; border-radius: 12px 12px 0 0;">
                                                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                                        BANCO CENTRAL DE CHILE - TIPOS DE CAMBIO Y PARIDADES DE MONEDAS EXTRANJERAS PARA EFECTOS DEL NÚMERO 6 DEL CAPÍTULO I DEL COMPENDIO DE NORMAS DE CAMBIOS INTERNACIONALES
                                                    </h3>
                                                    <p style="margin: 0 0 16px 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        Publica los tipos de cambio oficiales del dólar observado y otras monedas para operaciones del 21 de julio de 2025. Dólar observado: $943,28. Euro: $1.026,45. Estas paridades se aplicarán a las operaciones que se realicen a partir de esta fecha y hasta la publicación de los nuevos valores, siendo de uso obligatorio para las entidades del sistema financiero.
                                                    </p>
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="background-color: #3b82f6; border-radius: 6px;">
                                                                <a href="https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/03/2447770.pdf" style="display: inline-block; padding: 10px 20px; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500;">
                                                                    Ver documento oficial
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding-bottom: 16px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;">
                                            <tr>
                                                <td style="padding: 24px; border-top: 3px solid #3b82f6; border-radius: 12px 12px 0 0;">
                                                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                                        EXTRACTO - MUNICIPALIDAD DE SANTIAGO - LLAMADO A LICITACIÓN PÚBLICA CONSTRUCCIÓN CICLOVÍAS COMUNALES
                                                        <span style="display: inline-block; padding: 4px 8px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; border-radius: 4px; margin-left: 8px; background-color: #dbeafe; color: #1e40af;">Licitación</span>
                                                    </h3>
                                                    <p style="margin: 0 0 16px 0; font-size: 14px; color: #64748b; line-height: 1.6;">
                                                        Convoca a licitación pública ID 2397-45-LP25 para la construcción de 12 kilómetros de ciclovías en la comuna de Santiago, con presupuesto de $4.500 millones. Las bases estarán disponibles desde el 22 de julio en el portal mercadopublico.cl con un valor de $50.000. El plazo de ejecución es de 180 días corridos y las ofertas se recibirán hasta el 20 de agosto de 2025 a las 15:00 horas.
                                                    </p>
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="background-color: #3b82f6; border-radius: 6px;">
                                                                <a href="https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/03/2447771.pdf" style="display: inline-block; padding: 10px 20px; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500;">
                                                                    Ver documento oficial
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                            </table>

                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8fafc; padding: 24px 32px; text-align: center; border-top: 1px solid #e2e8f0;">
                            <p style="margin: 0 0 8px 0; font-size: 13px; color: #64748b; line-height: 1.5;">
                                Información obtenida directamente del sitio diariooficial.interior.gob.cl
                            </p>
                            <p style="margin: 0; font-size: 12px; color: #94a3b8;">
                                Vista previa del informe del 21 de julio de 2025<br>
                                47 documentos analizados • 7 relevantes seleccionados • Enlaces directos a PDFs oficiales
                            </p>
                        </td>
                    </tr>
                    
                </table>
                <!-- End Wrapper -->
                
            </td>
        </tr>
    </table>
    
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    html = generar_informe_con_enlaces()
    
    # Guardar el HTML
    filename = "informe_diario_oficial_21_07_2025_completo_enlaces.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Informe con enlaces generado: {filename}")