# Username enumeration via response timing

## Konu Açıklaması (Response Timing & Rate Limit Bypass via Headers)

### Response Times (Yanıt Süreleri ile Analiz)
Uygulama geçerli veya geçersiz kullanıcı adları için aynı hata mesajını ve aynı HTTP durum kodunu döndürse bile, arka planda çalışan işlemler süresel farklılıklara yol açabilir:
* Kullanıcı adı sistemde **yoksa**, uygulama hemen hata döndürür ve yanıt süresi kısa olur.
* Kullanıcı adı sistemde **varsa**, uygulama girilen parolanın doğruluğunu kontrol etmek için zaman alan karmaşık bir kriptografik hash fonksiyonu (örn. bcrypt, PBKDF2, Argon2 vb.) çalıştırır.
* Bu durum, geçerli kullanıcı adı denemelerinde HTTP yanıt süresinin ölçülebilir şekilde uzamasına yol açar. Geçerli kullanıcı adı tespitinde bilerek çok uzun bir sahte parola göndermek, hash hesaplama süresini daha da artırarak zaman farkını belirginleştirebilir.

### IP Tabanlı Engelleme & Rate Limiting Atlatma
* Hatalı giriş denemeleri sonucu IP kısıtlaması (rate limiting / IP lock) uygulandığında, uygulama istemci IP adresini doğrudan TCP soketinden değil de ters vekil sunucu (reverse proxy) başlıklarından okuyorsa bu mekanizma atlatılabilir.
* İstek başlığına `X-Forwarded-For: <sahte-ip>` eklenerek her istekte bu IP değeri değiştirildiğinde güvenlik duvarı veya uygulamanın rate limit filtresi aşılabilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Username enumeration via response timing
- **Zafiyet Türü:** Authentication / Brute Force (Response Timing & IP Rate Limit Bypass)
- **Amaç:** Username enumeration zafiyeti içeren sistemde yanıt sürelerini (response timing) analiz ederek geçerli kullanıcı adı ve şifreyi bulup hesaba giriş sağlamak.
- **Elde Edilen Bilgiler:**
  - **Username:** `am`
  - **Password:** `micheal`

### Çözüm Adımları

1. **İsteği Yakalama ve Davranışı Gözlemleme:**
   * Login sayfasına gidin ve rastgele yanlış bilgilerle giriş denemesi yapın.
   * Çıkan isteği Repeater'a gönderin ve verilen kullanıcı bilgilerini kullanarak denemeler yapın.

2. **IP Engeli (Rate Limit) Tespiti ve Atlatılması:**
   * Bir noktadan sonra hatalı giriş yapıldığı için IP adresi engeli (rate limit / IP lock) devreye girecektir.
   * Bu engeli aşmak için istek içerisine `X-Forwarded-For` başlığını ekleyin ve her birkaç istekte bir bu IP değerini değiştirin.

3. **Intruder Yapılandırması (Pitchfork Saldırısı):**
   * İsteği **Intruder**'a gönderin.
   * Hem `username` hem de `X-Forwarded-For` değerlerini payload pozisyonu olarak belirleyin (Pitchfork attack türü ile senkronize IP değiştirerek).
   * Payload listelerini yükleyip saldırıyı başlatın.

4. **Response Timing Farkını Belirginleştirme:**
   * Yanıt sürelerini inceleyin. Her bir denemede belirgin bir fark görülmüyorsa tekrar Repeater'a gelin:
   * Geçerli kullanıcı adı ile birlikte bilerek **çok uzun bir sahte şifre** gönderildiğinde, parolanın hashlenme süresinden dolayı yanıt süresinin belirgin şekilde uzadığını fark edeceksiniz.

5. **Kullanıcı Adı Tespiti:**
   * Bu yöntemi kullanarak Intruder'da şifre alanına uzun bir metin verip kullanıcı adı listesini taratın (her istekte `X-Forwarded-For` değerini değiştirmeyi unutmayın).
   * Saldırı bittiğinde bir değer için yanıt süresinin diğerlerine göre çok daha uzun sürdüğünü göreceksiniz. Bu değer geçerli kullanıcı adıdır (`am`).

6. **Parola Brute-Force Saldırısı:**
   * Bulunan kullanıcı adını sabit parametre olarak yazın.
   * Bu sefer parola alanını payload olarak belirleyin ve parola listesiyle saldırıyı başlatın.

7. **Giriş ve Labın Tamamlanması:**
   * Yanıt olarak **302 Found** kodu dönen isteğin parolasını alın (`micheal`).
   * Bulduğunuz geçerli bilgilerle sisteme başarıyla giriş yapın.
