# User ID controlled by request parameter, with unpredictable user IDs

## Konu Açıklaması (Horizontal Privilege Escalation & IDOR)

### Horizontal Privilege Escalation (Yatay Yetki Yükseltme)
Aynı yetki seviyesindeki bir kullanıcının, kendi yetkilerine sahip başka bir kullanıcının veri, dosya veya hesap bilgilerine erişebilmesi durumudur.

- **Örnek:** `/my-account?id=123`
- Bir saldırgan `id` parametresindeki değeri (örn. `123` yerine başka bir kullanıcının ID'si olan `124`) değiştirdiğinde, sunucu yetkilendirme kontrolü yapmıyorsa diğer kullanıcının özel verilerine erişim elde etmiş olur.

### IDOR (Insecure Direct Object Reference)
Güvensiz Doğrudan Nesne Referansı zafiyetidir. Uygulama, dosya, veritabanı kaydı veya kullanıcı hesabı gibi dahili nesnelere doğrudan istemci tarafından sağlanan parametrelerle erişim verdiğinde ve erişim denetimi uygulamadığında ortaya çıkar.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** User ID controlled by request parameter, with unpredictable user IDs
- **Zafiyet Türü:** Access Control (Horizontal Privilege Escalation / IDOR)
- **Amaç:** Carlos'un hesabına erişim sağlayıp API key'ini elde etmek.

### Çözüm Adımları
1. **Oturum Açma ve İstek Analizi:**
   - Lab başlatılır ve verilen `wiener:peter` bilgileri ile giriş yapılır.
   - Burp Suite **Proxy > HTTP history** kısmından `/login` ve `/my-account` istekleri incelenir.
   - `/my-account?id=...` isteğinde kullanıcının ID'sinin tahmin edilmesi zor bir GUID/UUID olduğu görülür.

2. **Kullanıcı ID (GUID) Tespiti:**
   - Uygulama içerisindeki blog gönderileri incelenir ve `carlos` tarafından yazılmış bir blog yazısı tespit edilir.
   - Carlos'un blog gönderisi veya yazar profili detaylarına girildiğinde, Burp Suite trafiğinde Carlos'a ait kullanıcı ID'si (GUID) tespit edilir ve kopyalanır.

3. **İstek Manipülasyonu ve API Key Elde Etme:**
   - Kendi hesabımıza ait `/my-account?id=...` isteği Burp Repeater sekmesine gönderilir (`Ctrl+R` / `Cmd+R`).
   - `id` parametresine kopyalanan Carlos'un GUID değeri yapıştırılarak istek sunucuya gönderilir.
   - Sunucudan dönen HTML yanıtı incelenerek Carlos'a ait hesabın detayları ve **API key** değeri ele geçirilir.
