<div id="header" align="center">

<img src="/img/muneco.png" width="300" />

<h1 align="center">👋 SeliNa Python</h1>

<h3 aling="center">Un chat gpt dentro de un avatar3d con animaciones y mucho más.</h3>
<br>

</div>

---
<div align="center">
<h3>🔨 👦 About Me :</h3>
<br>

 💻 RuXx .

</div>


<div align="center">
<h3>🔨 Languages and Tools:</h3>
<br>
<div>
<img src="https://upload.wikimedia.org/wikipedia/commons/c/cf/Angular_full_color_logo.svg" title="Angular" alt="Angular" width="45" height="45"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/html5/html5-original.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/css3/css3-plain-wordmark.svg" title="CSS3" alt="CSS" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/javascript/javascript-original.svg" title="Javascript" alt="Javascript" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/sass/sass-original.svg" title="SASS" alt="Sass" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/mysql/mysql-original-wordmark.svg" title="CSS3" alt="CSS" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/git/git-original-wordmark.svg" title="GIT" alt="Git" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="PYTHON" alt="python" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original-wordmark.svg" title="docker" alt="docker" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/firebase/firebase-plain-wordmark.svg" title="firebase" alt="firebase" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/java/java-original-wordmark.svg" title="java" alt="java" width="40" height="40"/>&nbsp;
</div>
</div>



## CMD
ctrl + q  ------> cerrar aplicación
kiv para moviles y tablet ( tactil )

## PALABRAS CLAVE


# predefinidos alias_dic
- hola
- entorno virtual
- git 
- react
- ruxx
- angular

 # bd_python
- que es python y para que se utiliza?
- como instalar python en windows?
- fundamentos de python
- tipos de datos basicos
- enteros
- int
- float
- numeros complejos
- complex
- cadena de texto
- str
- boolean
- listas
- set
- diccionarios
- operadores aritmeticos
- operadores logicos
- operadores de comparacion
- operadores de asignacion
- estructuras de control
- condicionales
- if
- for
- while
- continue
- pass
- break
- funcion python
- palindromo
- calculadora
- manejo de excepciones
- multiples excepciones
- excepciones anidadas
- finally
- else
- POO
- herencia
- polimorfismo
- abstraccion
- django
- flask
- spring boot
- modulo
- iterador
- decoradores
- context managers
- metaclase
- GIL
- gestion de memoria
- protocolo
- pytest
- unittest
- debugging
- logging
- flake8
- black
- Mypy
- isort
- gestor de dependencias
- packaging
- documentacion
- fastAPI
- SQLAlchemy
- alembic
- OAuth2
- JWT
- graphQL
- postgresql
- mysql
- mongodb
- redis
- conexiones asincronas
- asyncpg
- aiomysql
- caching
- patrones de diseño
- singleton
- factory
- Observer
- strategy
- solid
- microservicios



Arquitectura limpia (Clean Architecture): Separación de capas (dominio, aplicación, infraestructura).

Microservicios vs Monolito: Cuándo elegir cada uno.

Event-Driven Architecture: Uso de brokers como RabbitMQ, Kafka.

CQRS y Event Sourcing: Diseño para sistemas complejos.

7. DevOps y Deployment
Contenedores: Docker, Docker Compose.

Cloud: AWS (EC2, S3, Lambda), GCP, Azure.

CI/CD: GitHub Actions, GitLab CI, Jenkins.

Servidores web: Nginx, Gunicorn, uWSGI.

Monitorización: Prometheus, Grafana, Sentry.

Infra as Code: Terraform, CloudFormation.

8. Seguridad
OWASP Top 10: Prevención de SQLi, XSS, CSRF, etc.

Hardening: Configuración segura de servidores y aplicaciones.

Criptografía: Uso de bcrypt, cryptography.

Auditorías: Herramientas como Bandit para análisis estático.

9. Habilidades Blandas
Trabajo en equipo: Uso de metodologías ágiles (Scrum, Kanban).

Mentoría: Guiar a desarrolladores junior.

Comunicación: Explicar ideas técnicas a no técnicos.

Gestión de tiempo: Priorización de tareas complejas.

10. Extra (Dependiendo del enfoque)
Data Science: Pandas, NumPy, Matplotlib.

Machine Learning: Scikit-learn, TensorFlow, PyTorch.

Automatización: Scripts con click o argparse.

Web Scraping: BeautifulSoup, Scrapy, Selenium.



        def insert_code_block(self, text):
            self.text_widget.insert(tk.END, "\n", "code")
            start_index = self.text_widget.index(tk.INSERT)  # Obtener el índice actual
            self.text_widget.insert(tk.END, text, "code")
            end_index = self.text_widget.index(tk.INSERT)  # Obtener el índice después de insertar el texto

            # Crear un Frame para el botón, alineado a la izquierda
            button_frame = tk.Frame(self.text_widget, bg="#f4f4f4")
            button_frame.pack(anchor='w', padx=30, pady=(0, 10))  # Alineado a la izquierda

            # Crear el botón "Copiar código"
            copy_button = tk.Button(button_frame, text="Copiar código",
                                    command=lambda t=text: copy_to_clipboard(t),  # Pasar el texto como argumento
                                    bg='blue', fg='white', font=("Courier", 10, "bold"))
            copy_button.pack(side='left')  # Empaquetar el botón dentro del frame

            # Crear un widget de ventana para el frame del botón
            self.text_widget.window_create(end_index, window=button_frame)
            self.text_widget.insert(end_index, "\n")