#!/bin/bash
echo "[!] Menginstall Hunter Tools..."
pkg install python -y > /dev/null 2>&1
curl -sL https://raw.githubusercontent.com/nuixreborn-cmyk/hunter-tools/main/hunter.py -o hunter.py
echo "[!] Menjalankan Hunter Tools..."
python hunter.py
