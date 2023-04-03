#!/bin/bash
if [ ! -d "$HOME/.bin" ]; then
  echo -e "\033[32mLa carpeta ~/.bin no existe. Creando...\033[0m"
  mkdir "$HOME/.bin"
fi

REPO_NAME="oe_command"
REMOTE_URL="https://github.com/isliver/oe_command.git"
LOCAL_DIR="$HOME/.bin/oe_command"

if [ -d "$LOCAL_DIR" ]; then
    cd "$LOCAL_DIR"
    LOCAL_HASH=$(git rev-parse HEAD)
    REMOTE_HASH=$(git ls-remote --quiet --heads "$REMOTE_URL" "refs/heads/main" | cut -f1)

    if [ "$LOCAL_HASH" != "$REMOTE_HASH" ]; then
        git pull
        echo -e "\033[32mActualizando repositorio\033[0m"
    else
        echo -e "\033[32mNo hay cambios en el repositorio remoto\033[0m"
    fi
else
    git clone "$REMOTE_URL" "$LOCAL_DIR"
    echo -e "\033[32mClonando repositorio\033[0m"
fi

cd ~/.bin/oe_command
echo -e "\033[32mCopiando Archivos de configuracion\033[0m"
sudo cp oe /usr/local/bin
cp config.json ~/.config/oe