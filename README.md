# 🐉 Dobivorn Port Scanner v2.0

> **3 Başlı Ejderha** | Red Team | Purple Team | Blue Team

Hedef IP veya domain'in açık portlarını **hızlı** ve **profesyonel** bir şekilde tespit eden port tarayıcı. Çoklu thread, banner grabbing, UDP desteği ve JSON/CSV/TXT raporlama ile donatılmıştır.

---

## ✨ Özellikler

| Özellik | Açıklama |
|---------|----------|
| ⚡ **Çoklu Thread** | 50+ thread ile hızlı tarama |
| 🔍 **TCP Tarama** | Full TCP port taraması |
| 🌐 **UDP Tarama** | UDP port desteği (opsiyonel) |
| 📋 **Banner Grabbing** | Servis versiyonu tespiti |
| 🎯 **Servis Tanıma** | 100+ port için servis eşleştirmesi |
| 📊 **Raporlama** | JSON, CSV, TXT formatları |
| 🎨 **Renkli Çıktı** | Durum bazlı renklendirme |
| ⏱️ **Zaman Aşımı** | Ayarlanabilir timeout |

---

## 📦 Kurulum

```bash
git clone https://github.com/DobivornSec/dobivorn-portscanner.git
cd dobivorn-portscanner
pip install -r requirements.txt
```

**Gereksinimler:**
```bash
pip install colorama
```

---

## 🚀 Kullanım

### Temel tarama (varsayılan 83 popüler port)
```bash
python portscanner.py example.com
```

### Belirli portları tara
```bash
python portscanner.py google.com -p 22,80,443
```

### Port aralığı tara
```bash
python portscanner.py 192.168.1.1 -p 20-100
```

### Thread sayısı ve timeout ayarı
```bash
python portscanner.py example.com -t 100 -to 1
```

### UDP port taraması
```bash
python portscanner.py example.com --udp
```

### JSON rapor kaydetme
```bash
python portscanner.py google.com -o sonuc.json
```

### CSV rapor kaydetme
```bash
python portscanner.py google.com -o sonuc.csv --format csv
```

### TXT rapor kaydetme
```bash
python portscanner.py google.com -o sonuc.txt --format txt
```

---

## 📊 Örnek Çıktı

```bash
╔══════════════════════════════════════════════════════════════╗
║   🐉 Dobivorn Port Scanner v2.0 - 3 Başlı Ejderha              ║
║   🔴 Red Team | 🟣 Purple Team | 🔵 Blue Team                ║
║   ⚡ Multi-Thread | UDP | Banner Grab | JSON/CSV             ║
╚══════════════════════════════════════════════════════════════╝

[+] Domain çözümlendi: google.com -> 172.217.16.142
[+] Hedef: google.com
[+] IP: 172.217.16.142
[+] Port sayısı: 83
[+] Thread: 50
[+] Timeout: 2s
[+] Protocol: TCP
[+] Başlangıç: 2026-04-14 13:03:24

[✓] Port 80/tcp açık -> HTTP
[✓] Port 443/tcp açık -> HTTPS

╔══════════════════════════════════════════════════════════════╗
║                    TARAMA ÖZETİ                             ║
╚══════════════════════════════════════════════════════════════╝
[+] Hedef: google.com (172.217.16.142)
[+] Taranan port: 83
[+] Açık port: 2
[+] Bitiş: 2026-04-14 13:03:28

Açık portlar:
  → 80/tcp (HTTP)
  → 443/tcp (HTTPS)

[+] JSON raporu kaydedildi: sonuc.json
```

---

## 🔧 Parametreler

| Parametre | Açıklama | Varsayılan |
|-----------|----------|------------|
| `hedef` | Hedef IP veya domain | Zorunlu |
| `-p, --ports` | Port aralığı (20-100) veya liste (22,80,443) | 83 popüler port |
| `-t, --threads` | Thread sayısı | 50 |
| `-to, --timeout` | Zaman aşımı (saniye) | 2 |
| `-o, --output` | Çıktı dosyası | Yok |
| `--format` | Çıktı formatı (json/csv/txt) | json |
| `--udp` | UDP taraması | Kapalı |

---

## 📁 Varsayılan Tarama Portları (83 port)

| Port | Servis | Port | Servis |
|------|--------|------|--------|
| 21 | FTP | 80 | HTTP |
| 22 | SSH | 443 | HTTPS |
| 23 | Telnet | 445 | SMB |
| 25 | SMTP | 993 | IMAPS |
| 53 | DNS | 995 | POP3S |
| 110 | POP3 | 3306 | MySQL |
| 111 | RPC | 3389 | RDP |
| 139 | NetBIOS | 5432 | PostgreSQL |
| 143 | IMAP | 5900 | VNC |
| 443 | HTTPS | 8080 | HTTP-Alt |

... ve 70+ port daha

---

## 🚀 Performans

| Mod | Hız | Açıklama |
|-----|-----|----------|
| **TCP** | 50-100 port/saniye | Thread sayısına bağlı |
| **UDP** | 10-30 port/saniye | Daha yavaş, timeout bekler |

---

## 📊 Rapor Örnekleri

### JSON Rapor (`sonuc.json`)
```json
{
  "target": "google.com",
  "ip": "172.217.16.142",
  "scan_time": "2026-04-14 13:04:59",
  "total_ports": 83,
  "open_ports_count": 2,
  "open_ports": [
    {"port": 80, "protocol": "tcp", "service": "HTTP"},
    {"port": 443, "protocol": "tcp", "service": "HTTPS"}
  ]
}
```

### CSV Rapor (`sonuc.csv`)
```csv
port,protocol,service,banner
443,tcp,HTTPS,
80,tcp,HTTP,
```

### TXT Rapor (`sonuc.txt`)
```text
Target: google.com (172.217.16.142)
Scan Time: 2026-04-14 13:05:31
Total Ports: 83
Open Ports: 2

443/tcp - HTTPS
80/tcp - HTTP
```

---

## ⚠️ Uyarı

> Bu araç **eğitim ve yetkili testler** için geliştirilmiştir. İzinsiz tarama yapmak yasa dışı olabilir. Sorumluluk kullanıcıya aittir.

## ⭐ Star Atmayı Unutma!

Beğendiysen GitHub'da ⭐ bırakmayı unutma!
