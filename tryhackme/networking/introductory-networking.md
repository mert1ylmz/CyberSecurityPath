# TryHackMe: Introductory Networking

Ağın en temel katmanı — cihazlar birbiriyle nasıl konuşur, veri yolda hangi kılıklara girer, sorun olduğunda hangi araçlar ne söyler.

## OSI Modeli
Verinin kullanıcıdan çıkıp hedef cihaza ulaşana kadar geçtiği 7 katmanlı soyutlama:

1. **Physical** — fiziksel sinyal (kablo, dalga)
2. **Data Link** — MAC adresi, çerçeveler
3. **Network** — IP adresi, yönlendirme
4. **Transport** — TCP/UDP, güvenilirlik
5. **Session** — oturum yönetimi
6. **Presentation** — şifreleme, sıkıştırma
7. **Application** — HTTP, DNS, SMTP

**Neden önemli:** Bir açığın hangi katmanda olduğunu bilmek saldırıyı da savunmayı da belirliyor. ARP zehirlemesi Layer 2, TCP SYN flood Layer 4, XSS Layer 7 — tamamen farklı araçlar ve mantık.

## Encapsulation
Veri OSI'den aşağı inerken her katman kendi başlığını ekliyor, hedefe varıp yukarı çıkarken tersi oluyor.

```
Uygulama verisi → [TCP başlık][veri] → [IP başlık][TCP başlık][veri] → [Ethernet başlık][IP...][TCP...][veri]
```

Wireshark açtığında gördüğün paket yapısı tam olarak bu — bir paketi soyup katman katman incelemek encapsulation'ı anlamakla başlıyor.

## TCP/IP Modeli
Gerçekte kullanılan model. OSI teorik, TCP/IP pratik. 4 katman:

1. **Network Access** (OSI'nin 1-2)
2. **Internet** (OSI'nin 3)
3. **Transport** (OSI'nin 4)
4. **Application** (OSI'nin 5-6-7)

## Ping ve ICMP
`ping host` — bir cihazın ağda ayakta olup olmadığını test eden temel komut.

Altında **ICMP (Internet Control Message Protocol)** var — ağ cihazlarının birbirine durum ve hata bildirmesi için kullandığı protokol. Ping, ICMP Echo Request/Reply çiftini kullanıyor.

**Pentest bakışı:** Bazı ağlar ICMP'yi bloklar — bir host ping'e cevap vermiyor diye "yok" demek yanlış olabilir. Nmap'te `-Pn` (no ping) bayrağı bu yüzden var.

## Traceroute
`traceroute host` — kaynaktan hedefe giderken paketin geçtiği tüm ağ noktalarını (hop) listeliyor.

Nasıl çalışıyor: TTL değerini 1'den başlayarak artırıyor. Her router TTL'i 1 azaltıp 0'a düştüğünde "TTL expired" ICMP mesajı gönderiyor. Bu mesajları toplayarak yolu haritalıyor.

**Pentest bakışı:** Hedef ağın topolojisi hakkında ipucu veriyor — kaç router arkasında, hangi ISP, hangi coğrafya.

## WHOIS
`whois domain` — bir domain'in kayıt bilgilerini getiriyor: sahibi, kayıt tarihi, DNS sunucuları, iletişim bilgisi (GDPR sonrası çoğu gizli).

Passive recon'un temel araçlarından — hedef organizasyonun altyapı sağlayıcılarını ve kayıt tarihçesini anlamak için.

## Dig ve DNS
`dig domain` — modern DNS sorgulama aracı. `nslookup`'ın yerini aldı sayılır.

## DNS resolution akışı
Bir domain'i yazdığında ne oluyor:

1. **Local cache** — daha önce sorulmuş mu, bakılır
2. **Hosts file** — bilgisayarda manuel eşleşme var mı (`/etc/hosts` veya Windows'ta `C:\Windows\System32\drivers\etc\hosts`)
3. **Recursive DNS server** — genelde ISP'nin sunucusu veya 8.8.8.8, 1.1.1.1 gibi
4. **Root name servers** — 13 tane var, TLD sunucusunu söyler
5. **TLD servers** — `.com`, `.tr`, `.org` gibi üst düzey alan sunucuları
6. **Authoritative name server** — domain'in gerçek IP'sini bilen sunucu

Her adımda cache mekanizması var — aynı sorgu tekrar yapıldığında baştan başlanmıyor.

**Pentest bakışı:** DNS cache poisoning, DNS rebinding gibi saldırılar bu zincirin farklı noktalarını hedefliyor. Hosts file manipülasyonu da malware'in klasik hilelerinden.

## Kaynak
TryHackMe — Introductory Networking room
