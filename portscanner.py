#!/usr/bin/env python3
import socket
import sys
import threading
from datetime import datetime
import argparse

# Renk kodları
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def banner():
    print(f"""
{BLUE}╔════════════════════════════════════════╗
║   Dobivorn Port Scanner 🐉             ║
║   Basit ve Hızlı Port Tarayıcı         ║
╚════════════════════════════════════════╝{RESET}
    """)

def get_service_name(port):
    """Port numarasına göre servis adını döndür"""
    services = {
        20: "FTP (Data)", 21: "FTP", 22: "SSH", 23: "Telnet",
        25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3",
        111: "RPC", 135: "RPC", 139: "NetBIOS", 143: "IMAP",
        443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
        1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
        5900: "VNC", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
    }
    return services.get(port, "Bilinmiyor")

def scan_port(host, port, timeout=1):
    """Tek bir portu tara"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            service = get_service_name(port)
            print(f"{GREEN}[✓] Port {port}/tcp açık     -> {service}{RESET}")
            return True
        return False
    except socket.gaierror:
        print(f"{RED}[!] Host çözümlenemedi: {host}{RESET}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Kullanıcı tarafından durduruldu.{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}[!] Hata: {e}{RESET}")
        return False

def scan_ports(host, ports, timeout=1):
    """Port listesini tara"""
    print(f"{YELLOW}[+] Hedef: {host}{RESET}")
    print(f"[+] Başlangıç zamanı: {datetime.now()}{RESET}\n")
    
    open_ports = []
    for port in ports:
        if scan_port(host, port, timeout):
            open_ports.append(port)
    
    # Özet göster
    print(f"\n{BLUE}╔════════════════════════════════════════╗")
    print(f"║              TARAMA ÖZETİ                ║")
    print(f"╚════════════════════════════════════════╝{RESET}")
    print(f"{YELLOW}[+] Hedef: {host}{RESET}")
    print(f"[+] Taranan port sayısı: {len(ports)}")
    print(f"{GREEN}[+] Açık port sayısı: {len(open_ports)}{RESET}")
    
    if open_ports:
        print(f"\n{GREEN}Açık portlar:{RESET}")
        for port in open_ports:
            service = get_service_name(port)
            print(f"  → {port}/tcp ({service})")
    
    print(f"\n{YELLOW}[+] Bitiş zamanı: {datetime.now()}{RESET}")

def main():
    banner()
    
    parser = argparse.ArgumentParser(description="Dobivorn Port Scanner - Basit Port Tarayıcı")
    parser.add_argument("hedef", help="Hedef IP adresi veya domain")
    parser.add_argument("-p", "--ports", help="Port aralığı (örn: 20-100) veya liste (örn: 22,80,443)")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Zaman aşımı saniye (varsayılan: 1)")
    
    args = parser.parse_args()
    
    # Host'u çözümle
    try:
        host = socket.gethostbyname(args.hedef)
        print(f"[+] Domain çözümlendi: {args.hedef} -> {host}")
    except:
        host = args.hedef
    
    # Port listesini belirle
    if args.ports:
        if '-' in args.ports:
            # Port aralığı (20-100)
            start, end = map(int, args.ports.split('-'))
            ports = list(range(start, end + 1))
        else:
            # Port listesi (22,80,443)
            ports = [int(p.strip()) for p in args.ports.split(',')]
    else:
        # Varsayılan popüler portlar
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 
                 443, 445, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443]
    
    # Tarama başlat
    scan_ports(host, ports, args.timeout)

if __name__ == "__main__":
    main()
