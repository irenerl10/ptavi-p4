#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente UDP que abre un socket a un servidor."""

import socket
import sys

if len(sys.argv) < 6:
    sys.exit('Usage: client.py ip port register sip_addres expires_value')

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
LINE = ' '.join(sys.argv[3:])
EXPIRES = LINE.split()[2]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", LINE)
    DIR = LINE.split()[1]
    REGISTER_MAYUSC = LINE.split()[0].upper()
    EXP = 'Expires: ' + EXPIRES + '\r\n'
    if LINE.split()[0] == 'register':
        LINE = DIR + ' SIP/2.0\r\n'
    my_socket.send(bytes(REGISTER_MAYUSC + ' sip:' + LINE + EXP, 'utf-8'))
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
