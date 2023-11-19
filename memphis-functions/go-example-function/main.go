package main

import (
	"encoding/json"
	"github.com/memphisdev/memphis.go"
)

type Event struct {
	Field1 string `json:"field1"`
	Field2 string `json:"field2"`
}

// https://github.com/memphisdev/memphis.go#creating-a-memphis-function
func EventHandler(message []byte, headers map[string]string, inputs map[string]string) ([]byte, map[string]string,  error){
	// Here is a short example of converting the message payload to bytes and back
	var event Event
	json.Unmarshal(message, &event)
	
	// Return the payload back as []bytes
	eventBytes, _ := json.Marshal(event)
	return eventBytes, headers, nil
}


func main() {	
	memphis.CreateFunction(EventHandler)
}