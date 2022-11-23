from pki import *
from server_org2 import *
from server_utils import *
import subprocess
import os
import json
from client_socket import *


FILE_PATH = "data.enc"

def environment_variables ():
    try:
        pwd = subprocess.Popen("pwd", shell=True, stdout=subprocess.PIPE).stdout
        pwd_string = str(pwd.read().decode())
        pwd_string = pwd_string.rstrip()
        new_path_string = pwd_string + "/../bin"
        fabric_cfg_path = pwd_string + "/../config/"
        rootcert_file_path = pwd_string + "/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt"
        mspconfigpath = pwd_string + "/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp"

        os.environ["PATH"] += os.pathsep + new_path_string
        os.environ["FABRIC_CFG_PATH"] = fabric_cfg_path
        os.environ["CORE_PEER_TLS_ENABLED"] = "true"
        os.environ["CORE_PEER_LOCALMSPID"] = "\"Org2MSP\""
        os.environ["CORE_PEER_TLS_ROOTCERT_FILE"] = rootcert_file_path
        os.environ["CORE_PEER_MSPCONFIGPATH"] = mspconfigpath
        os.environ["CORE_PEER_ADDRESS"] = "localhost:9051"
    except:
        raise Exception("Failed to set environment variables")

def main():
    # Set environment variables
    # environment_variables()

    # Listen to client requests
    message = server()
    message_info = message.decode("utf-8").split("|")

    # Log request in the global blockchain
    issue_request (str(message_info[0]), str(message_info[1]), str(message_info[2]), "usig1", "upubkey1", "Org2")
    
    # Fetch the logged request from the blockchain
    req = json.loads(get_all_requests())[0]
    json_req = json.dumps(req)

    # Inform Org1 of the request
    client(json_req.encode(), 5041)

if __name__ == "__main__":
    main()
