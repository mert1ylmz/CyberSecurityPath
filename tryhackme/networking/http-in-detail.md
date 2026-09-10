# TryHackMe: HTTP in Detail

Web'in konuştuğu protokol — web güvenliğine giriş kapısı.

## HTTP nedir
**HyperText Transfer Protocol** — web tarayıcı ve web sunucusu arasında veri transferi sağlayan protokol. Stateless (durumsuz) — her istek kendi başına bir olay, sunucu geçmişi tutmuyor (o iş cookie/session ile ayrı).

## HTTPS
HTTP'nin TLS ile şifrelenmiş hali. TLS handshake'ten sonra tüm HTTP trafiği şifreli akıyor. Aynı protokol, aynı yapı — sadece taşıma katmanı güvenli.

**Not:** HTTPS içeriği şifreler ama **hedef domain'i şifrelemez** — SNI (Server Name Indication) TLS handshake'te açık geçiyor. Trafik analizinden kimin nereye bağlandığı hâlâ görünüyor.

## URL yapısı
Bir URL'nin tüm parçaları:

```
https://kullanici:sifre@tryhackme.com:443/view?id=1#top
   |         |            |            |    |    |     |
scheme   user:pass      host        port  path query  fragment
```

- **scheme** — protokol (http, https, ftp, ssh)
- **user:password** — nadir kullanılıyor, HTTP Basic Auth
- **host / domain** — hedef sunucu
- **port** — 80 (http) / 443 (https) varsayılan, farklıysa yazılır
- **path** — kaynağın yolu
- **query string** — `?anahtar=deger` çiftleri, sunucuya parametre
- **fragment** — `#bolum` — sadece istemcide çalışır, sunucuya gitmez

**Pentest bakışı:** URL'nin her parçası bir saldırı yüzeyi. Path traversal path'i hedef alır, SQLi çoğunlukla query string üzerinden gelir, open redirect URL manipülasyonu üzerinden çalışır.

## HTTP Metodları

- **GET** — kaynak istemek (idempotent, veri değiştirmemeli)
- **POST** — sunucuya veri göndermek (form submit, yeni kayıt oluşturma)
- **PUT** — kaynağı tamamen güncellemek
- **DELETE** — kaynağı silmek

Ek olarak: `PATCH` (kısmi güncelleme), `HEAD` (sadece başlıkları al), `OPTIONS` (sunucunun desteklediği metodları sor).

**Pentest bakışı:** Bir endpoint sadece GET bekliyor olabilir ama POST'a da cevap verebiliyorsa CSRF veya IDOR olabilir. `OPTIONS` çağrısı bir endpoint'in hangi metodları desteklediğini söylüyor — recon aracı olarak faydalı.

## Request Headers

- **Host** — hangi domain'e istek yapıldığını söylüyor (virtual hosting için gerekli)
- **User-Agent** — tarayıcı bilgisi (Firefox, Chrome, Safari...)
- **Content-Length** — gönderilen veri boyutu
- **Accept-Encoding** — hangi sıkıştırma yöntemlerini destekliyorsun (gzip, deflate)

**Pentest bakışı:** Header'lar manipüle edilebilir. User-Agent değiştirerek "farklı cihaz" gibi görünmek, Host header saldırıları (cache poisoning), Content-Length manipülasyonu (HTTP request smuggling) — hepsi header'lardan geçiyor.

## Response Headers

- **Set-Cookie** — client'a saklaması için cookie gönderme
- **Cache-Control** — cevabın ne kadar süre cache'lenebileceği
- **Content-Type** — gönderilen içeriğin tipi (text/html, application/json, image/png)
- **Content-Encoding** — hangi sıkıştırma kullanıldığı

**Pentest bakışı:** `Set-Cookie` bayrakları güvenlik için kritik — `HttpOnly` cookie'ye JS erişimini engeller, `Secure` sadece HTTPS'te gönderir, `SameSite` CSRF koruması. Bunların olmaması açık bir saldırı yüzeyi.

## Kavramların birlikte kullanımı
Burp Suite'te bir istek yakaladığında — request line (metod + path), headers, body — hepsini tek tek manipüle edip cevaba nasıl yansıdığını görüyorsun. HTTP'yi bilmek Burp'u anlamlı kullanmanın ön şartı.

## Kaynak
TryHackMe — HTTP in Detail room
