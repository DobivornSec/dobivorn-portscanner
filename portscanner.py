#!/usr/bin/env python3
"""
Dobivorn Port Scanner v2.0 🐉
3 Başlı Ejderha | Red Team | Purple Team | Blue Team

Özellikler:
- Çoklu thread desteği (hızlı tarama)
- TCP ve UDP tarama
- Banner grabbing (servis versiyonu)
- JSON/CSV/TXT raporlama
- Servis tanıma
- Renkli çıktı
"""

import socket
import sys
import threading
from datetime import datetime
import argparse
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style
import time

# Renkleri başlat
init(autoreset=True)

# Banner
BANNER = f"""
{Fore.BLUE}╔══════════════════════════════════════════════════════════════╗
║   🐉 Dobivorn Port Scanner v2.0 - 3 Başlı Ejderha              ║
║   🔴 Red Team | 🟣 Purple Team | 🔵 Blue Team                ║
║   ⚡ Multi-Thread | UDP | Banner Grab | JSON/CSV             ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# Servis ve port eşleştirme
SERVICES = {
    20: "FTP (Data)", 21: "FTP", 22: "SSH", 23: "Telnet",
    25: "SMTP", 53: "DNS", 67: "DHCP", 68: "DHCP",
    69: "TFTP", 80: "HTTP", 110: "POP3", 111: "RPC",
    123: "NTP", 135: "RPC", 137: "NetBIOS-NS", 138: "NetBIOS-DGM",
    139: "NetBIOS-SSN", 143: "IMAP", 161: "SNMP", 162: "SNMP-Trap",
    179: "BGP", 389: "LDAP", 443: "HTTPS", 445: "SMB",
    465: "SMTPS", 514: "Syslog", 587: "SMTP", 636: "LDAPS",
    873: "Rsync", 993: "IMAPS", 995: "POP3S", 1080: "SOCKS",
    1194: "OpenVPN", 1352: "Lotus Notes", 1433: "MSSQL", 1434: "MSSQL-Mon",
    1521: "Oracle", 1723: "PPTP", 1883: "MQTT", 2049: "NFS",
    2181: "ZooKeeper", 2375: "Docker", 2376: "Docker SSL",
    2379: "etcd", 2380: "etcd", 3306: "MySQL", 3389: "RDP",
    3690: "SVN", 4369: "EPMD", 5000: "UPnP", 5222: "XMPP",
    5432: "PostgreSQL", 5672: "AMQP", 5666: "NRPE", 5850: "VNC",
    5900: "VNC", 5901: "VNC", 5984: "CouchDB", 5985: "WinRM",
    5986: "WinRM", 6000: "X11", 6379: "Redis", 6667: "IRC",
    7001: "WebLogic", 7199: "Cassandra", 8000: "HTTP-Alt", 8008: "HTTP-Alt",
    8009: "AJP", 8080: "HTTP-Alt", 8086: "InfluxDB", 8087: "HTTP-Alt",
    8089: "HTTP-Alt", 8090: "HTTP-Alt", 8091: "Couchbase", 8140: "Puppet",
    8443: "HTTPS-Alt", 8883: "MQTT SSL", 8888: "HTTP-Alt", 9000: "Portainer",
    9042: "Cassandra", 9090: "Prometheus", 9092: "Kafka", 9100: "NodeExporter",
    9200: "Elasticsearch", 9300: "Elasticsearch", 9418: "Git", 9999: "Zabbix",
    10000: "Webmin", 11211: "Memcached", 12345: "NetBus", 15672: "RabbitMQ",
    16010: "HBase", 18080: "Spark", 20000: "DHS", 25565: "Minecraft",
    27017: "MongoDB", 27018: "MongoDB", 27019: "MongoDB", 28017: "MongoDB",
    31337: "Back Orifice", 50000: "MongoDB", 50070: "Hadoop", 60010: "HBase"
}

class PortScanner:
    def __init__(self, host, ports, threads=50, timeout=2, udp=False, output=None, format='json'):
        self.host = host
        self.ports = ports
        self.threads = threads
        self.timeout = timeout
        self.udp = udp
        self.output = output
        self.format = format
        self.open_ports = []
        self.lock = threading.Lock()
        
    def get_service_name(self, port):
        """Port numarasına göre servis adını döndür"""
        return SERVICES.get(port, "Bilinmiyor")
    
    def grab_banner(self, ip, port, protocol='tcp'):
        """Banner grabbing (servis versiyonu)"""
        try:
            if protocol == 'tcp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((ip, port))
                sock.send(b"\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                sock.close()
                return banner[:100]
            else:
                # UDP için basit test
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(3)
                sock.sendto(b"\r\n", (ip, port))
                data, _ = sock.recvfrom(1024)
                banner = data.decode('utf-8', errors='ignore').strip()
                sock.close()
                return banner[:100]
        except:
            return None
    
    def scan_port_tcp(self, ip, port):
        """TCP port taraması"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                service = self.get_service_name(port)
                banner = self.grab_banner(ip, port, 'tcp')
                
                result_data = {
                    'port': port,
                    'protocol': 'tcp',
                    'service': service,
                    'banner': banner,
                    'status': 'open'
                }
                
                # Renkli çıktı
                if banner:
                    print(f"{Fore.GREEN}[✓] Port {port}/tcp açık -> {service} [{banner[:50]}]{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}[✓] Port {port}/tcp açık -> {service}{Style.RESET_ALL}")
                
                return result_data
        except:
            pass
        return None
    
    def scan_port_udp(self, ip, port):
        """UDP port taraması"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            sock.sendto(b"\r\n", (ip, port))
            data, _ = sock.recvfrom(1024)
            sock.close()
            
            if data:
                service = self.get_service_name(port)
                banner = data.decode('utf-8', errors='ignore')[:100]
                
                result_data = {
                    'port': port,
                    'protocol': 'udp',
                    'service': service,
                    'banner': banner,
                    'status': 'open'
                }
                
                print(f"{Fore.CYAN}[✓] Port {port}/udp açık -> {service} [{banner[:50]}]{Style.RESET_ALL}")
                return result_data
        except socket.timeout:
            pass
        except:
            pass
        return None
    
    def scan_ports(self):
        """Çoklu thread ile port taraması"""
        print(BANNER)
        print(f"{Fore.YELLOW}[+] Hedef: {self.host}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] IP: {self.ip}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Port sayısı: {len(self.ports)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Thread: {self.threads}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Timeout: {self.timeout}s{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Protocol: {'UDP' if self.udp else 'TCP'}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Başlangıç: {datetime.now()}{Style.RESET_ALL}\n")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            if self.udp:
                futures = {executor.submit(self.scan_port_udp, self.ip, port): port for port in self.ports}
            else:
                futures = {executor.submit(self.scan_port_tcp, self.ip, port): port for port in self.ports}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    with self.lock:
                        self.open_ports.append(result)
        
        self.generate_report()
    
    def generate_report(self):
        """Rapor oluştur"""
        print(f"\n{Fore.BLUE}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    TARAMA ÖZETİ                                      ║")
        print(f"╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}[+] Hedef: {self.host} ({self.ip}){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Taranan port: {len(self.ports)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Açık port: {len(self.open_ports)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Bitiş: {datetime.now()}{Style.RESET_ALL}")
        
        if self.open_ports:
            print(f"\n{Fore.GREEN}Açık portlar:{Style.RESET_ALL}")
            for result in self.open_ports:
                banner_info = f" - {result['banner']}" if result.get('banner') else ""
                print(f"  → {result['port']}/{result['protocol']} ({result['service']}){banner_info}")
        
        # Dosyaya kaydet
        if self.output:
            if self.format == 'json':
                with open(self.output, 'w', encoding='utf-8') as f:
                    json.dump({
                        'target': self.host,
                        'ip': self.ip,
                        'scan_time': str(datetime.now()),
                        'total_ports': len(self.ports),
                        'open_ports_count': len(self.open_ports),
                        'open_ports': self.open_ports
                    }, f, indent=2, ensure_ascii=False)
                print(f"\n{Fore.GREEN}[+] JSON raporu kaydedildi: {self.output}{Style.RESET_ALL}")
            elif self.format == 'csv':
                with open(self.output, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['port', 'protocol', 'service', 'banner'])
                    writer.writeheader()
                    for r in self.open_ports:
                        writer.writerow({
                            'port': r['port'],
                            'protocol': r['protocol'],
                            'service': r['service'],
                            'banner': r.get('banner', '')
                        })
                print(f"\n{Fore.GREEN}[+] CSV raporu kaydedildi: {self.output}{Style.RESET_ALL}")
            elif self.format == 'txt':
                with open(self.output, 'w', encoding='utf-8') as f:
                    f.write(f"Target: {self.host} ({self.ip})\n")
                    f.write(f"Scan Time: {datetime.now()}\n")
                    f.write(f"Total Ports: {len(self.ports)}\n")
                    f.write(f"Open Ports: {len(self.open_ports)}\n\n")
                    for r in self.open_ports:
                        f.write(f"{r['port']}/{r['protocol']} - {r['service']}")
                        if r.get('banner'):
                            f.write(f" - {r['banner']}")
                        f.write("\n")
                print(f"\n{Fore.GREEN}[+] TXT raporu kaydedildi: {self.output}{Style.RESET_ALL}")
    
    def run(self):
        """Tarama başlat"""
        # Host'u çözümle
        try:
            self.ip = socket.gethostbyname(self.host)
            print(f"{Fore.GREEN}[+] Domain çözümlendi: {self.host} -> {self.ip}{Style.RESET_ALL}")
        except:
            self.ip = self.host
            print(f"{Fore.YELLOW}[+] IP: {self.ip}{Style.RESET_ALL}")
        
        self.scan_ports()

def parse_ports(port_str):
    """Port listesini parse et"""
    ports = []
    if '-' in port_str:
        start, end = map(int, port_str.split('-'))
        ports = list(range(start, end + 1))
    else:
        ports = [int(p.strip()) for p in port_str.split(',')]
    return ports

def main():
    parser = argparse.ArgumentParser(
        description="Dobivorn Port Scanner v2.0 - Hızlı Port Tarayıcı",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python portscanner.py example.com
  python portscanner.py 192.168.1.1 -p 20-100 -t 50
  python portscanner.py google.com -p 22,80,443
  python portscanner.py example.com --udp
  python portscanner.py example.com -o sonuc.json
  python portscanner.py example.com -o sonuc.csv --format csv
        """
    )
    
    parser.add_argument("hedef", help="Hedef IP adresi veya domain")
    parser.add_argument("-p", "--ports", help="Port aralığı (örn: 20-100) veya liste (örn: 22,80,443)")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Thread sayısı (varsayılan: 50)")
    parser.add_argument("-to", "--timeout", type=int, default=2, help="Zaman aşımı saniye (varsayılan: 2)")
    parser.add_argument("-o", "--output", help="Çıktı dosyası (JSON/CSV/TXT)")
    parser.add_argument("--format", choices=['json', 'csv', 'txt'], default='json', help="Çıktı formatı (varsayılan: json)")
    parser.add_argument("--udp", action="store_true", help="UDP port taraması yap")
    
    args = parser.parse_args()
    
    # Port listesini belirle
    if args.ports:
        ports = parse_ports(args.ports)
    else:
        # Varsayılan popüler portlar
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 
                 443, 445, 465, 587, 993, 995, 1080, 1194, 1352, 1433,
                 1521, 1723, 1883, 2049, 2181, 2375, 2376, 2379, 2380,
                 3306, 3389, 3690, 4369, 5432, 5672, 5900, 5901, 5984,
                 5985, 5986, 6379, 6667, 7001, 7199, 8000, 8008, 8009,
                 8080, 8086, 8087, 8088, 8089, 8090, 8091, 8140, 8443,
                 8883, 8888, 9000, 9042, 9090, 9092, 9100, 9200, 9300,
                 9418, 9999, 10000, 11211, 15672, 16010, 18080, 25565,
                 27017, 27018, 27019, 28017, 31337, 50000, 50070, 60010]
    
    # Tarama başlat
    scanner = PortScanner(
        host=args.hedef,
        ports=ports,
        threads=args.threads,
        timeout=args.timeout,
        udp=args.udp,
        output=args.output,
        format=args.format
    )
    
    try:
        scanner.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Kullanıcı tarafından durduruldu!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
