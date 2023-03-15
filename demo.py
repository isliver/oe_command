import argparse

parser = argparse.ArgumentParser()
parser.add_argument('mensaje', nargs='+', help='mensaje que se desea mostrar en pantalla')
parser.add_argument('-c', '--ejemplo', action='store_true', help='muestra un ejemplo en pantalla')
args = parser.parse_args()

if args.ejemplo:
    print('Esto es un ejemplo')
else:
    print(' '.join(args.mensaje))