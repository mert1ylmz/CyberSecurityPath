# TryHackMe: Reconnaissance Temelleri

Pentest'in ilk aşaması: hedef hakkında bilgi toplama. İki ana yaklaşım var — pasif (hedefe dokunmadan) ve aktif (hedefle etkileşerek).

## OSINT — Open Source Intelligence
Herkesin erişebileceği açık kaynaklardan bilgi toplama ve analiz etme. Sosyal medya, arama motorları, kamu kayıtları, açık iş ilanları, GitHub commit'leri — hepsi OSINT.

**Neden güçlü:** Yasal, tespit edilemez, ucuz. Bir şirketin kullandığı teknoloji stack'ini iş ilanlarından çıkarabilirsin ("Django deneyimi aranır" → backend Django). Bir çalışanın LinkedIn'inden yönetici zincirini haritalayabilirsin (spear phishing için). GitHub'da bırakılmış API key'ler, `.env` dosyaları — hepsi OSINT.

## Passive Reconnaissance
Hedeften bilgi toplarken **hedefe hiç paket göndermeden** çalışan yöntemler. Tespit edilmesi imkânsıza yakın.

Yaklaşımlar:

- **Açık DNS kayıtlarını sorgulama** — DNSDumpster, VirusTotal, SecurityTrails gibi third-party servisler DNS geçmişini kayıt altında tutuyor
- **Sertifika şeffaflık logları** — crt.sh üzerinden domain için verilmiş tüm SSL sertifikalarına bakmak. Subdomain keşfinin en etkili yollarından biri, çünkü organizasyonlar sertifika alırken subdomain'i açık ediyor
- **İnternet arşivinden geçmiş versiyonlar** — Wayback Machine'de sitenin eski versiyonlarına bakmak. Eskiden açık olan endpoint, silinmiş belge, değişmiş yapı görülüyor
- **Shodan ve Censys** — internete açık cihaz ve servisleri indeksleyen arama motorları. "Bu şirkete ait açık RDP portu var mı?" gibi soruların cevabını verir
- **GitHub repo taraması** — organizasyonun public repo'larında hassas veri (API key, şifre, konfigürasyon) aramak. `truffleHog`, `gitleaks` gibi araçlar bunu otomatize ediyor
- **WHOIS kayıtları** — domain sahiplik bilgisi, kayıt tarihi

## Active Reconnaissance
Hedefe **doğrudan paket göndererek** bilgi toplamak. Etkili ama tespit edilebilir — log'lara düşüyor, IDS/IPS uyarısı tetikleyebiliyor.

Yaklaşımlar:

- **Host discovery** — ağdaki hangi cihazlar ayakta? Ping sweep, ARP scan
- **Port scanning** — hangi portlar açık? Nmap standart araç
- **Web uygulaması ile etkileşim** — direktif keşfi (`gobuster`, `ffuf`), form testing, API endpoint fuzzing
- **Social engineering** — sahte mail, telefon, fiziksel yaklaşım
- **Physical approach** — tailgating, USB drop, kablo takma

## WHOIS
Domain kayıt bilgilerini sorgulama protokolü. **TCP port 43** üzerinden çalışıyor — query/response modeli.

Dönen bilgiler:
- **Registrar** — domain'i kimden alınmış (GoDaddy, Namecheap, Google Domains)
- **Registrant contact info** — sahibinin iletişim bilgisi (GDPR sonrası çoğu gizleniyor)
- **Dates** — kayıt, güncelleme, sona erme tarihleri
- **Name servers** — domain'in DNS'ini yöneten sunucular
- **Status code** — domain'in durumu (aktif, transfer kilidi, silme bekleniyor)
- **Abuse contact** — kötüye kullanım bildirimi için iletişim

**Neden değerli:** Bir domain'in ne zaman alındığı, hangi sağlayıcı kullanıldığı, iletişim iznesizliği bile hedef hakkında ipucu. Yeni alınmış domain phishing altyapısı olabilir.

## RDAP — WHOIS'in modern muadili
WHOIS eski bir protokol (1982) ve standart bir çıktı formatı yok — her registrar farklı text döndürüyor. **RDAP (Registration Data Access Protocol)** modern alternatif:

- HTTP üzerinden JSON döndürüyor — makine okunabilir
- WHOIS'ten daha yapılandırılmış veri koruması sağlıyor
- `curl` gibi standart HTTP araçlarıyla sorgulanabiliyor

Örnek:
```
curl https://rdap.verisign.com/com/v1/domain/tryhackme.com
```

**Neden geçiş yavaş:** WHOIS hâlâ her yerde çalışıyor, RDAP daha yeni. Ama uzun vadede WHOIS'in yerini alması bekleniyor.

## Recon iş akışı
Gerçek bir pentest'te sıra genelde şöyle:

1. **Pasif OSINT** — organizasyonun genel yapısını çıkar, hiç dokunma
2. **Pasif DNS/sertifika taraması** — subdomain listesi
3. **Aktif host discovery** — hangi subdomain gerçekten canlı
4. **Port scanning** — canlı hostlarda hangi servisler
5. **Servis fingerprinting** — servislerin versiyonları
6. **Uygulama seviyesi** — web'de path enumeration, API keşfi

Her aşama bir sonrakine input veriyor. Aşamayı atlamak zaman kaybı, sürpriz getiriyor.

## Kaynak
TryHackMe — Passive Reconnaissance & Active Reconnaissance rooms
