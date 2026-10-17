# Password brute-force via password change

## Konu Açıklaması (Changing User Passwords & Flawed Rate Limiting)

### 1. Changing User Passwords (Şifre Değiştirme Fonksiyonları)
Web uygulamalarında kullanıcı şifresi değiştirme akışı genellikle kullanıcının mevcut parolasını (`current-password`) doğrulamasını ve ardından yeni parolayı (`new-password-1` ve `new-password-2`) girmesini gerektirir.
* Geliştiriciler çoğu zaman giriş (login) sayfalarına hız sınırlaması (rate limiting), CAPTCHA veya hesap kilitleme mekanizmaları kurarlar.
* Ancak kimlik doğrulamış oturum gerektiren veya şifre değiştirme gibi ikincil fonksiyonlarda bu kaba kuvvet (brute-force) korumaları sıklıkla unutulur ya da gevşetilir.

---

### 2. Password Mismatch Oracle (Yanıltıcı Şifre Tekniği)
Hedef bir kullanıcının mevcut şifresini brute-force ile bulmaya çalışırken iki temel problem ortaya çıkar:
1. Şifre değiştirme formu doğru şifreyi bulduğunda şifreyi anında değiştirebilir; saldırgan şifrenin neye dönüştüğünü kontrol edemez veya hedef kullanıcıyı kilitleyebilir.
2. Form doğrulama sırası doğru kullanıldığında bir **bilgi sızıntısı (oracle)** elde edilebilir.

#### Uygulama Mantığı:
* Form gönderilirken yeni parola alanlarına birbirine **eşit olmayan** iki değer yazılır:
  ```text
  new-password-1 = aaa
  new-password-2 = bbb
  ```
* Sunucu form doğrulaması yaparken:
  - **Mevcut Şifre Yanlışsa:** Sunucu önce mevcut şifreyi kontrol eder ve *"Current password is incorrect"* hatası döndürür.
  - **Mevcut Şifre Doğruysa:** Sunucu mevcut şifreyi onaylar, yeni parolaları kıyaslar ve *"New passwords do not match"* hatası döndürür. Şifre değiştirilmez ancak parolanın doğru olduğu teyit edilmiş olur!

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Password brute-force via password change
- **Zafiyet Türü:** Authentication / Password Brute-Force (Flawed Password Change Implementation)
- **Amaç:** Şifre değiştirme fonksiyonundaki hız sınırlaması eksikliğini ve doğrulama mantığı açığını kullanarak `carlos` kullanıcısının mevcut parolasını tespit etmek ve hesabına erişim sağlamak.
- **Referans Bilgiler:**
  - **Hedef Kullanıcı:** `carlos`
  - **Kendi Hesabımız:** `wiener:peter`
  - **Araçlar:** Burp Suite (Proxy, Intruder)

### Çözüm Adımları

1. **Giriş Yapılması ve Şifre Değiştirme İsteğinin Yakalanması:**
   * Kendi geçerli kimlik bilgilerinizle (`wiener:peter`) sisteme giriş yapın.
   * `/my-account` sayfasına gidin ve şifre değiştirme formunu doldurun (örneğin mevcut şifre: `peter`, yeni şifreler: `x` ve `y`).
   * Gönder butonuna basarak `POST /my-account/change-password` isteğini Burp Suite ile yakalayın ve **Intruder** sekmesine gönderin.

2. **İstek Parametrelerinin Düzenlenmesi:**
   * İstek gövdesinde `username` parametresini hedef kullanıcı olan `carlos` olarak değiştirin:
     ```http
     POST /my-account/change-password HTTP/1.1
     Host: YOUR-LAB-ID.web-security-academy.net
     ...

     username=carlos&current-password=§test§&new-password-1=passA&new-password-2=passB
     ```
   * `new-password-1` ve `new-password-2` alanlarını birbirine **eşit olmayan** iki sabit değer olarak bırakın.
   * `current-password` parametresini payload pozisyonu olarak işaretleyin (`§...§`).

3. **Payload Listesinin Yüklenmesi:**
   * **Payloads** sekmesine geçin.
   * Payload type olarak **Simple list** seçin ve laboratuvarda sağlanan şifre listesini (passwords wordlist) yapıştırın/yükleyin.

4. **Saldırının Başlatılması ve Yanıtların Filtrelenmesi:**
   * Saldırıyı başlatın (**Start attack**).
   * Dönen HTTP yanıtlarını inceleyin:
     * Hatalı denemelerin tamamında yanıt gövdesinde *"Current password is incorrect"* yer alır.
     * Carlos'un doğru şifresi denendiğinde sunucu *"New passwords do not match"* yanıtı döner (ve yanıt uzunluğu / status code farklılaşır).
   * Bu farklı yanıtı veren payload değeri Carlos'un gerçek mevcut parolasıdır.

5. **Giriş Yapılması ve Labın Tamamlanması:**
   * Kendi oturumunuzdan çıkış yapın (`Log out`).
   * Giriş sayfasına gidin, `carlos` kullanıcı adı ve bulunan doğru parola ile sisteme giriş yapın.
   * `/my-account` sayfasına erişerek laboratuvarı tamamlayın.
