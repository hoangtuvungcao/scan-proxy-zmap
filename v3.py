from flask import Flask, jsonify, request
from waitress import serve
import threading, subprocess, time
import select, re, os

run = True  # Thêm biến này để dừng vòng lặp nếu cần
proxy = {}
ports = [1001, 1002, 1003, 1004, 1005, 9977, 8888, 8443, 8080, 8008, 8000, 7070, 443, 3128, 3128, 3008, 3008, 1014, 1080, 1014, 9977, 10009, 10008, 10007, 10006, 10010, 10001, 10002, 10003, 10004, 5109, 5108, 5107, 5106, 5105, 5104, 5103, 5102, 5101, 7010, 7009, 7008, 7007, 7006, 7005, 7004, 7003, 7002, 7001, 4009, 4008, 4007, 4006, 4005, 4004, 4003, 4002, 3128, 443, 80]


ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def strip_ansi_codes(s):
    return ANSI_ESCAPE.sub('', s)

SCAN_DURATION = 180
def demovi(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

def run_scan(port):
    """Thực hiện quét port"""
    demovi("http.txt")
    demovi("socks4.txt")
    demovi("socks5.txt")
    print(f"start  {port}...")

    command = f"zmap -w subnetvn -p {port} -q -B10G -T5 -i eth0 --cooldown-time 1 | ./KamiPP {port}"
    
    process = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    start_time = time.time()
    consecutive_zero_http = 0

    while True:
        if process.poll() is not None:
            break

        ready, _, _ = select.select([process.stdout], [], [], 0.5)
        if ready:
            line = process.stdout.readline()
            if line:
                clean_line = strip_ansi_codes(line).strip()
                if "with 0 open http threads" in clean_line.lower():
                    consecutive_zero_http += 1
                    if consecutive_zero_http >= 3:
                        process.kill()
                        print(f"[INFO] Dừng sớm quét port {port} - không có thread hoạt động")
                        return True
                else:
                    consecutive_zero_http = 0

        if time.time() - start_time > SCAN_DURATION:
            process.kill()
            print(f"[INFO] Đã hết thời gian cho port {port}")
            break

    return False

app = Flask(__name__)
def loadfile(filename):
    data = []
    try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    data = [line.strip() for line in lines if len(line.strip()) >= 6]

    except:
        ""
    print(data)
    return data    
last ={
    "http":[],
             "socks4":[],
             "socks5":[]

}
def unique_list(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]
proxy = {
             "http":[],
             "socks4":[],
             "socks5":[]
        }
def runing():
    global proxy, run
    while run:
     #   last["http"] += proxy["http"]
    #    last["socks4"] += proxy["socks4"]
   #     last["socks5"] += proxy["socks5"]
  #      last["http"] = unique_list(last["http"])
 #       last["socks4"]= unique_list(last["socks4"])
#        last["socks5"]= unique_list(last["socks5"])
        proxy = {
             "http":[],
             "socks4":[],
             "socks5":[]
        }

        for p in ports:
            try:
                run_scan(p)
                proxy["http"] +=loadfile("http.txt")
                proxy["socks4"] += loadfile("socks4.txt")
                proxy["socks5"] += loadfile("socks5.txt")
                # last["http"] +=loadfile("http.txt")
                # last["socks4"] += loadfile("socks4.txt")
                # last["socks5"] += loadfile("socks5.txt")
                # with open("output.txt", "r", encoding="utf-8") as f:
                #     lines = f.readlines()
                #     print(f"scan xong {lines}")
                #     proxy[p] = [line.strip() for line in lines if len(line.strip()) >= 6]
            except Exception as e:
                print(f"[ERROR] {e}")
                continue
        time.sleep(15 * 60)

 
@app.route("/index")
@app.route("/home")
@app.route("/")
@app.route("/sex")
def sex():
    global proxy
    api = request.args.get("api")
        
    if api =="hkscmghssdf":
          return jsonify({
            "msg":"update by kami off_server",
            "link":"https://zalo.me/g/tplcxx046",
            "code": 99 if not proxy else 0,
            "data": {} if not proxy else proxy,"last":last,
        })
    else:
                  return  "API KEY KHONG HO LE LEN HE ADMIN telegram : t.me/kami2k1 or user : kami2k1\n<br>zalo (dùng phone Tìm triên thanh tìm kiếm ) @quangz3  "

    #KAMI = "GAY HAHA GAY HAY CAY CAY CAY GAY "
    #return KAMI * 10000


threading.Thread(target=runing, daemon=True).start()


serve(app, host="0.0.0.0", port=5000, threads=500, connection_limit=10000)


