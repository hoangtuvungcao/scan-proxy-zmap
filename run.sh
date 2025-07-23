#!/bin/bash

for port in $(seq 1001 1010); do
  echo "🔍 Đang quét port $port (tối đa 180s)..."

  # chạy zmap và KamiPP trong nền, lưu PID
  (zmap -p $port -w subnetvn -q -i eth0 | KamiPP $port) &
  pid=$!

  # đợi tối đa 180s
  timeout=180
  while kill -0 "$pid" 2>/dev/null; do
    if [ $timeout -le 0 ]; then
      echo "⏱️ Hết giờ! Kill PID $pid"
      kill -9 "$pid" 2>/dev/null
      break
    fi
    sleep 1
    timeout=$((timeout - 1))
  done
done

