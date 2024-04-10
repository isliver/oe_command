import os
import json
from datetime import datetime
from constant import prices

pathHome = os.environ['HOME']
pathLogCost = f"{pathHome}/.config/oe"
fileLogCost = f"{pathHome}/.config/oe/log_cost.json"

def saveCost (model, cost):
    if not os.path.exists(pathLogCost):
        os.makedirs(pathLogCost)

    logData = {}

    if os.path.exists(fileLogCost):
        with open(fileLogCost, 'r') as file:
            logData = json.load(file)

    now = datetime.utcnow()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    cost["ts"] = timestamp
    
    if model not in logData:
        logData[model] = []

    logData[model].append(cost)

    with open(f"{pathLogCost}/log_cost.json", 'w') as file:
        json.dump(logData, file, indent=4)

def openLogCost ():
    with open(fileLogCost, 'r') as file:
        logData = json.load(file)
    
    return logData

def addResponse (response, model, verbose=False):
    completionTokens = 0

    if 'completion_tokens' in response['usage']:
        completionTokens = response['usage']['completion_tokens']
    else:
        return ''
    
    pricesModel = prices.prices[model]

    promptTokens = response['usage']['prompt_tokens']
    totalTokens = response['usage']['total_tokens']

    promptCosts = promptTokens * pricesModel["input"]
    completionCosts = completionTokens * pricesModel["output"]

    cost = {
        "prompt_cost": promptCosts / pricesModel["numerTokens"],
        "completion_cost": completionCosts / pricesModel["numerTokens"]
    }

    saveCost(model, cost)

    if verbose:
        print(f"Tokens resume = completion: {completionTokens} prompt: {promptTokens} total: {totalTokens}")
    
    return f"Tokens resume = completion: {completionTokens} prompt: {promptTokens} total: {totalTokens}"

def showCost ():
    costs = openLogCost()

    for model, values in costs.items():
        print(f"* Costos {model}")

        prompt_costs = 0
        completion_costs = 0

        for obj in values:
            prompt_costs += obj["prompt_cost"]
            completion_costs += obj["completion_cost"]
        
        print(f"Prompt: ${prompt_costs}")
        print(f"Completion: ${completion_costs}")
