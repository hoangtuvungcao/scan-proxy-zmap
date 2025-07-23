#!/bin/bash

# Danh sách port
ports=(1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020)

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
    timeout 180 zmap -p "$port" -w "$subnet_file" -q -i "$iface" | ./KamiPP "$port"
  ) &

  pid=$!
  wait $pid
done

