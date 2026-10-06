# Web shell upload via Content-Type restriction bypass

## Konu Açıklaması (Flawed File Type Validation)
İstemciden sunucuya dosya gönderilirken tarayıcı genellikle `Content-Type` başlığında dosya türünü belirtir (örneğin `image/jpeg` veya `image/png`).

- Birçok zayıf yapılandırılmış web uygulaması, yüklenen dosyanın içeriğini veya uzantısını kontrol etmek yerine sadece istemci tarafından gönderilen `Content-Type` HTTP başlığına güvenir.
- Saldırganlar Burp Suite gibi proxy araçlarıyla `Content-Type` başlığını `application/x-php` yerine `image/jpeg` olarak değiştirerek bu doğrulamayı kolayca atlatabilir (bypass).

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Web shell upload via Content-Type restriction bypass
- **Zafiyet Türü:** File Upload Vulnerabilities (Content-Type Bypass)
- **Amaç:** `Content-Type` kısıtlamasını atlatarak web shell yüklemek ve `carlos` kullanıcısının gizli anahtarını (`/home/carlos/secret`) elde etmek.

### Çözüm Adımları
1. **Dosya Yükleme İsteğinin Yakalanması:**
   - Hesaba giriş yapılır (`wiener:peter`).
   - İçerisinde PHP komutu barındıran betik dosyası (`exploit.php`) avatar olarak yüklendiğinde sunucudan *"Sorry, file of type application/x-php is not allowed"* uyarısı alındığı görülür.
   - Burp Suite **Proxy > HTTP history** sekmesinden ilgili `POST /my-account/avatar` isteği **Repeater** sekmesine gönderilir (`Ctrl+R` / `Cmd+R`).

2. **Content-Type Manipülasyonu:**
   - İstek gövdesinde (body) `exploit.php` dosyasına ait bölümdeki `Content-Type` başlığı bulunur:
     ```http
     Content-Disposition: form-data; name="avatar"; filename="exploit.php"
     Content-Type: application/x-php
     
     <?php echo file_get_contents('/home/carlos/secret'); ?>
     ```
   - `Content-Type: application/x-php` değeri `Content-Type: image/jpeg` veya `Content-Type: image/png` olarak değiştirilir.

3. **İsteğin Gönderilmesi ve Web Shell'in Çalıştırılması:**
   - Değiştirilmiş istek sunucuya gönderilir ve sunucunun dosyayı başarıyla kabul ettiği (`200 OK`) görülür.
   - Yüklenen dosyaya erişmek için `GET /files/avatars/exploit.php` isteği atılır.
   - Dönen yanıttan `carlos` kullanıcısına ait secret anahtarı alınarak lab çözülür.
