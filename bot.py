import speech_recognition as sr
import threading
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, cv2, subprocess, os
from pygame import mixer
import numpy as np
import subprocess as sub

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
engine = pyttsx3.init()

# Variable global para almacenar el último comando
ultimo_comando = None


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
    """Función para que el asistente hable"""
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()


def escuchar():
    """Función que escucha en un hilo separado y actualiza el último comando"""
    global ultimo_comando
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=2)
        while True:
            try:
                print("👂 Escuchando...")
                audio = listener.listen(source, timeout=15)
                rec = listener.recognize_google(audio, language="es").lower()
                print(f"✅ Has dicho: {rec}")
                ultimo_comando = rec  # Guardar el comando en la variable global
            except sr.UnknownValueError:
                print("❌ No entendí lo que dijiste")
            except sr.WaitTimeoutError:
                print("⌛ Tiempo de espera agotado")
            except sr.RequestError as e:
                print(f"⚠️ Error con el servicio de reconocimiento: {e}")


def run_selina():
    """Función principal que ejecuta comandos sin reiniciar la escucha"""
    global ultimo_comando
    mixer.init()

    while True:
        if ultimo_comando:  # Solo actúa si hay un nuevo comando
            rec = ultimo_comando
            ultimo_comando = None  # Reiniciar el comando para evitar repetirlo

            if 'reproduce' in rec:
                music = rec.replace('reproduce', '').strip()
                talk(f"Reproduciendo {music}")
                pywhatkit.playonyt(music)

            elif 'busca' in rec:
                search = rec.replace('busca', '').strip()
                try:
                    wikipedia.set_lang("es")
                    wiki = wikipedia.summary(search, sentences=1)
                    talk(wiki)
                except Exception:
                    talk("No encontré información sobre eso")

            elif 'alarma' in rec:
                num = rec.replace('alarma', '').strip()
                talk(f"Alarma activada a las {num} horas")
                while True:
                    now = datetime.datetime.now().strftime('%H:%M')
                    if now == num:
                        print('¡DESPIERTA!')
                        mixer.music.load("auronplay-alarma.mp3")
                        mixer.music.play()
                        if keyboard.read_key() == "s":
                            mixer.music.stop()
                            break

            elif 'cam' in rec:
                talk("Enseguida")
                capture()

            elif 'abre' in rec:
                for site in sites:
                    if site in rec:
                        print(f"🌐 Abriendo {site}: {sites[site]}")
                        subprocess.run(f'start chrome {sites[site]}', shell=True)
                        talk(f"Abriendo {site}")

            elif 'archivo' in rec:
                for file in files:
                    if file in rec:
                        print(f"📂 Abriendo {file}: {files[file]}")
                        sub.Popen([files[file]], shell=True)
                        talk(f'Abriendo {file}')

            elif 'escribe' in rec:
                try:
                    with open("nota.txt", 'a') as f:
                        write(f)
                except FileNotFoundError:
                    with open("nota.txt", 'a') as f:
                        write(f)

            elif 'salir' in rec:
                talk("Saliendo del asistente")
                break



