from tools import config

linuxSo = config.SETTING['so']

def commandPromt ( command ):
    content = f"""You are a Linux terminal assistant.
    You must provide useful commands for the ZSH system in the {linuxSo} operating system.
    Your answers should only be the commands without descriptions, explanations, or code.
    If there is no answer, return 'Command not found'"""

    messagesList = [
        {
            "role": "system",
            "content": content
        },
        {
            "role": "user",
            "content": command
        }
    ]

    return messagesList

def questionPromt ( command ):
    content = """
    Your task is to answer as briefly as possible the questions you are asked.
    """

    messagesList = [
        {
            "role": "system",
            "content": content
        },
        {
            "role": "user",
            "content": command
        }
    ]

    return messagesList

def grammarPromt ( command ):
    prompt = f"""
    Check the grammar and spelling of the following sentence while respecting its original language:

    "{command}"

    Do not add any extra comments, only the check the grammar and spelling.
    """

    messagesList = [{"role": "user", "content": prompt}]

    return messagesList

def translationPromt ( command ):
    prompt = f"""
    Translate the following text. \ 
    Between English and Spanish: \ 
    ```{command}```
    Do not add any extra comments, only the one translation.
    """

    messagesList = [{"role": "user", "content": prompt}]

    return messagesList


promts = {
    'command': commandPromt,
    'question': questionPromt,
    'grammar': grammarPromt,
    'translation': translationPromt
}


def getMessagesList(commandMode, command):
    func = promts.get(commandMode, lambda x: "Invalid option")
    return func(command)
