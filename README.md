# 🐉 Dobivorn Port Scanner v3.0

> **3 Başlı Ejderha** | Red Team | Purple Team | Blue Team

Hızlı ve güçlü port tarayıcı. TCP/UDP desteği, OS tespiti, banner grabbing, CIDR ağ taraması ve çoklu thread ile yüksek performans.

---

## ✨ Özellikler (v3.0)

| Özellik | Açıklama |
|---------|----------|
| 🔍 **OS Tespiti** | TTL değeri ile işletim sistemi tahmini |
| ⏱️ **Port Gecikmesi** | Her port için yanıt süresi (ms) |
| 📊 **CIDR Desteği** | `192.168.1.0/24` formatında ağ taraması |
| 📈 **İlerleme çubuğu** | Gerçek zamanlı tarama durumu |
| 🎯 **Gelişmiş Banner** | HTTP, SSH, FTP, SMTP için özel probe |
| 📝 **Raporlama** | JSON, CSV, TXT formatları |
| ⚡ **Multi-Thread** | 100+ thread ile hızlı tarama |
| 🔄 **TCP/UDP** | Her iki protokol desteği |

---

## 📦 Kurulum

```bash
git clone https://github.com/DobivornSec/dobivorn-portscanner.git
cd dobivorn-portscanner
pip install -r requirements.txt
```

**Gereksinimler:**
```bash
pip install colorama ipaddress
```

---

## 🚀 Kullanım

### Temel Tarama
```bash
python portscanner.py google.com
```

### Belirli Port Aralığı
```bash
python portscanner.py google.com -p 20-100
```

### UDP Tarama
```bash
python portscanner.py google.com --udp -p 53,67,68,123
```

### JSON Rapor Kaydetme
```bash
python portscanner.py google.com -o sonuc.json
```

### CIDR Ağ Taraması
```bash
python portscanner.py 192.168.1.0/24 -p 22,80,443 -o network_scan.json
```

### Tüm Özellikler
```bash
python portscanner.py github.com -p 22,80,443,3306,5432,6379,8080,8443 -t 100 -o detayli_tarama.json
```

---

## 📊 Parametreler

| Parametre | Açıklama | Varsayılan |
|-----------|----------|------------|
| `hedef` | IP, domain veya CIDR | Zorunlu |
| `-p, --ports` | Port aralığı (20-100) veya liste (22,80,443) | Popüler 80 port |
| `-t, --threads` | Thread sayısı | 50 |
| `-to, --timeout` | Zaman aşımı (saniye) | 2 |
| `-o, --output` | Çıktı dosyası | Yok |
| `--format` | json, csv, txt | json |
| `--udp` | UDP taraması | Kapalı |

---

## 📁 Örnek Çıktı

```bash
[+] Domain çözümlendi: github.com -> 140.82.121.3

╔══════════════════════════════════════════════════════════════════════════╗
║   🐉 Dobivorn Port Scanner v3.0 - 3 Başlı Ejderha                        ║
║   🔴 Red Team | 🟣 Purple Team | 🔵 Blue Team                            ║
║   ⚡ Multi-Thread | UDP | SYN Scan | OS Detect | CIDR | Banner Grab     ║
╚══════════════════════════════════════════════════════════════════════════╝

[+] Hedef: github.com
[+] IP: 140.82.121.3
[+] OS Tespiti: Linux/Unix (TTL: 64)
[+] Port sayısı: 8
[+] Thread: 100
[+] Timeout: 2s
[+] Protocol: TCP
[+] Başlangıç: 2026-04-14 15:58:50.624349

[✓] Port 80/tcp açık -> HTTP (57.44ms)
[✓] Port 443/tcp açık -> HTTPS (57.44ms)
[✓] Port 22/tcp açık -> SSH (56.32ms)

[*] Tarama tamamlandı!

╔══════════════════════════════════════════════════════════════════════════╗
║                         TARAMA ÖZETİ                                    ║
╚══════════════════════════════════════════════════════════════════════════╝
[+] Hedef: github.com (140.82.121.3)
[+] Taranan port: 8
[+] Açık port: 3
[+] Bitiş: 2026-04-14 15:58:52.633674

Açık portlar:
  → 80/tcp (HTTP) [57.44ms]
  → 443/tcp (HTTPS) [57.44ms]
  → 22/tcp (SSH) [56.32ms]

[+] JSON raporu kaydedildi: detayli_tarama.json
```

---

## 📝 Örnek JSON Rapor

```json
{
  "target": "github.com",
  "ip": "140.82.121.3",
  "os_detection": "Linux/Unix (TTL: 64)",
  "scan_time": "2026-04-14 15:58:52.633674",
  "total_ports": 8,
  "open_ports_count": 3,
  "open_ports": [
    {
      "port": 80,
      "protocol": "tcp",
      "service": "HTTP",
      "banner": "HTTP/1.1 301 Moved Permanently...",
      "response_time": 57.44
    },
    {
      "port": 443,
      "protocol": "tcp",
      "service": "HTTPS",
      "banner": null,
      "response_time": 57.44
    },
    {
      "port": 22,
      "protocol": "tcp",
      "service": "SSH",
      "banner": null,
      "response_time": 56.32
    }
  ]
}
```

---

## ⚠️ Uyarı

> Bu araç **eğitim ve yetkili testler** için geliştirilmiştir. İzinsiz kullanım yasa dışıdır. Sorumluluk kullanıcıya aittir.

---

## ⭐ Star Atmayı Unutma!

Beğendiysen GitHub'da ⭐ bırakmayı unutma!

---

## 📝 Sürüm Geçmişi

| Sürüm | Yenilikler |
|-------|------------|
| v3.0 | OS tespiti, port gecikmesi, CIDR desteği, ilerleme çubuğu, gelişmiş banner |
| v2.0 | TCP/UDP, multi-thread, JSON/CSV/TXT rapor |
| v1.0 | Temel port tarama |
