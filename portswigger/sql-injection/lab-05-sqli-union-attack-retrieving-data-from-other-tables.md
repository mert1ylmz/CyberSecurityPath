# SQL injection UNION attack, retrieving data from other tables

## Konu Açıklaması (Retrieving Data from Other Tables via UNION Attacks)
Bir web uygulamasında SQL Injection zafiyeti bulunduğunda; sorgunun kaç adet sütun döndürdüğü ve bu sütunlardan hangilerinin metin (string) verisi alabildiği tespit edildikten sonra, `UNION` operatörü kullanılarak veritabanındaki diğer hassas tablolardan (örneğin kullanıcı bilgileri, kimlik doğrulama verileri vb.) veri sızdırılabilir.

Örneğin, orijinal sorgunun iki string sütun döndürdüğü ve veritabanında `username` ile `password` sütunlarına sahip bir `users` tablosu olduğu biliniyorsa/tahmin ediliyorsa:
```sql
' UNION SELECT username, password FROM users --
```
Bu sorgu çalıştırıldığında veritabanı orijinal sorgunun sonuçlarının altına `users` tablosundaki tüm kayıtları ekleyerek tek bir yanıt halinde döndürür.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** SQL injection UNION attack, retrieving data from other tables
- **Zafiyet Türü:** SQL Injection (UNION Attack - Data Retrieval)
- **Amaç:** Ürün kategorisi filtresindeki SQLi zafiyetini sömürerek `users` tablosundaki kullanıcı adı ve şifre bilgilerini ele geçirmek ve `administrator` hesabı ile sisteme giriş yapmak.

### Çözüm Adımları
1. **Zafiyetin Tespiti ve İstekin İncelenmesi:**
   - Web sitesinde herhangi bir kategori seçilir.
   - Burp Suite **Proxy > HTTP history** üzerinden `GET /filter?category=...` isteği yakalanır ve **Repeater**'a gönderilir.

2. **Kolon Sayısı ve Veri Tiplerinin Belirlenmesi:**
   - `category=' UNION SELECT 'a', 'b'--` payload'u test edilir.
   - İki sütun olduğu ve her iki sütunun da string verileri desteklediği doğrulanır.

3. **Verilerin Sızdırılması:**
   - `category` parametresi `users` tablosundan veri çekecek şekilde düzenlenir:
     ```sql
     ' UNION SELECT username, password FROM users --
     ```
   - İstek gönderildiğinde dönen yanıtta `administrator` kullanıcısının parolası görüntülenir.

4. **Giriş ve Labın Tamamlanması:**
   - Giriş sayfasına (`/login`) gidilerek ele geçirilen `administrator` kullanıcı adı ve parolası ile oturum açılır, lab başarıyla tamamlanır.
