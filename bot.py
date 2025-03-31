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



# Diccionarios de sitios, archivos y contactos
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

}

files = {
    'libro': 'buthowudidknow.pdf',
    'foto': 'image.png',
    'manual': 'manual_goku.pdf',
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

# Variable global para almacenar el último comando
ultimo_comando = None
ocupado = False
lock = threading.Lock()
camara_activa = False
confirmacion_pendiente = None


def capture():
    global camara_activa
    camara_activa = True
    cap = cv2.VideoCapture(0)
    
    while camara_activa:
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.imshow('Cámara en vivo', frame)
        
        # Cerrar con la tecla 'q' o por comando de voz
        if cv2.waitKey(1) & 0xFF == ord('q') or not camara_activa:
            break
            
    cap.release()
    cv2.destroyAllWindows()
    camara_activa = False


    cap.release()
    cv2.destroyAllWindows()


def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = escuchar()
    f.write(rec_write + os.linesep)
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)



def talk(text):
    """Función para que el asistente hable bloqueando la escucha"""
    global ocupado
    with lock:
        ocupado = True
    
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()
    
    with lock:
        ocupado = False



def escuchar():
    """Función que escucha y actualiza el último comando con mejoras"""

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

        while True:
            try:
                with lock:
                    if ocupado:
                        continue

                print("👂 Escuchando...")
                audio = listener.listen(source, timeout=5, phrase_time_limit=5)
                rec = listener.recognize_google(audio, language="es-ES").lower()  # Usar español de España

                with lock:
                    if not ocupado and rec:
                        ultimo_comando = rec

            except sr.UnknownValueError:
                print("❌ No se detectó voz")
            except Exception as e:
                print(f"Error: {str(e)}")
    s.close()
    

def reproduce_musica(rec):
    music = rec.replace('reproduce', '').strip()
    talk(f"Reproduciendo {music}")
    pywhatkit.playonyt(music)

def buscar_info(rec):
    search = rec.replace('busca', '').strip()
    try:
        wikipedia.set_lang("es")
        wiki = wikipedia.summary(search, sentences=1)
        talk(wiki)
    except Exception:
        talk("No encontré información sobre eso")

def activar_alarma(rec):
    num = rec.replace('alarma', '').strip()
    talk(f"Alarma activada a las {num} horas")
    while True:
        now = datetime.datetime.now().strftime('%H:%M')
        if now == num:
            print('¡DESPIERTA!')
            mixer.music.load("alarma.mp3")
            mixer.music.play()
            if keyboard.read_key() == "s":
                mixer.music.stop()
                break

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
    global confirmacion_pendiente

    # Manejar confirmación primero
    if confirmacion_pendiente:
        rec = rec.lower()
        if "si" in rec or "sí" in rec:
            if confirmacion_pendiente == "apagar":
                talk("Apagando el sistema")
                if platform.system() == "Windows":
                    os.system("shutdown /s /t 0")
                else:
                    os.system("shutdown -h now")
            elif confirmacion_pendiente == "reiniciar":
                talk("Reiniciando el sistema")
                if platform.system() == "Windows":
                    os.system("shutdown /r /t 0")
                else:
                    os.system("shutdown -r now")
        elif "no" in rec:
            talk("Operación cancelada")
        
        confirmacion_pendiente = None
        return  # Salir después de manejar la confirmación

    # Diccionario de comandos principal (fuera del bloque de confirmación)
    comandos = {
        "reproduce": reproduce_musica,
        "busca": buscar_info,
        "alarma": activar_alarma,
        "camara": lambda x: capture(),
        "abre": lambda x: abrir_sitio(x, sites),
        "archivo": lambda x: abrir_archivo(x, files),
        "escribe": lambda x: escribir_nota(),
        "apagar": lambda x: confirmar_accion("apagar"),
        "reiniciar": lambda x: confirmar_accion("reiniciar"),
        "salir": lambda x: [talk("Saliendo del sistema"), exit()]
    }

    # Buscar coincidencias en comandos
    for clave, funcion in comandos.items():
        if clave in rec:
            funcion(rec)
            return

    # Manejar comandos no reconocidos
    talk("No entendí el comando")



def run_selina():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 12345))
        print("✅ Selina está lista y escuchando en el puerto 12345")
    except OSError:
        print("❌ Ya hay otro proceso usando el puerto 12345")
        return True  # Ya

    global ultimo_comando, ocupado
    mixer.init()

    while True:
        rec = None
        
        with lock:
            if ultimo_comando and not ocupado:
                rec = ultimo_comando.lower()
                ultimo_comando = None
                ocupado = True

        if rec:
            try:
                print(f"⚙️ Procesando comando: {rec}")
                procesar_comando(rec)  # 🔥 Llamamos a la función que ya maneja los comandos
            except Exception as e:
                print(f"❌ Error procesando comando: {str(e)}")
            finally:
                with lock:
                    ocupado = False

        time.sleep(0.2)
    s.close()


        