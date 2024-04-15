import os
import json

pathHome = os.environ['HOME']
pathConfig = f"{pathHome}/.config/oe"

def loadConfig():
    with open(f"{pathConfig}/config.json", 'r') as archivo:
        return json.load(archivo)


def saveConfig(config, value):
    configFile = loadConfig()
    configFile[config] = value

    with open(f"{pathConfig}/config.json", 'w') as archivo:
        json.dump(configFile, archivo)


def getConfig():
    fileConfig = loadConfig()
    data = fileConfig

    if 'gpt_model' not in data:
        data['gpt_model'] = 'gpt-3.5-turbo'
    if 'open_api_key' not in data:
        data['open_api_key'] = ''
    if 'so' not in data:
        data['so'] = 'Archlinux'
    if 'ssh_servers' not in data:
        data['ssh_servers'] = []

    return data


SETTING = getConfig()
