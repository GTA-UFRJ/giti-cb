from pki import *
from server_org1 import *
from server_utils import *
import subprocess
import os
import json

FILE_PATH = "data.enc"
BASE_PATH = "/root/go/src/github.com/gta/fabric-samples/rnp-giti-cb"

def environment_variables ():
    try:
        bin_path = BASE_PATH + "/../bin/"
        fabric_cfg_path = BASE_PATH + "/../config/"
        rootcert_file_path = BASE_PATH + "/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"
        mspconfigpath = BASE_PATH + "/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"

        os.environ["PATH"] += os.pathsep + bin_path
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
    # environment_variables()

    # Receive message from user
    message = server()

    # Generate keys
    generateKeyPair()

    # Fetch permissions
    message_dict = json.loads(message)
    permissions = {}
    for key in message_dict:
        permissions[key] = message_dict[key][1]

    # Create data hash
    data_hash = hashMessage(message)
    
    # Log data into the local blockchain
    store_data(json.dumps(permissions).replace('"', '\\"'), "uid1", "usig1", "upubkey1", "Org1", str(data_hash), "0.0.0.0:2000")
    
    # Encrypt data and store it in the server
    enc_message = encryptMessage(message) 
    file_in = open(FILE_PATH,"wb")
    file_in.write(enc_message)
    file_in.close()

    #------------------------------------------------------------------------------------------------------

    # Listen for request events
    message = server()
    reqId = json.loads(message)['TxId']

    # Verify the request in the global blockchain
    req = json.loads(read_request(reqId))

    # Query permissions in the local blockchain
    permissions = json.loads(json.loads(get_all_data_files())[0]['Permissions'])

    # Decide if data should be shared
    data_keys = req['DataKeys'][1:-1].replace(' ',"").split(',')
    share = True
    for data_key in data_keys:
        print(data_key)
        if permissions[data_key] == 'none':
            share = False

    # Issue response in the global blockchain 
    if share == True:
        print("Sharing of data authorized. Issuing response transaction in the global blockchain...")
        issue_response(req['TxId'],"approved","","0.0.0.0:9000")
    else:
        print("Sharing of data NOT authorized. Issuing response transaction in the global blockchain...")
        issue_response(req['TxId'],"refused","User did not allow data to be shared.","0.0.0.0:9000")
    

if __name__ == "__main__":
    main()
