# Reflected XSS into HTML context with most tags and attributes blocked

## Konu Açıklaması (WAF Filtrelerini Atlatma & Tag / Attribute Fuzzing)

Modern web uygulamalarında XSS saldırılarına karşı sıklıkla Web Application Firewall (WAF) veya sunucu taraflı filtreleme mekanizmaları kullanılır. Bu mekanizmalar çoğunlukla kara liste (denylist / blocklist) mantığıyla çalışarak yaygın kullanılan HTML etiketlerini (`<script>`, `<img>`, `<svg>`, `<iframe>` vb.) ve olay dinleyicilerini (`onerror`, `onload`, `onclick` vb.) engeller.

Ancak kara liste tabanlı savunmalar çoğu zaman kusurludur:
1. **HTML5 Spesifikasyonu:** HTML5 ile gelen yüzlerce etiket ve onlarca yeni olay dinleyicisi (event handler) bulunmaktadır. WAF kurallarının bu etiketlerin tamamını eksiksiz kapsaması zordur.
2. **Kaba Kuvvet ile Filtre Testi (Fuzzing):** Burp Suite Intruder gibi araçlar kullanılarak WAF'ın hangi etiketleri ve hangi öznitelikleri/olay dinleyicilerini engellemediği sistematik olarak tespit edilebilir.
3. **Etkileşimsiz Tetikleme (Zero Interaction):** Kurbanın sayfada herhangi bir yere tıklamasını veya fareyi hareket ettirmesini beklemeden, sayfa/iframe boyut değişimi (`onresize`) gibi tarayıcı olayları otomatik olarak tetiklenerek XSS yürütülebilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Reflected XSS into HTML context with most tags and attributes blocked
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Practitioner
- **Zafiyet Türü:** Reflected Cross-Site Scripting (XSS) / WAF Filter Bypass
- **Kaynak (Source):** Arama sorgu parametresi (`?search=...`)
- **Bağlam (Context):** HTML Body / Yansıyan metin bağlamı
- **Kısıtlama:** Çoğu HTML etiketi ve özniteliği WAF tarafından engellenmektedir.
- **Hedef:** WAF filtrelerini atlatıp kurban etkileşimi gerektirmeksizin (zero user interaction) `print()` fonksiyonunu çalıştırmak.

---

### Adım Adım Çözüm (Walkthrough)

#### 1. WAF Korumasının Doğrulanması
Arama kutusuna standart bir XSS vektörü girilerek test edilir:
```html
<img src=1 onerror=print()>
```
Sunucu bu isteğe `400 Bad Request` yanıtı vererek `"Tag is not allowed"` hatası döner. Bu durum arama girdisinin bir WAF tarafından filtrelendiğini doğrular.

#### 2. İzin Verilen HTML Etiketlerini Tespit Etme (Burp Intruder)
WAF'ın engellemediği etiketleri bulmak için:
1. Burp Suite üzerinden arama isteği yakalanır ve **Burp Intruder** sekmesine gönderilir (`Ctrl + I` / `Cmd + I`).
2. Arama parametresi değeri `<>` olarak ayarlanır ve arasına payload pozisyonu eklenir:
   ```http
   GET /?search=<§§> HTTP/2
   ```
3. [PortSwigger XSS Cheat Sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet) sayfasına gidilir ve **"Copy tags to clipboard"** seçeneği ile tüm HTML etiketleri panoya kopyalanır.
4. Burp Intruder -> **Payloads** sekmesinde **Paste** denilerek etiket listesi yapıştırılır ve saldırı başlatılır (**Start attack**).
5. Sonuçlar HTTP durum koduna göre sıralandığında, neredeyse tüm etiketlerin `400 Bad Request` döndürdüğü, ancak `<body>` etiketinin **`200 OK`** döndürdüğü görülür.

#### 3. İzin Verilen Olay Dinleyicilerini (Event Handlers) Tespit Etme
`<body>` etiketiyle kullanılabilecek izinli öznitelik ve olay dinleyicilerini bulmak için:
1. Burp Intruder pozisyonu şu şekilde güncellenir:
   ```http
   GET /?search=<body%20§§=1> HTTP/2
   ```
