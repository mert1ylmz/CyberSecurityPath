# TryHackMe - Pickle Rick CTF Writeup

Bu doküman, TryHackMe platformundaki **Pickle Rick** makinesinin çözüm adımlarını ve notlarını içermektedir.

**Platform:** TryHackMe  
**Oda:** Pickle Rick ([tryhackme.com/room/picklerick](https://tryhackme.com/room/picklerick))  
**Zorluk:** Kolay (Easy)  
**Kategori:** Web / Linux / Privilege Escalation  

---

## 1. Keşif & Tarama (Reconnaissance)

Hedef makinedeki açık portları ve servisleri tespit etmek için `nmap` taraması yapıldı:

```bash
nmap -sCV -v <Machine-IP-Address>
```

**Nmap Sonuçları:**
* `22/tcp` - **open** (SSH)
* `80/tcp` - **open** (HTTP)

---

## 2. Web Keşfi (HTTP - Port 80)

* Tarayıcı üzerinden hedefin 80 portuna gidildi:
  ```text
  http://10.114.172.50:80
  ```
* Web sitesi ziyaret edildiğinde **"Help Morty!"** sayfasıyla karşılaşıldı.

---

## 3. Gizli Dosya & Dizin İncelemeleri

* `/sitemap` ve `/robots.txt` yolları kontrol edildi.
* `/robots.txt` dosyası incelendiğinde bir parola bulundu:
  * **Bulunan Değer / Şifre:** `Wubbalubbadubdub` *(notlarda sürpriz parola olarak işaretlendi)*

---

## 4. Kaynak Kod İncelemesi

* Burp Suite veya tarayıcı geliştirici araçları ile ana sayfanın HTML kaynak kodları incelendi:
  * **Kullanıcı Adı (Username):** `R1ckRul3s`

---

## 5. Dizin Taraması (Directory Busting)

Gobuster aracı ile web dizin ve dosya taraması gerçekleştirildi:

**Keşfedilen Sayfalar ve Dosyalar:**
* `/login.php`
* `/portal.php`
* `/index.html`

---

## 6. Panele Giriş (Authentication)

* Elde edilen kimlik bilgileri (`Username: R1ckRul3s`, Parola: `/robots.txt` içindeki değer) ile `/login.php` üzerinden giriş yapıldı.
* Başarılı girişin ardından **Command Panel** (`/portal.php`) sayfasına erişim sağlandı.

---

## 7. Komut Çalıştırma & Dosya İnceleme

Portal üzerindeki komut çalıştırma alanında dosya listelemesi yapıldı:

```bash
ls -l
```

* Listelenen dosyalar arasında gizli dosya tespit edildi.
* `cat` komutu engellendiği/çalışmadığı için dosya `cat` ile açılamadı.
* Alternatif olarak `less` komutu kullanıldı:
  ```bash
  less Sup3r_S3cret_Pickl3_Ingred.txt
  ```
* **1. Flag (1st Ingredient):** `mr. meeseek hair`

---

## 8. İpuçları ve Diğer Flaglerin Aranması

* `clue.txt` adlı dosya `less` komutu ile incelenerek sonraki flaglerin nerede olduğuna dair ipuçları öğrenildi:
  ```bash
  less clue.txt
  ```
* Sistemdeki kullanıcı dizinlerini görmek için `/home` dizini listelendi:
  ```bash
  ls -la /home
  ```

---

## 9. 2. Flag (Second Ingredient)

* `/rick` dizini incelendi ve içinde `second ingredients` adlı dosya bulundu.
* Dosya içeriği `less` komutu ile okundu:
  ```bash
  less "/home/rick/second ingredients"
  ```
* **2. Flag:** `1 Jerry tear`

---

## 10. Yetki Yükseltme (Privilege Escalation) & 3. Flag

* Doğrudan root dizini incelenmeye çalışıldığında izin hatası (Yetkisiz erişim) alındı.
* `sudo` yetkisi kullanılarak `/root` dizinindeki `3rd.txt` dosyası okundu:
  ```bash
  sudo less "/root/3rd.txt"
  ```
* **3. Flag:** `fleas juice` *(not: fleep juice)*

---

## Kaynaklar

- [TryHackMe — Pickle Rick Room](https://tryhackme.com/room/picklerick)
