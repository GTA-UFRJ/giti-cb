package main

import (
	"fmt"
	"log"
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
	"github.com/golang-collections/go-datastructures/queue"
)

type SmartContract struct {
  contractapi.Contract
}

// Define transaction structures
type ReqTransaction struct {
	TxId string		`json:"TxId"`
    	TxType string		`json:"TxType"`
	DataKeys string		`json:"DataKeys"`
	UserId string		`json:"UserId"`
	UserPubkey string	`json:"UserPubkey"`
	UserSig string		`json:"UserSig"`
	DstOrg string		`json:"DstOrg"`
	SrcOrg string		`json:"SrcOrg"`
	Status string		`json:"Status"`
	RespTxId string		`json:"RespTxId"`
    	TxIndex string		`json:"TxIndex"`
}

type RespTransaction struct {
	TxId string	    	`json:"TxId"`
    	TxType string		`json:"TxType"`
	ReqTxId string		`json:"reqTxId"`
	Result string		`json:"result"`
	ErrorReason string	`json:"errorReason"`
	EntryPoint string	`json:"entryPoint"`
    	TxIndex string		`json:"TxIndex"`
}



// Define organization structure
type Org struct{
	Requests string `json:"Requests"`
	OrgId string	`json:"OrgId"`
	OrgName string	`json:"OrgName"`
}


// Initialize queue of pending transactions
var q queue.Queue

// Initialize two organizations without any request
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	orgs :=[]Org{
		{OrgId: "1", OrgName: "Org1", Requests: ""},
		{OrgId: "2", OrgName: "Org2", Requests: ""},
	}

 	for _, org := range orgs {
    		orgJSON, err := json.Marshal(org)
    	if err != nil {
      	    return err
    	}

    	err = ctx.GetStub().PutState(org.OrgId, orgJSON)
    	if err != nil {
      		return fmt.Errorf("failed to put to world state. %v", err)
    	}
  }

  return nil
}

// Define invocable functions on the smart contract

// issueRequest issues a new request transaction to the world state with given details.
func (s *SmartContract) IssueRequest(ctx contractapi.TransactionContextInterface, dataKeys string, uid string, uSig string, uPubkey string, dstOrg string, srcOrg string) error {
    
    	data := []byte(dataKeys + uid + uSig + uPubkey + dstOrg + srcOrg)
	hash := md5.Sum(data)
	txId := hex.EncodeToString(hash[:])

	exists, err := s.ReqExists(ctx, txId)
  	if err != nil {
		return err
  	}
  	if exists {
        	return fmt.Errorf("the request transaction %s already exists", txId)
  	}

	reqTx := ReqTransaction{
		TxId:		txId,
		TxType:		"request",
		DataKeys:	dataKeys,
		UserId:		uid,
		UserPubkey:	uPubkey,
		UserSig:	uSig,
		DstOrg:		dstOrg,
		SrcOrg:		srcOrg,
		Status:		"open",
		RespTxId:	"",
	}

  	reqTxJSON, err := json.Marshal(reqTx)
  	if err != nil {
    		return err
 	}
	
  	return ctx.GetStub().PutState(txId, reqTxJSON)
}

// issueResponse issues a new response transaction to the world state with given details.
func (s *SmartContract) IssueResponse(ctx contractapi.TransactionContextInterface, reqTxId string, result string, errorReason string, entryPoint string) error {

    	data := []byte(reqTxId + result + errorReason + entryPoint)
	hash := md5.Sum(data)
	txId := hex.EncodeToString(hash[:])

	respExists, err := s.RespExists(ctx, txId)
  	if err != nil {
    		return err
  	}
  	if respExists {
    		return fmt.Errorf("the response transaction  %s already exists", txId)
  	}

	reqExists, err := s.ReqExists(ctx, reqTxId)
  	if !reqExists {
    		return fmt.Errorf("the request transaction %s does not exist",reqTxId)
  	}

	respTx := RespTransaction {
		TxId:		txId,
		TxType:		"response",
		ReqTxId:	reqTxId,
		Result:		result,
		ErrorReason:	errorReason,
		EntryPoint:	entryPoint,
	}

  	respTxJSON, err := json.Marshal(respTx)
  	if err != nil {
    		return err
 	}

	s.UpdateRequest(ctx, reqTxId, txId, result)

  	return ctx.GetStub().PutState(txId, respTxJSON)
}


// ReadRequest returns the request transaction  stored in the world state with given id.
func (s *SmartContract) ReadRequest(ctx contractapi.TransactionContextInterface, reqId string) (*ReqTransaction, error) {
	reqJSON, err := ctx.GetStub().GetState(reqId)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if reqJSON == nil {
		return nil, fmt.Errorf("the request transaction %s does not exist", reqId)
	}

	var reqTx ReqTransaction
	err = json.Unmarshal(reqJSON, &reqTx)
	if err != nil {
		return nil, err
	}
	return &reqTx, nil
}

// ReadResponse returns the response transaction stored in the world state with given id.
func (s *SmartContract) ReadResponse(ctx contractapi.TransactionContextInterface, respId string) (*RespTransaction, error) {
	respJSON, err := ctx.GetStub().GetState(respId)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if respJSON == nil {
		return nil, fmt.Errorf("the response transaction %s does not exist", respId)
	}

	var respTx RespTransaction
	err = json.Unmarshal(respJSON, &respTx)
	if err != nil {
		return nil, err
	}
	return &respTx, nil
}


// UpdateRequest updates an existing request in the world state with provided parameters.
func (s *SmartContract) UpdateRequest(ctx contractapi.TransactionContextInterface, reqId string, respId string, status string) error {
	exists, err := s.ReqExists(ctx, reqId)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the request %s does not exist", reqId)
	}

	reqTx, err := s.ReadRequest(ctx, reqId)
	if err != nil {
		return err
	}
	reqTx.RespTxId = respId
	reqTx.Status = status
  	reqJSON, err := json.Marshal(reqTx)
	
	if err != nil {
		return err
	}
	
	return ctx.GetStub().PutState(reqId, reqJSON)
}


// ReqExists returns true when a request transaction with given ID exists in world state
func (s *SmartContract) ReqExists(ctx contractapi.TransactionContextInterface, txId string) (bool, error) {
	reqJSON, err := ctx.GetStub().GetState(txId)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}
	return reqJSON != nil, nil
}



// RespExists returns true when a request transaction with given ID exists in world state
func (s *SmartContract) RespExists(ctx contractapi.TransactionContextInterface, txId string) (bool, error) {
	respJSON, err := ctx.GetStub().GetState(txId)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}
	return respJSON != nil, nil
}



// GetAllRequests returns all request transatcions found in world state
func (s *SmartContract) GetAllRequests(ctx contractapi.TransactionContextInterface) ([]*ReqTransaction, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()
	var requests []*ReqTransaction
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var reqTx ReqTransaction
		err = json.Unmarshal(queryResponse.Value, &reqTx)
		if err != nil {
			return nil, err
		}
		if reqTx.TxId != "" && reqTx.TxType == "request" {
			requests = append(requests, &reqTx)
		}
	}

	return requests, nil
}


// GetAllResponses returns all response transatcions found in world state
func (s *SmartContract) GetAllResponses(ctx contractapi.TransactionContextInterface) ([]*RespTransaction, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()
	var responses []*RespTransaction
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var respTx RespTransaction
		err = json.Unmarshal(queryResponse.Value, &respTx)
		if err != nil {
			return nil, err
		}
		if respTx.TxId != "" && respTx.TxType == "response" {
			responses = append(responses, &respTx)
		}
	}

	return responses, nil
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


