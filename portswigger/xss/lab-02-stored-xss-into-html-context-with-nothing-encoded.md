# Stored XSS into HTML context with nothing encoded

## Konu Açıklaması (Stored / Persistent XSS)

**Stored Cross-Site Scripting (Kalıcı veya İkinci Dereceden XSS)**; uygulamanın kullanıcıdan, harici bir API'den veya güvenilmeyen herhangi bir kaynaktan veri alıp, bu veriyi sunucu tarafında (veritabanı, dosya sistemi, loglar vb.) saklaması ve daha sonra başka kullanıcılara gösterirken **filtrelemeden veya HTML entity kodlaması (output encoding) yapmadan** doğrudan HTML gövdesine basması sonucu meydana gelir.

* **Etki Kapsamı:** Reflected XSS'in aksine kurbana özel hazırlanmış bir link göndermeye gerek yoktur. İlgili sayfayı (örneğin blog yazısını veya profil sayfasını) ziyaret eden **herkesin** tarayıcısında zararlı JavaScript kodu otomatik olarak çalışır.
* **Oturum Ele Geçirme:** Betik kurbanın oturum bağlamında çalıştığı için saldırgan kurbanın oturum çerezlerini (`document.cookie`), kişisel bilgilerini çalabilir veya kurban adına yetkisiz işlemler gerçekleştirebilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Stored XSS into HTML context with nothing encoded
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Apprentice
- **Zafiyet Türü:** Stored Cross-Site Scripting (XSS)
- **Bağlam (Context):** HTML Body / Yorum Alanı (Herhangi bir kodlama/filtreleme yok)
- **Amaç:** Blog yorum bölümüne JavaScript kodu enjekte ederek sayfayı ziyaret eden kullanıcılar için bir `alert()` açılır penceresi tetiklemek.

---

### Çözüm Adımları

1. **Hedef Alanın Tespiti:**
   - Web sitesinin ana sayfasına gidilir ve herhangi bir blog gönderisi seçilerek açılır.
   - Sayfanın alt kısmında ziyaretçilerin yorum yazabileceği **"Leave a comment"** formunun bulunduğu görülür.

2. **Form Alanlarının Doldurulması ve Payload Girişi:**
   - Formdaki alanlar incelendiğinde `Name`, `Email`, `Website` ve `Comment` girdileri tespit edilir.
   - **Comment** metin kutusuna doğrudan şu JavaScript yükü girilir:
     ```html
     <script>alert(1)</script>
     ```
   - Diğer alanlara standart/örnek bilgiler yazılır:
     - **Name:** `Test User`
     - **Email:** `test@example.com`
     - **Website:** `https://example.com`

3. **Yorumun Gönderilmesi (Form Submission):**
   - **"Post Comment"** butonuna tıklanarak yorum sunucuya iletilir.
   - Sunucu girdiyi doğrulamadan ve temizlemeden veritabanına kaydeder.

4. **Tetikleme ve Doğrulama:**
   - Gönderi sayfasına geri dönüldüğünde veya sayfa yenilendiğinde, tarayıcının ekrana `1` değerini içeren bir uyarı penceresi (`alert`) getirdiği gözlemlenir.
   - Lab başarıyla çözülür.

---

### Teknik Analiz (Neden Çalıştı?)

* **HTML Entity Kodlama Eksikliği:**
  Uygulama, veritabanından çekilen yorum içeriğini HTML gövdesine basarken `<` ve `>` gibi özel HTML karakterlerini güvenli muadilleri olan `&lt;` ve `&gt;` karakterlerine dönüştürmemiştir.
* **Doğrudan Yürütme:**
  Kurbanın tarayıcısı gelen HTML yanıtını ayrıştırırken (parse ederken) `<script>` etiketini bir programlama talimatı olarak yorumlamış ve JavaScript motoruna aktararak `alert(1)` fonksiyonunu anında tetiklemiştir.

---

## Korunma Yöntemleri (Remediation)

1. **Bağlama Uygun Çıktı Kodlama (Context-Aware Output Encoding):**
   HTML gövdesine yazdırılacak tüm kullanıcı verileri HTML entity formatına dönüştürülmelidir:
   - `<` $\rightarrow$ `&lt;`
   - `>` $\rightarrow$ `&gt;`
   - `&` $\rightarrow$ `&amp;`
   - `"` $\rightarrow$ `&quot;`
   - `'` $\rightarrow$ `&#x27;`
2. **HTML Sanitization:**
   Eğer zengin metin (Rich Text / Markdown) desteği gerekiyorsa, güvenilmeyen girdiler DOMPurify gibi test edilmiş bir temizleme kütüphanesinden geçirilmelidir.
3. **Content Security Policy (CSP):**
   Sayfada satır içi (inline) `<script>` çalıştırılmasını engelleyen `default-src 'self'` direktifli bir CSP başlığı tanımlanmalıdır.
