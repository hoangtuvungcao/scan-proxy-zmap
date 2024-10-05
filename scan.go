package main

import (
	"crypto/tls"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"time"
	"bufio"
	"sync"
)
var syncWait sync.WaitGroup

var statok, fall, all int
var port int

func checkProxy(proxyURL string) {
	defer syncWait.Done()
	
	proxy := fmt.Sprintf("http://%s:%d", proxyURL, port) 

	parsedProxy, err := url.Parse(proxy)
	if err != nil {
		fmt.Println("???? đúng cc đâu em xem sẽ đi", err)
		return
	}

	
	transport := &http.Transport{
		Proxy: http.ProxyURL(parsedProxy),
		
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}

	client := &http.Client{
		Transport: transport,
		Timeout:   5 * time.Second,
	}

	
	resp, err := client.Get("https://httpbin.org/get")
	if err != nil {
		all++
		fall++
		return
	}
	defer resp.Body.Close() // Đảm bảo đóng body

	if resp.StatusCode == http.StatusOK {
		statok++
	} else {
		all++
		fall++
	}
	all++
}

func main() {
	const (
		Reset   = "\033[0m"
		Red     = "\033[31m"
		Green   = "\033[32m"
		Yellow  = "\033[33m"
		Blue    = "\033[34m"
		Magenta = "\033[35m"
		Cyan    = "\033[36m"
		White   = "\033[37m"
	)
	
	if len(os.Args) >= 2 {
		portArg := os.Args[1]
		var err error
		port, err = strconv.Atoi(portArg) 
		if err != nil {
			
			port = 8080
		}
	} else {
		port = 8080 
	}
	var timest  int


	go func() {
		for {
			fmt.Printf(Yellow+" KAMI SCAN PROXY : OKE : %d  | "+Red+"FALL : %d | "+Cyan+"ALL : %d | Time : %d"+Reset+"\n", statok, fall, all, timest)
			time.Sleep(1 * time.Second)
			timest++
			
		}
	}()

	for {
        r := bufio.NewReader(os.Stdin)
        scan := bufio.NewScanner(r)
        for scan.Scan() {
            go checkProxy(scan.Text())
			
            syncWait.Add(1)
        }
    }
	
	
}