2. PortSwigger XSS Cheat Sheet üzerinden **"Copy events to clipboard"** seçeneğine tıklanarak tüm JavaScript olayları panoya kopyalanır.
3. Intruder -> **Payloads** sekmesindeki eski liste temizlenip kopyalanan olaylar yapıştırılır ve saldırı başlatılır.
4. Çıkan sonuçlar incelendiğinde çoğu olayın `400` aldığı, ancak **`onresize`** olayının **`200 OK`** yanıtı döndürdüğü saptanır.

#### 4. Otomatik Tetikleme ve Exploit Server ile İstismar
`onresize` olayı normalde pencere boyutu değiştiğinde tetiklenir. Lab gereksinimi kurbanın manuel etkileşimde bulunmamasını (zero-interaction) şart koşmaktadır.

Bunu otomatik hale getirmek için **Exploit Server** üzerinde bir `<iframe>` kullanılır:
1. Lab ortamındaki **Go to exploit server** butonuna tıklanır.
2. **Body** alanına aşağıdaki exploit payload'ı yapıştırılır (kendi lab ID'niz ile güncelleyin):
   ```html
   <iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'></iframe>
   ```
3. **Store** butonuna tıklanarak exploit kaydedilir.
4. **Deliver exploit to victim** butonuna basılarak kurbana iletilir ve laboratuvar başarıyla tamamlanır.

---

### Payload ve İstismar Mekanizması

```
Exploit Sunucusu:
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>
                                                                       │                       │
                                                                       │                       └─► 2. onload tetiklenir, iframe genişliğini 100px yapar (resize)
                                                                       └─► 1. Hedef sayfa iframe içinde açılır, WAF body ve onresize'a izin verir
                                                                               │
                                                                               ▼
                                                               3. Boyut değişince onresize devreye girer:
                                                                  💥 print() fonksiyonu etkileşimsiz çalışır!
```

1. **Bağlamdan Çıkış (`">`):** Arama parametresi sayfaya yansırken tırnak ve büyüktür karakterleri ile önceki HTML yapısı kapatılır.
2. **WAF Bypass:** WAF `<body>` etiketini ve `onresize` olay dinleyicisini kara listede tutmadığı için istek engellenmeden sunucuya ulaşır ve HTML gövdesine basılır.
3. **Otomatik Tetikleme (Zero Interaction):** Kurban exploit sayfasını açtığında, `<iframe>` yüklenir yüklenmez `onload` devreye girerek iframe'in genişliğini (`style.width='100px'`) anlık olarak değiştirir. Bu boyut değişimi iframe içindeki `<body>` nesnesinin `onresize` olayını ateşler ve hiçbir kullanıcı müdahalesine gerek kalmadan `print()` fonksiyonu yürütülür.

---

## Korunma Yöntemleri (Remediation)

1. **Kara Liste (Denylist) Yerine Beyaz Liste (Allowlist) Yaklaşımı:**
   - WAF veya sunucu tarafında belirli etiketleri engellemeye çalışmak her zaman atlatılabilir (bypass edilebilir).
   - Yalnızca kesin olarak izin verilen güvenli karakterler ve yapılar kabul edilmelidir.

2. **Bağlama Uygun Çıktı Kodlama (Context-Aware Output Encoding):**
   - Kullanıcıdan gelen arama verisi HTML gövdesine basılırken HTML entity encoding uygulanmalıdır:
     - `"` $\rightarrow$ `&quot;`
     - `<` $\rightarrow$ `&lt;`
     - `>` $\rightarrow$ `&gt;`
     - `'` $\rightarrow$ `&#x27;`
     - `&` $\rightarrow$ `&amp;`

3. **Güçlü Content Security Policy (CSP):**
   - Satır içi olay dinleyicilerinin (`onresize`, `onload` vb.) çalışmasını engelleyen CSP direktifleri kullanılmalıdır:
     ```http
     Content-Security-Policy: default-src 'self'; script-src 'self';
     ```

