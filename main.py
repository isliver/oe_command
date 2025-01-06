import os
import sys
import argparse
import json
from tools import update
from tools import openai
from tools import gpt_cost
from tools import oe_promsts
from tools import config
from constant import prices

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

def getGPTResult (gptModel, messagesList):
    response = openai.create(
        model=gptModel,
        messages=messagesList
    )

    if 'error' in response:
        errorResponse = response['error']['message']
        print(f"GPT:\n\033[31m{errorResponse}\033[0m")
        sys.exit(0)

    responseIA = response['choices'][0]['message']['content']

    if commandMode != 'command':
        print(f"Response:\n\033[;32m{responseIA}\033[0m")
        sys.exit(0)

    commandIA = responseIA.replace('\n', '')
    filterCommandIA = getCommand(commandIA)
    superUser = ""

    if filterCommandIA == 'Command not found':
        return 'fail'

    if verbose > 0 :
        print(filterCommandIA)
        return 'done'

    if 'sudo' in filterCommandIA:
        filterCommandIA = filterCommandIA.replace('sudo', '')

    print(f"Command:\n\033[;36m{filterCommandIA}\033[0m [Y/n]")

    ask = input()

    if ask.lower() == "c":
        os.system(f"echo \"{filterCommandIA}\" | xclip -sel clip")
        sys.exit(0)

    if ask.lower() == "s":
        superUser = "sudo "

    if ask.lower() == "n":
        sys.exit(0)

    if ask.lower() == "r":
        return 'retry'

    os.system(f"{superUser}{filterCommandIA}")

    return 'done'

parser = argparse.ArgumentParser()
parser.add_argument("message", nargs="+", help="Mensaje con la consulta")
parser.add_argument("-c", "--cost", help="Muestra el costo total hasta el momento", action="store_true")
parser.add_argument("-q", "--question", help="Pregunta a chat gpt")
parser.add_argument("-g", "--grammar", help="Revisa la gramatica del texto", action="store_true")
parser.add_argument("-t", "--translation", help="Traduce texto", action="store_true")
parser.add_argument("-a", "--api", help="Cambiar open ia api key", action="store_true")
parser.add_argument("-u", "--update", help="Actualiza oe", action="store_true")
parser.add_argument("-o", "--only", help="Retorna solo el comando", action="store_true")

args = parser.parse_args()
commandMode = 'command'
verbose = 0

if args.cost:
    gpt_cost.showCost()
    sys.exit(0)

if args.question:
    commandMode = 'question'

if args.grammar:
    commandMode = 'grammar'

if args.translation:
    commandMode = 'translation'

if args.only:
    verbose = 1

if args.api:
    newKey = " ".join(args.message)
    config.saveConfig("open_api_key", newKey)
    print("OpenAI API Key ha sido actualizada")
    sys.exit(0)

if args.update:
    update.update()
    sys.exit(0)

commandArg = " ".join(args.message)

gptModel = config.SETTING['gpt_model']

if gptModel not in prices.prices:
    gptModel = 'gpt-4o-mini'

openApi = config.SETTING['open_api_key']

if openApi == 'api':
    print(f"\033[31mNo se encuentra API key de openai.\033[0m")
    print(f"Puedes encontrarla en https://platform.openai.com/account/api-keys y agregarla con 'oe -a API_KEY'")
    sys.exit(0)

openai.api_key = openApi

messagesList = oe_promsts.getMessagesList(commandMode, commandArg)
result = getGPTResult(gptModel, messagesList)

if result == 'done':
    sys.exit(0)

retry = True

while retry:
    result = getGPTResult('gpt-4', messagesList)
    
    if result != 'retry':
        print('Comando no encontrado')
        retry = False
