# DOM XSS in document.write sink using source location.search

## Konu Açıklaması (DOM-based XSS: Source & Sink)

**DOM-based Cross-Site Scripting (DOM XSS)**, istemci tarafında çalışan JavaScript kodunun, saldırgan tarafından kontrol edilebilen bir kaynaktan (**Source**) veri alıp bu veriyi dinamik kod yürütmeyi veya kontrolsüz HTML işlemeyi destekleyen güvensiz bir alıcıya (**Sink**) aktarmasıyla meydana gelir.

* **Farkı:** Reflected ve Stored XSS'te zararlı kod doğrudan sunucunun HTTP yanıtındaki HTML içerisinde gelirken; DOM XSS'te sunucudan gelen yanıt tamamen statik ve zararsız olabilir. Zafiyet, **sayfa yüklendikten sonra tarayıcının kendi JavaScript kodlarının DOM nesnelerini güvensizce manipüle etmesinden** kaynaklanır.
* **Source (Kaynak):** Kullanıcı tarafından kontrol edilebilen `window.location.search`, `location.hash`, `document.referrer` gibi JavaScript nesneleridir.
* **Sink (Yürütme Noktası):** `document.write()`, `innerHTML`, `outerHTML`, `eval()`, `setTimeout()` gibi veriyi doğrudan HTML veya kod olarak yorumlayan tehlikeli fonksiyon ve özelliklerdir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** DOM XSS in document.write sink using source location.search
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Apprentice
- **Zafiyet Türü:** DOM-based Cross-Site Scripting (DOM XSS)
- **Kaynak (Source):** `location.search`
- **Alıcı / Yürütme Noktası (Sink):** `document.write`
- **Bağlam (Context):** `<img>` Etiketi İçi Öznitelik Bağlamı (`src="..."` attribute context)
- **Amaç:** Arama kutusu üzerinden enjeksiyon yaparak bir `alert()` fonksiyonu tetiklemek.

---

### Çözüm Adımları

1. **Kaynak ve Bağlam Tespiti:**
   - Web sitesindeki arama kutusuna benzersiz bir test değeri girilir (örneğin: `test1234`) ve arama yapılır.
   - URL adresi kontrol edilir: `https://lab-id.web-security-academy.net/?search=test1234`

2. **DOM İncelemesi (DevTools):**
   - Sayfada sağ tıklanarak **İncele (Inspect)** seçilir veya `F12` ile Geliştirici Araçları açılır.
   - `Elements` sekmesinde `Ctrl + F` (veya `Cmd + F`) ile `test1234` ifadesi aranır.

3. **İstemci Tarafındaki Zafiyetli Kodun Analizi:**
   - Sayfa kaynağında çalışan JavaScript betiği incelendiğinde şu fonksiyon tespit edilir:
     ```javascript
     function trackSearch(query) {
         document.write('<img src="/resources/images/tracker.gif?searchTerms=' + query + '">');
     }
     var query = (new URLSearchParams(window.location.search)).get('search');
     if(query) {
         trackSearch(query);
     }
     ```
   - **Analiz:** Kod, `location.search` içerisindeki `search` parametresini (`query`) okumakta ve hiçbir filtre uygulamadan `document.write()` fonksiyonu aracılığıyla bir `<img>` etiketinin `src` özniteliğine string birleştirme (`+`) ile eklemektedir.

4. **Öznitelikten Kaçış (Attribute Breakout) ve Payload Girişi:**
   - `src="..."` özniteliğinden çıkmak için bir çift tırnak (`"`) kullanılır.
   - Yeni bir `<script>` etiketi açmaya veya `>` ile etiketi kapatmaya gerek kalmadan, mevcut `<img>` etiketine JavaScript olay dinleyicisi (`onload` veya `onerror`) eklenir:
     ```text
     123" onload="alert(1)
     ```
     *(Alternatif: `123" onerror="alert(1)`)*
   - Arama kutusuna bu değer yazılıp **Search** butonuna basılır.

5. **Sonuç:**
   - Görsel DOM ağacına eklendiğinde `onload` olayı anında tetiklenir, `alert(1)` penceresi açılır ve laboratuvar tamamlanır.

---

### Teknik Analiz (Neden Çalıştı?)

* **Attribute Breakout Mekanizması:**
  `document.write` tarafından oluşturulması hedeflenen orijinal HTML şablonu:
  ```html
  <img src="/resources/images/tracker.gif?searchTerms=GIRDI">
  ```
  Biz `123" onload="alert(1)` payload'unu verdiğimizde tarayıcının DOM ağacına yazdığı nihai HTML çıktısı şu şekle bürünmüştür:
  ```html
  <img src="/resources/images/tracker.gif?searchTerms=123" onload="alert(1)">
  ```
* Görüldüğü gibi çift tırnak (`"`) sayesinde `searchTerms` parametresi kapatılmış, `onload="alert(1)"` yeni bir HTML özniteliği olarak eklenmiş ve görsel kaynağı yüklendiğinde JavaScript motoru tarafından doğrudan çalıştırılmıştır.

---

## Korunma Yöntemleri (Remediation)

1. **Güvensiz Sink'lerden Kaçınma:**
   `document.write()`, `innerHTML` veya `outerHTML` gibi ham HTML işleyen metotlar yerine, yalnızca güvenli metin (text) işleyen güvenli API'ler kullanılmalıdır:
   - `element.textContent`
   - `element.innerText`
2. **Güvenli DOM Manipülasyonu:**
   HTML string birleştirmesi yerine doğrudan DOM nesneleri oluşturulmalıdır:
   ```javascript
   const img = document.createElement('img');
   img.src = '/resources/images/tracker.gif?searchTerms=' + encodeURIComponent(query);
   document.body.appendChild(img);
   ```
3. **URL Parametrelerini Encode Etme:**
   Eğer verinin bir URL parametresi veya öznitelik içinde yer alması zorunluysa, mutlaka `encodeURIComponent()` fonksiyonundan geçirilmelidir.
