package main

import (
	"fmt"
	"log"
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
  contractapi.Contract
}

// Define transaction structures
type DataFile struct {
	DataId string		`json:"DataId"`
	Permissions string	`json:"Permissions"`
	UserId string		`json:"UserId"`
	UserPubkey string	`json:"UserPubkey"`
	UserSig string		`json:"UserSig"`
	HostOrg string		`json:"HostOrg"`
	DataHash string		`json:"DataHash"`
	Address string		`json:"Address"`
}



// Initialize two organizations without any request
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
  return nil
}

// Define invocable functions on the smart contract

// StoreData logs new data file to the world state with given details.
func (s *SmartContract) StoreData(ctx contractapi.TransactionContextInterface, permissions string, uid string, uSig string, uPubkey string, hostOrg string, dataHash string, address string) error {
    
    	bytes := []byte(permissions + uid + uSig + uPubkey + hostOrg + dataHash + address)
	hash := md5.Sum(bytes)
	dataId := hex.EncodeToString(hash[:])

	exists, err := s.DataExists(ctx, dataId)
  	if err != nil {
		return err
  	}
  	if exists {
        	return fmt.Errorf("the data %s is already on chain", dataId)
  	}

	dataFile := DataFile {
		DataId:		dataId,
		Permissions:	permissions,
		UserId:		uid,
		UserPubkey:	uPubkey,
		UserSig:	uSig,
		HostOrg:	hostOrg,
		DataHash:	dataHash,
		Address:	address,
	}

  	dataJSON, err := json.Marshal(dataFile)
  	if err != nil {
    		return err
 	}
	
  	return ctx.GetStub().PutState(dataId, dataJSON)
}

// ReadData returns the data stored in the world state with given id.
func (s *SmartContract) ReadData(ctx contractapi.TransactionContextInterface, dataId string) (*DataFile, error) {
	dataJSON, err := ctx.GetStub().GetState(dataId)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if dataJSON == nil {
		return nil, fmt.Errorf("the data file %s does not exist", dataId)
	}

	var dataFile DataFile
	err = json.Unmarshal(dataJSON, &dataFile)
	if err != nil {
		return nil, err
	}
	return &dataFile, nil
}


// UpdateDataAddress updates an existing data file address in the world state with provided parameters.
func (s *SmartContract) UpdateDataAddress(ctx contractapi.TransactionContextInterface, dataId string, address string) error {
	exists, err := s.DataExists(ctx, dataId)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the data file %s does not exist", dataId)
	}

	dataFile, err := s.ReadData(ctx, dataId)
	if err != nil {
		return err
	}
	dataFile.Address = address
  	dataJSON, err := json.Marshal(dataFile)
	
	if err != nil {
		return err
	}
	
	return ctx.GetStub().PutState(dataId, dataJSON)
}

// UpdateDataPermissions updates the permissions of an existing data file in the world state with provided parameters.
func (s *SmartContract) UpdateDataPermissions(ctx contractapi.TransactionContextInterface, dataId string, permissions string) error {
	exists, err := s.DataExists(ctx, dataId)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the data file %s does not exist", dataId)
	}

	dataFile, err := s.ReadData(ctx, dataId)
	if err != nil {
		return err
	}
	dataFile.Permissions = permissions
  	dataJSON, err := json.Marshal(dataFile)
	
	if err != nil {
		return err
	}
	
	return ctx.GetStub().PutState(dataId, dataJSON)
}

// DataExists returns true when a data file with given ID exists in world state
func (s *SmartContract) DataExists(ctx contractapi.TransactionContextInterface, dataId string) (bool, error) {
	dataJSON, err := ctx.GetStub().GetState(dataId)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}
	return dataJSON != nil, nil
}



// GetAllDataFiles returns all request transatcions found in world state
func (s *SmartContract) GetAllDataFiles(ctx contractapi.TransactionContextInterface) ([]*DataFile, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()
	var requests []*DataFile
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var dataFile DataFile
		err = json.Unmarshal(queryResponse.Value, &dataFile)
		if err != nil {
			return nil, err
		}
		if dataFile.DataId != "" {
			requests = append(requests, &dataFile)
		}
	}

	return requests, nil
}


func main() {
	globalBCChaincode, err := contractapi.NewChaincode(&SmartContract{})
	if err != nil {
		log.Panicf("Error creating global-bc chaincode: %v", err)
	}

	if err := globalBCChaincode.Start(); err != nil {
		log.Panicf("Error starting global-bc chaincode: %v", err)
	}
}


