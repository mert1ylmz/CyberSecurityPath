# 2FA broken logic

## Konu Açıklaması (Flawed Two-Factor Verification Logic & 2FA Brute-Forcing)

### 1. Flawed Two-Factor Verification Logic (Kusurlu İki Aşamalı Doğrulama Mantığı)
Bazı sistemlerde kullanıcı ilk aşamayı (kullanıcı adı ve şifre) tamamladıktan sonra web sitesi ikinci aşamaya geçerken hangi hesabı doğruladığını güvensiz şekilde takip eder.

#### Zafiyetli İstek Akışı Örneği:
1. **Birinci Aşama:**
   ```http
   POST /login-step1 HTTP/1.1
   Host: vulnerable-website.com

   username=carlos&password=qwerty
   ```
2. **Sunucu Yanıtı ve Cookie Ataması:**  
   Sunucu kullanıcıyı doğrular ve ikinci adıma geçerken kimliği belirten bir çerez tanımlar:
   ```http
   HTTP/1.1 200 OK
   Set-Cookie: account=carlos
   ```
3. **İkinci Aşama Doğrulama Sayfası:**
   ```http
   GET /login-step2 HTTP/1.1
   Cookie: account=carlos
   ```
4. **Kod Gönderimi:**  
   Kullanıcı doğrulama kodunu girip gönderdiğinde, sunucu isteğin hangi hesaba ait olduğunu sadece bu çereze (`Cookie: account=...`) bakarak belirler:
   ```http
   POST /login-step2 HTTP/1.1
   Host: vulnerable-website.com
   Cookie: account=carlos

   verification-code=123456
   ```

> **Tehlike:** Bu mimaride saldırgan, kurbanın şifresini bilmese dahi istekteki `account` çerezini hedef kurbanın (`carlos`) kullanıcı adıyla değiştirip geçerli bir kodu brute-force ederek kurbanın hesabını ele geçirebilir.

---

### 2. Brute-Forcing 2FA Verification Codes (2FA Kodlarına Kaba Kuvvet Saldırısı)
Şifrelerde olduğu gibi 2FA kodları için de web uygulamalarının brute-force saldırılarına karşı hız sınırlaması (rate limiting) veya hesap kilitleme önlemleri alması gerekir. 2FA kodları çoğunlukla yalnızca **4 veya 6 haneli nümerik** değerlerden oluştuğu için, yeterli koruma yoksa kaba kuvvet saldırısıyla bulunmaları oldukça kolaydır.

Bazı web siteleri, kullanıcı çok sayıda hatalı deneme yaptığında oturumu sonlandırarak koruma sağlamaya çalışır. Ancak bu kurgu iyi geliştirilmemişse ve oturum sonlandırılsa dahi üretilen kod geçersiz kılınmıyorsa, saldırganlar için etkin bir güvenlik sağlamaz.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** 2FA broken logic
- **Zafiyet Türü:** Multi-Factor Authentication (Flawed 2FA Logic & Brute-Force)
- **Amaç:** İki aşamalı doğrulama mantığı bozuk olan sistemde mantık hatasını kullanarak `carlos` kullanıcısının hesabına yetkisiz erişim sağlamak.
- **Referans Bilgiler:**
  - **Hedef Kullanıcı:** `carlos`
  - **Örnek Kod Aralığı:** `0922`, `0975` vb. (4 haneli nümerik kodlar)
  - **Kendi Hesabımız:** `wiener:peter`

### Çözüm Adımları

1. **İsteğin Yakalanması ve Mantık İncelemesi:**
   * `/login` sayfasına gidin, verilen kendi kimlik bilgilerinizle giriş yapın ve 2FA ekranında kasıtlı olarak yanlış bir 2FA kodu girin.
   * Arka planda giden HTTP isteklerini Burp Suite üzerinden inceleyin. Sunucunun doğrulanacak kullanıcıyı `verify` çerezinde tuttuğunu tespit edin.

2. **Hedef Kullanıcı İçin Kod Üretimini Tetikleme:**
   * `GET /login2` isteğini **Burp Repeater**'a gönderin.
   * İstekteki oturum çerezini (`session`) kendi değeriniz olarak bırakın, ancak `verify` çerezinin değerini `carlos` olarak değiştirip isteği gönderin. *(Bu işlem Carlos için sunucu tarafında yeni bir 2FA kodu üretilmesini tetikler).*

3. **Turbo Intruder ile 4 Haneli Kod Brute-Force:**
   * Daha sonra hatalı kod girdiğimiz `POST /login2` isteğini yakalayarak **Turbo Intruder**'a gönderin.
   * İstek başlıklarındaki `verify` çerezini `carlos` olarak düzenleyin.
   * Turbo Intruder üzerinde 4 haneli tüm olası kodları (`0000` - `9999`) deneyecek Python script'ini hazırlayın:
     * İstekleri gönderin ve HTTP `302 Found` (yönlendirme) veya başarılı dönen yanıtı filtreleyin.

4. **Oturum Çerezinin Değiştirilmesi ve Labın Tamamlanması:**
   * Başarılı yanıttan elde edilen `session` çerezini kopyalayın.
   * Tarayıcının **Developer Tools -> Storage -> Cookies** kısmından mevcut oturum çerezi ile değiştirin.
   * Adres satırına `/my-account` yazarak Carlos'un hesabına erişin ve laboratuvarı tamamlayın.
