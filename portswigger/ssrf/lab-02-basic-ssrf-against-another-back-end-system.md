# Basic SSRF against another back-end system

## Konu Açıklaması (SSRF Attacks Against Other Back-End Systems)
Bazı mimarilerde web sunucusu, doğrudan internete açık olmayan fakat dahili ağ üzerinden erişilebilen diğer back-end sistemler ile haberleşir.

- Dahili ağlarda IP adresleri genellikle özel bloklarda (`192.168.x.x`, `10.x.x.x`, `172.16.x.x`) yer alır ve dahili servisler genellikle ekstra kimlik doğrulama gerektirmeyebilir.
- Saldırgan, dışa açık web sunucusunda bulduğu bir SSRF zafiyetini otomatize tarama araçlarıyla (Burp Intruder vb.) birleştirerek iç ağdaki gizli/özel IP adreslerini ve servisleri keşfedebilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Basic SSRF against another back-end system
- **Zafiyet Türü:** Server-Side Request Forgery (SSRF)
- **Amaç:** Dahili ağdaki (192.168.0.X) özel sunucuyu tarayarak bulmak, admin paneline erişmek ve `carlos` kullanıcısını silmek.

### Çözüm Adımları
1. **İsteğin Yakalanması ve Intruder'a Gönderilmesi:**
   - Ürün sayfasındaki stok kontrolü (Check stock) isteği Burp Suite **Proxy > HTTP history** üzerinden yakalanır.
   - İstek **Intruder** aracına gönderilir (`Ctrl+I` / `Cmd+I`).

2. **Dahili Ağ Taramasının Yapılandırılması:**
   - Intruder **Positions** sekmesinde `stockApi` parametresi `http://192.168.0.§1§:8080/admin` şeklinde ayarlanır.
   - **Payloads** sekmesinde:
     - Payload type: **Numbers**
     - From: `1`, To: `255`, Step: `1` olarak ayarlanır.
   - Tarama başlatılır (**Start attack**).

3. **Aktif Back-End Sunucusunun Tespiti:**
   - Dönen HTTP yanıt kodları incelenir. Genellikle çoğu IP için `500 Internal Server Error` dönerken, tek bir IP adresinden (örneğin `192.168.0.x`) `200 OK` yanıtı döndüğü tespit edilir.

4. **Kullanıcının Silinmesi:**
   - Aktif IP adresi ile olan istek **Repeater** sekmesine aktarılır.
   - `stockApi` değeri `http://192.168.0.X:8080/admin/delete?username=carlos` şeklinde düzenlenerek istek gönderilir.
   - `carlos` kullanıcısı başarıyla silinir ve lab tamamlanır.
