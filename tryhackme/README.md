# TryHackMe Notları ve Çözümleri

Bu dizin, TryHackMe platformunda takip edilen öğrenme yolları (**Cyber Security 101**, **Pre-Security**, **Jr Penetration Tester**) ve tamamlanan CTF makinelerine ait detaylı Türkçe notları, komut rehberlerini ve writeup'ları içermektedir.

---

## Dizin Yapısı

### 1. [CTF Odaları & Writeup'lar](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/ctf/)
- [Pickle Rick](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/ctf/pickle-rick.md) — Web keşfi, robots.txt incelemesi, komut enjeksiyonu ve sudo yetki yükseltme.
- [Surfer](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/ctf/surfer.md) — Zayıf kimlik doğrulama, dahili yönetim paneli keşfi, Burp Suite ile SSRF (Server-Side Request Forgery) istismarı.

### 2. [Networking (Ağ Temelleri & Trafik Analizi)](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/networking/)
- [Introductory Networking](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/networking/introductory-networking.md) — OSI ve TCP/IP modelleri, paket kapsülleme (encapsulation), ping, traceroute, whois ve DNS çözümleme mantığı.
- [Intro to LAN](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/networking/intro-to-lan.md) — Yerel ağ topolojileri, switch ve router mantığı, ARP protokolü, DHCP ve alt ağ (subnetting) temelleri.
- [DNS in Detail](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/networking/dns-in-detail.md) — DNS hiyerarşisi, kayıt tipleri (A, AAAA, CNAME, MX, TXT) ve pratik sorgulama araçları (`nslookup`, `dig`).
- [HTTP in Detail](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/networking/http-in-detail.md) — HTTP protokolü, istek/yanıt yapısı, HTTP metodları, durum kodları (status codes) ve cookie mekanizması.
- [Tcpdump: The Basics](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/networking/tcpdump-the-basics.md) — Komut satırından paket yakalama, libpcap, BPF filtreleri, başlık baytları, TCP bayrak filtreleme ve pcap analizi.
- [Nmap: The Basics](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/networking/nmap-the-basics.md) — Host keşfi (ARP/ICMP/TCP ping), TCP Connect vs. SYN scan, UDP taramaları, işletim sistemi/versiyon tespiti, zamanlama şablonları ve çıktı yönetimi.

### 3. [Reconnaissance (Bilgi Toplama & Keşif)](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/recon/)
- [Reconnaissance Temelleri](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/recon/reconnaissance-temelleri.md) — OSINT, pasif bilgi toplama teknikleri (DNS, Shodan, Wayback Machine, crt.sh), aktif keşif aşamaları ve WHOIS/RDAP.
- [Active Reconnaissance](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/recon/thm-active-reconnaissance.md) — Hedefle doğrudan etkileşim, ping, traceroute TTL mantığı, telnet ve netcat ile banner grabbing / port probing.
- *İlgili Araç:* Port ve servis keşfi için [Nmap: The Basics](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/networking/nmap-the-basics.md) notlarına da başvurabilirsiniz.

### 4. [Web Application Security](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/web-security/)
- [Web Application Security](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/web-security/web-application-security.md) — Web saldırı senaryoları ve OWASP Top 10 zafiyet kategorileri (Authentication, Access Control, Injection vb.).

### 5. [Scripting](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/scripting/)
- [Bash Scripting](file:///Users/mert/Projects/CyberSecurityPath/tryhackme/scripting/bash-scripting.md) — Linux ortamında otomasyon ve güvenlik araçları için temel Bash betik geliştirme.
