import socket

"""
The macros below define the loopback address and the port that
the server will listen to capture data transfers from users. We
also define the buffersize and set it to 32KB to limit data size
"""

HOST='0.0.0.0' 
PORT=5042

BUFFSIZE=32768

def server():
	"""
	The server function establishes a socket that the server uses
	to receive data from users. This data is then transfered to 
	another function that will appropriately store it.
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)
	conn, addr = s.accept()
	msg = conn.recv(BUFFSIZE)
	return msg