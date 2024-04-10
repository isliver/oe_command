def commandPromt ( command ):
    content = """You are a Linux terminal assistant.
    You must provide useful commands for the ZSH system in the Linux operating system.
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
    'translation': translationPromt
}


def getMessagesList(commandMode, command):
    func = promts.get(commandMode, lambda x: "Invalid option")
    return func(command)
