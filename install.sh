#!/bin/bash

echo "Instalando requerimientos"
pip3 install -r requirements.txt

echo "Copiando Archivos de configuracion"
cp oe /usr/local/bin
cp config.json /usr/local/bin