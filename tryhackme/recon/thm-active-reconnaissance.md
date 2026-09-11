# TryHackMe — Active Reconnaissance Writeup

**Platform:** TryHackMe
**Oda:** Active Reconnaissance
**Konu:** Hedef sistemle doğrudan etkileşerek bilgi toplama; temel recon araçları (web browser, ping, traceroute, telnet, netcat)

---

## Active Reconnaissance Nedir?

Active reconnaissance, bir hedef sistem veya ağ ile **doğrudan etkileşime girerek** bilgi toplamaktır. Passive recon'un aksine hedefe paket gönderdiğimiz için baştan itibaren bir iz bırakırız.

- Hedefe paket gönderdiğimiz an bilinme ve iz bırakma ihtimali başlar.
- Active recon sırasında iz bırakır; IDS, log girişleri, WAF blokları gibi tespit mekanizmalarını tetikleyebilir.
- Dikkatsiz yapılan active recon, hiçbir zarar verilmese bile başlı başına bir risk/tehdit haline gelebilir.

### İz bırakabileceğimiz / bizi yakalayabilecek savunma katmanları
- **CDN'ler** (Content Delivery Network)
- **WAF** (Web Application Firewall)
- **Zero-trust modelleri**
- **HTTPS** trafiği
- **SIEM** (Security Information and Event Management)
- **EDR** (Endpoint Detection and Response)

---

## Web Browser

Basit bir tarayıcı bile ilk recon aracı olarak kullanılabilir. Bilinmesi gereken temel port/protokol eşleşmeleri:

| Protokol | Taşıyıcı / Port |
|---|---|
| HTTP | TCP 80 |
| HTTPS | TCP 443 |
| HTTP/3 | UDP 443 — QUIC |

**Faydalı kısayol ve eklentiler:**
- `Cmd + Option + I` → Developer Tools (geliştirici araçları)
- Tarayıcı eklentileri:
  - **FoxyProxy** — proxy yönetimi
  - **User-Agent Switcher and Manager** — User-Agent değiştirme
  - **Wappalyzer** — hedef sitenin kullandığı teknolojileri tespit etme

---

## ping

`ping`, uzak bir host'a küçük bir test paketi gönderip yanıt bekleyerek hedefin erişilebilir (ayakta) olup olmadığını anlamamızı sağlar.

- **ICMP** (Internet Control Message Protocol) kullanır.
- **ICMP Echo Request (type 8)** gönderir. Hedef paketi alır ve eğer erişilebilirse cevaben **ICMP Echo Reply (type 0)** gönderir.
- Kullanımı hızlı ve hafiftir.

### Kullanım — platform farkı
| Platform | Komut |
|---|---|
| Linux / macOS | `ping -c 5 Makine_IP` (veya Host_Name) |
| Windows | `ping -n 5 Makine_IP` (veya Host_Name) |

- `-c` flag → gönderilecek paket sayısını belirtir (*specify the number of packets to send*).
- `-c` flag'i kullanılmazsa (Linux/macOS'ta) sonsuza kadar paket gönderir.

### IP sürümü seçme
```
ping -4 -c 5 Makine_IP      → IPv4
ping -6 -c 5 Makine_IPv6    → IPv6
```

### TTL
**TTL (Time To Live)** → Paket düşürülmeden (drop edilmeden) önce yönlendiriciler (router) arasında yapabileceği atlama (hop) sayısıdır.

---

## traceroute

`traceroute`, paketlerin senin sisteminden hedef host'a giderken izlediği yolu (route) izler.

- Yol üzerindeki router IP adreslerini keşfetmemizi sağlar.
- Topoloji çıkarımı için kullanılır: nerede filtreleme olduğunu bulmak, veya mapping (ağ haritalama) amacıyla değerlidir.
- Aynı rotayı her seferinde vermeyebilir — çünkü yönlendirme protokolleri (BGP, OSPF) yolu değiştirebilir.

