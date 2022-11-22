from pki import *
from server import *

FILE_PATH = "data.enc"

def main():
	
    message = server()
    key = generateKeyPair()
    enc_message = encryptMessage(message)


    file_in = open(FILE_PATH,"wb")
    file_in.write(enc_message)
    file_in.close()



if __name__ == "__main__":
    main()