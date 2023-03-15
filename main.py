import os
import openai
import gpt_cost
import sys
import argparse

def getCommand (response):
    findCode = response.find('```')

    if findCode < 0:
        return response
    
    findCodeEnd = response.find('```', findCode + 1)
    bashReponse = response[findCode:findCodeEnd]
    cleanMD = bashReponse.replace('```','').replace('bash','')

    return cleanMD

def defineServers ():
    servers = [
        {
            "name": "Continuum",
            "user": "isliver",
            "url": "soundanalytics.cl"
        }
    ]

    training_servers = ""

    for server in servers:
        training_servers += f"name:{server['name']}\nuser:{server['user']}\nurl: {server['url']}\n\n"

    return training_servers

parser = argparse.ArgumentParser()
parser.add_argument("message", nargs="+", help="Mensaje con la consulta")
parser.add_argument("-c", "--cost", help="Muestra el costo total hasta el momento", action="store_true")
parser.add_argument("-q", "--question", help="Pregunta a chat gpt")

args = parser.parse_args()
commandMode = True

if args.cost:
    gpt_cost.showTotalCost()
    sys.exit(0)

if args.question:
    commandMode = False

commandArg = " ".join(args.message)

openai.api_key = "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"

servers = defineServers()
LINUX_SO = "Archlinux"

if commandMode:
    content = f"Su tarea es dar comandos bash útiles que hagan lo que un usuario le pide. Solo debes proveer comandos para el sistema de zsh, no debes agregar ninguna explicacion o comentario y no se utilizaran bloques de codigo. Sistema operativo {LINUX_SO}. servidores: {servers}. Si no sabes como responder la pregunta solo di 'Comando no encontrado'"
else:
    content = "Tu tarea es responder lo mas breve posible las preguntas que se te haga."

messagesList = [
    {
        "role": "system",
        "content": content
    }
]

userMessage = {
    "role": "user",
    "content": commandArg
}

messagesList.append(userMessage)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messagesList
)

gpt_cost.addResponse(response)
gpt_cost.showCost("gpt-3.5-turbo", True)

responseIA = response['choices'][0]['message']
commandIA = responseIA['content'].replace('\n','')

filterCommandIA = getCommand(commandIA)

if not commandMode:
    print(f"Response:\n\033[;32m{filterCommandIA}\033[0m")
    sys.exit(0)

print(f"Command:\n\033[;36m{filterCommandIA}\033[0m [Y/n]")

ask = input()

if ask.lower() == "n":
    sys.exit(0)

os.system(filterCommandIA)