### Nasıl çalışır (TTL mantığı)
- Traceroute, IP header'daki **TTL** değeri ile oynayarak çalışır.
- Her router, paketin TTL'ini 1 azaltır. TTL 0'a düşünce, o router paketi düşürür ve geri **ICMP Time-to-Live Exceeded** mesajı gönderir. Traceroute bu mesajları toplayarak yol üzerindeki her hop'u ortaya çıkarır.
- **Dikkat:** Bazı router'lar recon'u engellemek için ICMP TTL Exceeded mesajı göndermez; bu durumda o hop çıktıda `*` olarak görünür.

### Protokol seçenekleri
- Standart olarak **UDP** datagramları gönderir. UDP filtrelenmişse, geçmek için `-T` flag (TCP) kullanılır:
  ```
  traceroute -T IP_Adresi
  ```
- **ICMP** protokolünü kullanmak için `-I`:
  ```
  traceroute -I IP_Adresi
  ```

### İlgili araç
- **mtr** → gerçek zamanlı (real-time) yol izleme; traceroute + ping'in sürekli güncellenen birleşimi gibidir.

---

## Telnet

**TELNET (Teletype Network)**, 1969'da uzaktaki bir sisteme CLI (komut satırı) ile bağlanmak için geliştirilmiştir.

- Uzaktaki bir sunucuyu yönetmek için kullanılır; **port 23** üzerinde çalışır.
- **Güvenlik açığı:** Baştan itibaren tüm veriyi **cleartext (düz metin)** formatında gönderir. Bu veri içinde kullanıcı adı ve şifre de yer alır. Bu nedenle ağ trafiği dinlenirse (sniff) credential'lar açıkça yakalanabilir. Bu yüzden güvenli alternatif olarak **SSH** bugünün standardıdır.
- Buna rağmen recon için kullanılabilir: herhangi bir TCP portuna bağlanarak **banner grabbing** (servis banner'ını okuma / versiyon tespiti) yapılabilir.

---

## Netcat (nc)

Netcat, client olarak bir porta bağlanabilen ya da server olarak bir portu dinleyebilen çok amaçlı bir ağ aracıdır.

- **TCP ve UDP** protokollerini destekler.
- Şunlar için kullanılır: **banner grabbing**, **port probing** (port tarama), basit **file transfer** (dosya transferi), ve basit **client-server** iletişimi/haberleşme.
- **ncat** (nmap'in gelişmiş versiyonu), ekstra olarak IPv6 ve SSL şifreleme desteği sunar.

### Temel bağlantı
```
nc IP_Adresi Port
```

### Netcat ile dinleme (Listening) — bayraklar
| Flag | Anlamı |
|---|---|
| `-l` | listen mode (dinleme modu) |
| `-p` | specify port number (port numarası belirtme) |
| `-n` | numeric only — DNS çözümlemesi yapma (no DNS resolution) |
| `-v` | verbose |
| `-vv` | more verbose (daha ayrıntılı) |
| `-k` | client bağlantısı koptuktan sonra dinlemeye devam et (keep listening after the client disconnects) |

### Ekstra
- Güvenli / şifreli bağlantı için: `ncat --ssl`
- IPv6 için: `-6`
- HTTP banner almak için curl alternatifi:
  ```
  curl -I http://...    (veya https://...)
  ```

---

## Öğrenilenler / Özet

- **Active recon = iz bırakır.** Passive recon'dan farkı, hedefe doğrudan paket göndermesi ve dolayısıyla IDS/WAF/SIEM/EDR gibi savunma katmanlarınca tespit edilebilmesidir.
- **ICMP her yerde:** ping (Echo Request/Reply) ve traceroute (TTL Exceeded) aynı temel ICMP mekanizmasının farklı kullanımlarıdır. TTL kavramı ikisini de birbirine bağlar.
- **Cleartext protokoller tehlikelidir:** Telnet'in en büyük zaafı düz metin iletişimidir; bu yüzden yerini SSH almıştır — ama banner grabbing için hâlâ kullanışlıdır.
- **Netcat "İsviçre çakısı":** Tek bir araçla port tarama, banner grabbing, dosya transferi ve bağlantı dinleme yapılabiliyor; ncat ile SSL/IPv6 desteği ekleniyor.

---

## Kaynaklar
- [TryHackMe — Active Reconnaissance](https://tryhackme.com/room/activerecon)
- `ping`, `traceroute`, `telnet`, `nc`/`ncat`, `curl` man page'leri
