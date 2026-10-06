# Remote code execution via web shell upload

## Konu Açıklaması (File Upload Vulnerabilities & Web Shells)
**File Upload Vulnerabilities (Dosya Yükleme Zafiyetleri)**, web sunucusunun yüklenen dosyaların türünü, içeriğini veya uzantısını yeterince doğrulamadığı durumlarda ortaya çıkar.

- **Web Shell:** Saldırganın HTTP istekleri aracılığıyla sunucu üzerinde komut çalıştırmasını sağlayan zararlı betik dosyasıdır (ör. `.php`, `.jsp`, `.asp`).
- Sunucu yüklenen betik dosyasını bir görsel veya statik dosya olarak sunmak yerine çalıştırırsa (execute ederse), saldırgan sunucu üzerinde tam denetim kazanabilir (Remote Code Execution - RCE).

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Remote code execution via web shell upload
- **Zafiyet Türü:** File Upload Vulnerabilities
- **Amaç:** Web shell yükleyerek sunucuda komut çalıştırmak ve `carlos` kullanıcısının gizli anahtarını (`/home/carlos/secret`) okumak.

### Çözüm Adımları
1. **Zararlı PHP Script (Web Shell) Hazırlanması:**
   - Bilgisayarda gizli anahtarı okuyacak PHP kodu içeren bir dosya (`exploit.php`) oluşturulur:
     ```php
     <?php echo file_get_contents('/home/carlos/secret'); ?>
     ```

2. **Görsel Yükleme İşlemi ve Trafiğin İzlenmesi:**
   - Lab üzerindeki hesaba (`wiener:peter`) giriş yapılır.
   - Profil sayfasında (My Account) avatar değiştirme alanından hazırlanan `exploit.php` dosyası yüklenir.
   - Burp Suite **Proxy > HTTP history** sekmesinden `POST /my-account/avatar` isteği incelenir. Sunucunun dosyayı herhangi bir doğrulama yapmadan kabul ettiği görülür.

3. **Web Shell'in Tetiklenmesi (RCE):**
   - Profil sayfasına dönülerek veya HTTP history üzerinden avatar görselinin çağrıldığı istek (`GET /files/avatars/exploit.php`) bulunur ve **Repeater** sekmesine gönderilir.
   - İstek gönderildiğinde sunucunun PHP dosyasını çalıştırdığı ve HTTP yanıtında `carlos` kullanıcısının secret anahtarının yazdırıldığı görülür.

4. **Labın Tamamlanması:**
   - Elde edilen anahtar metni lab çözüm alanına girilerek lab tamamlanır.
