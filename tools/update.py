import subprocess
import os
import re

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
        os.chdir(LOCAL_DIR)
        os.system('git pull')
    else:
        print(f"\033[;36mNo existen cambios\033[0m")