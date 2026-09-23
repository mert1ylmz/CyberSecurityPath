# Unprotected admin functionality

## Konu Açıklaması (Access Control & Vertical Privilege Escalation)

### Access Control (Erişim Kontrolü)
Access Control, bir kaynağa kimin veya neyin erişebileceğini denetleyen güvenlik mekanizmasıdır. Üç temel bileşenden oluşur:
1. **Authentication (Kimlik Doğrulama):** Kullanıcının iddia ettiği kişi olduğunu doğrular (örn. kullanıcı adı ve şifre).
2. **Session Management (Oturum Yönetimi):** HTTP isteklerinde kullanıcının devam eden oturumunu ve kimliğini tanımlar.
3. **Access Control (Erişim Kontrolü):** Oturumu doğrulanan kullanıcının gerçekleştirmek istediği eyleme izinli olup olmadığını denetler.

### Vertical Privilege Escalation (Dikey Yetki Yükseltme)
Kullanıcının erişim yetkisi bulunmayan daha üst düzey bir role veya fonksiyona (örneğin standart bir kullanıcının Admin paneline) erişim kazanması durumudur.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Unprotected admin functionality
- **Zafiyet Türü:** Access Control (Vertical Privilege Escalation)
- **Amaç:** Korumasız admin paneline erişip `carlos` adlı kullanıcıyı silmek.

### Çözüm Adımları
1. **Uygulamanın İncelemesi:**
   - Lab başlatılır ve hedef web sitesinin ana sayfası incelenir.
   - Sayfa URL adresine manuel olarak `/admin` yazılarak yönetim paneline doğrudan erişim denenir (başarısız olur / sayfa bulunamaz).

2. **Bilgi Toplama (robots.txt Tespiti):**
   - Arama motoru tarama kurallarını barındıran `robots.txt` dosyasına erişmek için URL sonuna `/robots.txt` eklenir.
   - `robots.txt` dosyasının içeriğinde aşağıdaki kural tespit edilir:
     ```text
     User-agent: *
     Disallow: /administrator-panel
     ```

3. **Admin Paneline Erişim ve Kullanıcı Silme:**
   - `robots.txt` içerisinde gizlenen `/administrator-panel` adresi URL'e eklenerek admin paneline ulaşılır.
   - Yönetim paneli arayüzünde listelenen kullanıcılar arasından `carlos` kullanıcısı tespit edilerek silinir ve lab tamamlanır.
