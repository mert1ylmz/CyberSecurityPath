# Username enumeration via subtly different responses

## Konu Açıklaması (Username Enumeration & Subtly Different Responses)

### Username Enumeration (Kullanıcı Adı Numaralandırma)
Saldırganın, web sitesine girdiği kullanıcı adının sistemde geçerli olup olmadığını anlayabildiği durumlardır.
* **Örnek:** Doğru kullanıcı adı girildiğinde "şifre yanlış" denmesi ya da girilen kullanıcı adının doğrudan dikkate alınması/farklı işlenmesi.

### Brute-Force Sırasında Dikkat Edilmesi Gereken Yanıt İşaretleri
Brute-force kullanarak sisteme girmeye çalışan saldırganın dikkat etmesi gereken temel yanıt işaretleri:
* **Status Codes:** Brute-force saldırısı sırasında yapılan her denemede çoğunlukla aynı HTTP status code görülür. Ancak bir tanesinin farklı olması önemli bir ipucu (güçlü bir işaret) olabilir.
* **Error Messages (Hata Mesajları):** Girilen bilgilerden hangisinin yanlış olduğuna bağlı olarak hata mesajları farklılık gösterebilir (örn. *"Invalid username"* vs *"Incorrect password"*). Kimi zaman bu farklar çok belirgin olmayıp ufak bir noktalama işareti, harf büyüklüğü veya ek bir kelime gibi incelikli (subtle) farklılıklar şeklinde karşımıza çıkar.
* **Response Times:** Gönderilen isteklerin çoğu aynı sürede dönerken, bir tanesinin belirgin olarak daha farklı bir sürede dönmesi (örn. arka plandaki hash işleminin zaman alması); girilen kullanıcı adı ve parolanın geçerli bir deneme olduğunu gösterebilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Username enumeration via subtly different responses
- **Zafiyet Türü:** Authentication / Brute Force (Subtly Different Error Messages)
- **Amaç:** Sistemi brute-force kullanarak test etmek, dönen hata mesajlarındaki küçük farklılıkları (subtle differences) yakalayarak geçerli kullanıcı adı ile şifreyi bulup sisteme giriş yapmak.
- **Elde Edilen Bilgiler:**
  - **Username:** `alabama`
  - **Password:** `qa2wsx`

### Çözüm Adımları

1. **İsteğin Yakalanması:**
   * Sayfanın login sayfasına yanlış bilgilerle deneme girişi yapın ve yakalanan login isteğini Burp Suite **Intruder** modülüne gönderin.

2. **Grep - Extract Yapılandırması:**
   * **Options** sekmesindeki **Grep - Extract** bölümüne `"Invalid username or password"` ifadesini ekleyin (veya hata mesajının döndüğü alanı işaretleyin).

3. **Kullanıcı Adı Tespiti (Username Enumeration):**
   * HTTP isteği içerisinde `username` değerini payload pozisyonu olarak seçin ve kullanıcı adı listesini (payload) yükleyin.
   * Saldırıyı başlatın ve diğerlerinden **farklı hata mesajı / çıktı döndüren** isteği tespit edin (Kullanıcı adı: `alabama`).

4. **Parola Brute-Force Saldırısı:**
   * Bu sefer tespit edilen kullanıcı adını (`alabama`) sabit tutun; `password` değerini payload pozisyonu olarak işaretleyin.
   * Parola wordlist'ini yükleyin ve saldırıyı yeniden başlatın.

5. **Giriş ve Labın Tamamlanması:**
   * **Farklı status code (302 Redirect)** dönen başarılı isteği tespit edin (Parola: `qa2wsx`).
   * Elde edilen geçerli bilgilerle sisteme giriş yapın.
