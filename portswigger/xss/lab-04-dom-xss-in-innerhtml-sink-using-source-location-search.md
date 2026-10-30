# DOM XSS in innerHTML sink using source location.search

## Konu Açıklaması (DOM-based XSS: innerHTML Sink)

**DOM-based Cross-Site Scripting (DOM XSS)**, istemci tarafında çalışan JavaScript kodunun, saldırgan tarafından kontrol edilebilen bir kaynaktan (**Source**) veri alıp bu veriyi dinamik kod yürütmeyi veya kontrolsüz HTML parse etmeyi destekleyen güvensiz bir alıcıya (**Sink**) aktarmasıyla meydana gelir.

`innerHTML`, JavaScript'te bir DOM elemanının içerdiği HTML veya XML işaretlemesini almak veya değiştirmek için kullanılan yaygın bir özelliktir. Ancak kullanıcı kontrolündeki veriler sanitize edilmeden doğrudan `innerHTML` özelliğine atandığında, tarayıcı bu veriyi ham HTML olarak yorumlar ve DOM XSS zafiyeti ortaya çıkar.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** DOM XSS in `innerHTML` sink using source `location.search`
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Apprentice
- **Zafiyet Türü:** DOM-based Cross-Site Scripting (DOM XSS)
- **Kaynak (Source):** `location.search` (`search` parametresi)
- **Alıcı Fonksiyon (Sink):** `element.innerHTML`
- **Enjeksiyon Bağlamı (Context):** HTML öğesi gövdesi (Arama sonucu alanı)
- **Hedef:** Sayfada `alert()` fonksiyonunu çalıştırarak DOM XSS zafiyetini istismar etmek.

---

### Teknik Arka Plan: Neden `<script>` Çalışmaz?

Modern tarayıcılarda W3C HTML5 spesifikasyonuna göre:  
> **`innerHTML` aracılığıyla DOM'a dinamik olarak eklenen `<script>` etiketleri güvenlik nedeniyle yürütülmez.**

Bu nedenle `innerHTML` bağlamında XSS tetiklerken doğrudan `<script>alert(1)</script>` payload'u başarısız olur. Bunun yerine tarayıcının DOM ağacına eklediği anda parse edip anında çalıştırdığı satır içi olay işleyicileri (**inline event handlers**) kullanılır. En yaygın ve etkili yöntem, yüklenmesi kasıtlı olarak geçersiz kılınan bir `<img>` etiketi ve onun `onerror` özniteliğidir.

---

### Kaynak Kod ve Taint Flow Analizi

Sayfa üzerinde ve Geliştirici Araçları (DevTools) ile arama fonksiyonunu yöneten script incelendiğinde:

```javascript
function doSearchQuery(query) {
    document.getElementById('searchMessage').innerHTML = query;
}
var query = (new URLSearchParams(window.location.search)).get('search');
if (query) {
    doSearchQuery(query);
}
```

- **Source (Kaynak):** `window.location.search` (`search` parametresi).
- **Sink (Alıcı):** `document.getElementById('searchMessage').innerHTML`
- **Zafiyet Mekanizması:** Kullanıcı kontrollü `query` değişkeni filtrelenmeden ve HTML entity encode edilmeden doğrudan `innerHTML` içerisine aktarılmaktadır.

---

### Adım Adım Çözüm Metodolojisi

1. **Arama Fonksiyonunun İncelenmesi:**
   Sayfadaki arama çubuğuna rastgele bir değer (örneğin `test1234`) yazılıp aratılır.
   URL yapısı kontrol edilir:
   ```text
   https://<LAB-ID>.web-security-academy.net/?search=test1234
   ```

2. **Sink Tespiti (DevTools):**
   Tarayıcıda `F12` ile Geliştirici Araçları açılır veya arama sonucuna sağ tıklanıp **İncele (Inspect)** denir. Arama sonucunu ekrana basan JavaScript kodu incelenir. Girdinin doğrudan `searchMessage` id'li elementin `.innerHTML` sink'ine aktığı doğrulanır.

3. **Payload Hazırlığı:**
   `innerHTML` doğrudan `<script>` bloklarını yürütmeyeceği için, DOM'a eklendiği anda hata fırlatarak JavaScript çalıştıran bir görsel etiketi hazırlanır:
   ```html
   <img src="1" onerror="alert()">
   ```

4. **İstismar ve Tetikleme:**
   Arama kutusuna payload girilir veya doğrudan URL üzerinden parametre olarak gönderilir:
   ```text
   https://<LAB-ID>.web-security-academy.net/?search=<img+src%3D1+onerror%3Dalert()>
   ```
   Tarayıcı `src="1"` adresindeki görseli bulamaz, `onerror` olayı derhal devreye girer, `alert()` fonksiyonu çalışır ve laboratuvar başarıyla tamamlanır.

---

### Güvenli Kodlama (Remediation)

Kullanıcı girdisini bir HTML elementi içerisine metin olarak basarken asla `innerHTML` kullanılmamalıdır. Bunun yerine veriyi doğrudan düz metin (plain text) olarak işleyen güvenli DOM özellikleri (`textContent` veya `innerText`) tercih edilmelidir:

```javascript
function doSearchQuery(query) {
    // Güvenli: HTML karakterleri encode edilir ve betik olarak yorumlanmaz
    document.getElementById('searchMessage').textContent = query;
}
```

Alternatif olarak, zengin metin içeriği eklenmesi zorunluysa DOMPurify gibi güvenilir kütüphanelerle HTML sanitization işlemi uygulanmalıdır:

```javascript
// DOMPurify ile güvenli HTML enjeksiyonu
document.getElementById('searchMessage').innerHTML = DOMPurify.sanitize(query);
```
