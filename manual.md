# Manual de Usuario - Selina IA

## Introducción
Selina IA es un asistente virtual inteligente con interfaz gráfica y control por voz, diseñado para facilitar la interacción con tu computadora a través de comandos naturales.

## Funcionalidades Principales

### 🎤 Control por Voz
El asistente puede ser activado para escuchar comandos de voz. Di "Selina" o activa el botón del micrófono en la interfaz.

### 💬 Interfaz de Chat
- **Chat dinámico**: El cuadro de entrada se expande automáticamente según el contenido
- **Respuestas formateadas**: Soporte para texto enriquecido, código, listas y más
- **Historial**: Mantén conversaciones continuas con el asistente

### 📅 Calendario y Tareas
- Gestión completa de tareas por voz
- Consultar tareas pendientes/completadas
- Agregar nuevas tareas
- Marcar tareas como completadas

## Comandos de Voz Disponibles

### 🗂️ Gestión de Carpetas
Puedes abrir cualquier carpeta del sistema diciendo:

**Carpetas del usuario:**
- "abre carpeta documentos" → Abre Documentos
- "abre carpeta descargas" → Abre Descargas
- "abre carpeta imágenes" → Abre Imágenes
- "abre carpeta vídeos" → Abre Vídeos
- "abre carpeta música" → Abre Música
- "abre carpeta escritorio" → Abre Escritorio

**Carpetas del sistema:**
- "abre carpeta raíz" → Abre C:\
- "abre carpeta sistema" → Abre C:\Windows\System32
- "abre carpeta temp" → Abre carpeta temporal
- "abre carpeta programas" → Abre Program Files
- "abre papelera" → Abre Papelera de reciclaje

**Carpetas personalizadas:**
- "abre carpeta [nombre]" → Intenta abrir cualquier carpeta por nombre

### 🖥️ Aplicaciones y Programas
Puedes abrir aplicaciones diciendo "abre" seguido del nombre:

**Navegadores:**
- "abre chrome" → Google Chrome
- "abre firefox" → Mozilla Firefox
- "abre edge" → Microsoft Edge
- "abre navegador" → Chrome por defecto

**Herramientas de desarrollo:**
- "abre vscode" → Visual Studio Code
- "abre código" → Visual Studio Code
- "abre terminal" → Command Prompt
- "abre powershell" → PowerShell
- "abre visual studio" → Visual Studio
- "abre android studio" → Android Studio
- "abre eclipse" → Eclipse IDE
- "abre sublime" → Sublime Text
- "abre notepad++" → Notepad++

**Aplicaciones de Microsoft Office:**
- "abre word" → Microsoft Word
- "abre excel" → Microsoft Excel
- "abre powerpoint" → Microsoft PowerPoint
- "abre outlook" → Microsoft Outlook

**Multimedia:**
- "abre spotify" → Spotify
- "abre vlc" → VLC Media Player
- "abre fotos" → Aplicación Fotos de Windows
- "abre paint" → Paint
- "abre paint 3d" → Paint 3D

**Herramientas del sistema:**
- "abre configuración" → Configuración de Windows
- "abre panel" → Panel de control
- "abre calculadora" → Calculadora
- "abre explorador" → Explorador de archivos
- "abre mi pc" → Este equipo
- "abre tienda" → Microsoft Store

**Aplicaciones comunes:**
- "abre steam" → Steam
- "abre discord" → Discord
- "abre zoom" → Zoom
- "abre teams" → Microsoft Teams
- "abre skype" → Skype
- "abre whatsapp" → WhatsApp
- "abre telegram" → Telegram

### 🎵 Entretenimiento
- "reproduce [canción]" → Busca y reproduce en YouTube
- "alarma" → Configura una alarma (te pedirá la hora)
- "detener" → Detiene la alarma activa

### 🔍 Búsqueda e Información
- "busca [tema]" → Busca información en Wikipedia

### ✍️ Productividad
- "escribe" → Toma nota por voz y la guarda en nota.txt
- "tarea agregar [título]" → Agrega una nueva tarea
- "qué tareas tengo hoy" → Consulta tareas del día
- "marcar tarea [título] como completada" → Completa una tarea

### 🔧 Sistema
- "sube el volumen" → Aumenta el volumen del sistema
- "baja volumen" → Reduce el volumen del sistema
- "mute" → Silencia el audio
- "apagar" → Apaga el sistema (pide confirmación)
- "reiniciar" → Reinicia el sistema (pide confirmación)

### 🌐 Web y Archivos
- "abre [sitio web]" → Abre sitio web conocido (ej: "abre google")
- "cerrar web" → Cierra Chrome
- "archivo [nombre]" → Abre archivo conocido

## Cómo Usar el Asistente

### Activación por Voz
1. Haz doble clic en el muñeco de Selina
2. Presiona el botón del micrófono 🎤
3. Di tu comando claramente
4. El asistente procesará y ejecutará la acción

### Interfaz Gráfica
1. Haz doble clic en el muñeco para abrir el chat
2. Escribe tu mensaje en el cuadro de entrada
3. Presiona Enter o el botón "Enviar"
4. El asistente responderá en el área superior

### Atajos de Teclado
- **Ctrl+Q**: Cierra la aplicación
- **Ctrl+C**: Abre el calendario

## Consejos de Uso

### Para Mejor Reconocimiento de Voz
- Habla claro y a un volumen normal
- Evita ruido de fondo
- Pronuncia correctamente los nombres de aplicaciones
- Si no reconoce, intenta decirlo de otra manera

### Carpetas y Aplicaciones
- Para carpetas: usa "abre carpeta [nombre]"
- Para apps: usa "abre [nombre de app]"
- Si una app no está en la lista, intenta decir exactamente su nombre

### Tareas y Calendario
- Di "qué tareas tengo" para ver todas las tareas
- Especifica "hoy" o "mañana" para fechas concretas
- Para agregar: "agregar tarea [descripción] para [fecha]"

## Solución de Problemas

### El Asistente no Responde
- Verifica que el micrófono esté activado
- Asegúrate de que no haya otras aplicaciones usando el audio
- Reinicia el asistente si es necesario

### Aplicaciones no se Abren
- Verifica que la aplicación esté instalada
- Comprueba que esté en el PATH del sistema
- Para apps personalizadas, usa la ruta completa si es necesario

### Carpetas no se Encuentran
- Asegúrate de que la carpeta existe
- Usa rutas absolutas para carpetas personalizadas
- Verifica los permisos de acceso

## Personalización
El sistema está diseñado para ser extensible. Puedes agregar nuevos comandos modificando el archivo `commands.py` en la carpeta `voice/`.

## Soporte
Si encuentras problemas o necesitas ayuda, consulta los archivos de configuración en `selina_ia/config/settings.py` para ajustar parámetros como umbrales de voz, rutas de archivos, etc.