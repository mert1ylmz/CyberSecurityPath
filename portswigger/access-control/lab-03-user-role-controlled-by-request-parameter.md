# User role controlled by request parameter

## Konu Açıklaması (Parameter-based Access Control Methods)
Bazı uygulamalar, kullanıcının erişim rolünü veya yetki düzeyini kullanıcının doğrudan müdahale edebileceği istek parametreleri üzerinden yönetir.

- Bu parametreler URL parametresi, POST body parametresi veya Cookie (çerez) içerisine yerleştirilebilir:
  - `/login/home.asp?admin=true`
  - `/login/home.asp?role=1`
  - `Cookie: admin=false`
- Erişim yetkisinin istemci (client) tarafındaki parametrelere güvenilerek belirlenmesi büyük bir güvenlik açığıdır. Kullanıcı Burp Suite veya tarayıcı araçlarıyla bu parametreleri değiştirerek yetkisiz ayrıcalıklar kazanabilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** User role controlled by request parameter
- **Zafiyet Türü:** Access Control (Parameter-based Access Control)
- **Amaç:** İstek parametrelerini manipüle ederek admin yetkilerini kazanmak ve `carlos` kullanıcısını silmek.

### Çözüm Adımları
1. **Kullanıcı Girişi ve Oturum Analizi:**
   - Lab başlatılır ve sağlanan `wiener:peter` kimlik bilgileri ile sisteme giriş yapılır.
   - Burp Suite **Proxy > HTTP history** sekmesinden giriş isteği (`/login`) ve dönen yanıt incelenir.

2. **Cookie Parametresinin Tespiti:**
   - Giriş işlemi sonrasında sunucu tarafından atanan veya sonraki isteklerde (`/my-account`) gönderilen istek başlıklarında `Cookie: admin=false` parametresinin olduğu tespit edilir.

3. **Yetki Yükseltme İstek Manipülasyonu:**
   - İlgili istek Burp Repeater sekmesine gönderilir (`Ctrl+R` / `Cmd+R`).
   - Cookie başlığındaki `admin=false` değeri `admin=true` olarak güncellenir ve istek tekrar gönderilir.
   - Sunucudan dönen yanıt incelenerek yönetim yetkilerinin aktifleştiği doğrulanır.

4. **Kullanıcının Silinmesi:**
   - `admin=true` cookie değeri korunarak silme isteği gönderilir:
     ```http
     GET /admin/delete?username=carlos HTTP/1.1
     Host: lab-id.web-security-academy.net
     Cookie: admin=true; session=...
     ```
   - `carlos` kullanıcısı başarıyla silinir ve lab tamamlanır.
