# Basic SSRF against the local server

## Konu Açıklaması (Server-Side Request Forgery - SSRF)
**Server-Side Request Forgery (SSRF)**, saldırganın sunucu tarafında çalışan web uygulamasını zorlayarak, uygulamanın istemediği/beklemediği dahili veya harici sunuculara HTTP istekleri göndermesini sağladığı bir zafiyet türüdür.

- Bu zafiyet sayesinde saldırgan, sunucunun erişebildiği ancak dış dünyaya kapalı olan iç ağ istemcilerine, `127.0.0.1` (localhost) adresine veya dahili mikroservislere erişim sağlayabilir.
- Sunucu güvene dayalı iç ağ yapılandırmasına sahipse, saldırgan admin panellerine erişebilir veya yetkisiz işlemler gerçekleştirebilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Basic SSRF against the local server
- **Zafiyet Türü:** Server-Side Request Forgery (SSRF)
- **Amaç:** Admin yetkilerine erişerek `carlos` isimli kullanıcıyı silmek.

### Çözüm Adımları
1. **İsteğin Tespiti ve İnceleme:**
   - Lab başlatılır ve ürünler sayfasındaki herhangi bir ürün incelenir.
   - Ürün sayfasında yer alan stok durumunu kontrol etme seçeneği (Check stock) kullanılır.
   - Burp Suite **Proxy > HTTP history** sekmesinden stok kontrolü isteği (`POST /product/stock`) yakalanır.
   - İstekte `stockApi` parametresinin başka bir URL (`http://...`) adresine istek attığı gözlemlenir.

2. **İstetin Manipüle Edilmesi (SSRF):**
   - İlgili stok kontrol isteği **Repeater** sekmesine gönderilir (`Ctrl+R` / `Cmd+R`).
   - `stockApi` parametresinin değeri sunucu yerel adresine (`http://127.0.0.1/admin`) erişecek şekilde değiştirilir:
     ```http
     POST /product/stock HTTP/1.1
     Host: lab-id.web-security-academy.net
     
     stockApi=http%3A%2F%2F127.0.0.1%2Fadmin
     ```

3. **Admin Paneline Erişim ve Silme Linkinin Elde Edilmesi:**
   - Gönderilen istek sonucunda sunucunun `200 OK` yanıtı döndürdüğü ve admin paneli HTML içeriğinin yanıt olarak geldiği görülür.
   - Yanıt içeriği incelendiğinde `carlos` kullanıcısını silmek için kullanılan URL tespit edilir: `/admin/delete?username=carlos`.

4. **Kullanıcının Silinmesi:**
   - `stockApi` parametresi tespit edilen silme URL'si ile güncellenir:
     `stockApi=http%3A%2F%2F127.0.0.1%2Fadmin%2Fdelete%3Fusername%3Dcarlos`
   - İstek Repeater üzerinden gönderilir.
   - `carlos` kullanıcısı başarıyla silinir ve lab tamamlanır.
