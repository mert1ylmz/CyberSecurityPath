# TryHackMe: Nmap : The Basics

Bu doküman, TryHackMe platformundaki **Nmap: The Basics** odasına ait teorik ve pratik notları, host keşfi, port tarama teknikleri, servis/işletim sistemi tespiti, zamanlama şablonları ve çıktı yönetimi konularını içermektedir.

**Platform:** TryHackMe  
**Oda:** Nmap: The Basics ([tryhackme.com/room/nmap01](https://tryhackme.com/room/nmap01))  
**Kategori:** Networking / Reconnaissance / Port Scanning  

---

## 1. Giriş (Introduction)

**Nmap (Network Mapper)**, ağ keşfi ve güvenlik denetimi için geliştirilmiş açık kaynaklı bir ağ tarayıcısıdır. Sistem yöneticileri ve sızma testi uzmanları tarafından; ağdaki canlı cihazları (host discovery), bu cihazlarda açık olan portları, çalışan servisleri ve versiyonlarını, ayrıca işletim sistemlerini tespit etmek amacıyla yaygın olarak kullanılır.

---

## 2. Host Keşfi: Kimler Çevrimiçi? (Host Discovery : Who is Online?)

Nmap ile hedef sistemler tekil veya bloklar halinde farklı biçimlerde tanımlanabilir:
* **IP Aralığı (Range):** `192.168.0.1-10`
* **Alt Ağ / Subnet (CIDR):** `192.168.0.1/24` *(192.168.0.1 ile 192.168.0.254 arası tüm adresler)*
* **Alan Adı (Hostname):** `example.com`

Ağ üzerindeki canlı hostları port taraması yapmadan hızlıca tespit etmek için `-sn` (No port scan / Ping sweep) bayrağı kullanılır.

### Doğrudan Bağlı "Yerel" Ağ Taraması (Scanning a "Local" Network)
```bash
nmap -sn 192.168.66.0/24
```
* Doğrudan bağlı olunan yerel ağda (aynı broadcast domain) Nmap, hedeflere **ARP istekleri** gönderir.
* Bir cihaz ARP isteğine cevap verirse, Nmap o cihazı anında `"Host is up"` olarak etiketler. Bu yöntem son derece hızlı ve güvenilirdir çünkü yerel ağda ARP engellenemez.

### Uzak Ağ Taraması (Scanning a Remote Network)
```bash
nmap -sn 192.168.11.0/24
```
* Arada en az bir yönlendirici (router) bulunan ağlar "remote network" olarak adlandırılır.
* Uzak ağlarda ARP kullanılamaz. Nmap canlı cihazları bulmak için sıralı olarak şu paketleri gönderir:
  1. **ICMP Echo Request** (`ping`)
  2. **ICMP Timestamp Request**
  3. **TCP SYN** paketi (varsayılan olarak port `443`'e)
  4. **TCP ACK** paketi (varsayılan olarak port `80`'e)
* Bu problardan herhangi birine yanıt gelirse hedef canlı kabul edilir.

### Hedefleri Taramadan Listeleme (List Scan)
`-sL` bayrağı, hedeflere hiçbir paket göndermeksizin yalnızca DNS çözümlemesi (reverse DNS lookup) yaparak hedefleri listeler:
```bash
nmap -sL 192.168.0.1/24
```

### Lab Soru ve Çözümü:

> **Soru:** Tarama hedefiniz `192.168.0.1/27` olduğunda taranacak son IP adresi hangisidir?  
> **Açıklama & Hesaplama:**  
> * CIDR `/27` alt ağ maskesi: `255.255.255.224` (`11111111.11111111.11111111.11100000`)
> * Kalan host bit sayısı: `32 - 27 = 5` bit
> * Blok boyutu: `2^5 = 32` IP adresi
> * Alt ağ aralığı: `192.168.0.0` (Network ID) ile `192.168.0.31` (Broadcast ID) arasındadır.  
> **Cevap:** `192.168.0.31`

---

## 3. Port Taraması: Kim Dinliyor? (Port Scanning : Who is Listening)

Canlı hostlar keşfedildikten sonra, hangi ağ servislerinin bu sistemleri dinlediğini bulmak için port taraması gerçekleştirilir.

### TCP Connect Scan (`-sT`)
* Hedefteki her bir port için tam bir **TCP 3-Way Handshake** (Üçlü El Sıkışma) gerçekleştirir.
* Akış:
  1. İstemci `---SYN--->` Hedef
  2. Hedef `---SYN/ACK--->` İstemci (Port açıksa)
  3. İstemci `---ACK--->` Hedef
* Bağlantı tamamlandıktan sonra Nmap bağlantıyı `RST` paketi ile temiz şekilde kapatır.
* **Avantajı:** Root/yönetici ayrıcalığı gerektirmez; standart kullanıcı hesabı ile çalıştırılabilir.
* **Dezavantajı:** Tam bağlantı kurulduğu için hedef sistemin uygulama loglarında kolaylıkla iz bırakır.

### TCP SYN Scan / Stealth Scan (`-sS`)
* Varsayılan ve en popüler tarama türüdür. Tam bir bağlantı kurmaz (Half-Open Scan).
* **Akış:**
  1. İstemci `---SYN--->` Hedef
  2. Hedef `---SYN/ACK--->` İstemci (Port açıksa)
  3. İstemci `---RST--->` Hedef (Bağlantı tamamlanmadan derhal sıfırlanır)
* Port kapalıysa hedef doğrudan `RST` yanıtı döner.
* **Gereksinim:** Ham soket (raw socket) paketleri oluşturabilmek için `sudo` / `root` yetkisi gerektirir.

### UDP Port Taraması (`-sU`)
* UDP bağlantısız (connectionless) bir protokoldür; el sıkışma mekanizması yoktur.
* Nmap hedefe boş UDP paketleri gönderir:
  * Eğer hedeften **ICMP Port Unreachable (Type 3, Code 3)** yanıtı gelirse portun **kapalı** olduğu anlaşılır.
  * Yanıt gelmezse port **open|filtered** olarak değerlendirilir.
* UDP taramaları işletim sistemlerinin ICMP yanıt limitleri (rate-limiting) nedeniyle TCP'ye göre belirgin şekilde daha yavaştır.

### Hedef Portları Sınırlama (Limiting Target Ports)
Nmap varsayılan olarak en popüler 1.000 portu tarar.
* `-F` — **Fast Mode:** En yaygın 100 portu tarar.
* `-p <port-aralığı>` — Özel port veya aralık belirtir:
  * `-p 22,80,443`
  * `-p 10-1024`
  * `-p-25` (1'den 25'e kadar)
  * `-p-` (1'den 65535'e kadar tüm portlar)

### Lab Soru ve Çözümleri:

> **Soru 1:** `10.114.128.179` hedef sisteminde kaç adet açık TCP portu bulunmaktadır?  
> **Komut:**
> ```bash
> nmap -sT 10.114.128.179
> ```
> **Cevap:** `6`

> **Soru 2:** `10.114.128.179` üzerindeki dinleyen web sunucusunu bulun ve tarayıcınızla erişin. Ana sayfadaki bayrak (flag) nedir?  
> **Komut:**
> ```bash
> nmap -sS 10.114.128.179
> ```
> *(Tarama çıktısında standart dışı web portu `8008` açık olarak tespit edildi.)*  
> **Erişim:** `http://10.114.128.179:8008`  
> **Cevap:** Port 8008 üzerindeki web sayfası içeriğinde yer alan flag.

---

## 4. Versiyon & İşletim Sistemi Tespiti (Version Detection)

### İşletim Sistemi Tespiti (OS Detection)
Hedef sistemin TCP/IP yığınına (stack fingerprinting) gönderilen özel paketlere verilen yanıtları analiz ederek işletim sistemini tahmin eder:
```bash
nmap -sS -O 192.168.124.111
```

### Servis ve Versiyon Tespiti (Service and Version Detection)
Açık portlarda dinleyen uygulamaların banner ve protokol yanıtlarını sorgulayarak tam sürüm numarasını çıkarır:
```bash
nmap -sS -sV 192.168.124.111
```

* **Agresif Tarama (`-A`):** OS tespiti (`-O`), versiyon tespiti (`-sV`), varsayılan NSE scriptleri (`-sC`) ve traceroute işlemlerini tek bayrakla etkinleştirir.
* **Ping Kontrolünü Atlama (`-Pn`):** Hedef sistem ICMP paketlerini engellese bile hedefin canlı olduğunu varsayar ve doğrudan port taramasına geçer.

### Lab Soru ve Çözümü:

> **Soru:** `10.114.128.179` hedefinde çalışan web sunucusunun adı ve tespit edilen sürümü nedir?  
> **Komut:**
> ```bash
> nmap -sV -p 8007-8009 10.114.128.179
> ```
> **Cevap:** `lighttpd 1.4.74`

---

## 5. Zamanlama ve Performans Kontrolü (Timing & Performance)

Tarama hızını ve gürültüsünü (noise) ayarlamak IDS/IPS atlatma ve ağ tıkanıklığını önleme açısından kritiktir.

### Zamanlama Şablonları (`-T0` - `-T5`)
```bash
nmap -sS 10.114.128.179 -T<seviye>
```

| Şablon | İsim | Yaklaşık Süre / Davranış | Kullanım Amacı |
|---|---|---|---|
| `-T0` | `paranoid` | Saatler sürer (örn. ~9.8 saat) | IDS atlatma, aşırı yavaş ve sessiz |
| `-T1` | `sneaky` | ~27.59 dakika | Güvenlik duvarı/IDS alarmı düşürme |
| `-T2` | `polite` | ~40.56 saniye | Ağı yormamak, bant genişliğini korumak |
| `-T3` | `normal` | ~0.13 saniye | Nmap varsayılan zamanlama modu |
| `-T4` | `aggressive` | ~0.11 saniye | Hızlı ve güvenilir yerel/lab ağları |
| `-T5` | `insane` | Çok hızlı | Paket kaybı riski yüksek, son derece gürültülü |

### Ek İnce Ayar Parametreleri:
* `--min-parallelism <sayı>` / `--max-parallelism <sayı>` — Paralel olarak yürütülecek probe sayısını kontrol eder.
* `--min-rate <sayı>` / `--max-rate <sayı>` — Saniyede gönderilecek minimum/maksimum paket sayısını belirler.
* `--host-timeout <süre>` — Bir hedef için harcanacak maksimum bekleme süresini ayarlar.

> **Soru:** `T4` zamanlama şablonunun sayısal olmayan karşılığı nedir?  
> **Cevap:** `-T aggressive`

---

## 6. Çıktı Yönetimi: Gördüklerinizi Kontrol Edin (Output)

### Ayrıntı ve Hata Ayıklama (Verbosity & Debugging)
* `-v`, `-vv`, `-vvv` — Çıktıdaki ayrıntı seviyesini artırır.
* `-d`, `-d2`, `-d9` — Hata ayıklama (debugging) çıktısını açar (`-d9` maksimum düzey).

### Tarama Raporunu Kaydetme Formatları
* `-oN <dosya>` — Standart insan tarafından okunabilir normal metin formatı.
* `-oX <dosya>` — XML formatı (otomasyon araçları ve raporlama için).
* `-oG <dosya>` — Grepable format (tek satırlık, `grep`/`awk`/`cut` ile ayrıştırmaya uygun).
* `-oA <dosya-öneki>` — Normal, XML ve Grepable formatlarının hepsini tek seferde kaydeder.

### Lab Soru ve Çözümleri:

> **Soru 1:** Hata ayıklama (debugging) için komuta hangi seçeneği eklemeniz gerekir?  
> **Cevap:** `-d`

> **Soru 2:** `nmap 10.114.128.179` komutunu yerel kullanıcı (root yetkisi olmadan) ayrıcalıklarıyla çalıştırırsanız Nmap hangi tarama türünü kullanır?  
> **Cevap:** `connect scan` (Çünkü SYN/raw socket taraması root yetkisi gerektirir; yetki yoksa Nmap otomatik olarak TCP Connect Scan `-sT` moduna geçer.)

---

## 7. Özet Komut Tablosu

| Komut / Bayrak | Açıklama |
|---|---|
| `nmap -sn <target>` | Port taraması yapmadan yalnızca canlı hostları tespit eder (Ping sweep) |
| `nmap -sS <target>` | TCP SYN (Stealth / Half-open) port taraması yapar (sudo gerektirir) |
| `nmap -sT <target>` | TCP Connect port taraması yapar (kullanıcı yetkisiyle çalışır) |
| `nmap -sU <target>` | UDP port taraması gerçekleştirir |
| `nmap -sV <target>` | Açık portlardaki servis ve sürüm bilgilerini tespit eder |
| `nmap -O <target>` | Hedef sistemin işletim sistemini tahmin eder |
| `nmap -A <target>` | OS tespiti, versiyon tespiti, script taraması ve traceroute'u birlikte çalıştırır |
| `nmap -Pn <target>` | Ping kontrolünü atlayarak tüm portları doğrudan taramaya zorlar |
| `nmap -p- <target>` | 1'den 65535'e kadar olan tüm TCP portlarını tarar |
| `nmap -F <target>` | En popüler 100 portu hızlıca tarar |
| `nmap -T4 <target>` | Taramayı agresif hızda gerçekleştirir |
| `nmap -oA <name> <target>` | Sonuçları normal, XML ve grepable formatlarda kaydeder |

---

## Kaynaklar

- [TryHackMe — Nmap: The Basics](https://tryhackme.com/room/nmap01)
- [Nmap Official Documentation & Reference Guide](https://nmap.org/book/man.html)
