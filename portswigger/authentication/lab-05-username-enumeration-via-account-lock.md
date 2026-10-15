# Username enumeration via account lock

## Konu Açıklaması (Account Locking, Rate Limiting & HTTP Basic Authentication)

### 1. Account Locking (Hesap Kilitleme)
Web sitelerinin kaba kuvvet (brute-force) saldırılarını engellemesinin yaygın yollarından biri, hesapta şüpheli hareketler algılandığında hesabı kilitlemektir. Bu durum genellikle birkaç hatalı giriş denemesinden sonra tetiklenir.

Normal giriş hatalarından farklı olarak, sunucudan dönen hata mesajlarında hesabın kilitlendiğini açıkça belirten yanıtlar yer alabilir. Bu durum saldırgan için kullanıcı tespiti (user enumeration) açısından yol gösterici olabilir.

> **Güvenlik Açığı / Zayıf Nokta:**  
> Bu yöntem hedefli bir brute-force saldırısına karşı belirli bir koruma sağlasa da, saldırganlar **"Password Spraying"** mantığıyla rastgele veya çok sayıda kullanıcı hesabına erişim sağlamaya çalıştığında bu savunma mekanizması etkisiz kalabilir.

#### Bu Korumayı Aşma / Atlatma Mantığı:
1. **Aday Kullanıcı Adlarını Topla:** Hedef sisteme ait olası kullanıcı adlarından oluşan bir liste hazırlanır.
2. **Kısa Şifre Listesi Belirle:** Geçerli ve yaygın olacağı düşünülen çok kısa bir şifre listesi belirlenir. Seçilen şifre deneme sayısı, hedef sistemin izin verdiği maksimum başarısız giriş deneme sayısını (lockout threshold) kesinlikle aşmamalıdır.
3. **Burp Intruder ile Eşleştir:** Burp Suite Intruder veya benzeri bir otomasyon aracı kullanarak kullanıcı adları ile bu kısa şifreler eşleştirilip denemeler yapılır.

---

### 2. User Rate Limiting (İstek / Hız Sınırlaması)
Saldırganların brute-force saldırılarını engellemek için kullanılan diğer bir yöntem **Rate Limiting** (istek frekansı sınırlaması) mekanizmasıdır. Bu koruma devredeyken, kısa bir süre içerisinde çok fazla istek gönderen istemcinin IP adresi geçici veya kalıcı olarak bloklanır.

Genellikle bu IP blokajı şu yollarla kaldırılabilir:
* Belirli bir bekleme süresi geçtikten sonra **otomatik olarak**,
* Sistem yöneticisi (Admin) tarafından manuel olarak,
* Kullanıcının **CAPTCHA** doğrulamasını başarıyla tamamlaması ile.

> **Önemli Not:**  
> Limit mekanizması istemciden gelen IP adresine göre çalıştığı için, bazen tek bir HTTP isteği içerisine birden fazla şifre/kullanıcı denemesi paketlenerek (örneğin JSON array formatında toplu istek gönderilerek) hız sınırlandırması atlatılabilir.

---

### 3. HTTP Basic Authentication
Eski bir mekanizma olmasına rağmen uygulama kolaylığı nedeniyle bazı sistemlerde hâlâ **HTTP Basic Authentication** kullanıldığı görülmektedir.

#### Çalışma Mantığı:
* İstemci, sunucuya kimlik doğrulama verisi göndermek için HTTP başlıklarını kullanır.
* Kullanıcı adı ve şifre `username:password` formatında birleştirilir.
* Birleştirilen metin **Base64** algoritması ile encode edilir:
  ```http
  Authorization: Basic base64(username:password)
  ```
* Bu token tarayıcı tarafından otomatik olarak saklanır ve yönetilir. Sonraki her istekte sunucuya `Authorization` başlığı ile iletilir.

#### Zafiyetleri ve Güvenlik Sorunları:
1. **Şifreleme Değildir:** Base64 bir şifreleme değil, yalnızca bir kodlama (encoding) formatıdır; kolaylıkla decode edilebilir.
2. **MitM (Ortadaki Adam) Riski:** Kullanıcı bilgileri her istekte tekrar tekrar gönderilir. Eğer iletimde **HSTS (HTTP Strict Transport Security)** veya güçlü SSL/TLS yoksa, araya giren saldırganlar (Man-in-the-Middle) bu verileri rahatlıkla ele geçirebilir.
3. **Kaba Kuvvet Koruması Eksikliği:** Çoğu zaman brute-force saldırılarına karşı ek bir koruma mekanizması barındırmaz.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Username enumeration via account lock
- **Zafiyet Türü:** Authentication / Account Locking (Username Enumeration & Password Spraying)
- **Amaç:** Hesap kilitleme (Account Locking) koruması bulunan web uygulamasında geçerli kullanıcı adı ve şifre bilgilerini tespit edip hesaba başarılı giriş yapmak.
- **Referans Bilgiler:**
  - **Username:** `activestat`
  - **Password:** `123qwe`

### Çözüm Adımları

1. **İsteğin Yakalanması ve İncelenmesi:**
   * Uygulamanın `/login` sayfasına gidin, rastgele bilgiler girerek bir login denemesi yapın ve Burp Suite üzerinden giden HTTP isteğini yakalayın/inceleyin.

2. **Saldırı Tipinin Belirlenmesi ve Turbo Intruder:**
   * Bu saldırıda iki parametre için varyasyon (kullanıcı adları ve şifre denemeleri) gerekeceğinden normal şartlarda **Cluster Bomb** saldırı tipi kullanılır. Ancak Burp Community Edition Intruder kısıtlaması nedeniyle yavaş kalacaktır; bu yüzden **Turbo Intruder** eklentisini kullanın.

3. **Turbo Intruder Parametre İşaretleme:**
   * Login isteğini Turbo Intruder'a gönderin ve test parametresini işaretleyin:
     ```http
     username=%s&password=123qwe
     ```

4. **Kullanıcı Adı Tespiti (Hesap Kilitleme Tetikleme):**
   * Kullanıcı adlarını tespit etmek için Turbo Intruder script'ini ayarlayın. Her bir kullanıcı adına peş peşe 5 adet yanlış şifre/null istek göndererek hesabın kilitlenmesini tetikleyin.
   * Saldırıyı başlatın. Dönen HTTP yanıtlarını (response) inceleyin; diğer kullanıcılardan farklı yanıt dönen (örneğin *"Your account is locked"* uyarısı veren) kullanıcı adını not alın (`activestat`).

5. **Parola Brute-Force Saldırısı:**
   * Bu geçerli kullanıcı adı için Turbo Intruder script'ini sadece şifre denemeleri yapacak şekilde güncelleyin ve şifre listesini ekleyin.

6. **Giriş ve Labın Tamamlanması:**
   * Saldırıyı başlatın ve gelen yanıtları inceleyin. Hata mesajı içermeyen veya HTTP `302 Found` yönlendirmesi veren yanıttaki doğru şifreyi (`123qwe`) tespit edin.
   * Elde edilen bilgilerle hesaba giriş yaparak laboratuvarı tamamlayın.
