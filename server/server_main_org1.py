from pki import *
from server_org1 import *
from server_utils import *
import subprocess
import os

FILE_PATH = "data.enc"

def environment_variables ():
    try:
        pwd = subprocess.Popen("pwd", shell=True, stdout=subprocess.PIPE).stdout
        pwd_string = str(pwd.read().decode())
        pwd_string = pwd_string.rstrip()
        new_path_string = pwd_string + "/../bin"
        fabric_cfg_path = pwd_string + "/../config/"
        rootcert_file_path = pwd_string + "/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"
        mspconfigpath = pwd_string + "/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"

        os.environ["PATH"] += os.pathsep + new_path_string
        os.environ["FABRIC_CFG_PATH"] = fabric_cfg_path
        os.environ["CORE_PEER_TLS_ENABLED"] = "true"
        os.environ["CORE_PEER_LOCALMSPID"] = "\"Org1MSP\""
        os.environ["CORE_PEER_TLS_ROOTCERT_FILE"] = rootcert_file_path
        os.environ["CORE_PEER_MSPCONFIGPATH"] = mspconfigpath
        os.environ["CORE_PEER_ADDRESS"] = "localhost:7051"
    except:
        raise Exception("Failed to set environment variables")


def main():
	
    message = server()
    key = generateKeyPair()
    enc_message = encryptMessage(message)

    
    file_in = open(FILE_PATH,"wb")
    file_in.write(enc_message)
    file_in.close()

    

if __name__ == "__main__":
    main()
