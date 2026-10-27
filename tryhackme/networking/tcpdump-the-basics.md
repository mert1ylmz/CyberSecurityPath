# TryHackMe: Tcpdump : The Basics

Bu doküman, TryHackMe platformundaki **Tcpdump: The Basics** odasına ait teorik bilgileri, paket yakalama ve filtreleme tekniklerini, komut bayraklarını ve pratik lab soru çözümlerini içermektedir.

**Platform:** TryHackMe  
**Oda:** Tcpdump: The Basics ([tryhackme.com/room/tcpdump](https://tryhackme.com/room/tcpdump))  
**Kategori:** Networking / Traffic Analysis / Packet Inspection  
**Varsayılan Kimlik Bilgileri:**
* **Username:** `user`
* **Password:** `THM123`

---

## 1. Giriş (Introduction)

`tcpdump`, komut satırı üzerinden ağ paketlerini yakalamak, filtrelemek ve analiz etmek için kullanılan güçlü bir ağ analiz aracıdır.

* **Arka Plan Kütüphanesi:** Paket yakalama işlemleri için C tabanlı `libpcap` kütüphanesini kullanır.
* **Kullanım Amacı:** Ağ sorunlarını gidermek, güvenlik ihlallerini tespit etmek, şüpheli paket trafiğini izlemek ve paket dökümlerini (`.pcap`) analiz etmek.

---

## 2. Temel Paket Yakalama (Basic Packet Capture)

### Ağ Arayüzünü Belirtme (Specify the Network Interface)
* `-i INTERFACE` — Dinlenecek ağ arayüzünü seçer (ör. `-i eth0`).
* `-i any` — Sistemdeki aktif tüm ağ arayüzlerini dinler.
* `ip address show` (veya `ip a`) — Sistemde mevcut ve kullanılabilir ağ arayüzlerini listeler.

### Paketleri Dosyaya Kaydetme (Save the Captured Packets)
* `-w FILE` — Yakalanan paketleri standart pcap formatında bir dosyaya yazar:
  ```bash
  sudo tcpdump -i eth0 -w capture.pcap
  ```

### PCAP Dosyasından Paket Okuma (Read Captured Packets from a File)
* `-r FILE` — Önceden kaydedilmiş bir pcap dosyasını okuyup analiz eder:
  ```bash
  tcpdump -r traffic.pcap
  ```

### Yakalanacak Paket Sayısını Sınırlama (Limit the Number of Captured Packets)
* `-c COUNT` — Belirtilen sayıda paket yakalandıktan sonra tcpdump otomatik olarak durur. Bir sınır verilmezse kullanıcı `Ctrl + C` ile durdurana kadar yakalama devam eder:
  ```bash
  tcpdump -i eth0 -c 10
  ```

### IP ve Port Çözümlemesini Kapatma (Numeric Format)
Tcpdump varsayılan olarak IP adreslerini alan adlarına (DNS lookup), port numaralarını ise iyi bilinen servis isimlerine (ör. 80 yerine http) çevirmeye çalışır. Bu durum analizi yavaşlatabilir.
* `-n` — IP adreslerinin DNS çözümlemesini kapatır, adresleri sayısal (IP) olarak gösterir.
* `-nn` — Hem IP adreslerinin hem de port numaralarının isim çözümlemesini kapatır (tam sayısal format).

### Ayrıntı Düzeyini Artırma (Verbose Output)
* `-v` — Paket hakkında TTL, ID, toplam uzunluk gibi ek başlık bilgilerini gösterir.
* `-vv` — Daha fazla detay (ör. NFS veya SMB decode detayları).
* `-vvv` — En yüksek ayrıntı düzeyi.

> **Soru:** Komutunuza adresleri yalnızca sayısal formatta görüntülemek için hangi seçeneği ekleyebilirsiniz?  
> **Cevap:** `-n`

---

## 3. Filtreleme İfadeleri (Filtering Expressions)

Büyük ağ trafiklerinde hedef odaklı analiz yapabilmek için BPF (Berkeley Packet Filter) filtreleme ifadeleri kullanılır.

### Host Filtreleme (Filtering by Host)
Paketleri kaynak veya hedef IP/hostname bilgisine göre ayırır:
* `host IP` veya `host HOSTNAME` — Belirtilen host ile ilgili tüm paketler.
* `src host IP` — Yalnızca kaynak adresi belirtilen host olan paketler.
* `dst host IP` — Yalnızca hedef adresi belirtilen host olan paketler.

*Örnek:*
```bash
sudo tcpdump host example.com -w http.pcap
```

### Port Filtreleme (Filtering by Port)
* `port NUMBER` — İlgili portu içeren tüm paketler (kaynak veya hedef).
* `src port NUMBER` — Kaynak portu filtreler.
* `dst port NUMBER` — Hedef portu filtreler.

### Protokol Filtreleme (Filtering by Protocol)
Trafiği doğrudan taşıma veya ağ protokolüne göre sınırlar:
* `ip` — IPv4 paketleri
* `ip6` — IPv6 paketleri
* `udp` — UDP paketleri
* `tcp` — TCP paketleri
* `icmp` — ICMP kontrol paketleri

### Mantıksal Operatörler (Logical Operators)
Birden fazla filtreleme kuralını birleştirmek için kullanılır:
* `and` (veya `&&`)
* `or` (veya `||`)
* `not` (veya `!`)

*Örnekler:*
```bash
tcpdump host 1.1.1.1 and tcp
tcpdump udp or icmp
tcpdump not tcp
```

### Lab Soru ve Çözümleri:

> **Soru 1:** `traffic.pcap` dosyasında ICMP protokolünü kullanan kaç paket bulunmaktadır?  
> **Komut:**
> ```bash
> ssh user@10.114.166.57
> # Şifre: THM123
> tcpdump -r traffic.pcap icmp -n | wc -l
> ```
> **Cevap:** `26`

> **Soru 2:** 192.168.124.137 adresinin MAC adresini soran (ARP request) host'un IP adresi nedir?  
> **Komut:**
> ```bash
> tcpdump -r traffic.pcap -e arp -n
> ```
> **Cevap:** `192.168.124.148`

> **Soru 3:** İlk DNS sorgusunda hangi hostname (subdomain) görünmektedir?  
> **Komut:**
> ```bash
> tcpdump -r traffic.pcap -n -c 1 port 53
> ```
> **Cevap:** `mirrors.rockylinux.org`

---

## 4. İleri Düzey Filtreleme (Advanced Filtering)

Gerçek dünya senaryolarında binlerce hatta milyonlarca paketi başlık baytlarına ve özel bayraklara göre filtrelemek gerekir.

### Paket Boyutuna Göre Filtreleme
* `greater LENGTH` — Belirtilen bayt uzunluğundan daha büyük paketleri filtreler.
* `less LENGTH` — Belirtilen bayt uzunluğundan daha küçük paketleri filtreler.

### Mantıksal ve Bit Düzeyinde İşlemler (Binary Operations)
* `&` — Bitwise AND (bitsel ve)
* `|` — Bitwise OR (bitsel veya)
* `!` — NOT (değil)

### Başlık Baytları (Header Bytes) ile Filtreleme
Paket başlığındaki belirli ofsetlere erişerek derinlemesine denetim sağlar:
```text
proto [ expr : size ]
```
* `proto`: İncelenecek protokol (ör. `ether`, `ip`, `tcp`).
* `expr`: İncelenecek bayt ofseti (0 tabanlı indeks).
* `size`: İncelenecek bayt uzunluğu (opsiyonel; 1, 2 veya 4 bayt).

*Örnekler:*
* `ether[0] & 1 != 0` — Multicast veya broadcast Ethernet çerçevelerini yakalar.
* `ip[0] & 0xf != 5` — IPv4 başlık uzunluğu standart 20 bayttan (5 x 4 bayt) farklı olan (IP options içeren) paketleri yakalar.

### TCP Bayraklarına Göre Filtreleme (TCP Flags)
TCP başlığındaki kontrol bayraklarını denetlemek için `tcp[tcpflags]` sözdizimi kullanılır:
* `tcp-syn` (SYN bayrağı)
* `tcp-ack` (ACK bayrağı)
* `tcp-fin` (FIN bayrağı)
* `tcp-rst` (RST bayrağı)
* `tcp-push` (PSH bayrağı)

*Kullanım Örnekleri:*
```bash
# Yalnızca SYN bayrağı set edilmiş paketler
tcpdump "tcp[tcpflags] == tcp-syn"

# İçinde SYN bayrağı bulunan paketler (SYN-ACK dahil)
tcpdump "tcp[tcpflags] & tcp-syn != 0"

# Hem SYN hem de ACK bayrağı içeren paketler
tcpdump "tcp[tcpflags] & (tcp-syn|tcp-ack) != 0"
```

### Lab Soru ve Çözümleri:

> **Soru 1:** Yalnızca TCP Reset (RST) bayrağı set edilmiş kaç paket vardır?  
> **Komut:**
> ```bash
> sudo tcpdump -r traffic.pcap "tcp[tcpflags] == tcp-rst" | wc -l
> ```

> **Soru 2:** 15000 bayttan daha büyük paketler gönderen host'un IP adresi nedir?  
> **Komut:**
> ```bash
> tcpdump -r traffic.pcap greater 15000 -n
> ```

---

## 5. Paketleri Görüntüleme Formatları (Displaying Packets)

Paket içeriğini ve başlıklarını terminalde okunabilir hale getiren parametreler:

* `-q` — Hızlı ve özet çıktı (daha az protokol detayı).
* `-e` — Bağlantı katmanı (Data Link / Link-level) başlıklarını basar; kaynak ve hedef MAC adreslerini incelemek için kullanılır.
* `-A` — Paket yükünü (payload) ASCII karakter formatında ekrana yazar (HTTP, SMTP gibi metin tabanlı protokolleri okumak için idealdir).
* `-xx` — Paket verilerini ve bağlantı katmanı başlıklarını hexadecimal formatta basar.
* `-X` — Paket başlıklarını ve verilerini hem hexadecimal hem de ASCII formatında yan yana basar.

> **İpucu:** Eğer Wi-Fi veya Ethernet trafiğinde MAC adreslerini görmek istiyorsanız komuta `-e` bayrağını eklemek yeterlidir.

### Lab Soru ve Çözümü:

> **Soru:** ARP isteği gönderen cihazın MAC adresi nedir?  
> **Komut:**
> ```bash
> tcpdump -r traffic.pcap -c 1 -e arp
> ```
> **Cevap:** `52:54:00:7a:d3:5b`

---

## 6. Özet Komut Referansı

| Parametre / Filtre | Açıklama |
|---|---|
| `-i <interface>` | Dinlenecek ağ arayüzünü seçer |
| `-w <file.pcap>` | Trafiği pcap dosyasına kaydeder |
| `-r <file.pcap>` | Pcap dosyasından analiz yapar |
| `-c <count>` | Belirtilen paket adedinden sonra durur |
| `-n` / `-nn` | DNS ve port isim çözümlemesini devre dışı bırakır |
| `-e` | Link-level başlıklarını (MAC adresleri) görüntüler |
| `-A` | Paket içeriğini ASCII metin olarak görüntüler |
| `-X` | Paket içeriğini Hex + ASCII olarak görüntüler |
| `host <IP>` | Belirli IP adresine ait trafiği filtreler |
| `port <Port>` | Belirli porta ait trafiği filtreler |
| `greater <size>` | Belirtilen boyuttan büyük paketleri getirir |
| `tcp[tcpflags] == tcp-syn` | Yalnızca SYN paketlerini filtreler |

---

## Kaynaklar

- [TryHackMe — Tcpdump: The Basics](https://tryhackme.com/room/tcpdump)
- `tcpdump(1)` ve `pcap-filter(7)` man page belgeleri
