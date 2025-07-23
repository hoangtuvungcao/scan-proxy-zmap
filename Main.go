package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"net/url"
	"os"
	"strings"
	"sync"
	"time"

	"h12.io/socks"
)

type config struct {
	Web     string `json:"web"`
	Ua      string `json:"ua"`
	Apet    string `json:"apet"`
	Timeout int    `json:"timeout"`
}

func loadConfig() (*config, error) {
	file, err := os.Open("config.json")
	if err != nil {
		return nil, fmt.Errorf("error opening config file: %v", err)
	}
	defer file.Close()

	var cfg config
	decoder := json.NewDecoder(file)
	if err := decoder.Decode(&cfg); err != nil {
		return nil, fmt.Errorf("error decoding config file: %v", err)
	}

	return &cfg, nil
}

var (
	syncWait   = sync.WaitGroup{}
	website    string
	user_agent string
	apet       string
	Config     *config
)

func TaGet(ip string, port string) {
	var (
		name string
		prun bool = false
	)

	defer syncWait.Done()
	proxy := fmt.Sprintf("%s:%s", ip, port)
	if !Http_check(proxy) {
		if !socks4(proxy, "5") {
			if socks4(proxy, "4") {
				name = "socks4"
				prun = true
			}
		} else {
			name = "socks5"
			prun = true
		}

	} else {
		name = "http"
		prun = true
	}
	if prun {
		fmt.Println("\033[32m" + name + "\033[0m " + "\033[33m" + proxy + "\033[0m")

		savefile(name, proxy)
	}

}

var fileLock sync.Mutex

func savefile(name, ip string) {
	fileLock.Lock()
	defer fileLock.Unlock()
	filename := fmt.Sprintf("%s.txt", name)
	file, err := os.OpenFile(filename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("Không mở được file:", err)
		return
	}
	defer file.Close()

	newLine := fmt.Sprintf("%s\n", ip)

	if _, err := file.WriteString(newLine); err != nil {
		fmt.Println("Không ghi được vào file:", err)
	}
}
func socks4(p, v string) bool {

	tr := &http.Transport{
		Dial: socks.Dial(fmt.Sprintf("socks%s://%s?timeout=%ds", v, p, 8)),
	}
	client := http.Client{
		Timeout:   time.Second * time.Duration(Config.Timeout),
		Transport: tr,
	}

	req, err := http.NewRequest("GET", Config.Web, nil)
	if err != nil {
		log.Fatalln(err)
	}
	req.Header.Add("User-Agent", Config.Ua)
	req.Header.Add("accept", Config.Apet)

	res, err := client.Do(req)
	if err != nil {
		return false
	}
	res.Body.Close()
	if res.StatusCode == 200 {
		return true
	}

	return false
}
func Http_check(p string) bool {

	proxyUrl, err := url.Parse(fmt.Sprintf("http://%s", p))
	if err != nil {
		log.Println(err)
		return false
	}

	tr := &http.Transport{
		Proxy: http.ProxyURL(proxyUrl),
		DialContext: (&net.Dialer{
			Timeout:   time.Second * time.Duration(Config.Timeout),
			KeepAlive: time.Second,
			DualStack: true,
		}).DialContext,
	}
	client := http.Client{
		Timeout:   time.Second * time.Duration(Config.Timeout),
		Transport: tr,
	}
	req, err := http.NewRequest("GET", Config.Web, nil)
	if err != nil {
		log.Fatalln(err)
	}
	req.Header.Add("User-Agent", Config.Ua)
	req.Header.Add("accept", Config.Apet)

	res, err := client.Do(req)
	if err != nil {
		return false
	}
	res.Body.Close()
	if res.StatusCode == 200 {
		return true
	}
	return false
}
func main() {
	cfg, err := loadConfig()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error loading config: %v\n", err)
		return
	}
	Config = cfg

	if len(os.Args) < 2 {
		fmt.Println("Usage: ./tool <port | listen>")
		return
	}
	scan := bufio.NewScanner(os.Stdin)
	for scan.Scan() {
		target := strings.TrimSpace(scan.Text())
		if target == "" {
			continue
		}

		var fullTarget string
		if os.Args[1] == "listen" {
			fullTarget = "80"
		} else {
			fullTarget = os.Args[1]
		}

		syncWait.Add(1)
		go TaGet(target, fullTarget)
	}

	if err := scan.Err(); err != nil {
		fmt.Fprintf(os.Stderr, "Lỗi khi đọc input: %v\n", err)
	}

	syncWait.Wait()
}
