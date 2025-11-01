"""
Configuraciones centralizadas del sistema Selina IA
"""
import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).parent.parent
PROJECT_ROOT = BASE_DIR.parent

# Configuración de base de datos
DATABASE_PATH = BASE_DIR / "data" / "my_database.sqlite"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Configuración de embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMB_DIM = 384
INDEX_PATH = BASE_DIR / "data" / "vector_index.faiss"
METADATA_PATH = BASE_DIR / "data" / "vector_metadata.json"

# Configuración de LLM
LLM_MODEL = "qwen2.5:0.5b"
LLM_TEMPERATURE = 0.5
LLM_NUM_PREDICT = 500
LLM_REPEAT_PENALTY = 1.2

# Configuración de voz
VOICE_ENERGY_THRESHOLD = 5000
VOICE_PAUSE_THRESHOLD = 0.8
VOICE_PHRASE_TIME_LIMIT = 5
VOICE_NON_SPEAKING_DURATION = 0.5

# Configuración de interfaz
WINDOW_TITLE = "NoBt GPT 🐍"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 750

# Configuración de imágenes
IMAGES_DIR = BASE_DIR / "ui" / "images"

# Configuración de audio
ALARM_SOUND = PROJECT_ROOT / "alarma.mp3"

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Diccionarios de comandos (mover a archivos separados si crecen mucho)
SITES = {
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
    'manual': 'https://www.notion.so/BD_Selina-271f48680df180a2971ae5201b6a7205?source=copy_link',
}

CANCIONES = {
    'motivación': 'https://www.youtube.com/watch?v=Pnf8Y0kE4Z8&ab_channel=MotiversityenEspa%C3%B1ol',
    'chill': 'https://www.youtube.com/watch?v=cq2Ef6rvL6g&t=3587s&ab_channel=RelaxChilloutMusic',
    'estudiar': 'https://www.youtube.com/watch?v=DZ5LneDpTBc&ab_channel=musicforlife',
    'relax': 'https://www.youtube.com/watch?v=LAqOdX5jgb4&ab_channel=JAZZ%26BLUES',
}

FILES = {
    'libro': PROJECT_ROOT / 'buthowudidknow.pdf',
    'foto': PROJECT_ROOT / 'logonobt.png',
    'manual': PROJECT_ROOT / 'manual_goku.pdf',
    'python': PROJECT_ROOT / 'python.pdf',
    'ejercicios': PROJECT_ROOT / 'Ejercicios-Python.pdf',
}

CONTACTS = {
    'Danny Primo': '+34606197854'
}