import os
import gpt_cost
import sys
import argparse
import json
from tools import update
from tools import openai

pathHome = os.environ['HOME']
pathConfig = f"{pathHome}/.config/oe"

def loadConfig ():
    with open(f"{pathConfig}/config.json", 'r') as archivo:
        return json.load(archivo)

def getCommand (response):
    findCode = response.find('```')

    if findCode < 0:
        return response
    
    findCodeEnd = response.find('```', findCode + 1)
    bashReponse = response[findCode:findCodeEnd]
    cleanMD = bashReponse.replace('```','').replace('bash','')

    return cleanMD

def defineServers (servers):
    training_servers = ""

    for server in servers:
        training_servers += f"name:{server['name']}\nuser:{server['user']}\nurl: {server['url']}\n\n"

    return training_servers

def saveConfig (config, value):
    configFile = loadConfig ()
    configFile[config] = value

    with open(f"{pathConfig}/config.json", 'w') as archivo:
        json.dump(configFile, archivo)

parser = argparse.ArgumentParser()
parser.add_argument("message", nargs="+", help="Mensaje con la consulta")
parser.add_argument("-c", "--cost", help="Muestra el costo total hasta el momento", action="store_true")
parser.add_argument("-q", "--question", help="Pregunta a chat gpt")
parser.add_argument("-a", "--api", help="Cambiar open ia api key", action="store_true")
parser.add_argument("-u", "--update", help="Actualiza oe", action="store_true")

args = parser.parse_args()
commandMode = True

if args.cost:
    gpt_cost.showTotalCost()
    sys.exit(0)

if args.question:
    commandMode = False

if args.api:
    newKey = " ".join(args.message)
    saveConfig("open_api_key", newKey)
    print("OpenAI API Key has been updated.")
    sys.exit(0)

if args.update:
    update.update()
    sys.exit(0)

commandArg = " ".join(args.message)

config = loadConfig()

gptModel = config['gpt_model']
openApi = config['open_api_key']
linuxSo = config['so']
sshServers = config['ssh_servers']
servers = defineServers(sshServers)

if openApi == 'api':
    print(f"\033[31mNo se encuentra API key de openai.\033[0m")
    print(f"Puedes encontrarla en https://platform.openai.com/account/api-keys y agregarla con 'oe -a API_KEY'")
    sys.exit(0)

openai.api_key = openApi

if commandMode:
    content = f"Su tarea es dar comandos bash útiles que hagan lo que un usuario le pide. Solo debes proveer comandos para el sistema de zsh, no debes agregar ninguna explicacion o comentario y no se utilizaran bloques de codigo. Sistema operativo {linuxSo}. Si no sabes como responder la pregunta solo di 'Comando no encontrado'"
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

response = openai.create(
    model=gptModel,
    messages=messagesList
)

if 'error' in response:
    errorResponse = response['error']['message']
    print(f"GPT:\n\033[31m{errorResponse}\033[0m")
    sys.exit(0)

gpt_cost.addResponse(response)
gpt_cost.showCost(gptModel, True)

responseIA = response['choices'][0]['message']['content']

if not commandMode:
    print(f"Response:\n\033[;32m{responseIA}\033[0m")
    sys.exit(0)

commandIA = responseIA.replace('\n','')
filterCommandIA = getCommand(commandIA)

print(f"Command:\n\033[;36m{filterCommandIA}\033[0m [Y/n]")

ask = input()

if ask.lower() == "n":
    sys.exit(0)

os.system(filterCommandIA)