predefined_answers = {
    "hola": "Pulsa ESC para destruir el mundo",

    "el ale es moña" : "si 100 % confirmed",

    "entorno virtual": (
        "Para crear un entorno virtual en Python:\n"
        "```\npython -m venv env\n```\n\n"
        "Para activarlo en CMD:\n"
        "```\nenv\\Scripts\\activate\n```"
    ),
    
    "git": (
        "# Comandos básicos de Git\n\n"
        "Inicializa un nuevo repositorio de Git en el directorio actual.\n"
        "```\ngit init\n```\n\n"
        "Clona un repositorio existente en una nueva carpeta\n"
        "```\ngit clone <url-del-repositorio>\n```\n\n"
        "Muestra el estado actual del repositorio, incluyendo archivos modificados, añadidos y eliminados.\n"
        "```\ngit status\n```\n\n"
        "Añade archivos al área de preparación (staging area).\n"
        "```\ngit add <archivo>\n"
        "git add .\n```\n\n"
        "Guarda los cambios en el historial del repositorio con un mensaje descriptivo.\n"
        "```\ngit commit -m 'Mensaje del commit'\n```\n\n"
        "Actualiza el repositorio local con los cambios del repositorio remoto.\n"
        "```\ngit pull <nombre-remoto> <nombre-rama>\n```\n\n"
        "Cambia a otra rama o restaura archivos en el directorio de trabajo.\n"
        "```\ngit checkout <nombre-rama>  # Cambia a una rama existente\n"
        "git checkout -b <nombre-rama>  # Crea y cambia a una nueva rama\n```\n\n"
        "Fusiona cambios de una rama en la rama actual.\n"
        "```\ngit merge <nombre-rama>'\n```\n\n"
        "Muestra el historial de commits del repositorio.\n"
        "```\ngit log\n```\n\n"
        "Gestiona las conexiones a repositorios remotos.\n"
        "```\ngit remote add <nombre-remoto> <url>  # Añade un nuevo repositorio\n"
        "git remote -v                         # Muestra los repositorios\n```\n\n"
        "Descarga los objetos y referencias de otro repositorio.\n"
        "```\ngit fetch <nombre-remoto>\n```\n\n"
        "Deshace commits y cambia el estado del HEAD.\n"
        "```\ngit reset --hard <commit>  # Restablece el repositorio al estado de un commit específico\n```\n\n"
        "Aplica commits de una rama sobre otra, reescribiendo el historial.\n"
        "```\ngit rebase <nombre-rama>\n```\n\n"
        "Guarda temporalmente los cambios no confirmados para limpiar el directorio de trabajo.\n"
        "```\ngit stash\n"
        "git stash pop  # Restaura los cambios guardados\n```\n\n"
    ),

    "react": (
        "### Instalar Create React App\n"
        "Create React App es una herramienta oficial para crear aplicaciones React.\n"
        "```\nnpm install -g create-react-app\n```\n\n"
        "### Crear un nuevo proyecto React\n"
        "```\nnpx create-react-app my-app\n```\n"
        "\n"
        "```\nnpm start\n```\n"
    ),

    "RuXx": (
        "### SeLiNa IA - By:   *RuXx* \n\n"
        "```\n"
        "           .---.        .-----------\n"
        "          /     \\  __  /    ------\n"
        "         / /     \\(..)/    -----\n"
        "        //////   ' \\/ `   ---\n"
        "       //// / // :    : ---\n"
        "      // /   /  /`    '--\n"
        "     //          //..\\\\\n"
        "    /       ====UU====UU====\n"
        "                '//||\\\\`\n"
        "```\n"
    ),

    "angular": (
        "**Crear un nuevo proyecto**\n"
        " Crea un nuevo proyecto Angular con una estructura básica.\n"
        "```\nng new mi-proyecto\n```\n"
        "\n"
        "**Servir la aplicación**\n"
        "Levanta un servidor de desarrollo en http://localhost:4200/.\n"
        "```\nng serve\n```\n"
        "\n"
        "**Generar un componente**\n"
        "Crea un nuevo componente con sus archivos (.html, .ts, .scss, .spec.ts).\n"
        "```\nng generate component nombre-componente\n```\n"
        "\n"
        "**Generar un servicio**\n"
        "Crea un nuevo servicio para manejar lógica de negocio o peticiones HTTP.\n"
        "```\nng generate service nombre-servicio\n```\n"
        "\n"
        "**Generar un módulo**\n"
        "Crea un nuevo módulo para organizar mejor la aplicación.\n"
        "```\nng generate module nombre-modulo\n```\n"
        "\n"
        "**Construir la aplicación para producción**\n"
        "Compila y optimiza la aplicación para producción.\n"
        "```\nng build --configuration=production\n```\n"
        "\n"
        "**Agregar una nueva ruta (lazy loading)**\n"
        "Crea un módulo y lo enlaza con RouterModule para carga diferida.\n"
        "```\nng generate module nombre --route=nombre --module=app\n```\n"
        "\n"
        "**listar todos los comandos disponibles**\n"
        "```\nng help\n```\n"

    ),



    

    
}