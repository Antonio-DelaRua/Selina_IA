import speech_recognition as sr
import threading
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, cv2, subprocess, os
from pygame import mixer
import numpy as np
import subprocess as sub
import time
import re

# Diccionarios de sitios, archivos y contactos
sites = {
    'google': 'https://www.google.com',
    'youtube': 'https://www.youtube.com',
    'facebook': 'https://www.facebook.com',
    'whatsapp': 'https://web.whatsapp.com',
    'cursos': 'https://freecodecamp.org/learn'
}

files = {
    'libro': 'but how u did know erazo.pdf',
    'foto': 'luffy erazo.jpg'
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
                audio = listener.listen(source, timeout=5.0, phrase_time_limit=10)
                rec = listener.recognize_google(audio, language="es-ES").lower()  # Usar español de España

                with lock:
                    if not ocupado and rec:
                        ultimo_comando = rec

            except sr.UnknownValueError:
                print("❌ No se detectó voz")
            except Exception as e:
                print(f"Error: {str(e)}")



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
    for site in sites:
        if site in rec:
            print(f"🌐 Abriendo {site}: {sites[site]}")
            subprocess.run(f'start chrome {sites[site]}', shell=True)
            talk(f"Abriendo {site}")

def abrir_archivo(rec, files):
    for file in files:
        if file in rec:
            print(f"📂 Abriendo {file}: {files[file]}")
            subprocess.Popen([files[file]], shell=True)
            talk(f'Abriendo {file}')

def escribir_nota():
    try:
        with open("nota.txt", 'a') as f:
            write(f)
    except FileNotFoundError:
        with open("nota.txt", 'a') as f:
            write(f)

def run_selina():
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
                
                if re.match(r'reproduce .+', rec):
                    reproduce_musica(rec)
                elif re.match(r'busca .+', rec):
                    buscar_info(rec)
                elif 'reproduce' in rec:
                    reproduce_musica(rec)
                elif 'busca' in rec:
                    buscar_info(rec)
                elif 'alarma' in rec:
                    activar_alarma(rec)
                elif 'cam' in rec:
                    talk("Enseguida")
                    capture()
                elif 'abre' in rec:
                    abrir_sitio(rec, sites)
                elif 'archivo' in rec:
                    abrir_archivo(rec, files)
                elif 'escribe' in rec:
                    escribir_nota()
                elif 'salir' in rec:
                    talk("Saliendo del asistente")
            except Exception as e:
                print(f"Error procesando comando: {str(e)}")
            finally:
                with lock:
                    ocupado = False

        time.sleep(0.2)


        