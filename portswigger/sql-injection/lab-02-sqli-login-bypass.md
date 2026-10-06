# SQL injection vulnerability allowing login bypass

## Konu Açıklaması (Login Bypass via SQL Injection)
Birçok web uygulamasında kullanıcı girişi doğrulanırken SQL sorgusu doğrudan girdilerle oluşturulur:
`SELECT * FROM users WHERE username = 'USER_INPUT' AND password = 'PASSWORD_INPUT'`

- Eğer `username` alanı sanitize edilmiyorsa, saldırgan tek tırnak (`'`) ve yorum satırı (`--` veya `#`) kullanarak sorgunun şifre kontrolü yapan `AND password = ...` kısmını devre dışı bırakabilir.
- Böylece parola doğrulaması yapılmadan hedef kullanıcı olarak sisteme giriş sağlanır.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** SQL injection vulnerability allowing login bypass
- **Zafiyet Türü:** SQL Injection (Login Bypass)
- **Amaç:** SQL Injection zafiyetini sömürerek `administrator` kullanıcısı olarak sisteme giriş yapmak.

### Çözüm Adımları
1. **Giriş Formunun İncelemesi:**
   - Login sayfasına (`/login`) gidilir.
   - Kullanıcı adı kısmına `administrator`, parola kısmına rastgele bir metin yazılarak istek atılır.
   - Burp Suite **Proxy > HTTP history** sekmesinden `POST /login` isteği yakalanır ve **Repeater** sekmesine aktarılır.

2. **SQL Injection Payload'unun Hazırlanması:**
   - `username` parametresinin değeri `administrator'--` olarak ayarlanır.
   - Arka planda çalışan sorgu şu hale gelir:
     `SELECT * FROM users WHERE username = 'administrator'--' AND password = '...'`
   - Sorguda `administrator` kullanıcısı bulunduktan sonra kalan parola şartı yorum satırı (`--`) olduğu için göz ardı edilir.

3. **Giriş İşleminin Gerçekleştirilmesi:**
   - Düzenlenen istek Repeater üzerinden gönderilir.
   - Sunucudan `302 Found` yanıtı alınır ve `administrator` oturum çerezleri elde edilir.
   - Yönetici olarak hesaba başarıyla giriş yapılır ve lab tamamlanır.
