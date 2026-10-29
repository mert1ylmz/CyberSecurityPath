# 🐉 TryHackMe - Hydra Room Notes & Cheatsheet

![TryHackMe](https://img.shields.io/badge/TryHackMe-Hydra-red.svg?style=flat-square&logo=tryhackme)
![Tool](https://img.shields.io/badge/Tool-THC--Hydra-blue.svg?style=flat-square)
![Category](https://img.shields.io/badge/Category-Brute--Force-orange.svg?style=flat-square)

Bu doküman, TryHackMe platformundaki **Hydra** odasında yürütülen kaba kuvvet (brute-force / dictionary attack) çalışmalarını, komut sözdizimi açıklamalarını ve oda görevlerinin (Task 1 & Task 2) eksiksiz çözümlerini içermektedir.

**Platform:** TryHackMe  
**Oda:** Hydra ([tryhackme.com/room/hydra](https://tryhackme.com/room/hydra))  
**Zorluk:** Kolay (Easy)  
**Kategori:** Network / Web / Authentication / Brute-Force  
**Hedef IP:** `10.113.163.247`

---

## 📑 İçindekiler

1. [Genel Bakış & Hydra Nedir?](#1-genel-bakış--hydra-nedir)
2. [Temel Parametreler ve Bayraklar (Flags)](#2-temel-parametreler-ve-bayraklar-flags)
3. [TryHackMe Hydra Oda Çözümleri](#3-tryhackme-hydra-oda-çözümleri)
   - [Task 1: Web Formu Parola Kırma (HTTP-POST-Form)](#task-1-web-formu-parola-kırma-http-post-form)
   - [Task 2: SSH Servisi Parola Kırma (SSH Brute-Force)](#task-2-ssh-servisi-parola-kırma-ssh-brute-force)
4. [Elde Edilen Kimlik Bilgileri Özeti](#4-elde-edilen-kimlik-bilgileri-özeti)
5. [Pratik İpuçları ve Hata Giderme](#5-ipuçları-ve-hata-giderme)
6. [Kaynaklar](#6-kaynaklar)

---

## 1. Genel Bakış & Hydra Nedir?

**THC-Hydra**, sayısız ağ protokolü ve web formuna karşı paralel ve yüksek hızlı kimlik doğrulama denemeleri gerçekleştirebilen popüler bir online parola kırma (brute-force) aracıdır.

* **Varsayılan Wordlist Konumu (Kali/Parrot):** `/usr/share/wordlists/rockyou.txt`
* **Desteklenen Protokoller:** HTTP(S)-GET/POST, SSH, FTP, Telnet, RDP, VNC, SMB, MySQL, POP3, IMAP vb.

---

## 2. Temel Parametreler ve Bayraklar (Flags)

```bash
hydra [FLAGS] [HEDEF_IP] [PROTOKOL] [MODÜL_PARAMETRELERİ]
```

| Parametre | Açıklama |
| :--- | :--- |
| `-l <kullanıcı>` | Hedef tek bir kullanıcı adı tanımlar (Örn: `-l molly`). |
| `-L <dosya_yolu>` | Kullanıcı adı listesi içeren wordlist tanımlar. |
| `-p <parola>` | Tek bir sabit parola dener. |
| `-P <dosya_yolu>` | Parola listesi (`rockyou.txt` vb.) kullanır. |
| `-t <sayı>` | Eşzamanlı iş parçacığı (thread) sayısı. SSH ve hassas servislerde rate-limit yememek için düşük tutulur (`-t 4`). |
| `-s <port>` | Servis varsayılan port dışında çalışıyorsa portu belirtir. |
| `-f` | Geçerli ilk kullanıcı adı & parola çifti bulunduğunda işlemi durdurur. |
| `-v` / `-V` | Ayrıntılı (Verbose) çıktı modu (`-V` her denemeyi terminale yazar). |
| `-o <dosya>` | Çıktıyı ve bulunan kimlik bilgilerini bir dosyaya kaydeder. |

---

## 3. TryHackMe Hydra Oda Çözümleri

Oda toplamda **2 görevden (Task)** oluşmaktadır.

---

### Task 1: Web Formu Parola Kırma (HTTP-POST-Form)

Bu görevde bir web sitesi oturum açma formu (`/login.php`) hedef alınarak kullanıcı adı bilinen (`molly`) bir hesaba karşı sözlük saldırısı gerçekleştirilmiştir.

#### Çalıştırılan Komut

```bash
hydra -l Molly -P /usr/share/wordlists/rockyou.txt <HEDEF_IP> http-post-form "/login.php:user=^USER^&pass=^PASS^:F=Invalid username or password"
```

#### Komut Sözdizimi Analizi

* `http-post-form`: Web girişinde HTTP POST metodu kullanıldığını belirtir.
* `"/login.php:user=^USER^&pass=^PASS^:F=Invalid username or password"` kalıbı üç parçadan oluşur (`:` ile ayrılır):
  1. **URL Yolu:** `/login.php` (isteğin POST edildiği uç nokta).
  2. **Gövde (Body) Parametreleri:** `user=^USER^&pass=^PASS^` (Hydra, `^USER^` yerine `-l` ile verilen değeri, `^PASS^` yerine wordlist'teki parolaları koyar).
  3. **Hata Belirteci:** `F=Invalid username or password` (Uygulama hatalı girişte sayfaya bu metni basıyorsa başarısızlık olarak kabul edilir; bu ifade dönmediğinde parolanın bulunduğu anlaşılır).

#### Görev Sonucu

* **Kullanıcı:** `molly`
* **Parola:** `sunshine`

---

### Task 2: SSH Servisi Parola Kırma (SSH Brute-Force)

Bu görevde hedef makinenin 22 numaralı SSH portuna yönelik kaba kuvvet saldırısı uygulanmıştır.

#### Çalıştırılan Komut

```bash
hydra -l Molly -P /usr/share/wordlists/rockyou.txt ssh://10.113.163.247 -t 4
```

#### Komut Sözdizimi Analizi

* `ssh://10.113.163.247`: Hedef protokolü ve hedef makine IP adresini tanımlar.
* `-t 4`: SSH servisine aynı anda en fazla 4 eşzamanlı bağlantı açılmasını sağlar (SSH servisleri genellikle çok sayıda eşzamanlı bağlantıda paket düşürür veya kilitlenir).

#### Görev Sonucu

* **Kullanıcı:** `molly`
* **Parola:** `butterfly`

#### Doğrulama (SSH Bağlantısı)

Elde edilen parola ile hedef sisteme giriş yapılabilir:

```bash
ssh molly@10.113.163.247
# Parola: butterfly
```

---

## 4. Elde Edilen Kimlik Bilgileri Özeti

| Görev | Servis / Protokol | Hedef | Kullanıcı Adı | Parola |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1** | HTTP POST Form (`/login.php`) | `<HEDEF_IP>` | `molly` | `sunshine` |
| **Task 2** | SSH (Port 22) | `10.113.163.247` | `molly` | `butterfly` |

---

## 5. İpuçları ve Hata Giderme

> [!TIP]
> **Hata Belirteçleri (`F=` vs `S=`):**  
> Web formlarında başarısızlığı yakalamak için `F=` (Failure), başarılı yönlendirme veya hoş geldiniz mesajını yakalamak için `S=` (Success) kullanılır. Örneğin: `S=302 Found` veya `S=Welcome`.

> [!WARNING]
> **SSH Bağlantı Hataları (Too Many Connections):**  
> SSH servislerine saldırırken `-t 16` (varsayılan) gibi yüksek değerler hedef sunucunun `MaxStartups` sınırına takılmasına ve Hydra'nın hata vermesine neden olur. SSH için her zaman `-t 4` veya daha düşük bir thread değeri önerilir.

---

## 6. Kaynaklar

- [TryHackMe — Hydra Odası](https://tryhackme.com/room/hydra)
- [THC-Hydra GitHub Repository](https://github.com/vanhauser-thc/thc-hydra)
