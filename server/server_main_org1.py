from pki import *
from server_org1 import *
from server_utils import *
import subprocess
import os
import json

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
    
    # Set environment variables
    environment_variables()

    # Receive message from user
    message = server()
    generateKeyPair()
    message_dict = json.loads(message)
    permissions = {}
    for key in message_dict:
        permissions[key] = message_dict[key][1]
    data_hash = hashMessage(message)

    # Log metadata into the local blockchain
    store_data (str(permissions), "uid1", "usig1", "upubkey1", str(data_hash), "0.0.0.0:2000")
    
    # Encrypt data and store it in the server
    enc_message = encryptMessage(message) 
    file_in = open(FILE_PATH,"wb")
    file_in.write(enc_message)
    file_in.close()

    #------------------------------------------------------------------------------------------------------

    # Listen for request event
    message = server()
    req = read_request(message.decode("utf-8")-)
    print(req)

    # Decide if data should be shared


    # file_in = open(FILE_PATH,"rb")
    # lines = file_in.read()
    # file_in.close()

    # dec_message = decryptMessage(lines)
    # dec_message_dict = json.loads(dec_message)
    
    # share = True

    # for key in result:
    #     if dec_message_dict == "none":
    #         share = False
    
    # if share == True:
    #     #emite_positiva
    # else:
    #     #emite_negativa            

    

if __name__ == "__main__":
    main()
