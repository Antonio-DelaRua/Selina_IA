def format_markdown(md_text):
    """
    Formatea texto Markdown eliminando líneas con '---', ajustando saltos de párrafo,
    eliminando etiquetas de lenguaje después de '```' (como 'bash') y manejando comillas internas.
    """
    lines = md_text.split("\n")
    formatted_lines = []
    skip_next_empty = False  # Para manejar saltos después de eliminar '---'

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Eliminar líneas que solo contienen '---'
        if stripped_line == "---":
            skip_next_empty = True  # Indicar que el próximo salto debe ser manejado
            continue

        # Eliminar líneas vacías si la anterior fue un '---' eliminado
        if skip_next_empty and not stripped_line:
            continue
        skip_next_empty = False

        # Eliminar la etiqueta de lenguaje después de ```
        if stripped_line.startswith("```") and len(stripped_line) > 3:
            line = "```"

        # Si la línea no está vacía y la anterior tampoco, añadir doble salto
        if i > 0 and stripped_line and lines[i-1].strip() and not stripped_line.startswith("```"):
            if formatted_lines and not formatted_lines[-1].endswith("\\n\\n"):
                formatted_lines[-1] = formatted_lines[-1].replace("\\n", "\\n\\n")

        # Manejar comillas internas
        if '"' in line:
            line = line.replace('"', "'")
        elif "'" in line:
            line = line.replace("'", '"')

        formatted_lines.append(f'"{line}\\n"')

    formatted_text = "\n".join(formatted_lines)

    with open("formatted_output.txt", "w", encoding="utf-8") as file:
        file.write(formatted_text)

    print("Archivo formateado generado: formatted_output.txt")


# Ejemplo de entrada Markdown (tu contenido)
md_content = """
## Introducción a Spring Boot

Spring Boot es un framework de Java basado en Spring que facilita la creación de aplicaciones empresariales y microservicios. Su objetivo principal es simplificar la configuración y puesta en marcha de aplicaciones Spring, eliminando la necesidad de una configuración extensa.

### Características principales:
- **Autoconfiguración**: Spring Boot configura automáticamente los componentes según las dependencias presentes en el proyecto.
- **Standalone**: No requiere un servidor de aplicaciones externo como Tomcat o Jetty.
- **Manejo de dependencias**: Usa `Spring Boot Starter` para gestionar dependencias fácilmente.
- **Spring Boot Actuator**: Proporciona monitoreo y métricas para aplicaciones en producción.

---

## Ejemplo de uso

A continuación, un ejemplo de una aplicación simple con Spring Boot que expone un servicio REST.

### 1. Agregar dependencias en `pom.xml`

```xml
<dependencies>
    <!-- Dependencia principal de Spring Boot -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    
    <!-- Plugin de Spring Boot -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### 2. Crear la clase principal `Application.java`

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 3. Crear un controlador REST `HelloController.java`

```java
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    public String sayHello() {
        return "¡Hola desde Spring Boot!";
    }
}
```

### 4. Ejecutar la aplicación

Para iniciar la aplicación, usa el siguiente comando en la terminal:

```sh
mvn spring-boot:run
```

### 5. Probar el servicio

Una vez en ejecución, puedes acceder a la API en:

```
http://localhost:8080/api/hello
```

Este endpoint responderá con:

```
¡Hola desde Spring Boot!
```

---

Este es un ejemplo básico de cómo se puede utilizar Spring Boot para crear una API REST. 🚀


"""


format_markdown(md_content)
