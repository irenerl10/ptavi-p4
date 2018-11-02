#!/usr/bin/python3.
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
from datetime import datetime, date, timedelta
import time
import json


if len(sys.argv) != 2:
    sys.exit('Usage: python3 server.py port')
PORT = int(sys.argv[1])


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""
    users = {}

    def register2json(self):
        with open('registered.json', 'w') as jsonfile:
            json.dump(self.users, jsonfile, indent=3)

    def json2registered(self):
        try:
            with open('registered.json', 'r') as jsonfile:
                self.users = jsonload(jsonfile)
        except(NameError, FileNotFoundError, AttributeError):
                pass

    def time_expired(self):
        list = []
        FECHA_HORA = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        for USER in self.users:
            if self.users[USER]['expires'] <= FECHA_HORA:
                list.append(USER)
        for USER in list:
            del self.users[USER]

    def handle(self):
        """handle method of the server class
        (all requests will be handled by this method)."""
        self.json2registered()
        for line in self.rfile:
            LINE = line.decode('utf-8').split()
            IP_CLIENT = self.client_address[0]
            PORT_CLIENT = self.client_address[1]
            print("El cliente nos manda ", line.decode('utf-8'))
            if LINE[0] == 'REGISTER':
                USER = LINE[1].split(':')[1]

            if LINE[0] == 'Expires:':
                TIMEXP = line.decode('utf-8').split()[1]
                if TIMEXP != '0':
                    FORMATO = "%Y-%m-%d %H:%M:%S"
                    TIME = time.gmtime(time.time())
                    TIME_STR = time.strftime(time.strftime(FORMATO, TIME))
                    EXPTIME = datetime.now() + timedelta(seconds=int(TIMEXP))
                    self.users[USER] = {
                              'address': IP_CLIENT,
                              'expires': EXPTIME.strftime('%H:%M:%S %d-%m-%Y')}
                    self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                elif TIMEXP == '0':
                    try:
                        del self.users[USER]
                        self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                    except(KeyError, NameError, AttributeError):
                        self.wfile.write(b'SIP/2.0 404 User Not Found\r\n\r\n')
        self.time_expired()
        self.register2json()


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), EchoHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
