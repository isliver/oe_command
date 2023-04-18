import subprocess
import os
import re

def getInfoChange ():
    semanticEmojis = {
        "feat": "🚀",
        "fix": "🐛",
        "docs": "📝",
        "style": "💄",
        "refactor": "🔨",
        "test": "🧪",
        "chore": "🧹"
    }

    urlRepo = "https://github.com/isliver/oe_command/commit/"

    cmd = 'git log --pretty=format:"%H:%h:%s" HEAD..origin/main'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error al obtener los commits: {result.stderr}")
    else:
        commits = result.stdout.strip().split('\n')

        for commit in commits:
            if len(commit) == 0:
                continue
            
            largeHash, shortHash, type, message = commit.split(':')
            link = f"\033]8;;{urlRepo}/{largeHash}\a{shortHash}\033]8;;\a"
            print(f"[{link}]\t\t\t{semanticEmojis[type]}{message}")

def update ():
    print(f"\033[;36mVerificando versiones\033[0m")
    pathHome = os.environ['HOME']
    REMOTE_URL = "https://github.com/isliver/oe_command.git"
    LOCAL_DIR = f"{pathHome}/.bin/oe_command"

    localGit = subprocess.run(['git','-C',LOCAL_DIR, 'rev-parse', 'HEAD'], stdout=subprocess.PIPE)
    remoteGit = subprocess.run(['git', 'ls-remote', '--quiet', '--heads', REMOTE_URL, 'refs/heads/main', '|', 'cut', '-f1'], stdout=subprocess.PIPE)

    localGitHash = localGit.stdout.decode('utf-8').strip()
    remoteGitHash = remoteGit.stdout.decode('utf-8').strip()
    remoteGitHash = re.findall(r'\b[0-9a-f]{6,40}\b', remoteGitHash)[0]

    if localGitHash != remoteGitHash:
        print(f"\033[;36mNueva version\033[0m")
        getInfoChange ()

        os.chdir(LOCAL_DIR)
        os.system('git pull')
    else:
        print(f"\033[;36mNo existen cambios\033[0m")