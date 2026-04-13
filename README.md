# Dobivorn Port Scanner 🐉

Basit ve hızlı bir TCP port tarayıcı. Hedef IP veya domain'in açık portlarını tespit eder.

## Özellikler

- 🔍 Tek hedef (IP veya domain)
- 📋 Varsayılan popüler port listesi (23 port)
- 🎯 Özel port listesi veya aralığı belirleme
- ⏱️ Zaman aşımı ayarı
- 🎨 Renkli terminal çıktısı

## Kurulum

```bash
git clone https://github.com/DobivornSec/dobivorn-portscanner.git
cd dobivorn-portscanner
# requirements.txt gerekmez, pure Python

## Kullanım 

# Varsayılan portlarla tarama
python3 portscanner.py example.com

# Belirli portları tara
python3 portscanner.py google.com -p 80,443,22

# Port aralığı tara
python3 portscanner.py 192.168.1.1 -p 20-100

# Zaman aşımı belirle
python3 portscanner.py tesla.com -t 2

## Örnek Çıktı

[✓] Port 80/tcp açık     -> HTTP
[✓] Port 443/tcp açık    -> HTTPS

Açık portlar:
  → 80/tcp (HTTP)
  → 443/tcp (HTTPS)
  
## Yapılacaklar

    Thread desteği (hızlandırma)

    UDP tarama

    Banner grabbing (servis versiyonu)

    Çıktıyı dosyaya kaydetme
