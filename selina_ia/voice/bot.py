"""
Bot de voz principal - refactorizado para usar commands.py
"""
from .commands import (
    talk, escuchar, procesar_comando, detener_asistente,
    iniciar_asistente, run_selina, set_estado_asistente
)

# Re-exportar las funciones principales para compatibilidad
__all__ = [
    'talk', 'escuchar', 'procesar_comando', 'detener_asistente',
    'iniciar_asistente', 'run_selina', 'set_estado_asistente'
]