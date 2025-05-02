package main

import (
	"fmt"
	"io"
	"net/http"
)

func download(url string) (string, error) {
	var err error                              // now in scope all the way in the function
	if resp, err := http.Get(url); err == nil { // ; seperates by and for statements
		defer resp.Body.Close()                            //when resp goes out of scope
		if bts, err := io.ReadAll(resp.Body); err == nil { // combining if and declaration because there are new bc bts is new eventhough err is not
			return string(bts), err// look in the resp for the body is a readCloser- interface ReadCloser
		} else{
				return "", err
	} else {
		return []byte(""), err
			}
		//fmt.Printf("%v")

	}
	//return err
}
