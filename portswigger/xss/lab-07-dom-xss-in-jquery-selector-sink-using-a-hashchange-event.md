# DOM XSS in jQuery selector sink using a hashchange event

## Konu Açıklaması (DOM-based XSS: jQuery `$()` Selector Sink & `hashchange` Event)

### A. jQuery Seçici Fonksiyonu (`$()`) Bir Sink Olarak Nasıl Çalışır?

jQuery'nin `$()` (veya `jQuery()`) fonksiyonu hem DOM elemanlarını seçmek için (örn. `$('div')`, `$('#header')`) hem de dinamik HTML nesneleri oluşturmak için kullanılır.

Eski veya güvenlik yaması almamış jQuery sürümlerinde, `$()` fonksiyonuna verilen dize bir CSS seçici yerine `<` karakteriyle başlayan veya HTML etiketi barındıran bir dize içeriyorsa, jQuery bunu bir sorgu seçicisi yerine **yeni bir HTML öğesi oluşturma komutu** olarak yorumlar. Eğer bu dize kullanıcı kontrolündeki bir kaynaktan (`location.hash` gibi) filtrelenmeden doğrudan `$()` içine aktarılırsa, saldırgan tarayıcıda rastgele HTML/JavaScript kodu çalıştırabilir.

### B. `hashchange` Olayı Neden Gereklidir?

Bir web uygulamasında URL'in `#` (fragment) kısmında değişiklik yapıldığında sayfa yeniden yüklenmez; bunun yerine tarayıcı `hashchange` olayını tetikler.

Geliştiriciler genellikle URL'deki hash değerine göre sayfada belirli bir başlığa kaydırma yapmak için şu yapıyı kullanırlar:

```javascript
$(window).on('hashchange', function() {
    var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
    if (post) post.get(0).scrollIntoView();
});
```

* Sayfa ilk açıldığında `hashchange` olayı kendiliğinden **tetiklenmez** (sayfa henüz yüklenmiştir, hash henüz değişmemiştir).
* Saldırgan kurbanı doğrudan zararlı `#payload` içeren bir URL'ye yönlendirirse `hashchange` çalışmaz.
* Bu nedenle saldırgan, kurbanın tarayıcısında bu olayı **otomatik olarak tetiklemek** için bir `<iframe>` kullanır.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** DOM XSS in jQuery selector sink using a `hashchange` event
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Practitioner
- **Zafiyet Türü:** DOM-based Cross-Site Scripting (DOM XSS)
- **Kaynak (Source):** `location.hash` / `window.location.hash`
- **Alıcı Fonksiyon (Sink):** jQuery `$()` seçici fonksiyonu (`$() selector`)
- **Tetikleyici Olay (Event):** `hashchange`
- **Hedef:** Kurbanın tarayıcısında otomatik olarak `hashchange` olayını tetikleyip `print()` fonksiyonunu çalıştıran bir istismar sayfası (Exploit Server) hazırlamak.

---

### Kaynak Kod ve Taint Flow Analizi

Lab ana sayfasının kaynak kodları incelendiğinde aşağıdaki JavaScript bloğu tespit edilir:

```javascript
$(window).on('hashchange', function(){
    var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
    if (post) post.get(0).scrollIntoView();
});
```

#### Veri Akışı (Taint Flow) İncelemesi:
1. **Source (Kaynak):** `window.location.hash.slice(1)`
   * URL'deki `#` karakterinden sonra gelen tüm metin alınır ve `decodeURIComponent()` ile çözülür.
2. **Sink (Alıcı):** `$('section.blog-list h2:contains(' + ... + ')')`
   * Kullanıcı girdisi doğrudan `$()` fonksiyonuna parametre olarak verilir.
   * Girdi `<img src=x onerror=print()>` olduğunda, jQuery seçici ifadesi bozulur ve jQuery bu dizeyi doğrudan HTML ayrıştırıcısına (parser) yönlendirir.

---

### İstismar (Exploit) Mekanizması

#### `<iframe>` ile Çift Yükleme (Double Load) Yöntemi

Kurbanın tarayıcısında `hashchange` olayını sıfır etkileşimle zorlamak için Exploit Server üzerinde şu payload kurgulanır:

```html
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/#" onload="this.src+='<img src=x onerror=print()>'"></iframe>
```

#### Adım Adım Çalışma Mantığı:
1. `iframe` ilk olarak `src="https://YOUR-LAB-ID.web-security-academy.net/#"` adresini yükler.
2. Sayfanın ilk yüklemesi tamamlandığında `iframe`'in `onload` dinleyicisi çalışır.
3. `onload` fonksiyonu `this.src` adresinin sonuna `<img src=x onerror=print()>` dizesini ekler:
   `https://YOUR-LAB-ID.web-security-academy.net/#<img src=x onerror=print()>`
4. Tarayıcı adres çubuğundaki hash'in değiştiğini algılar ve hedef sayfadaki **`hashchange` olayını tetikler**.
5. jQuery kod bloğu çalışır, `decodeURIComponent()` girdiyi açar ve `$()` seçicisine iletir.
6. jQuery zararlı `<img>` etiketini bellekte oluşturur; görsel bulunamadığında `onerror` tetiklenir ve `print()` fonksiyonu kurbanın tarayıcısında çalışır.

---

### Adım Adım Çözüm Metodolojisi

1. **Hedef Kodu İnceleyin:**
   Lab ana sayfasında DevTools (`F12`) açarak `$(window).on('hashchange', ...)` bloğunu teyit edin.

2. **Exploit Server'ı Açın:**
   Lab başlığından **Go to exploit server** butonuna tıklayın.

3. **İstismar Kodunu Hazırlayın:**
   `Body` alanına aşağıdaki kodu ekleyin (`YOUR-LAB-ID` alanını güncelleyin):
   ```html
   <iframe src="https://YOUR-LAB-ID.web-security-academy.net/#" onload="this.src+='<img src=x onerror=print()>'"></iframe>
   ```

4. **Yerel Test:**
   **Store** ve ardından **View exploit** butonuna tıklayarak tarayıcıda yazdırma penceresinin (`print()`) açıldığını doğrulayın.

5. **Kurbana İletin:**
   Exploit server'a dönüp **Deliver to victim** butonuna basarak laboratuvarı çözün.

---

### Güvenli Kodlama (Remediation)

Kullanıcı kontrolündeki hash verisi doğrudan jQuery seçici dizesine birleştirilmemeli; bunun yerine DOM elemanları seçildikten sonra metin içerikleri güvenli şekilde (`.text()`) karşılaştırılmalıdır:

```javascript
$(window).on('hashchange', function(){
    var hashVal = decodeURIComponent(window.location.hash.slice(1));
    // Başlıkların metin içeriğini doğrudan karşılaştırarak güvenli arama yapın
    $('section.blog-list h2').filter(function() {
        return $(this).text() === hashVal;
    }).first().each(function() {
        this.scrollIntoView();
    });
});
```

