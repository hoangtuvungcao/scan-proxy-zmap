from flask import Flask, jsonify, request
from waitress import serve
import threading, subprocess, time
import select, re, os

run = True  # Thêm biến này để dừng vòng lặp nếu cần
proxy = {}
ports = sorted(set(
    list(range(10001, 10011)) +  # 10001-10010
    list(range(5101, 5111)) +    # 5101-5110
    list(range(1001, 1006)) +    # 1001-1005
    [3128, 7070] +               # port lẻ

    list(range(1001, 1010)) +
    list(range(10001, 10010)) +
    [8080, 80, 3128, 443, 8443, 1080, 8000, 8008, 8888] +
    list(range(4002, 4010)) +
    list(range(5101, 5110)) +
    [1014, 3008, 9977] +
    list(range(7001, 7010))
))

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
def runing():
    global proxy, run
    while run:
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
            "data": {} if not proxy else proxy
        })
    else:
                  return  "API KEY KHONG HO LE LEN HE ADMIN telegram : t.me/kami2k1 or user : kami2k1\n<br>zalo (dùng phone Tìm triên thanh tìm kiếm ) @quangz3  "

    #KAMI = "GAY HAHA GAY HAY CAY CAY CAY GAY "
    #return KAMI * 10000


threading.Thread(target=runing, daemon=True).start()


serve(app, host="0.0.0.0", port=5000, threads=500, connection_limit=10000)


