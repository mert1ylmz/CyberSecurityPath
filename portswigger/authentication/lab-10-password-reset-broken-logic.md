# Password reset broken logic

## Konu Açıklaması (Resetting User Passwords & Broken Logic Flaws)

### 1. Resetting User Passwords (Şifre Sıfırlama Mekanizmaları)
Kullanıcıların parolalarını unutmaları sık karşılaşılan bir durumdur; bu nedenle web uygulamaları alternatif kimlik doğrulama adımları sunarak şifre sıfırlama mekanizması kurarlar. Bu mekanizma doğrudan hesap erişimini etkilediğinden kritik öneme sahiptir.

#### Yaygın Yöntemler ve Riskleri:
* **E-posta ile Yeni Şifre Gönderimi:** Bazı sistemler rastgele bir şifre üretip bunu doğrudan kullanıcının e-posta adresine iletir. Ancak e-posta protokolleri uçtan uca şifrelenmediğinde ve güvenli kabul edilmediğinde bu yöntem **Man-in-the-Middle (MitM)** ve dinleme saldırılarına karşı risk barındırır.
* **URL Tabanlı Sıfırlama Bağlantısı:** Daha güvenli olan bu yöntemde kullanıcıya tek kullanımlık bir bağlantı gönderilir. Bu bağlantıdaki token'ın:
  - Yüksek entropili (tahmin edilemez / kriptografik olarak güvenli) olması,
  - Kullanıcı hesabı ile sunucu tarafında sıkı şekilde eşleştirilmesi,
  - Belirli bir geçerlilik süresine (TTL) sahip olması ve tek bir kullanımdan sonra derhal geçersiz kılınması gerekmektedir.

---

### 2. Broken Logic in Password Reset (Mantık Hataları)
Şifre sıfırlama akışında token doğrulaması ile formun işlenmesi adımları birbirinden bağımsız ele alındığında kritik mantık açıkları doğabilir:
* Token doğrulandıktan sonra sunucu, şifresi değiştirilecek kullanıcıyı istek gövdesindeki (body) veya gizli formdaki `username` parametresinden alabilir.
* Token parametresi istekten tamamen kaldırıldığında veya manipüle edildiğinde sunucu bu kontrolü atlayarak (bypass) şifre güncelleme işlemini doğrudan parametrede belirtilen hedef kullanıcı için gerçekleştirebilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Password reset broken logic
- **Zafiyet Türü:** Authentication / Broken Password Reset Logic
- **Amaç:** Şifre sıfırlama fonksiyonundaki mantık hatasını kullanarak `carlos` kullanıcısının şifresini sıfırlamak ve `/my-account` sayfasına erişmek.
- **Referans Bilgiler:**
  - **Hedef Kullanıcı:** `carlos`
  - **Kendi Hesabımız:** `wiener:peter` (veya test e-posta erişimi olan kullanıcı)
  - **Araçlar:** Burp Suite (Proxy, Repeater)

### Çözüm Adımları

1. **Şifre Sıfırlama Akışının Başlatılması:**
   * Login sayfasındaki **"Forgot password?"** bağlantısına tıklayın.
   * Kendi kullanıcınız (`wiener`) için şifre sıfırlama talebinde bulunun.
   * **Email client** sekmesine gidin ve gelen e-postadaki şifre sıfırlama bağlantısını açın:
     ```text
     https://YOUR-LAB-ID.web-security-academy.net/forgot-password?temp-forgot-password-token=...
     ```

2. **Şifre Sıfırlama İsteğinin Yakalanması:**
   * Açılan formda yeni bir şifre girin ve formu gönderin.
   * Burp Suite **HTTP history** sekmesinden giden `POST /forgot-password?temp-forgot-password-token=...` isteğini yakalayın ve **Repeater**'a gönderin (`Ctrl+R` / `Cmd+R`).

3. **İstek Parametrelerinin İncelenmesi:**
   * İstek detayları incelendiğinde parametrelerin şu şekilde iletildiği görülür:
     ```http
     POST /forgot-password?temp-forgot-password-token=TOKEN_DEGERI HTTP/1.1
     Host: YOUR-LAB-ID.web-security-academy.net
     ...

     temp-forgot-password-token=TOKEN_DEGERI&username=wiener&new-password-1=password123&new-password-2=password123
     ```

4. **Mantık Hatasının İstismar Edilmesi (Token Bypass):**
   * URL query string'indeki `?temp-forgot-password-token=...` parametresini tamamen silin (veya token'ı boş bırakın).
   * İstek gövdesindeki (body) `temp-forgot-password-token` alanını silin veya kaldırın.
   * `username` parametresini `carlos` olarak değiştirin ve dilediğiniz yeni bir parola belirleyin:
     ```http
     POST /forgot-password HTTP/1.1
     Host: YOUR-LAB-ID.web-security-academy.net
     ...

     username=carlos&new-password-1=hacked123&new-password-2=hacked123
     ```
   * Sunucunun token değerini doğrulamadan yalnızca gönderilen `username` değerine ait hesabı güncellediğini gözlemleyin (`HTTP 302 Found`).

5. **Giriş Yapılması ve Labın Tamamlanması:**
   * Login sayfasına dönün.
   * Kullanıcı adı olarak `carlos`, şifre olarak belirlediğiniz yeni parolayı (`hacked123`) girerek giriş yapın.
   * Carlos'un `/my-account` sayfasına başarıyla erişerek laboratuvarı tamamlayın.
