"""
Procesamiento de comandos de voz - refactorizado de bot.py
"""
import webbrowser
import numpy as np
import pyautogui as at
import time
import socket
import platform
import os
import subprocess
from pygame import mixer
import datetime
import cv2
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import ctypes
import threading
import speech_recognition as sr
import pyttsx3, pywhatkit, wikipedia, keyboard
from config.settings import (
    SITES, CANCIONES, FILES, CONTACTS, ALARM_SOUND,
    VOICE_ENERGY_THRESHOLD, VOICE_PAUSE_THRESHOLD, VOICE_PHRASE_TIME_LIMIT, VOICE_NON_SPEAKING_DURATION
)
from core.database import Task, SessionLocal
import datetime
import re

# Inicializar reconocimiento de voz y motor de texto a voz
listener = sr.Recognizer()
listener.dynamic_energy_threshold = True  # Umbral dinámico de energía
listener.pause_threshold = VOICE_PAUSE_THRESHOLD  # Tiempo de pausa entre frases
listener.phrase_time_limit = VOICE_PHRASE_TIME_LIMIT  # Límite máximo de frase
listener.non_speaking_duration = VOICE_NON_SPEAKING_DURATION  # Silencios no considerados como pausas
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

def cambiar_volumen(accion):
    try:
        import os
        if platform.system() == "Windows":
            if accion == "subir":
                # Método 1: Usar PowerShell para Windows moderno
                try:
                    # Comando PowerShell para subir volumen
                    ps_command = 'powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"'
                    os.system(ps_command)
                    talk("Subiendo el volumen")
                    print("🔊 Volumen aumentado con PowerShell")
                    return
                except:
                    pass

                # Método 2: Usar pyautogui con más pulsaciones
                try:
                    import pyautogui as pg
                    for _ in range(3):  # Más pulsaciones para notar el cambio
                        pg.press('volumeup')
                        pg.sleep(0.1)  # Pequeña pausa
                    talk("Subiendo el volumen")
                    print("🔊 Volumen aumentado con teclas")
                    return
                except:
                    pass

                # Método 3: Usar nircmd si está disponible
                try:
                    result = os.system("nircmd.exe changesysvolume 10000 >nul 2>&1")  # +10000 unidades
                    if result == 0:
                        talk("Subiendo el volumen")
                        print("🔊 Volumen aumentado con NirCmd")
                        return
                except:
                    pass

            elif accion == "bajar":
                # Método 1: Usar PowerShell para Windows moderno
                try:
                    ps_command = 'powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"'
                    os.system(ps_command)
                    talk("Bajando el volumen")
                    print("🔊 Volumen reducido con PowerShell")
                    return
                except:
                    pass

                # Método 2: Usar pyautogui con más pulsaciones
                try:
                    import pyautogui as pg
                    for _ in range(3):  # Más pulsaciones para notar el cambio
                        pg.press('volumedown')
                        pg.sleep(0.1)  # Pequeña pausa
                    talk("Bajando el volumen")
                    print("🔊 Volumen reducido con teclas")
                    return
                except:
                    pass

                # Método 3: Usar nircmd si está disponible
                try:
                    result = os.system("nircmd.exe changesysvolume -10000 >nul 2>&1")  # -10000 unidades
                    if result == 0:
                        talk("Bajando el volumen")
                        print("🔊 Volumen reducido con NirCmd")
                        return
                except:
                    pass

        # Si estamos en otro sistema operativo
        talk("Función de volumen no disponible en este sistema")
        print("⚠️ Control de volumen no soportado en este sistema")

    except Exception as e:
        error_msg = f"Error ajustando volumen: {e}"
        print(f"❌ {error_msg}")
        talk("No pude ajustar el volumen del sistema")

