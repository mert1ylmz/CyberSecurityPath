# 🌐 TryHackMe - Net Sec Challenge Writeup

![TryHackMe](https://img.shields.io/badge/TryHackMe-Net_Sec_Challenge-red.svg?style=flat-square&logo=tryhackme)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-yellow.svg?style=flat-square)
![Category](https://img.shields.io/badge/Category-Nmap_%7C_Hydra_%7C_IDS_Evasion-blue.svg?style=flat-square)

Bu doküman, TryHackMe platformundaki **Net Sec Challenge** odasında ağ güvenliği modüllerini pekiştirmek amacıyla gerçekleştirilen kapsamlı port/servis keşfi (`nmap`), standart dışı portta çalışan FTP servisine kaba kuvvet saldırısı (`hydra`) ve TCP bayrak manipülasyonu ile IDS atlatma (`-sN` Null Scan) adımlarını içermektedir.

**Platform:** TryHackMe  
**Oda:** Net Sec Challenge ([tryhackme.com/room/netsecchallenge](https://tryhackme.com/room/netsecchallenge))  
**Zorluk:** Orta (Medium)  
**Kategori:** Network Security / Port Scanning / Brute-Force / IDS Evasion  
**Hedef IP:** `10.112.129.99`

---

## 📑 İçindekiler

1. [Keşif & Port Taraması (Nmap)](#1-keşif--port-taraması-nmap)
2. [Servis Banner & Versiyon Flag'lerinin Tespiti (Port 22 & 80)](#2-servis-banner--versiyon-flaglerinin-tespiti-port-22--80)
3. [Standart Dışı Portta FTP Keşfi (`-p-`)](#3-standart-dışı-portta-ftp-keşfi--p-)
4. [Hydra ile Özel Portta FTP Brute-Force & Flag](#4-hydra-ile-özel-portta-ftp-brute-force--flag)
5. [TCP Null Scan (`-sN`) ile IDS Atlatma](#5-tcp-null-scan--sn-ile-ids-atlatma)
6. [Özet Tablo & Çıkarımlar](#6-özet-tablo--çıkarımlar)
7. [Kaynaklar](#7-kaynaklar)

---

## 1. Keşif & Port Taraması (Nmap)

İlk olarak hedef makinedeki yaygın portları, servis versiyonlarını ve varsayılan NSE betik çıktılarını görmek için standart `nmap` taraması yapıldı:

```bash
nmap -sC -sV 10.112.129.99
```

**İlk Taramada Bulunan Açık Portlar (6 Port):**
* `22/tcp` — **open** (`ssh`)
* `80/tcp` — **open** (`http`)
* `139/tcp` — **open** (`netbios-ssn`)
* `445/tcp` — **open** (`netbios-ssn` / SMB)
* `8081/tcp` — **open** (`http` - IDS izleme paneli)
* `10001/tcp` — **open** (`scp-config`)

Ardından yaygın 1000 port listesinde yer almayan tüm TCP portlarını (1–65535) kontrol etmek amacıyla `-p-` parametresiyle tam port taraması gerçekleştirildi:

```bash
nmap -p- 10.112.129.99
```

* Standart dışı yüksek portlarda **`10121/tcp`** portunun da açık olduğu tespit edildi.
* Böylece hedefte toplamda **7 açık TCP portu** (`22`, `80`, `139`, `445`, `8081`, `10001`, `10121`) bulunduğu doğrulandı (`10.000` altındaki en yüksek açık port: `8081`).

---

## 2. Servis Banner & Versiyon Flag'lerinin Tespiti (Port 22 & 80)

`nmap -sC -sV 10.112.129.99` çıktısındaki servis başlıkları (banner / HTTP Server header) incelendiğinde doğrudan iki adet gizli bayrak (flag) elde edildi:

1. **HTTP Servis Versiyonu (`80/tcp`):** Web sunucusunun `http-server-header` / `VERSION` bilgisinde gizlenmiş olan flag bulundu.
2. **SSH Servis Bilgisi (`22/tcp`):** SSH servisinin banner / hostkey çıktısı içerisinde yer alan ikinci flag tespit edildi.

---

## 3. Standart Dışı Portta FTP Keşfi (`-p-`)

Görevde standart port (`21`) dışında çalışan gizli bir FTP sunucusunun versiyon bilgisi istenmektedir. Tam port taramasında keşfedilen `10121` numaralı porta yönelik hedefli versiyon taraması çalıştırıldı:

```bash
nmap -sC -sV -p 10121 10.112.129.99
```

**Bulgu:**
* **Port:** `10121/tcp`
* **Servis & Versiyon:** `vsftpd 3.0.5`

---

## 4. Hydra ile Özel Portta FTP Brute-Force & Flag

Senaryoya göre sistemde **`eddie`** ve **`quinn`** adında iki farklı kullanıcı hesabı bulunmaktadır ve bu hesaplardan birinin FTP dizininde gizli bir flag dosyası yer almaktadır.

FTP servisi varsayılan `21` portu yerine `10121` portunda çalıştığı için **THC-Hydra** aracına `-s 10121` parametresi verilerek sözlük saldırısı düzenlendi:

```bash
hydra -l quinn -P /usr/share/wordlists/rockyou.txt 10.112.129.99 -s 10121 ftp
```

*(İki kullanıcıyı tek seferde denemek için kullanıcı adları bir dosyaya yazılıp `-L users.txt` parametresi de kullanılabilir.)*

**Bulunan Kimlik Bilgileri:**
* **Kullanıcı Adı:** `quinn`
* **Parola:** `cookie`

Elde edilen bilgilerle `10121` portu üzerinden FTP sunucusuna giriş yapıldı:

```bash
ftp 10.112.129.99 10121
# Name: quinn
# Password: cookie
```

Dizin içeriği listelenip dosya okunduğunda gizli bayrağa ulaşıldı:

```ftp
ftp> ls -la
ftp> get ftp_flag.txt -
```

* **FTP Flag:** `THM{QUINN_IS_BACK007}`

---

## 5. TCP Null Scan (`-sN`) ile IDS Atlatma

Son görevde `http://10.112.129.99:8081` adresindeki izleme arayüzü tarafından takip edilen **IDS (Saldırı Tespit Sistemi)** kurallarına yakalanmadan hedef makineyi `nmap` ile taramak istenmektedir.

Standart SYN (`-sS`) veya TCP Connect (`-sT`) taramaları `SYN` bayrağı taşıyan paketler gönderdiği için IDS tarafından anında algılanmaktadır. Bu kuralı atlatmak için hiçbir TCP kontrol bayrağının (`SYN`, `ACK`, `FIN`, `RST`, `PSH`, `URG`) set edilmediği **TCP Null Scan (`-sN`)** tekniği kullanıldı:

```bash
sudo nmap -sN 10.112.129.99
```

> [!NOTE]
> **RFC 793 Mantığı:** Hiçbir bayrağı işaretlenmemiş bir TCP paketi hedef porta ulaştığında; port **kapalıysa** hedef sistem `RST` (Reset) paketi döner, port **açıksa** (veya güvenlik duvarı varsa) paket yanıtsız bırakılır (`open|filtered`). `SYN` bayrağı içermediği için yalnızca `SYN` imzalarını izleyen basit IDS kurallarını başarıyla atlatır.

Tarama tamamlandıktan sonra `http://10.112.129.99:8081` sayfası kontrol edilerek son bayrak (IDS Evasion Flag) elde edildi.

---

## 6. Özet Tablo & Çıkarımlar

| Aşama | Kullanılan Komut / Yöntem | Sonuç / Bulgu |
| :--- | :--- | :--- |
| **Yaygın Port Taraması** | `nmap -sC -sV 10.112.129.99` | `22`, `80`, `139`, `445`, `8081`, `10001` açık |
| **Tam Port Taraması** | `nmap -p- 10.112.129.99` | `10121/tcp` bulundu (Toplam **7** açık port) |
| **Banner Keşfi** | `80/http` ve `22/ssh` servis versiyon çıktıları | HTTP Server Header & SSH Banner flag'leri |
| **Gizli FTP Tespiti** | `nmap -sV -p 10121 10.112.129.99` | `vsftpd 3.0.5` |
| **FTP Brute-Force** | `hydra -l quinn -P rockyou.txt 10.112.129.99 -s 10121 ftp` | `quinn:cookie` -> `THM{QUINN_IS_BACK007}` |
| **IDS Evasion** | `sudo nmap -sN 10.112.129.99` | TCP Null Scan ile IDS tetiklenmeden tarama |

### Güvenlik Çıkarımları
1. **Standart Dışı Portlar Güvenlik Sağlamaz:** Bir servisi `21` yerine `10121` portuna taşımak (*Security through Obscurity*), `-p-` ile yapılan tam port taramasına karşı koruma sağlamaz.
2. **Servis Başlıklarının Gizlenmesi (Banner Hardening):** Web ve SSH sunucularında özel versiyon ve başlık bilgilerinin (`ServerTokens`, `DebianBanner`) dışarıya açık bırakılması saldırganlara keşif aşamasında kritik bilgi sunar.
3. **Derinlemesine IDS Kuralları:** Yalnızca `SYN` paketlerini izleyen imza tabanlı IDS kuralları Null (`-sN`), FIN (`-sF`) veya Xmas (`-sX`) taramalarıyla kolayca atlatılabilir; anormal bayrak kombinasyonları da kural setlerine dahil edilmelidir.

---

## 7. Kaynaklar

- [TryHackMe — Net Sec Challenge Odası](https://tryhackme.com/room/netsecchallenge)
- [Nmap Reference Guide — TCP Null, FIN, and Xmas Scans (`-sN`, `-sF`, `-sX`)](https://nmap.org/book/scan-methods-null-fin-xmas-scan.html)

