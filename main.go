package main

import (
	"log"
	"net/http"
)

func main() {

	fs := http.FileServer(http.Dir("./web"))
	http.Handle("/", fs)
	err := http.ListenAndServe(":8090", nil)
	if err != nil {
		log.Fatal(err)
	}
}
