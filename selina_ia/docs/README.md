# Selina IA - Asistente Virtual Inteligente

Un asistente virtual con interfaz gráfica, reconocimiento de voz, base de datos local y capacidades de IA avanzadas.

## 🚀 Características

- **Interfaz Gráfica**: Interfaz Tkinter con muñeco animado
- **Reconocimiento de Voz**: Control por voz en español
- **Base de Datos Local**: SQLite con embeddings FAISS
- **IA Local**: Modelo Ollama para respuestas inteligentes
- **Herramientas MCP**: Sistema de herramientas modulares
- **Filesystem**: Operaciones de archivos seguras

## 📁 Estructura del Proyecto

```
selina_ia/
├── config/           # Configuraciones centralizadas
│   └── settings.py   # Todas las configuraciones del sistema
├── core/            # Núcleo del sistema
│   ├── agent.py     # Agente principal con MCP
│   ├── database.py  # Gestión de BD (SQLAlchemy)
│   └── embeddings.py # Gestión de embeddings FAISS
├── ui/              # Interfaz de usuario
│   ├── gui.py       # Interfaz gráfica principal
│   ├── animations.py # Animaciones del muñeco
│   └── images/      # Recursos gráficos
├── voice/           # Sistema de voz
│   ├── bot.py       # Bot de voz (compatibilidad)
│   └── commands.py  # Procesamiento de comandos
├── utils/           # Utilidades
│   ├── whatsapp.py  # Utilidades WhatsApp
│   └── info.py      # Información de la compañía
├── data/            # Datos persistentes
│   ├── my_database.sqlite
│   ├── vector_index.faiss
│   └── vector_metadata.json
└── main.py          # Punto de entrada
```

## 🛠️ Instalación

1. **Requisitos previos**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Instalar Ollama**:
   ```bash
   # Descargar e instalar Ollama desde https://ollama.ai
   ollama pull qwen2.5:0.5b
   ```

3. **Ejecutar**:
   ```bash
   cd selina_ia
   python main.py
   ```

## 🎯 Uso

### Interfaz Gráfica
- **Doble clic**: Abre ventana de chat
- **Arrastrar**: Mueve el muñeco
- **Clic derecho**: Menú de animaciones

### Comandos de Voz
- "abre google" - Abre sitio web
- "alarma a las 8:30" - Configura alarma
- "reproduce música" - Reproduce en YouTube
- "apagar" - Apaga el sistema (con confirmación)

### Comandos MCP
- `/mcp help` - Lista herramientas disponibles
- `/mcp {"tool": "read_file", "arguments": {"path": "archivo.py"}}`
- `/mcp {"tool": "explain_concept", "arguments": {"concept": "listas"}}`

## 🔧 Configuración

Todas las configuraciones están centralizadas en `config/settings.py`:

- **Modelo IA**: `LLM_MODEL = "qwen2.5:0.5b"`
- **Base de datos**: `DATABASE_URL = "sqlite:///data/my_database.sqlite"`
- **Embeddings**: `EMBEDDING_MODEL = "all-MiniLM-L6-v2"`
- **Voz**: Parámetros de reconocimiento de voz
- **Sitios**: Diccionarios de comandos y URLs

## 🏗️ Arquitectura

### Separación de Responsabilidades
- **config/**: Configuraciones centralizadas
- **core/**: Lógica de negocio e IA
- **ui/**: Interfaz de usuario
- **voice/**: Procesamiento de voz
- **utils/**: Utilidades auxiliares
- **data/**: Datos persistentes

### Patrón MCP (Model Context Protocol)
- **Filesystem Tools**: Operaciones seguras de archivos
- **Database Tools**: Consultas inteligentes a la BD
- **LLM Tools**: Generación de respuestas con IA

## 📊 Base de Datos

### Tablas
- **history**: Historial de conversaciones
- **python_db**: Base de conocimientos Python
- **Embeddings**: Vectores FAISS para búsqueda semántica

### Funcionalidades
- Búsqueda semántica con embeddings
- Almacenamiento automático de respuestas
- Consultas inteligentes por contexto

## 🔍 Desarrollo

### Agregar Nueva Funcionalidad
1. **UI**: Añadir en `ui/gui.py`
2. **Voz**: Añadir comando en `voice/commands.py`
3. **IA**: Extender herramientas en `core/agent.py`
4. **Config**: Actualizar `config/settings.py`

### Testing
```bash
# Ejecutar tests
python -m pytest tests/

# Verificar imports
python -c "import selina_ia; print('✅ Imports OK')"
```

## 📝 Notas de Desarrollo

- **Logging**: Configurado en `config/settings.py`
- **Errores**: Manejo centralizado con logging
- **Compatibilidad**: Mantiene funcionalidad original
- **Escalabilidad**: Arquitectura modular para crecimiento

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autor

**NoBt** - Desarrollo de software e IA