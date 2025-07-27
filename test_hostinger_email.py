#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de email con Hostinger
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuración de Hostinger
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587  # o 465 para SSL
EMAIL = "contacto@informediariochile.cl"
PASSWORD = "Rfdr1729!"  # Contraseña de Hostinger

def test_connection():
    """Prueba solo la conexión SMTP"""
    print("🔌 Probando conexión SMTP con Hostinger...")
    print(f"   Servidor: {SMTP_SERVER}")
    print(f"   Puerto: {SMTP_PORT}")
    print(f"   Usuario: {EMAIL}")
    print("-" * 50)
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        print("✅ Conexión establecida")
        
        server.starttls()
        print("✅ TLS activado")
        
        server.login(EMAIL, PASSWORD)
        print("✅ Autenticación exitosa")
        
        server.quit()
        print("\n✨ ¡Conexión SMTP funcionando correctamente!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ Error de autenticación:")
        print("   - Verifica que la contraseña sea correcta")
        print("   - Asegúrate de usar el email completo como usuario")
        print("   - La contraseña es la del email, no la de tu cuenta Hostinger")
        return False
        
    except smtplib.SMTPConnectError:
        print("\n❌ Error de conexión:")
        print("   - Verifica que el servidor sea smtp.hostinger.com")
        print("   - Prueba con puerto 465 si 587 no funciona")
        print("   - Algunos ISP bloquean estos puertos")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def send_test_email(recipient_email):
    """Envía un email de prueba"""
    print(f"\n📧 Enviando email de prueba a {recipient_email}...")
    
    try:
        # Conectar y autenticar
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['From'] = f"Informe Diario Chile <{EMAIL}>"
        msg['To'] = recipient_email
        msg['Subject'] = f"Prueba de Email - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        # Contenido del email
        text = """¡Hola!

Este es un email de prueba desde el nuevo dominio informediariochile.cl

Si recibes este mensaje, significa que la configuración SMTP está funcionando correctamente.

Configuración utilizada:
- Servidor: smtp.hostinger.com
- Puerto: 587 (TLS)
- Email: contacto@informediariochile.cl

Saludos,
Equipo Informe Diario Chile
"""
        
        html = """
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2 style="color: #0066cc;">¡Prueba Exitosa! 🎉</h2>
              
              <p>Este es un email de prueba desde el nuevo dominio <strong>informediariochile.cl</strong></p>
              
              <p>Si recibes este mensaje, significa que la configuración SMTP está funcionando correctamente.</p>
              
              <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0;">Configuración utilizada:</h3>
                <ul style="margin: 0;">
                  <li>Servidor: smtp.hostinger.com</li>
                  <li>Puerto: 587 (TLS)</li>
                  <li>Email: contacto@informediariochile.cl</li>
                </ul>
              </div>
              
              <p style="color: #666; font-size: 14px;">
                Saludos,<br>
                Equipo Informe Diario Chile
              </p>
            </div>
          </body>
        </html>
        """
        
        # Adjuntar partes
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Enviar
        server.send_message(msg)
        server.quit()
        
        print("✅ Email enviado exitosamente!")
        print(f"   Revisa la bandeja de entrada de {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Test de Configuración Email - Hostinger")
    print("=" * 50)
    
    # Verificar contraseña
    if PASSWORD == "TU_CONTRASEÑA":
        print("⚠️  IMPORTANTE: Actualiza la contraseña en este archivo")
        print("   Línea 13: PASSWORD = 'tu_contraseña_real'")
        print("\nPasos:")
        print("1. Ve a hPanel de Hostinger")
        print("2. Emails → Cuentas de correo")
        print("3. Busca contacto@informediariochile.cl")
        print("4. Copia o resetea la contraseña")
        return
    
    # Probar conexión
    if test_connection():
        print("\n" + "=" * 50)
        respuesta = input("\n¿Quieres enviar un email de prueba? (s/n): ")
        
        if respuesta.lower() == 's':
            email_destino = input("Email destinatario (Enter para rfernandezdelrio@uc.cl): ").strip()
            if not email_destino:
                email_destino = "rfernandezdelrio@uc.cl"
            
            send_test_email(email_destino)
    
    print("\n" + "=" * 50)
    print("✨ Test completado")

if __name__ == "__main__":
    main()