import subprocess
import os

BASE_PATH = "/root/go/src/github.com/gta/fabric-samples/rnp-giti-cb"

# Global blockchain functions

def issue_request (data_keys, dst_org, uid, usig, upubkey, org_id):
    command = "peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile \"${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem\" -C global-channel -n global-bc --peerAddresses localhost:7051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt\" --peerAddresses localhost:9051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt\" -c \'{\"function\":\"IssueRequest\",\"Args\":[\""+ data_keys + "\",\"" + uid + "\",\"" + usig + "\",\"" + upubkey + "\",\"" + dst_org + "\",\"" + org_id + "\"]}\'"
    print("Issuing command: " + command)
    command_result = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,cwd=BASE_PATH).stdout
    print(str(command_result.read().decode()))
    return str(command_result.read().decode())

def issue_response (req_id, result, error_reason, entry_point):
    command = "peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile \"${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem\" -C global-channel -n global-bc --peerAddresses localhost:7051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt\" --peerAddresses localhost:9051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt\" -c \'{\"function\":\"IssueRequest\",\"Args\":[\""+ req_id + "\",\"" + result + "\",\"" + error_reason + "\",\""+ entry_point + "\"]}\'"
    print("Issuing command: " + command)
    command_result = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,cwd=BASE_PATH).stdout
    print(str(command_result.read().decode()))

def read_request (req_id):
    command = "peer chaincode query -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile \"${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem\" -C global-channel -n global-bc --peerAddresses localhost:7051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt\" -c \'{\"function\":\"ReadRequest\",\"Args\":[\"" + req_id + "\"]}\'"
    print("Issuing command: " + command)
    command_result = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,cwd=BASE_PATH).stdout
    print(str(command_result.read().decode()))
    return str(command_result.read().decode())


# Local blockchain functions

def read_data (data_id):
    command = "peer chaincode query -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile \"${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem\" -C local-channel -n local-bc --peerAddresses localhost:7051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt\" --peerAddresses localhost:9051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt\" -c \'{\"function\":\"ReadData\",\"Args\":[\"" + data_id + "\"]}\'"
    print("Issuing command: " + command)
    command_result = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,cwd=BASE_PATH).stdout
    print(str(command_result.read().decode()))
    return str(command_result.read().decode())

def store_data (permissions, uid, usig, upubkey, org_id, data_hash, address):
    command = "peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile \"${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem\" -C local-channel -n local-bc --peerAddresses localhost:7051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt\" --peerAddresses localhost:9051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt\" -c \'{\"function\":\"StoreData\",\"Args\":[\"" + permissions + "\",\"" + uid + "\",\"" + usig + "\",\"" + upubkey + "\",\"" + org_id + "\",\"" + data_hash + "\",\"" + address + "\"]}\'"
    print("Issuing command: " + command)
    command_result = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,cwd=BASE_PATH).stdout
    print(str(command_result.read().decode()))

def update_data_permissions (data_id, permissions):
    command = "peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile \"${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem\" -C local-channel -n local-bc --peerAddresses localhost:7051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt\" --peerAddresses localhost:9051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt\" -c \'{\"function\":\"UpdateDataPermissions\",\"Args\":[\"" + data_id + "\",\"" + permissions + "\"]}\'"
    print("Issuing command: " + command)
    command_result = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,cwd=BASE_PATH).stdout
    print(str(command_result.read().decode()))

def update_data_address (data_id, address):
    command = "peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile \"${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem\" -C local-channel -n local-bc --peerAddresses localhost:7051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt\" --peerAddresses localhost:9051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt\" -c \'{\"function\":\"UpdateDataAddress\",\"Args\":[\"" + data_id + "\",\"" + address + "\"]}\'"
    print("Issuing command: " + command)
    command_result = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,cwd=BASE_PATH).stdout
    print(str(command_result.read().decode()))

def get_all_data_files ():
    command = "peer chaincode query -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile \"${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem\" -C local-channel -n local-bc --peerAddresses localhost:7051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt\" --peerAddresses localhost:9051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt\" -c \'{\"function\":\"GetAllDataFiles\",\"Args\":[\"\"]}\'"
    print("Issuing command: " + command)
