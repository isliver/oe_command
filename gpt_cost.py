globalCompletionTokens = 0
globalPromptTokens = 0
globalTotalTokens = 0

def saveCost (cost):
    f = open("logCost", "a")
    f.write(str(cost) + "\n")
    f.close()

def showTotalCost ():
    f = open("logCost", "r")
    totalCost = 0

    for x in f:
        totalCost += float(x)
    
    print(f"Total cost: ${totalCost}")

def addResponse (response, verbose=False):
    global globalCompletionTokens
    global globalPromptTokens
    global globalTotalTokens

    completionTokens = 0

    if 'completion_tokens' in response['usage']:
        completionTokens = response['usage']['completion_tokens']

    promptTokens = response['usage']['prompt_tokens']
    totalTokens = response['usage']['total_tokens']
    
    globalCompletionTokens += completionTokens
    globalPromptTokens += promptTokens
    globalTotalTokens += totalTokens

    if verbose:
        print(f"Tokens resume = completion: {completionTokens} prompt: {promptTokens} total: {totalTokens}")

def showCost (model="text-davinci-003", save=False, verbose=False):
    global globalCompletionTokens
    global globalPromptTokens
    global globalTotalTokens
    
    costByTokens = costByModel(model)
    finalCost = ( globalTotalTokens * costByTokens ) / 1000
    saveCost (finalCost)

    if verbose:
        print(f"MODEL: {model}")
        print(f"Final Tokens consume = completion: {globalCompletionTokens} prompt: {globalPromptTokens} total: {globalTotalTokens}")
        print(f"Final cost: ${finalCost}")

def costByModel (model):
    if model == "text-davinci-003":
        return 0.02
    elif model == "gpt-3.5-turbo":
        return 0.002