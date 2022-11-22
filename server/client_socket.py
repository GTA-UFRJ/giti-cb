import socket
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE,SIG_DFL)

"""
The macros below define are set to the IP and PORT used by the
server to recive client data
"""

HOST = '0.0.0.0'     

BUFFSIZE = 1024

def client(dataInBytes, PORT):
    """
    client function establishes communication with the server to
    send client data. The argument dataInBytes represents the data
    that the client sends through the socket
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Connecting to server")
        s.connect((HOST, PORT))
        print("Sending data")
        s.sendall(dataInBytes)
    except Exception as e:
        print("Something went wrong with %s. Exception: %s"	% (HOST,e))