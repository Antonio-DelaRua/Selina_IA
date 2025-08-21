import speech_recognition as sr
import threading
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, cv2, subprocess, os
from pygame import mixer
import numpy as np
import subprocess as sub
import time
import socket
import platform
import cv2
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Diccionarios de sitios, archivos y contactos

canciones = {
    'motivación': 'https://www.youtube.com/watch?v=Pnf8Y0kE4Z8&ab_channel=MotiversityenEspa%C3%B1ol',
    'chill': 'https://www.youtube.com/watch?v=cq2Ef6rvL6g&t=3587s&ab_channel=RelaxChilloutMusic',
    'estudiar': 'https://www.youtube.com/watch?v=DZ5LneDpTBc&ab_channel=musicforlife',
    'relax': 'https://www.youtube.com/watch?v=LAqOdX5jgb4&ab_channel=JAZZ%26BLUES',
}

sites = {
    'google': 'https://www.google.com',
    'youtube': 'https://www.youtube.com',
    'facebook': 'https://www.facebook.com',
    'whatsapp': 'https://web.whatsapp.com',
    'cursos': 'https://freecodecamp.org/learn',
    'deportes': 'https://www.as.com',
    'netflix': 'https://www.netflix.com/es/',
    'instagram': 'https://www.instagram.com/',
    'git': 'https://github.com/',
    'motivación': 'https://www.youtube.com/watch?v=Pnf8Y0kE4Z8&ab_channel=MotiversityenEspa%C3%B1ol',
    'twitter': 'https://x.com/home',
    'twitch': 'https://www.twitch.tv',
    'tiktok': 'https://www.tiktok.com',
    'spotify': 'https://open.spotify.com/',
    'linkedin': 'https://www.linkedin.com',
    'pinterest': 'https://www.pinterest.es',
    'discord': 'https://discord.com',
    'gmail': 'https://mail.google.com',
    'drive': 'https://drive.google.com',
    'notion': 'https://www.notion.so',
    'canva': 'https://www.canva.com',
    'stackoverflow': 'https://stackoverflow.com',
    'freecodecamp': 'https://www.freecodecamp.org',
    'gpt': 'https://chatgpt.com/',
    'udemy': 'https://www.udemy.com',
    'modelos': 'https://openrouter.ai/',
}

files = {
    'libro': 'buthowudidknow.pdf',
    'foto': 'logonobt.png',
    'manual': 'manual_goku.pdf',
    'python': 'python.pdf',
    'ejercicios': 'Ejercicios-Python.pdf',
}

contacts = {
    'Danny Primo': '+34606197854'
}

# Inicializar reconocimiento de voz y motor de texto a voz

listener = sr.Recognizer()
listener.dynamic_energy_threshold = True  # Umbral dinámico de energía
listener.pause_threshold = 1.5  # Tiempo de pausa entre frases
listener.phrase_time_limit = 8  # Límite máximo de frase
listener.non_speaking_duration = 0.5  # Silencios no considerados como pausas
engine = pyttsx3.init()

# Variable global 
ultimo_comando = None
ocupado = False
lock = threading.Lock()
camara_activa = False
confirmacion_pendiente = None
alarma_activa = False
hora_alarma = None
alarma_thread = None
reproduccion_pendiente = False
alarma_pendiente = False
asistente_activo = False  # Variable para controlar el estado del asistente

# Variable global para el estado del asistente
estado_asistente = None

def set_estado_asistente(estado):
    global estado_asistente
    estado_asistente = estado

def capture():
    cap = cv2.VideoCapture(0)
    low_yellow = np.array([25, 192, 20], np.uint8)
    high_yellow = np.array([30, 255, 255], np.uint8)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        yellow_mask = cv2.inRange(frame_HSV, low_yellow, high_yellow)

        contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area = cv2.contourArea(c)
            if area > 1000:
                new_contour = cv2.convexHull(c)
                cv2.drawContours(frame, [new_contour], 0, (0, 255, 255), 3)

        cv2.imshow('Detección de color', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = escuchar()
    f.write(rec_write + os.linesep)
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)

def cambiar_volumen(accion):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    current_volume = volume.GetMasterVolumeLevelScalar()  # Obtener volumen actual (0.0 a 1.0)

    if accion == "subir":
        nuevo_volumen = min(1.0, current_volume + 0.1)  # Aumenta en 10%
        talk("Subiendo el volumen")
    elif accion == "bajar":
        nuevo_volumen = max(0.0, current_volume - 0.1)  # Disminuye en 10%
        talk("Bajando el volumen")
    else:
        return

    volume.SetMasterVolumeLevelScalar(nuevo_volumen, None)
    print(f"🔊 Volumen ajustado a {int(nuevo_volumen * 100)}%")

