#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

if len(sys.argv) != 2:
	sys.exit('Usage: python3 seerver.py port')
PORT = int(sys.argv[1])

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        for line in self.rfile:
            LINE =  line.decode('utf-8').split()
            IP_CLIENT = self.client_address[0]
            PORT_CLIENT = self.client_address[1]
            print("El cliente nos manda ", line.decode('utf-8'))
            if LINE[2] == 'REGISTER':
                self.wfile.write(b'SIP 2.0 OK\r\n\r\n')
                

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), EchoHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
