package main

import (
	"encoding/json"
	"github.com/memphisdev/memphis-functions.go/memphis"
)

type Event struct {
	Field1 string `json:"field1"`
	Field2 string `json:"field2"`
}

// https://github.com/memphisdev/memphis.go#creating-a-memphis-function
func EventHandler(message any, headers map[string]string, inputs map[string]string) (any, map[string]string,  error){
	// Here is a short example of converting the message payload to bytes and back
	as_bytes = message.([]byte)
	
	var event Event
	json.Unmarshal(as_bytes, &event)
	
	// Return the payload back 
	return event, headers, nil
}


func main() {	
	memphis.CreateFunction(EventHandler)
}