def talk(text):
    """Función para que el asistente hable bloqueando la escucha"""
    global ocupado, estado_asistente
    with lock:
        ocupado = True
    
    print(f"🗣️ {text}")
    estado_asistente.set(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()
    
    with lock:
        ocupado = False
        estado_asistente.set("Estado: Inactivo")

def escuchar():
    """Función que escucha y actualiza el último comando con mejoras"""
    global estado_asistente, asistente_activo

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 54321))
        print("✅ Selina está lista y escuchando en el puerto 54321")
    except OSError:
        print("❌ Ya hay otro proceso usando el puerto 54321")
        return True  # Ya

    global ultimo_comando, ocupado
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=2)
        listener.pause_threshold = 0.8  # Reducir pausa necesaria entre frases
        listener.phrase_time_limit = 5  # Límite de tiempo por frase
        listener.energy_threshold = 3000  # Ajuste más preciso

        while asistente_activo:
            try:
                with lock:
                    if ocupado:
                        continue

                print("👂 Escuchando...")
                estado_asistente.set("👂 Escuchando...")
                audio = listener.listen(source, timeout=5, phrase_time_limit=5)
                rec = listener.recognize_google(audio, language="es-ES").lower()  # Usar español de España

                with lock:
                    if not ocupado and rec:
                        ultimo_comando = rec

            except sr.UnknownValueError:
                print("❌ No se detectó voz")
                estado_asistente.set("❌ No se detectó voz")
            except Exception as e:
                print(f"Error: {str(e)}")
                estado_asistente.set(f"Error: {str(e)}")
    s.close()

def reproduce_musica(rec=None):
    global reproduccion_pendiente
    
    if not reproduccion_pendiente:
        # Primera parte: preguntar por la canción
        reproduccion_pendiente = True
        talk("¿Qué canción quieres escuchar?")
        return
    
    # Segunda parte: recibir el título
    if rec:
        reproduccion_pendiente = False
        music = rec.strip()
        talk(f"Reproduciendo {music}")
        pywhatkit.playonyt(music)

def buscar_info(rec):
    search = rec.replace('busca', '').strip()
    try:
        wikipedia.set_lang("es")
        wiki = wikipedia.summary(search, sentences=2)
        talk(wiki)
    except Exception:
        talk("No encontré información sobre eso")

def verificar_alarma():
    global alarma_activa
    while alarma_activa:
        now = datetime.datetime.now().strftime('%H:%M')
        if now == hora_alarma:
            print('¡DESPIERTA!')
            mixer.music.load("alarma.mp3")
            mixer.music.play()
            # Reproducir alarma hasta que se detenga
            while mixer.music.get_busy() and alarma_activa:
                time.sleep(0.1)
            break
        time.sleep(10)  # Verificar cada 10 segundos

def activar_alarma(rec=None):
    global alarma_activa, hora_alarma, alarma_thread, alarma_pendiente
    
    if not alarma_pendiente:
        # Primera parte: preguntar por la hora
        alarma_pendiente = True
        talk("¿A qué hora quieres la alarma?")
        return
    
    # Segunda parte: recibir la hora
    if rec:
        alarma_pendiente = False
        try:
            # Limpiar y formatear la hora
            hora = rec.replace(' ', '').replace(':', '')
            if len(hora) != 4 or not hora.isdigit():
                raise ValueError
                
            hora_formateada = f"{hora[:2]}:{hora[2:]}"
            hora_alarma = hora_formateada
            
            # Detener cualquier alarma previa
            if alarma_thread and alarma_thread.is_alive():
                alarma_activa = False
                alarma_thread.join()
            
            alarma_activa = True
            talk(f"Alarma configurada a las {hora_formateada}")
            alarma_thread = threading.Thread(target=verificar_alarma)
            alarma_thread.start()
            
        except Exception as e:
            talk("Formato de hora inválido. Intenta de nuevo")
            alarma_pendiente = True  # Volver a preguntar

def abrir_sitio(rec, sites):
    """Abre un sitio web si está en la lista de sitios conocidos."""
    rec = rec.lower()  # Convertir a minúsculas para evitar errores de comparación
    
    for site, url in sites.items():
        if site in rec:
            print(f"🌐 Abriendo {site}: {url}")
            subprocess.run(f'start chrome {url}', shell=True)
            talk(f"Abriendo {site}")
            return  # Salir después de encontrar el sitio correcto
    
    talk("No encontré ese sitio en mi lista.")

def cerrar_web():
    if platform.system() == "Windows":
        os.system("taskkill /IM chrome.exe /F")
        talk("Cerrando el navegador Chrome")
    elif platform.system() == "Darwin":
        os.system("pkill Chrome")
        talk("Cerrando el navegador Chrome")
    else:
        os.system("pkill chrome")
        talk("Cerrando el navegador Chrome")

def abrir_archivo(rec, files):
    """Abre un archivo si está en la lista de archivos conocidos."""
    rec = rec.lower()
    
    for file, path in files.items():
        if file in rec:
            if os.path.exists(path):  # Verifica si el archivo realmente existe
                print(f"📂 Abriendo {file}: {path}")
                subprocess.Popen([path], shell=True)
                talk(f'Abriendo {file}')
            else:
                talk(f"No encontré el archivo {file}. Verifica que esté en la ubicación correcta.")
            return  # Salir después de encontrar el archivo correcto
    
    talk("No encontré ese archivo en mi lista.")

