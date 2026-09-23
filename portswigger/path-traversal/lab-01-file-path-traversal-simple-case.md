# File path traversal, simple case

## Konu Açıklaması (Path Traversal)
**Path Traversal (Dizin Atlama)**, saldırganın web uygulamasındaki yetersiz girdi denetimlerini kullanarak sunucu dosya sisteminde yetkisiz dosya ve dizinlere erişim sağladığı bir zafiyet türüdür.

- Saldırgan `../` (dot-dot-slash) dizin atlama karakter dizisini kullanarak uygulamanın çalıştığı kök dizinin dışına çıkar ve üst dizinlere geçer.
- Bu teknik sayesinden sunucu üzerindeki sistem dosyaları, yapılandırma dosyaları ve hassas veriler yetkisiz şekilde okunabilir.
- **Ayrıca:** Yol (path) veya encoding (URL encoding, double URL encoding vb.) manipülasyonları kullanılarak da korumalar bypass edilip hedef dosyalara erişim sağlanabilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** File path traversal, simple case
- **Zafiyet Türü:** Path Traversal
- **Zorluk:** Simple

### Çözüm Adımları
1. **Burp Suite ve Proxy Ayarları:**
   - Burp Suite başlatılır. (Sertifika uyarısı durumunda sertifika indirilmeden de uygulama açılabilir).
   - Firefox tarayıcısında **FoxyProxy** eklentisi aktif edilerek Burp Suite proxy adresine (`127.0.0.1:8080`) yönlendirilir.
   - Burp Suite CA sertifikası Firefox tarayıcısına içe aktarılarak HTTPS trafiğinin sorunsuz izlenmesi sağlanır.

2. **Trafiğin Yakalanması:**
   - PortSwigger platformu üzerinden lab başlatılır.
   - Burp Suite **Proxy > HTTP history** sekmesinden gelen ve giden istekler incelenir.
   - Görsel yükleme isteklerini rahatça bulabilmek için HTTP history bölümünde **Image** filtresi aktif edilir.

3. **Zafiyetin Değerlendirilmesi ve İstek Manipülasyonu:**
   - Görsel çağıran isteklerden biri (`/image?filename=...`) seçilerek **Repeater** sekmesine gönderilir (`Ctrl+R` / `Cmd+R`).
   - `filename` parametresinin değeri dizin atlama dizisi ile değiştirilir:
     ```http
     GET /image?filename=../../../../etc/passwd HTTP/1.1
     Host: lab-id.web-security-academy.net
     ```
   - İstek gönderildiğinde sunucu yanıtında `/etc/passwd` dosyasının içeriği elde edilir ve lab başarıyla tamamlanır.
