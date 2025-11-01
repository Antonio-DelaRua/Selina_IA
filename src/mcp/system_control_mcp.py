from typing import Dict, Any
from .base import MCPServer
import subprocess
import os
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
try:
    from pycaw.pycaw import AudioUtility, IAudioEndpointVolume
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
try:
    import screen_brightness_control as sbc
    BRIGHTNESS_AVAILABLE = True
except ImportError:
    BRIGHTNESS_AVAILABLE = False
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
import win32gui
import win32con
import win32process
import win32com.client
from pathlib import Path

class SystemControlMCP(MCPServer):
    """MCP para controlar funciones del sistema"""
    
    def __init__(self):
        super().__init__("system_control_mcp")
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self._initialize_audio()

    def _initialize_audio(self):
        """Inicializar control de audio"""
        if not AUDIO_AVAILABLE:
            self.volume = None
            return

        try:
            devices = AudioUtility.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        except Exception as e:
            print(f"Error inicializando audio: {e}")
            self.volume = None
        
    async def initialize(self) -> None:
        """Nada específico que inicializar"""
        pass
        
    async def shutdown(self) -> None:
        """Limpieza al cerrar"""
        if self.volume:
            self.volume = None
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Manejar solicitudes de control del sistema"""
        action = request.get("action", "").lower()
        
        actions = {
            "open": self._handle_open,
            "volume": self._handle_volume,
            "brightness": self._handle_brightness,
            "window": self._handle_window,
            "system": self._handle_system
        }
        
        handler = actions.get(action)
        if handler:
            return await handler(request)
        
        return {"error": "Acción no reconocida"}

    async def _handle_open(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Abrir aplicaciones o archivos"""
        try:
            target = request.get("target", "")
            
            # Aplicaciones comunes
            common_apps = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "explorer": "explorer.exe",
                "cmd": "cmd.exe",
                "paint": "mspaint.exe"
            }
            
            if target in common_apps:
                subprocess.Popen(common_apps[target])
                return {"success": True, "message": f"Aplicación {target} abierta"}
            
            # Intentar abrir como ruta de archivo
            if os.path.exists(target):
                os.startfile(target)
                return {"success": True, "message": f"Archivo {target} abierto"}
                
            return {"error": f"No se pudo encontrar {target}"}
            
        except Exception as e:
            return {"error": str(e)}

    async def _handle_volume(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Control de volumen"""
        try:
            if not self.volume:
                return {"error": "Control de volumen no disponible"}
                
            action = request.get("volume_action")
            value = request.get("value", 0)
            
            current_volume = self.volume.GetMasterVolumeLevelScalar() * 100
            
            if action == "set":
                self.volume.SetMasterVolumeLevelScalar(value / 100, None)
                return {"success": True, "volume": value}
                
            elif action == "up":
                new_volume = min(current_volume + value, 100)
                self.volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
                return {"success": True, "volume": new_volume}
                
            elif action == "down":
                new_volume = max(current_volume - value, 0)
                self.volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
                return {"success": True, "volume": new_volume}
                
            elif action == "mute":
                self.volume.SetMute(True, None)
                return {"success": True, "muted": True}
                
            elif action == "unmute":
                self.volume.SetMute(False, None)
                return {"success": True, "muted": False}
                
            return {"error": "Acción de volumen no válida"}
            
        except Exception as e:
            return {"error": str(e)}

    async def _handle_brightness(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Control de brillo"""
        if not BRIGHTNESS_AVAILABLE:
            return {"error": "Control de brillo no disponible"}

        try:
            action = request.get("brightness_action")
            value = request.get("value", 0)

            current = sbc.get_brightness()[0]

            if action == "set":
                sbc.set_brightness(value)
                return {"success": True, "brightness": value}

            elif action == "up":
                new_value = min(current + value, 100)
                sbc.set_brightness(new_value)
                return {"success": True, "brightness": new_value}

            elif action == "down":
                new_value = max(current - value, 0)
                sbc.set_brightness(new_value)
                return {"success": True, "brightness": new_value}

            return {"error": "Acción de brillo no válida"}

        except Exception as e:
            return {"error": str(e)}

    async def _handle_window(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Control de ventanas"""
        try:
            action = request.get("window_action")
            title = request.get("title", "")
            
            def window_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if title.lower() in window_title.lower():
                        windows.append(hwnd)
                        
            windows = []
            win32gui.EnumWindows(window_callback, windows)
            
            if not windows:
                return {"error": "Ventana no encontrada"}
                
            hwnd = windows[0]
            
            if action == "minimize":
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                return {"success": True, "action": "minimized"}
                
            elif action == "maximize":
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                return {"success": True, "action": "maximized"}
                
            elif action == "restore":
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                return {"success": True, "action": "restored"}
                
            elif action == "close":
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                return {"success": True, "action": "closed"}
                
            return {"error": "Acción de ventana no válida"}
            
        except Exception as e:
            return {"error": str(e)}

    async def _handle_system(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Operaciones del sistema"""
        try:
            action = request.get("system_action")
            
            if action == "lock":
                ctypes.windll.user32.LockWorkStation()
                return {"success": True, "action": "locked"}
                
            elif action == "hibernate":
                os.system("shutdown /h")
                return {"success": True, "action": "hibernating"}
                
            elif action == "sleep":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return {"success": True, "action": "sleeping"}
                
            elif action == "shutdown":
                os.system("shutdown /s /t 60")  # 60 segundos de retraso
                return {"success": True, "action": "shutting_down", "delay": 60}
                
            elif action == "restart":
                os.system("shutdown /r /t 60")  # 60 segundos de retraso
                return {"success": True, "action": "restarting", "delay": 60}
                
            elif action == "cancel_shutdown":
                os.system("shutdown /a")
                return {"success": True, "action": "shutdown_cancelled"}
                
            return {"error": "Acción del sistema no válida"}
            
        except Exception as e:
            return {"error": str(e)}