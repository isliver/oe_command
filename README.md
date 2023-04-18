# OE: OpenAI ChatBot con GPT-3
Este código contiene un Chatbot que utiliza la API de OpenAI y el modelo de GPT-3 para responder preguntas y dar comandos útiles para el sistema operativo Linux.

## Instalación

Para instalar la aplicación, sigue los siguientes pasos:

1. Abre una terminal o línea de comandos y navega al directorio donde se encuentra el archivo `install.sh`.

2. Ejecuta el siguiente comando para otorgar permisos de ejecución al archivo:

```bash
chmod +x install.sh
```

3. Ejecuta el archivo install.sh utilizando el siguiente comando:

```bash
./install.sh
```

Este comando instalará las dependencias requeridas y copiará los archivos necesarios al directorio de instalación.

Una vez completados estos pasos, la aplicación debería estar instalada y lista para su uso.

o bien con el script:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/isliver/oe_command/main/install.sh)"
```
*se tiene que tener instalado curl*

## Funcionalidades

Carga la configuración del archivo config.json ubicado en el directorio .config/oe en la carpeta HOME del usuario.
Lee argumentos de la línea de comandos para ejecutar diferentes funcionalidades:
Mensaje para la consulta

```bash
-c, --cost: Muestra el costo total de las consultas realizadas hasta el momento.
-q, --question: Realiza una pregunta al Chatbot en lugar de dar un comando útil.
-t, --translation: utiliza el modelo de lenguaje GPT para traducir el texto.
-a, --api: cambia la clave API de OpenAI.
-u, --update: actualiza el programa.
```

Utiliza la API de OpenAI para obtener una respuesta al mensaje de consulta.
Si la respuesta contiene un bloque de código, extrae el comando Bash y lo muestra para confirmar su ejecución.
Ejecuta el comando Bash si se confirma la ejecución.

## Uso

Ejecute el archivo Python desde la línea de comandos pasando como argumento el mensaje de la consulta. Por ejemplo:

```bash
oe Como puedo ver los archivos ocultos en Linux
Command:
ls -a [Y/n]
```

Seleccione la opción correspondiente para continuar: presione Enter para ejecutar el comando, "n" para cancelar, "s" para ejecutar el comando con "sudo", o "c" para copiar el comando en el portapapeles.

Para realizar consultas breves a chat gpt

```
oe -q Cuál es la capital de Francia
Response:
París.
```

Para realizar una traduccion

```
oe -t hola mundo                 
Response:
hello world
```

Para ver el costo total de las consultas realizadas hasta el momento, ejecute:

```
oe -c today
```

## Configuración
El archivo de configuración config.json debe estar ubicado en la carpeta .config/oe en la carpeta HOME del usuario. El archivo debe contener las siguientes propiedades:

* gpt_model: Modelo de lenguaje OPEN AI (default: gpt-3.5-turbo).
* open_api_key: Clave de la API de OpenAI (default: env OPENAI_API_KEY).
* so: Sistema operativo utilizado (actualmente solo soporta Linux) (default: Archlinux).
* ssh_servers: Lista de objetos con información de los servidores SSH que se pueden utilizar en las respuestas del Chatbot.

## Otros

Si deseas utilizar la opción de copiar la respuesta al portapapeles en una terminal que no tiene instalado X11, necesitarás instalar el paquete "xclip". 