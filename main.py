import os
import sys
import argparse
import json
from tools import update
from tools import openai
from tools import gpt_cost

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
parser.add_argument("-t", "--translation", help="Traduce texto", action="store_true")
parser.add_argument("-a", "--api", help="Cambiar open ia api key", action="store_true")
parser.add_argument("-u", "--update", help="Actualiza oe", action="store_true")

args = parser.parse_args()
commandMode = 'command'

if args.cost:
    gpt_cost.showTotalCost()
    sys.exit(0)

if args.question:
    commandMode = 'question'

if args.translation:
    commandMode = 'translation'

if args.api:
    newKey = " ".join(args.message)
    saveConfig("open_api_key", newKey)
    print("OpenAI API Key ha sido actualizada")
    sys.exit(0)

if args.update:
    update.update()
    sys.exit(0)

commandArg = " ".join(args.message)

config = loadConfig()

if 'OPENAI_API_KEY' in os.environ:
    openApi = os.environ['OPENAI_API_KEY']
else:
    openApi = config['open_api_key']

gptModel = config['gpt_model']
linuxSo = config['so']
sshServers = config['ssh_servers']
servers = defineServers(sshServers)

if openApi == 'OPENAI_API_KEY':
    print(f"\033[31mNo se encuentra API key de openai.\033[0m")
    print(f"Puedes encontrarla en https://platform.openai.com/account/api-keys y agregarla con 'oe -a API_KEY'")
    sys.exit(0)

openai.api_key = openApi

content = ""

if commandMode == 'command':
    content = f"You are a Linux terminal assistant.You must provide useful commands for the ZSH system in the Linux operating system.Your answers should only be the commands without descriptions, explanations, or code.If there is no answer, return 'Command not found'."
elif commandMode == 'question':
    content = "Your task is to answer as briefly as possible the questions you are asked."

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

if commandMode == 'translation':
    prompt = f"""
    Translate the following text. \ 
    Between English and Spanish: \ 
    ```{commandArg}```
    Do not add any extra comments, only the one translation.
    """

    messagesList = [{"role": "user", "content": prompt}]

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

if commandMode != 'command':
    print(f"Response:\n\033[;32m{responseIA}\033[0m")
    sys.exit(0)

commandIA = responseIA.replace('\n','')
filterCommandIA = getCommand(commandIA)
superUser = ""

print(f"Command:\n\033[;36m{filterCommandIA}\033[0m [Y/n]")

ask = input()

if ask.lower() == "c":
    os.system(f"echo \"{filterCommandIA}\" | xclip -sel clip")
    sys.exit(0)

if ask.lower() == "s":
    superUser = "sudo "

if ask.lower() == "n":
    sys.exit(0)

os.system(f"{superUser}{filterCommandIA}")