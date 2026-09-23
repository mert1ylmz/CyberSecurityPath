# User ID controlled by request parameter with password disclosure

## Konu Açıklaması (Horizontal to Vertical Privilege Escalation)
Saldırgan ilk olarak yatay yetki yükseltme (Horizontal Privilege Escalation) tekniklerini kullanarak kendi seviyesindeki başka bir kullanıcının (örneğin hedef kullanıcının veya yöneticinin) hesabındaki hassas verileri (parola, token, sıfırlama bağlantısı vb.) ele geçirir.

- Ele geçirilen bu hassas bilgiler (Password Disclosure) kullanılarak daha üst düzey yetkilere sahip hesaba (örneğin Admin) giriş yapılır ve dikey yetki yükseltme (Vertical Privilege Escalation) gerçekleştirilir.
- **Örnek parametreler:** `/my-account?id=carlos`, `/my-account/change-password?id=carlos`

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** User ID controlled by request parameter with password disclosure
- **Zafiyet Türü:** Access Control (Horizontal to Vertical Privilege Escalation)
- **Amaç:** Yönetici şifresini sızdıran zafiyeti kullanarak admin şifresini ele geçirmek, giriş yapmak ve `carlos` kullanıcısını silmek.

### Çözüm Adımları
1. **Oturum Açma ve İstek Manipülasyonu:**
   - Verilen kullanıcı bilgileri ile sisteme giriş yapılır.
   - `/my-account?id=...` isteğindeki `id` parametresinin değeri `administrator` olarak değiştirilir.

2. **Hassas Bilgi İfşası (Password Disclosure):**
   - Burp Suite veya tarayıcı üzerinden sunucudan dönen HTTP yanıtı ve kaynak kodlar incelenir.
   - Hesabın kaynak kodunda/formunda yöneticiye ait parolanın açık metin olarak sızdırıldığı (password disclosure) görülür ve bu şifre kopyalanır.

3. **Yönetici Girişi ve Kullanıcı Silme:**
   - Oturum kapatılır ve ele geçirilen `administrator` kullanıcı adı ve şifresi ile yönetim hesabına giriş yapılır (Dikey Yetki Yükseltme).
   - Admin paneline erişilerek `carlos` kullanıcısı silinir ve lab çözümü tamamlanır.
