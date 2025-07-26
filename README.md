# 🔎 scan-proxy-zmap

Tool scan proxy HTTP bằng ZMap siêu nhanh. 

---

## 🚀 Cài đặt nhanh

```bash
apt update -y && \
apt install zmap -y && \
snap install go --classic && \
git clone https://github.com/hoangtuvungcao/scan-proxy-zmap && \
cd scan-proxy-zmap && \
go build && \
echo "✅ Done"
```
## hd dùng : 
```bash
zmap -p  [port] -w If there is an IP list, if there isn't, then that's it. -i [Network Interface] -q [off log zmap]  | ./KamiPP [port]
.... exp:

zamp -p 80 -w subnetvn -q | ./KamiPP 80
```
