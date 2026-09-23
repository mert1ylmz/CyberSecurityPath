# TryHackMe: Web Application Security

Web uygulamalarına yönelik en yaygın saldırı türleri, güvenlik zafiyetlerinin temel kategorileri ve OWASP Top 10 kapsamında ele alınan kritik güvenlik açıkları.

## Web Saldırı Senaryoları

Bir web uygulamasındaki temel iş akışlarında karşılaşılabilecek saldırı adımları:

1. **Oturum Açma (Log in):** Saldırgan otomatize araçlar ve geniş parola listeleri (wordlist) kullanarak kullanıcı adları ve şifreler üzerinde deneme-yanılma (Brute Force) yapabilir.
2. **Ürün Arama (Search):** Arama kutusu gibi girdi alanlarına özel karakterler ve kod parçacıkları eklenerek uygulamanın dönmemesi gereken verileri dönmesi veya yetkisiz kod çalıştırması hedeflenebilir (Injection/XSS/SQLi).
3. **Ödeme Bilgileri (Payment Details):** Ödeme veya kişisel verilerin iletimi sırasında verinin açık metin (cleartext) olarak mı yoksa zayıf şifreleme yöntemleriyle mi taşındığı denetlenir.

---

## OWASP Top 10 Temel Zafiyet Kategorileri

### 1. Identification and Authentication Failure (Kimlik & Doğrulama Başarısızlığı)
- **Identification (Kimlik Tanımlama):** Bir kullanıcının sistemde benzersiz olarak tanımlanabilmesidir.
- **Authentication (Kimlik Doğrulama):** Kullanıcının iddia ettiği kişi olduğunu kanıtlama sürecidir.

**Temel Zafiyet Örnekleri:**
- Otomatize araçlarla yapılan kaba kuvvet (Brute Force) saldırılarına karşı koruma sağlanmaması.
- Kullanıcıların kolay tahmin edilebilir zayıf parolalar seçmesine izin verilmesi.
- Kullanıcı parolalarının veritabanında açık metin (plain text) olarak saklanması.

---

### 2. Broken Access Control (Bozuk Erişim Kontrolü)
Erişim kontrolü, her kullanıcının yalnızca kendi rolüne ve yetkisine uygun kaynaklara erişmesini sağlar.

**Temel Zafiyet Örnekleri:**
- **En Az Ayrıcalık İlkesine (Principle of Least Privilege)** uyulmaması; kullanıcılara ihtiyaç duyduklarından fazla yetki verilmesi (ör. müşterinin fiyatları değiştirebilmesi).
- Oturum açmamış anonim kullanıcıların yetkilendirme gerektiren sayfalara erişebilmesi.
- **IDOR (Insecure Direct Object References):** Kullanıcının sistemdeki nesnelere (dosya, hesap, kayıt) ait benzersiz id değerlerini manipüle ederek diğer kullanıcıların verilerine erişebilmesi veya değiştirebilmesi. Uygulamanın girdi verisine aşırı güvenip nesne düzeyinde yetki kontrolü yapmamasından kaynaklanır.

---

### 3. Injection (Kod Enjeksiyonu)
Kullanıcıdan alınan girdilerin yeterince doğrulanmaması (**validation**) ve temizlenmemesi (**sanitization**) sonucunda saldırganın sistemde zararlı kod veya komut çalıştırabilmesidir.

---

### 4. Cryptographic Failures (Kriptografik Başarısızlıklar)
Verilerin gizliliğini ve bütünlüğünü sağlayan şifreleme süreçlerindeki hatalardan kaynaklanır.

**Temel Zafiyet Örnekleri:**
- Hassas verilerin şifrelenmeden açık metin olarak iletilmesi (HTTPS yerine güvensiz HTTP kullanımı).
- Zayıf veya modası geçmiş şifreleme algoritmalarına güvenilmesi (ör. Sezar şifrelemesi / basit harf kaydırma: `TRY HACK ME` -> `USZ IBDL NF`).
- Kriptografik fonksiyonlarda varsayılan veya zayıf gizli anahtarların kullanılması (ör. anahtar olarak `1234` seçilmesi).
