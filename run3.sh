#!/bin/bash

# Danh sách port
ports=(1001 1002 1003 1004 1005 9977 8888 8443 8080 8008 8000 7070 443 3128 3128 3008 3008 1014 1080 1014 9977 10009 10008 10007 10006 10010 10001 10002 10003 10004 5109 5108 5107 5106 5105 5104 5103 5102 5101 7010 7009 7008 7007 7006 7005 7004 7003 7002 7001 4009 4008 4007 4006 4005 4004 4003 4002 3128 443 80)

# File chứa subnet
subnet_file="subnetvn"

# Giao diện mạng
iface="eth0"

# Kiểm tra file subnet tồn tại
if [ ! -f "$subnet_file" ]; then
  echo "❌ File $subnet_file không tồn tại!"
  exit 1
fi

# Lặp qua từng port
for port in "${ports[@]}"; do
  echo "🔍 Đang quét port $port (timeout 180s)..."

  (
    timeout 180 zmap -p "$port" -w "$subnet_file" -q -i "$iface" | KamiPP "$port"
  ) &

  pid=$!
  wait $pid
done

