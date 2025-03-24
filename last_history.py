import os
import subprocess
from datetime import datetime


HISTORIAL_FILE = "historial_respuestas.txt"


def guardar_en_txt(prompt, response, max_entries=10):
    """
    Guarda la consulta y la respuesta en un archivo de texto, manteniendo solo las últimas 10 entradas,
    con mejor formato para mayor legibilidad.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nueva_entrada = f"\n\n{'=' * 100}\n📅 Fecha: {timestamp}\n❓ Pregunta: {prompt}\n💡 Respuesta:\n{response}\n{'=' * 100}\n\n"

    # Leer historial existente si el archivo ya existe
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            historial = f.read().strip().split("=" * 100 + "\n\n")  # Dividir correctamente

        # Mantener solo las últimas `max_entries - 1` respuestas y agregar la nueva
        historial = (historial[-(max_entries - 1):] if len(historial) >= max_entries else historial) + [nueva_entrada]
    else:
        historial = [nueva_entrada]

    # Sobrescribir el archivo con las últimas 10 respuestas
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(historial) + "\n")

def abrir_historial():
    """
    Abre el archivo historial_respuestas.txt con el editor de texto predeterminado.
    """
    if not os.path.exists(HISTORIAL_FILE):
        return "⚠️ No hay historial guardado aún."

    try:
        if os.name == "nt":  # Windows
            os.startfile(HISTORIAL_FILE)
        elif os.name == "posix":  # macOS/Linux
            subprocess.run(["xdg-open", HISTORIAL_FILE] if "linux" in os.sys.platform else ["open", HISTORIAL_FILE])
        return "📂 Historial abierto correctamente."
    except Exception as e:
        return f"❌ Error al abrir el historial: {e}"