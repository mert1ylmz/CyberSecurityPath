# Reflected XSS into HTML context with nothing encoded

## Konu Açıklaması (Reflected Cross-Site Scripting)

**Reflected Cross-Site Scripting (Yansıyan XSS)**, bir web uygulamasının HTTP isteğiyle beraber gelen kullanıcı verisini (parametre, form girdisi vb.) alıp, **güvensiz bir şekilde (herhangi bir doğrulama veya HTML entity kodlaması yapmadan)** anlık HTTP yanıtına doğrudan yansıtması durumunda ortaya çıkar.

### Örnek Senaryo:
Bir web sitesinin arama fonksiyonu olduğunu ve kullanıcı tarafından sağlanan arama parametresini aldığını varsayalım:
```http
https://insecure-website.com/search?term=gift
```

Uygulama sunucusu bu terimi alır ve dönen HTML yanıtında ekrana basar:
```html
<p>You searched for: gift</p>
```

Uygulamanın bu sorguya herhangi bir filtreleme veya kodlama uygulamadığını varsayarsak, saldırgan arama parametresine zararlı bir JavaScript kodu yerleştirebilir:
```http
https://insecure-website.com/search?term=<script>/* Zararlı Kod */</script>
```

Sunucu bu isteği aldığında doğrudan şu HTML çıktısını üretir:
```html
<p>You searched for: <script>/* Zararlı Kod */</script></p>
```
Kurban bu bağlantıya tıkladığında, zararlı betik kurbanın tarayıcısında meşru web sitesi bağlamında çalışır.

---

### Reflected XSS Saldırılarının Etkisi (Impact)

Saldırgan, kurbanın tarayıcısında çalıştırılan betiği kontrol edebilirse, o kullanıcının güvenliğini tamamen riske atabilir:
- Kullanıcının o uygulamada yapabildiği her işlemi (aksiyonu) kurban adına gerçekleştirebilir.
- Kullanıcının erişebildiği tüm hassas bilgileri (oturum çerezleri, profil verileri) görüntüleyebilir ve sızdırabilir.
- Kullanıcıya ait verileri değiştirebilir.
- Diğer kullanıcılarla etkileşim başlatabilir (solucan/worm benzeri yayılım).

---

### Reflected XSS Zafiyetlerini Tespit Etme ve Test Metodolojisi

Reflected XSS açıklarını tespit etmek için adım adım şu yaklaşım izlenir:

1. **Test every entry point:** URL parametreleri, form alanları ve HTTP başlıkları dahil tüm girdi noktaları test edilir.
2. **Submit random alphanumeric values:** Her parametreye sistemde kolayca aranabilecek rastgele ve benzersiz bir alfasayısal değer (canary) gönderilir.
3. **Determine the reflection context:** Yanıt içerisinde gönderilen değerin nereye düştüğü (HTML gövdesi, öznitelik içi, script bloğu vb.) incelenir.
4. **Test a candidate payload:** İlgili bağlamın gerektirdiği temel payload denenir (ör. `<script>alert(1)</script>`).
5. **Test alternative payload:** WAF veya basit filtreler devreye girerse olay dinleyicileri (`<img src=1 onerror=alert(1)>`) gibi alternatif yükler kullanılır.
6. **Test the attack in a browser:** Enjeksiyonun gerçek bir tarayıcıda çalıştığı ve zararlı betiğin yürütüldüğü doğrulanır.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Reflected XSS into HTML context with nothing encoded
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Apprentice
- **Zafiyet Türü:** Reflected Cross-Site Scripting (XSS)
- **Bağlam (Context):** HTML Body / Arama Parametresi (Herhangi bir kodlama/filtreleme yok)
- **Amaç:** Reflected XSS zafiyeti bulunan sayfada `alert()` fonksiyonunu başarıyla çalıştırmak.

---

### Çözüm Adımları

1. **Arama İşlevinin İncelenmesi:**
   - Web sitesinin ana sayfasına gidilir ve arama (search) kutucuğuna herhangi bir test kelimesi (örneğin `test`) yazılarak arama yapılır.
   - URL yapısı incelenir: `https://lab-id.web-security-academy.net/?search=test`
   - Sayfa kaynağında girdiğimiz değerin bir HTML paragrafı içine doğrudan basıldığı görülür:
     ```html
     <h1>0 search results for 'test'</h1>
     ```

2. **Payload Enjeksiyonu:**
   - URL kısmındaki `search` parametresine veya doğrudan ana sayfadaki arama kutusuna şu kod eklenir:
     ```html
     <script>alert(1)</script>
     ```
   - URL üzerinden denendiğinde istek şu şekilde gönderilir:
     ```text
     https://lab-id.web-security-academy.net/?search=%3Cscript%3Ealert(1)%3C%2Fscript%3E
     ```

3. **Tetikleme ve Doğrulama:**
   - İstek gönderildiğinde sayfa yüklenir ve tarayıcıda `1` değerini içeren bir uyarı penceresi (`alert`) açılır.
   - Laboratuvar başarıyla tamamlanır.

---

### Teknik Analiz (Neden Çalıştı?)

* **Girdi Doğrulama ve Çıktı Kodlama Eksikliği:**
  Uygulama, `search` parametresinden aldığı veriyi sunucudan tarayıcıya döndürürken `<` ve `>` karakterlerini `&lt;` ve `&gt;` formatına çevirmemiştir (HTML Entity Encoding yapılmamıştır).
* **Doğrudan Yürütme:**
  Tarayıcı gelen HTML yanıtını ayrıştırırken `<script>` etiketini doğrudan bir JavaScript programlama talimatı olarak yorumlamış ve JavaScript motoruna aktararak `alert(1)` kodunu çalıştırmıştır.

---

## Korunma Yöntemleri (Remediation)

1. **Context-Aware Output Encoding (Bağlama Uygun Çıktı Kodlama):**
   HTML gövdesine yazdırılan kullanıcı girdileri HTML entity formatına encode edilmelidir:
   - `<` $\rightarrow$ `&lt;`
   - `>` $\rightarrow$ `&gt;`
   - `"` $\rightarrow$ `&quot;`
   - `'` $\rightarrow$ `&#x27;`
   - `&` $\rightarrow$ `&amp;`
2. **Girdi Doğrulama (Input Validation):** Beklenen formatın dışındaki özel karakterler sıkı bir beyaz liste (allowlist) ile filtrelenmelidir.
3. **Content Security Policy (CSP):** `default-src 'self'` gibi politikalarla satır içi (inline) JavaScript yürütülmesi kısıtlanmalıdır.
