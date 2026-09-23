# Username enumeration via different responses

## Konu Açıklaması (Authentication Vulnerabilities & Brute Force)

### Authentication vs. Authorization
- **Authentication (Kimlik Doğrulama):** Kullanıcının iddia ettiği kişi olduğunu doğrulama sürecidir ("Kullanıcı kim?").
- **Authorization (Yetkilendirme):** Kimliği doğrulanmış kullanıcının sistem üzerinde neleri yapmaya yetkisi olduğunu belirleme sürecidir ("Kullanıcı ne yapabilir?").

### Authentication Vulnerabilities (Kimlik Doğrulama Zafiyetleri)
Saldırganların kullanıcı hesaplarına yetkisiz erişim sağlamasına, hassas verileri sızdırmasına ve diğer gelişmiş saldırı türlerine zemin hazırlamasına neden olan güvenlik açıklarına verilen genel addır.

### Brute Force Attacks (Kaba Kuvvet Saldırıları)
Saldırganın deneme-yanılma yöntemi ile geçerli kullanıcı adı ve parolaları tahmin etmeye çalıştığı otomatize saldırı türüdür. Sadece rastgele kombinasyonlarla değil, sezgisel (heuristic) algoritmalar ve özel kelime listeleri (wordlists) kullanılarak da gerçekleştirilir.

### Username Enumeration (Kullanıcı Adı Numaralandırma)
Web uygulamasının geçerli ve geçersiz kullanıcı adları için farklı HTTP yanıtları (yanıt metni, hata kodu, yanıt süresi vb.) döndürmesi durumudur. Saldırgan bu davranış farklılıklarını inceleyerek sistemde tanımlı geçerli kullanıcı adlarını tespit edebilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Username enumeration via different responses
- **Zafiyet Türü:** Authentication / Brute Force (Username Enumeration)
- **Amaç:** Farklı yanıtlar üzerinden kullanıcı adı numaralandırması ve parola Brute Force yapıp hesaba giriş sağlamak.

### Çözüm Adımları
1. **İsteğin Yakalanması ve Intruder'a Gönderilmesi:**
   - Login sayfasında rastgele kullanıcı adı ve parola girilerek hatalı bir giriş yapılır.
   - Burp Suite **Proxy > HTTP history** sekmesinden `/login` isteği yakalanır ve **Intruder** aracına gönderilir (`Ctrl+I` / `Cmd+I`).

2. **Kullanıcı Adı Numaralandırma (Username Enumeration):**
   - Intruder sekmesinde **Sniper** saldırı türü seçilir ve `username` parametresi payload pozisyonu olarak işaretlenir.
   - Verilen kullanıcı adı listesi (usernames wordlist) payload olarak eklenir ve saldırı başlatılır.
   - Yanıtlar ve yanıt uzunlukları (Length/Response) incelendiğinde, belirli bir kullanıcı adı için sunucunun diğerlerinden farklı bir hata mesajı döndürdüğü görülür (örneğin diğerlerinde *"Invalid username"*, geçerli kullanıcı adında *"Incorrect password"*).
   - Böylece sistemde tanımlı geçerli kullanıcı adı tespit edilmiş olur.

3. **Parola Brute Force Saldırısı:**
   - Bulunan geçerli kullanıcı adı `username` parametresine sabit olarak yazılır.
   - Bu kez `password` parametresi payload pozisyonu olarak işaretlenir.
   - Verilen parola listesi (passwords wordlist) payload olarak yüklenir ve Brute Force saldırısı başlatılır.
   - HTTP `302 Found` yönlendirmesi veya başarılı yanıt veren parola tespit edilerek hedef hesaba giriş sağlanır.