def escribir_nota():
    try:
        talk("¿Qué quieres que escriba?")
        with sr.Microphone() as source:
            audio = listener.listen(source, timeout=5)
            texto = listener.recognize_google(audio, language='es-ES')
            
        with open("nota.txt", "a") as f:
            f.write(texto + "\n")
            
        talk("Nota guardada correctamente")
        sub.Popen("nota.txt", shell=True)
        
    except Exception as e:
        talk("No pude escribir la nota")
        print(f"Error: {str(e)}")

def manejar_camara():
    talk("Enseguida")
    capture()

def apagar_pc():
    talk("Apagando el sistema")
    if platform.system() == "Windows":
        os.system("shutdown /s /t 0")
    else:
        os.system("shutdown -h now")

def reiniciar_pc():
    talk("Reiniciando el sistema")
    if platform.system() == "Windows":
        os.system("shutdown /r /t 0")
    else:
        os.system("shutdown -r now")

def confirmar_accion(accion):
    global confirmacion_pendiente
    confirmacion_pendiente = accion
    talk(f"¿Quieres {accion} el ordenador? Di sí o no")

def procesar_comando(rec):
    global confirmacion_pendiente, reproduccion_pendiente, alarma_activa, alarma_pendiente, asistente_activo

    if alarma_pendiente:
        activar_alarma(rec)
        return

    if reproduccion_pendiente:
        reproduce_musica(rec)
        return

    # Manejar confirmación primero
    if confirmacion_pendiente:
        rec = rec.lower().strip()
        if rec in ["sí", "si", "sí.", "si.", "sí por favor", "sí claro"]:
            if confirmacion_pendiente == "apagar":
                talk("Apagando el sistema")
                if platform.system() == "Windows":
                    subprocess.run("shutdown /s /t 0", shell=True)
                else:
                    subprocess.run("shutdown -h now", shell=True)
            elif confirmacion_pendiente == "reiniciar":
                talk("Reiniciando el sistema")
                if platform.system() == "Windows":
                    subprocess.run("shutdown /r /t 0", shell=True)
                else:
                    subprocess.run("shutdown -r now", shell=True)
        elif rec in ["no", "no gracias", "no quiero"]:
            talk("Operación cancelada")
        
        confirmacion_pendiente = None  # Resetear confirmación
        return  # Salir después de manejar la confirmación

    # Diccionario de comandos
    comandos = {
        "reproduce": lambda x: reproduce_musica(),  
        "busca": buscar_info,
        "detener": lambda x: [globals().update(alarma_activa=False), mixer.music.stop(), talk("Alarma detenida")] if alarma_activa else None,
        "alarma": lambda x: activar_alarma(),
        "cámara": lambda x: capture(),
        "abre": lambda x: abrir_sitio(x, sites),
        "cerrar web": lambda x: cerrar_web(),
        "música": lambda x: abrir_sitio(x, canciones),
        "archivo": lambda x: abrir_archivo(x, files),
        "escribe": lambda x: escribir_nota(),
        "sube volumen": lambda x: cambiar_volumen("subir"),
        "baja volumen": lambda x: cambiar_volumen("bajar"),
        "apagar": lambda x: confirmar_accion("apagar"),
        "reiniciar": lambda x: confirmar_accion("reiniciar"),
        "salir": lambda x: [talk("bye bye"), detener_asistente()],
    }

    # Buscar coincidencias en comandos
    for clave, funcion in comandos.items():
        if clave in rec:
            funcion(rec)
            return

    # Manejar comandos no reconocidos
    talk("No entendí el comando")

def detener_asistente():
    global asistente_activo
    asistente_activo = False
    talk("El asistente se ha detenido")

def iniciar_asistente():
    global asistente_activo
    asistente_activo = True
    threading.Thread(target=escuchar, daemon=True).start()
    threading.Thread(target=run_selina, daemon=True).start()

def run_selina():
    global estado_asistente

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 12345))
        print("✅ Selina está lista y escuchando en el puerto 12345")
    except OSError:
        print("❌ Ya hay otro proceso usando el puerto 12345")
        return True  # Ya

    global ultimo_comando, ocupado, alarma_activa
    mixer.init()

    while asistente_activo:
        rec = None
        
        with lock:
            if ultimo_comando and not ocupado:
                rec = ultimo_comando.lower()
                ultimo_comando = None
                ocupado = True

        if rec:
            try:
                print(f"⚙️ Procesando comando: {rec}")
                estado_asistente.set(f"⚙️ Procesando comando: {rec}")
                # Si es comando de alarma, manejar en hilo separado
                if 'alarma' in rec or 'detener' in rec:
                    threading.Thread(target=procesar_comando, args=(rec,)).start()
                else:
                    procesar_comando(rec)
            except Exception as e:
                print(f"❌ Error procesando comando: {str(e)}")
                estado_asistente.set(f"❌ Error procesando comando: {str(e)}")
            finally:
                with lock:
                    ocupado = False
                    estado_asistente.set("Estado: Inactivo")

        time.sleep(0.2)
    s.close()       