# TryHackMe - Surfer CTF Writeup

Bu doküman, TryHackMe platformundaki **Surfer** makinesinin çözüm adımlarını, zafiyet analizini ve detaylı notlarını içermektedir.

**Platform:** TryHackMe  
**Oda:** Surfer ([tryhackme.com/room/surfer](https://tryhackme.com/room/surfer))  
**Zorluk:** Kolay / Orta (Easy / Medium)  
**Kategori:** Web / SSRF (Server-Side Request Forgery) / CTF  
**Hedef IP:** `10.112.182.123`

---

## 1. Keşif & Ağ Taraması (Reconnaissance)

Hedef makinedeki açık portları ve çalışan servis versiyonlarını tespit etmek amacıyla detaylı bir `nmap` taraması yapıldı:

```bash
nmap -sC -sV 10.112.182.123
```

**Nmap Tarama Sonuçları:**
* `22/tcp` — **open** (SSH)
* `80/tcp` — **open** (HTTP - Web Sunucusu / Apache & PHP)

Yapılan ilk taramada sistemde bir SSH servisi ve bir HTTP web uygulamasının aktif olduğu görüldü.

---

## 2. Web Keşfi & Kimlik Doğrulama (Authentication)

Tarayıcı üzerinden hedefin web uygulamasına gidildi:

```text
http://10.112.182.123
```

Uygulama bir giriş paneli (Login page) ile karşıladı. İlk olarak varsayılan ve zayıf kimlik bilgileri test edildi:

* **Username:** `admin`
* **Password:** `admin`

Bu kimlik bilgileriyle yönetim paneline (Dashboard) başarıyla giriş yapıldı.

---

## 3. Web Dizin & Dosya Taraması (Directory Busting)

Sistemdeki gizli dizinleri, dosyaları ve potansiyel uç noktaları (endpoints) ortaya çıkarmak için `gobuster` aracı çalıştırıldı:

```bash
gobuster dir -u http://10.112.182.123 -w /usr/share/wordlists/dirb/common.txt -x php,html,txt
```

**Keşfedilen Önemli Dosya ve Yollar:**
* `/robots.txt`
* `/Readme.txt`

Bu dosyaların incelenmesi sonucunda sistemde yalnızca yerel ağdan (localhost/internal) erişilebilen dahili bir yönetim sayfası (`/internal/admin.php`) olduğu anlaşıldı.

---

## 4. Zafiyet & Versiyon Araştırması

Web sunucusunda çalışan PHP sürümü için bilinen açıklar incelendi:

```bash
searchsploit php 7.2
```

Sistemdeki servislerin genel analizi yapıldıktan sonra yönetim paneli içerisindeki fonksiyonlar incelenmeye başlandı.

---

## 5. SSRF Zafiyeti & Burp Suite ile İstismar (Exploitation)

Yönetim panelinde sayfa/rapor çıktısı almayı sağlayan **Export to PDF** özelliği tespit edildi.

### Zafiyet Mantığı (SSRF - Server-Side Request Forgery):
* **Export PDF** özelliği, kullanıcıdan bir URL parametresi alarak hedef web sayfasını sunucu tarafında ziyaret etmekte ve oluşturduğu görüntüyü PDF formatında kullanıcıya sunmaktadır.
* Dışarıdan doğrudan `http://10.112.182.123/internal/admin.php` sayfasına erişilmeye çalışıldığında erişim engeli (örneğin *403 Forbidden* veya yalnızca yerel ağ kısıtlaması) verilmektedir.
* Ancak bu istek sunucunun kendisine (`127.0.0.1` veya `localhost`) yaptırıldığında, sunucu dahili güvenlik filtrelerini atlayarak yerel yönetim sayfasına erişebilmektedir.

### Adım Adım İstismar:

1. Tarayıcı trafiği **Burp Suite** üzerinden geçirildi ve `Intercept` açıldı.
2. Panel üzerindeki **Export PDF** butonuna basılarak istek yakalandı.
3. Gönderilen POST/GET parametreleri incelendiğinde sayfa URL'ini tutan parametre görüldü.
4. Bu parametredeki hedef adres `/internal/admin.php` olarak güncellendi:
   ```text
   http://127.0.0.1/internal/admin.php
   ```
   *(veya tam yerel yol: `http://localhost/internal/admin.php`)*
5. İstek sunucuya iletildi (`Forward`).
6. Sunucu, kendi iç arayüzünden `/internal/admin.php` sayfasına erişti ve bu sayfanın içeriğini PDF'e dönüştürerek indirdi.
7. İndirilen PDF dosyası açıldığında **Admin Flag** değerine başarıyla ulaşıldı.

---

## 6. Alınan Dersler & Çıkarımlar

1. **SSRF Riskleri:** Sunucu tarafında URL parametresi alıp bu adrese HTTP isteği yapan fonksiyonlar (PDF oluşturucular, webhook'lar, URL önizleme servisleri) daima katı bir beyaz liste (allowlist) ile sınırlandırılmalıdır.
2. **Localhost İzolasyonu:** Dahili yönetim sayfaları (`/internal/admin.php`) sadece IP kontrolüne güvenmemeli, güçlü oturum ve rol tabanlı kimlik doğrulama mekanizmaları ile korunmalıdır.
3. **Varsayılan Parolalar:** Sistemlerin `admin:admin` gibi tahmin edilebilir varsayılan kimlik bilgileriyle yayına alınması zincirleme saldırılara yol açar.

---

## Kaynaklar

- [TryHackMe — Surfer Odası](https://tryhackme.com/room/surfer)
- [PortSwigger Web Security Academy — Server-Side Request Forgery (SSRF)](https://portswigger.net/web-security/ssrf)