def talk(text):
    """Función para que el asistente hable bloqueando la escucha"""
    global ocupado, estado_asistente
    with lock:
        ocupado = True

    print(f"🗣️ {text}")
    estado_asistente.set(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()

    # Pequeña pausa para asegurar que el audio termine
    time.sleep(0.1)

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
        listener.energy_threshold = VOICE_ENERGY_THRESHOLD  # Ajuste más preciso

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
        talk("¿dime?")
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
            mixer.music.load(str(ALARM_SOUND))
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
        subprocess.Popen("nota.txt", shell=True)

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

def abrir_configuracion():
    subprocess.run("start ms-settings:", shell=True)

def abrir_terminal():
    subprocess.run("start cmd", shell=True)

def abrir_descargas():
    # Intenta primero con Descargas y luego con Downloads
    possible_folders = ["Descargas", "Downloads"]
    found = False
    for folder in possible_folders:
        downloads_path = os.path.join(os.path.expanduser("~"), folder)
        if os.path.exists(downloads_path):
            subprocess.run(f'start "" "{downloads_path}"', shell=True)
            found = True
            break
    if not found:
        talk("No se encontró la carpeta de descargas en tu usuario.")

def abrir_documentos():
    possible_folders = ["Documents", "Documentos"]
    for folder in possible_folders:
        documents_path = os.path.join(os.path.expanduser("~"), folder)
        if os.path.isdir(documents_path):
            subprocess.run(f'explorer "{documents_path}"', shell=True)
            return
    talk("No se encontró la carpeta de documentos en tu usuario.")

def abrir_imagenes():
    possible_folders = ["Imágenes", "Pictures"]
    for folder in possible_folders:
        images_path = os.path.join(os.path.expanduser("~"), folder)
        if os.path.isdir(images_path):
            subprocess.run(f'explorer "{images_path}"', shell=True)
            return
    talk("No se encontró la carpeta de imágenes en tu usuario.")

def abrir_carpeta_personalizada(rec):
    """Abrir carpeta personalizada por voz"""
    # Extraer el nombre de la carpeta del comando
    # Ejemplos: "abre carpeta documentos", "abre carpeta música", "abre carpeta videos"
    folder_keywords = {
        "documentos": ["Documentos", "Documents"],
        "descargas": ["Descargas", "Downloads"],
        "imágenes": ["Imágenes", "Pictures"],
        "vídeos": ["Vídeos", "Videos"],
        "música": ["Música", "Music"],
        "escritorio": ["Escritorio", "Desktop"],
        "papelera": ["Papelera de reciclaje", "Recycle Bin"],
        "programas": ["Program Files", "Program Files (x86)"],
        "usuario": [os.path.expanduser("~")],
        "inicio": [os.path.expanduser("~")],
        "raíz": ["C:\\"],
        "sistema": ["C:\\Windows\\System32"],
        "temp": ["C:\\Windows\\Temp", os.path.expanduser("~\\AppData\\Local\\Temp")],
        "onedrive": ["OneDrive"],
        "appdata": ["AppData"],
        "programdata": ["ProgramData"],
        "windows": ["C:\\Windows"],
        "system32": ["C:\\Windows\\System32"],
        "boot": ["C:\\Boot"],
        "drivers": ["C:\\Windows\\System32\\drivers"],
        "fonts": ["C:\\Windows\\Fonts"],
        "inf": ["C:\\Windows\\INF"],
        "logs": ["C:\\Windows\\Logs"],
        "prefetch": ["C:\\Windows\\Prefetch"],
        "winsxs": ["C:\\Windows\\WinSxS"],
        "perfil": [os.path.expanduser("~")],
        "local": [os.path.expanduser("~\\AppData\\Local")],
        "roaming": [os.path.expanduser("~\\AppData\\Roaming")],
        "publico": ["C:\\Users\\Public"],
        "todos los usuarios": ["C:\\ProgramData"],
        "archivos de programa": ["C:\\Program Files"],
        "archivos de programa x86": ["C:\\Program Files (x86)"],
        "windows defender": ["C:\\ProgramData\\Microsoft\\Windows Defender"],
        "microsoft": ["C:\\Program Files\\Microsoft Office"],
        "office": ["C:\\Program Files\\Microsoft Office"],
        "steam": [os.path.expanduser("~\\AppData\\Roaming\\Steam")],
        "epic games": [os.path.expanduser("~\\AppData\\Local\\EpicGamesLauncher")],
        "ubisoft": [os.path.expanduser("~\\Program Files (x86)\\Ubisoft")],
        "origin": [os.path.expanduser("~\\AppData\\Local\\Origin")],
        "battle.net": [os.path.expanduser("~\\AppData\\Local\\Battle.net")],
        "nvidia": ["C:\\Program Files\\NVIDIA Corporation"],
        "amd": ["C:\\Program Files\\AMD"],
        "intel": ["C:\\Program Files\\Intel"],
        "realtek": ["C:\\Program Files\\Realtek"],
        "asus": ["C:\\Program Files (x86)\\ASUS"],
        "lenovo": ["C:\\Program Files\\Lenovo"],
        "hp": ["C:\\Program Files\\HP"],
        "dell": ["C:\\Program Files\\Dell"],
        "acer": ["C:\\Program Files\\Acer"],
        "samsung": ["C:\\Program Files\\Samsung"],
        "sony": ["C:\\Program Files\\Sony"],
        "panasonic": ["C:\\Program Files\\Panasonic"],
        "canon": ["C:\\Program Files\\Canon"],
        "epson": ["C:\\Program Files\\Epson"],
        "brother": ["C:\\Program Files\\Brother"],
        "lexmark": ["C:\\Program Files\\Lexmark"],
        "xerox": ["C:\\Program Files\\Xerox"],
        "kodak": ["C:\\Program Files\\Kodak"],
        "fuji": ["C:\\Program Files\\Fuji"],
        "nikon": ["C:\\Program Files\\Nikon"],
        "olympus": ["C:\\Program Files\\Olympus"],
        "pentax": ["C:\\Program Files\\Pentax"],
        "sigma": ["C:\\Program Files\\Sigma"],
        "tamron": ["C:\\Program Files\\Tamron"],
        "tokina": ["C:\\Program Files\\Tokina"],
        "zeiss": ["C:\\Program Files\\Zeiss"],
        "leica": ["C:\\Program Files\\Leica"],
        "hasselblad": ["C:\\Program Files\\Hasselblad"],
        "phase one": ["C:\\Program Files\\Phase One"],
        "mamiya": ["C:\\Program Files\\Mamiya"],
        "rollei": ["C:\\Program Files\\Rollei"],
        "contax": ["C:\\Program Files\\Contax"],
        "minolta": ["C:\\Program Files\\Minolta"],
        "konica": ["C:\\Program Files\\Konica"],
        "ricoh": ["C:\\Program Files\\Ricoh"],
        "pentax": ["C:\\Program Files\\Pentax"],
        "sigma": ["C:\\Program Files\\Sigma"],
        "tamron": ["C:\\Program Files\\Tamron"],
        "tokina": ["C:\\Program Files\\Tokina"],
        "zeiss": ["C:\\Program Files\\Zeiss"],
        "leica": ["C:\\Program Files\\Leica"],
        "hasselblad": ["C:\\Program Files\\Hasselblad"],
        "phase one": ["C:\\Program Files\\Phase One"],
        "mamiya": ["C:\\Program Files\\Mamiya"],
        "rollei": ["C:\\Program Files\\Rollei"],
        "contax": ["C:\\Program Files\\Contax"],
        "minolta": ["C:\\Program Files\\Minolta"],
        "konica": ["C:\\Program Files\\Konica"],
        "ricoh": ["C:\\Program Files\\Ricoh"],
    }

    rec_lower = rec.lower()
    for keyword, folders in folder_keywords.items():
        if keyword in rec_lower:
            for folder in folders:
                if keyword == "papelera":
                    # Para papelera de reciclaje
                    subprocess.run('start shell:RecycleBinFolder', shell=True)
                    talk(f"Abriendo {keyword}")
                    return
                elif keyword == "raíz":
                    subprocess.run(f'explorer "{folder}"', shell=True)
                    talk(f"Abriendo carpeta raíz")
                    return
                elif keyword == "sistema":
                    subprocess.run(f'explorer "{folder}"', shell=True)
                    talk(f"Abriendo carpeta del sistema")
                    return
                elif keyword == "temp":
                    for temp_folder in folders:
                        if os.path.exists(temp_folder):
                            subprocess.run(f'explorer "{temp_folder}"', shell=True)
                            talk(f"Abriendo carpeta temporal")
                            return
                else:
                    folder_path = os.path.join(os.path.expanduser("~"), folder)
                    if os.path.isdir(folder_path):
                        subprocess.run(f'explorer "{folder_path}"', shell=True)
                        talk(f"Abriendo carpeta {keyword}")
                        return

    # Si no encuentra carpeta específica, intentar abrir cualquier carpeta mencionada
    # Buscar patrones como "abre carpeta X" o "abre X"
    import re
    match = re.search(r'abre(?:\s+carpeta)?\s+(.+)', rec_lower)
    if match:
        folder_name = match.group(1).strip()
        # Intentar rutas comunes
        possible_paths = [
            os.path.join(os.path.expanduser("~"), folder_name),
            f"C:\\{folder_name}",
            f"C:\\Program Files\\{folder_name}",
            f"C:\\Program Files (x86)\\{folder_name}",
            folder_name  # Ruta absoluta si se proporciona
        ]

        for path in possible_paths:
            if os.path.isdir(path):
                subprocess.run(f'explorer "{path}"', shell=True)
                talk(f"Abriendo carpeta {folder_name}")
                return

    talk("No pude encontrar esa carpeta")

def abrir_aplicacion(rec):
    """Abrir aplicación por voz"""
    app_keywords = {
        "calculadora": "start calc",
        "paint": "start mspaint",
        "wordpad": "start write",
        "notepad": "start notepad",
        "explorer": "start explorer",
        "navegador": "start chrome",
        "chrome": "start chrome",
        "firefox": "start firefox",
        "edge": "start msedge",
        "word": "start winword",
        "excel": "start excel",
        "powerpoint": "start powerpnt",
        "outlook": "start outlook",
        "teams": "start teams",
        "zoom": "start zoom",
        "discord": "start discord",
        "spotify": "start spotify",
        "steam": "start steam",
        "photoshop": "start photoshop",
        "illustrator": "start illustrator",
        "premiere": "start premiere",
        "after effects": "start afterfx",
        "blender": "start blender",
        "unity": "start unity",
        "visual studio": "start devenv",
        "android studio": "start studio64",
        "eclipse": "start eclipse",
        "netbeans": "start netbeans",
        "sublime": "start sublime_text",
        "atom": "start atom",
        "brackets": "start brackets",
        "notepad++": "start notepad++",
        "vscode": "start code",
        "terminal": "start cmd",
        "powershell": "start powershell",
        "cmd": "start cmd",
        "explorador": "start explorer",
        "archivos": "start explorer",
        "mi pc": "start explorer",
        "este equipo": "start explorer",
        "panel": "start control",
        "configuración": "start ms-settings:",
        "tienda": "start ms-windows-store:",
        "microsoft store": "start ms-windows-store:",
        "paint 3d": "start ms-paint:",
        "fotos": "start ms-photos:",
        "reproductor": "start wmplayer",
        "windows media player": "start wmplayer",
        "vlc": "start vlc",
        "winrar": "start winrar",
        "7zip": "start 7zFM",
        "skype": "start skype",
        "whatsapp": "start whatsapp",
        "telegram": "start telegram",
        "slack": "start slack",
        "trello": "start trello",
        "evernote": "start evernote",
        "onenote": "start onenote",
        "dropbox": "start dropbox",
        "google drive": "start googledrivesync",
        "onedrive": "start onedrive",
        "adobe reader": "start AcroRd32",
        "pdf": "start AcroRd32",
        "libreoffice": "start soffice",
        "openoffice": "start soffice",
    }

    rec_lower = rec.lower()
    for app_name, command in app_keywords.items():
        if app_name in rec_lower:
            try:
                subprocess.run(command, shell=True)
                talk(f"Abriendo {app_name}")
                return
            except Exception as e:
                print(f"Error abriendo {app_name}: {e}")
                talk(f"No pude abrir {app_name}")
                return

    # Si no encuentra app específica, intentar buscar en PATH
    import re
    match = re.search(r'abre\s+(.+)', rec_lower)
    if match:
        app_name = match.group(1).strip()
        try:
            subprocess.run(app_name, shell=True)
            talk(f"Abriendo {app_name}")
            return
        except Exception as e:
            print(f"Error abriendo {app_name}: {e}")

    talk("No encontré esa aplicación")

def quitar_sonido():
    """Silenciar el audio del sistema usando pycaw"""
    try:
        # Obtener el dispositivo de audio predeterminado
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Obtener el estado actual del mute
        current_mute = volume.GetMute()
        # Alternar el estado del mute
        new_mute_state = 1 if current_mute == 0 else 0
        volume.SetMute(new_mute_state, None)

        if new_mute_state == 1:
            talk("Audio silenciado")
        else:
            talk("Audio reactivado")

    except Exception as e:
        print(f"Error controlando mute: {e}")
        # Fallback: usar comandos del sistema
        try:
            import os
            if platform.system() == "Windows":
                # Usar nircmd para mute si está disponible
                result = os.system("nircmd.exe mutesysvolume 2 >nul 2>&1")
                if result == 0:
                    talk("Audio silenciado con nircmd")
                    return
                # Usar PowerShell como alternativa
                ps_command = 'powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"'
                os.system(ps_command)
                talk("Audio silenciado")
        except:
            talk("No pude controlar el audio del sistema")

def abrir_vscode():
    subprocess.run("code", shell=True)

def confirmar_accion(accion):
    global confirmacion_pendiente
    confirmacion_pendiente = accion
    talk(f"¿Quieres {accion} el ordenador? Di sí o no")

def get_tasks_for_date_voice(date_str):
    """Obtener tareas para una fecha específica por voz"""
    try:
        # Parsear fecha desde texto
        today = datetime.date.today()

        if "hoy" in date_str.lower():
            target_date = today
        elif "mañana" in date_str.lower():
            target_date = today + datetime.timedelta(days=1)
        elif "ayer" in date_str.lower():
            target_date = today - datetime.timedelta(days=1)
        else:
            # Intentar parsear fecha específica (ej: "15 de enero", "15/01", etc.)
            # Por simplicidad, asumir hoy por defecto
            target_date = today

        tasks = Task.get_tasks_for_date(target_date)
        if not tasks:
            response = f"No tienes tareas programadas para {date_str}"
            print(f"🎤 Respuesta de voz: {response}")
            return response

        pending_tasks = [t for t in tasks if not t.completed]
        completed_tasks = [t for t in tasks if t.completed]

        response = f"Tus tareas para {date_str}:\n"

        if pending_tasks:
            response += "\nPendientes:\n"
            for task in pending_tasks:
                time_str = f" a las {task.time}" if task.time else ""
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
                response += f"{priority_emoji} {task.title}{time_str}\n"

        if completed_tasks:
            response += "\nCompletadas:\n"
            for task in completed_tasks:
                response += f"✅ {task.title}\n"

        print(f"🎤 Respuesta de voz: {response}")
        return response

    except Exception as e:
        error_msg = f"Error obteniendo tareas: {e}"
        print(f"🎤 Error en voz: {error_msg}")
        return error_msg

def add_task_voice(title, date_str=None, time_str=None):
    """Agregar tarea por voz"""
    try:
        # Parsear fecha
        today = datetime.date.today()
        if date_str:
            if "mañana" in date_str.lower():
                target_date = today + datetime.timedelta(days=1)
            elif "pasado mañana" in date_str.lower():
                target_date = today + datetime.timedelta(days=2)
            else:
                target_date = today
        else:
            target_date = today

        # Crear tarea
        session = SessionLocal()
        try:
            new_task = Task(
                title=title,
                description="",
                date=datetime.datetime.combine(target_date, datetime.time.min),
                time=time_str,
                priority='medium',
                completed=0,
                category='personal'
            )
            session.add(new_task)
            session.commit()
            response = f"Tarea '{title}' agregada para {target_date.strftime('%d/%m/%Y')}"
            print(f"🎤 Respuesta de voz: {response}")
            return response
        finally:
            session.close()

    except Exception as e:
        error_msg = f"Error creando tarea: {e}"
        print(f"🎤 Error en voz: {error_msg}")
        return error_msg

def complete_task_voice(title_part):
    """Marcar tarea como completada por voz"""
    try:
        session = SessionLocal()
        try:
            # Buscar tarea por título parcial
            tasks = session.query(Task).filter(
                Task.title.ilike(f"%{title_part}%"),
                Task.completed == 0
            ).all()

            if not tasks:
                response = f"No encontré tareas pendientes con '{title_part}'"
                print(f"🎤 Respuesta de voz: {response}")
                return response

            # Marcar la primera como completada
            task = tasks[0]
            task.completed = 1
            session.commit()

            response = f"Tarea '{task.title}' marcada como completada"
            print(f"🎤 Respuesta de voz: {response}")
            return response

        finally:
            session.close()

    except Exception as e:
        error_msg = f"Error completando tarea: {e}"
        print(f"🎤 Error en voz: {error_msg}")
        return error_msg

def procesar_comando(rec):
    global confirmacion_pendiente, reproduccion_pendiente, alarma_activa, alarma_pendiente, asistente_activo

    rec_lower = rec.lower()

    # Comandos de calendario primero (más específicos)
    if "tarea" in rec_lower or "tareas" in rec_lower:
        if "qué" in rec_lower or "que" in rec_lower:
            # "qué tareas tengo hoy" según manual.md
            if "hoy" in rec_lower:
                response = get_tasks_for_date_voice("hoy")
                talk(response)
                return
            elif "mañana" in rec_lower:
                response = get_tasks_for_date_voice("mañana")
                talk(response)
                return
            else:
                response = get_tasks_for_date_voice("hoy")
                talk(response)
                return

        elif "agregar" in rec_lower or "añadir" in rec_lower or "crear" in rec_lower:
            # "tarea agregar [título]" según manual.md
            # Extraer título (todo después de "tarea agregar" hasta fin)
            title_match = re.search(r'tarea\s+agregar\s+(.+)', rec_lower)
            if title_match:
                title = title_match.group(1).strip()
                response = add_task_voice(title)
                talk(response)
                return

        elif "completar" in rec_lower or "completada" in rec_lower or "terminar" in rec_lower or "marcar" in rec_lower:
            # "marcar tarea [título] como completada" según manual.md
            title_match = re.search(r'marcar\s+tarea\s+(.+?)\s+como\s+completada', rec_lower)
            if title_match:
                title_part = title_match.group(1).strip()
                response = complete_task_voice(title_part)
                talk(response)
                return

        elif "calendario" in rec_lower or "calendar" in rec_lower:
            talk("Abriendo calendario")
            # Nota: El calendario se abre desde la GUI, no desde voz
            return

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

    # Función para determinar si "abre" es para app o sitio web
    def procesar_abre(rec):
        rec_lower = rec.lower()
        # Lista de aplicaciones conocidas
        apps_conocidas = [
            "chrome", "firefox", "edge", "word", "excel", "powerpoint", "outlook",
            "vscode", "código", "terminal", "powershell", "visual studio", "android studio",
            "eclipse", "sublime", "notepad++", "calculadora", "paint", "paint 3d", "fotos",
            "spotify", "vlc", "configuración", "panel", "explorador", "mi pc", "tienda",
            "steam", "discord", "zoom", "teams", "skype", "whatsapp", "telegram"
        ]

        # Verificar si menciona una aplicación conocida
        for app in apps_conocidas:
            if app in rec_lower:
                return abrir_aplicacion(rec)

        # Verificar si menciona un sitio web conocido
        for site in SITES:
            if site in rec_lower:
                return abrir_sitio(rec, SITES)

        # Si no es específico, intentar abrir como aplicación primero
        return abrir_aplicacion(rec)

    # Diccionario de comandos
    comandos = {
        "reproduce": lambda x: reproduce_musica(),
        "busca": lambda x: buscar_info(x),
        "detener": lambda x: [globals().update(alarma_activa=False), mixer.music.stop(), talk("Alarma detenida")] if alarma_activa else None,
        "alarma": lambda x: activar_alarma(),
        "cámara": lambda x: manejar_camara(),
        "abre": lambda x: procesar_abre(x),
        "cerrar web": lambda x: cerrar_web(),
        "música": lambda x: abrir_sitio(x, CANCIONES),
        "archivo": lambda x: abrir_archivo(x, FILES),
        "escribe": lambda x: escribir_nota(),
        "código": lambda x: abrir_vscode(),
        "terminal": lambda x: abrir_terminal(),
        "descargas": lambda x: abrir_descargas(),
        "documentos": lambda x: abrir_documentos(),
        "imágenes": lambda x: abrir_imagenes(),
        "carpeta": lambda x: abrir_carpeta_personalizada(x),
        "abre carpeta": lambda x: abrir_carpeta_personalizada(x),
        "abre aplicación": lambda x: abrir_aplicacion(x),
        "abre app": lambda x: abrir_aplicacion(x),
        "mute": lambda x: quitar_sonido(),
        "sube el volumen": lambda x: cambiar_volumen("subir"),
        "baja volumen": lambda x: cambiar_volumen("bajar"),
        "apagar": lambda x: confirmar_accion("apagar"),
        "reiniciar": lambda x: confirmar_accion("reiniciar"),
        "configuración": lambda x: abrir_configuracion(),
        "salir": lambda x: [talk("bye bye"), detener_asistente()],
    }

    # Buscar coincidencias en comandos (ordenar por longitud para priorizar frases más específicas)
    comandos_ordenados = sorted(comandos.items(), key=lambda x: len(x[0]), reverse=True)
    for clave, funcion in comandos_ordenados:
        if clave in rec:
            funcion(rec)
            return

    # Manejar comandos no reconocidos

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