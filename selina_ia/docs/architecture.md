# Arquitectura de Selina IA

## 🏗️ Diseño General

Selina IA sigue una arquitectura modular y escalable, organizada en paquetes Python con responsabilidades claras.

## 📦 Estructura de Paquetes

### `config/`
**Responsabilidad**: Configuraciones centralizadas del sistema.

- `settings.py`: Todas las configuraciones (BD, IA, voz, UI, etc.)
- Beneficio: Un solo lugar para cambiar configuraciones

### `core/`
**Responsabilidad**: Lógica de negocio central e IA.

- `agent.py`: Agente principal con sistema MCP
- `database.py`: Gestión de BD SQLAlchemy
- `embeddings.py`: Gestión de FAISS y búsqueda semántica

### `ui/`
**Responsabilidad**: Interfaz de usuario y presentaciones.

- `gui.py`: Ventana principal y lógica de interfaz
- `animations.py`: Animaciones del muñeco
- `images/`: Recursos gráficos

### `voice/`
**Responsabilidad**: Procesamiento de voz y comandos.

- `commands.py`: Lógica de comandos de voz
- `bot.py`: Interfaz simplificada (compatibilidad)

### `utils/`
**Responsabilidad**: Utilidades auxiliares.

- `whatsapp.py`: Funciones WhatsApp
- `info.py`: Información de la compañía

### `data/`
**Responsabilidad**: Datos persistentes.

- `my_database.sqlite`: Base de datos principal
- `vector_index.faiss`: Índice de embeddings
- `vector_metadata.json`: Metadata de vectores

## 🔄 Flujo de Datos

### Consulta de Usuario
```
Usuario → UI (gui.py) → Agent (agent.py) → MCP Tools → Respuesta
```

### Comando de Voz
```
Micrófono → Voice (commands.py) → Agent → Respuesta → TTS
```

### Búsqueda Inteligente
```
Query → Embeddings (embeddings.py) → FAISS → Database → Respuesta
```

## 🛠️ Patrón MCP (Model Context Protocol)

### Herramientas Disponibles

#### Filesystem Tools
- `read_file`: Leer archivos de forma segura
- `list_directory`: Listar contenidos de directorio
- `search_files`: Buscar archivos por nombre
- `file_info`: Información detallada de archivos
- `move_file`: Mover/renombrar archivos

#### Database Tools
- `code_analysis`: Análisis de código Python
- `explain_concept`: Explicar conceptos de programación
- `debug_code`: Depuración de código
- `search_knowledge`: Búsqueda en base de conocimientos

### Priorización de Respuestas
1. **Filesystem**: Herramientas rápidas (lectura, listado)
2. **Database**: Búsqueda en conocimientos locales
3. **LLM**: Generación con IA (último recurso)

## 💾 Gestión de Base de Datos

### Tablas Principales

#### `history`
- Historial de conversaciones
- Campos: id, prompt, response, embedding, date

#### `python_db`
- Base de conocimientos Python
- Campos: id, prompt, response, embedding, date

### Funcionalidades
- **Embeddings**: Vectores para búsqueda semántica
- **FAISS Index**: Búsqueda rápida de similitud
- **Auto-guardado**: Respuestas nuevas se almacenan automáticamente

## 🎨 Interfaz de Usuario

### Componentes
- **Tkinter Canvas**: Área de trabajo full-screen
- **Label Animado**: Muñeco con sprites
- **Toplevel Window**: Ventana de chat modal
- **Text Widgets**: Área de entrada/salida con formato

### Estados
- `window_abierta`: Control de ventana modal
- `animacion_id`: Control de animaciones activas
- `estado_asistente`: Estado del sistema de voz

## 🔊 Sistema de Voz

### Reconocimiento
- **Google Speech Recognition**: API gratuita
- **Configuración española**: `language="es-ES"`
- **Umbrales dinámicos**: Adaptación automática

### Síntesis
- **pyttsx3**: Motor TTS local
- **Bloqueo inteligente**: Evita conflictos de audio

### Comandos
- **Diccionario extensible**: Fácil agregar nuevos comandos
- **Confirmaciones**: Para acciones críticas (apagar, etc.)
- **Estados**: Manejo de conversaciones multi-paso

## ⚙️ Configuración Centralizada

### Beneficios
- **Un solo archivo**: `config/settings.py`
- **Variables de entorno**: Fácil deployment
- **Validación**: Paths y valores verificados
- **Documentación**: Comentarios explicativos

### Categorías
- **Rutas**: BASE_DIR, PROJECT_ROOT, IMAGES_DIR
- **BD**: DATABASE_URL, tablas
- **IA**: LLM_MODEL, EMBEDDING_MODEL
- **Voz**: Parámetros de reconocimiento
- **UI**: Dimensiones, títulos
- **Comandos**: Diccionarios de sitios, archivos, contactos

## 🔧 Manejo de Errores

### Estrategias
- **Try/Except**: Captura específica por módulo
- **Logging**: Registro centralizado de eventos
- **Fallbacks**: Respuestas alternativas cuando falla algo
- **Timeouts**: Prevención de hangs en operaciones lentas

### Niveles de Logging
- **DEBUG**: Información detallada para desarrollo
- **INFO**: Eventos normales del sistema
- **WARNING**: Situaciones que requieren atención
- **ERROR**: Errores que afectan funcionalidad
- **CRITICAL**: Errores críticos del sistema

## 🚀 Escalabilidad

### Agregar Nueva Funcionalidad
1. **UI**: Extender `ui/gui.py`
2. **Voz**: Agregar comando en `voice/commands.py`
3. **IA**: Nueva herramienta MCP en `core/agent.py`
4. **Config**: Nuevo parámetro en `config/settings.py`

### Módulos Independientes
- Cada paquete puede desarrollarse/testearse por separado
- Interfaces claras entre módulos
- Dependencias mínimas entre paquetes

### Base de Datos Extensible
- Nuevas tablas fáciles de agregar
- Embeddings para cualquier tipo de contenido
- Consultas optimizadas con índices

## 🔒 Seguridad

### Filesystem
- **Validación de paths**: Solo rutas permitidas
- **Límites de tamaño**: Prevención de ataques DoS
- **Permisos**: Verificación antes de operaciones

### Base de Datos
- **SQL Injection**: Parámetros preparados
- **Validación**: Datos sanitizados antes de guardar
- **Backups**: Estrategia de respaldo de datos

### Red
- **Timeouts**: Prevención de ataques de denegación
- **Validación**: URLs y parámetros verificados
- **Logging**: Auditoría de operaciones

## 📊 Métricas y Monitoreo

### Logs
- **Archivo**: Rotación automática
- **Formato**: Timestamp, nivel, módulo, mensaje
- **Consola**: Output en desarrollo

### Rendimiento
- **Timeouts**: Prevención de operaciones lentas
- **Pooling**: Conexiones eficientes a BD
- **Lazy Loading**: Carga bajo demanda

### Salud del Sistema
- **Verificaciones**: Estado de componentes críticos
- **Alertas**: Notificación de problemas
- **Recuperación**: Reinicio automático de servicios