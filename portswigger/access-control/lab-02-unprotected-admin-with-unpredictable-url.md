# Unprotected admin functionality with unpredictable URL

## Konu Açıklaması (Unpredictable URL / Security Through Obscurity)
Bazı web uygulamalarında yetkilendirme kontrolü sağlamak yerine, yönetim paneli adresi tahmin edilmesi zor rastgele bir URL dizisi (örneğin `/admin-7a8b9c`) arkasına gizlenir. 

- Bu yaklaşım **"Security through obscurity" (Gizlilik yoluyla güvenlik)** olarak adlandırılır ve gerçek bir güvenlik önlemi değildir.
- Yönetim paneline giden URL rotaları genellikle istemci tarafına (client-side) gönderilen JavaScript dosyaları, HTML kaynak kodları veya inline script'ler içerisinde unutulabilir ve saldırganlar tarafından analiz edilerek ortaya çıkarılabilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Unprotected admin functionality with unpredictable URL
- **Zafiyet Türü:** Access Control (Vertical Privilege Escalation)
- **Amaç:** Tahmin edilmesi zor bir URL ile gizlenmiş admin paneline erişerek `carlos` kullanıcısını silmek.

### Çözüm Adımları
1. **Uygulama İncelemesi ve HTTP İsteği Analizi:**
   - Lab başlatılır ve uygulama arayüzü incelenir.
   - Burp Suite veya tarayıcı Geliştirici Araçları (Developer Tools) üzerinden HTTP istekleri ve yanıtları kontrol edilir.

2. **Kaynak Kod Analizi:**
   - Sayfanın kaynak kodu (`View Source`) ve sayfaya dahil edilen JavaScript dosyaları incelenir.
   - Kaynak kod içerisindeki script bloklarında admin paneline giden gizli URL patikası (path) araştırılır.
   - Kod içerisinde tanımlanmış admin paneli URL'i tespit edilir.

3. **Admin Paneline Erişim ve Kullanıcı Silme:**
   - Tespit edilen gizli URL adresi tarayıcıya girilerek admin paneline erişim sağlanır.
   - Admin panelinde yer alan `carlos` kullanıcısı silinerek lab çözümü tamamlanır.
