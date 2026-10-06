# OS command injection, simple case

## Konu Açıklaması (OS Command Injection)
**OS Command Injection (İşletim Sistemi Komut Enjeksiyonu)**, saldırganın web sunucusunda çalışan bir uygulama üzerinden sunucunun işletim sisteminde doğrudan komutlar çalıştırmasına olanak tanıyan kritik bir zafiyettir.

- Genellikle uygulamanın kullanıcı girdilerini yeterince temizlemeden (sanitization) doğrudan bir sistem kabuğuna (`sh`, `bash`, `cmd.exe`) parametre olarak geçirmesi sonucu meydana gelir.
- Saldırganlar komut ayırıcı karakterleri (`|`, `;`, `&`, `&&`, `\n`) kullanarak kendi komutlarını mevcut sorguya ekleyebilirler.

### Yararlı İşletim Sistemi Komutları:
| Amaç | Linux | Windows |
| :--- | :--- | :--- |
| Geçerli kullanıcı adı | `whoami` | `whoami` |
| İşletim sistemi bilgisi | `uname -a` | `ver` |
| Ağ yapılandırması | `ifconfig` | `ipconfig /all` |
| Aktif ağ bağlantıları | `netstat -an` | `netstat -an` |
| Çalışan süreçler | `ps -ef` | `tasklist` |

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** OS command injection, simple case
- **Zafiyet Türü:** OS Command Injection
- **Amaç:** Stok kontrol fonksiyonundaki komut enjeksiyonu zafiyetini kullanarak sunucuda `whoami` komutunu çalıştırmak ve kullanıcı adını yazdırmak.

### Çözüm Adımları
1. **İsteğin Yakalanması:**
   - Bir ürün detay sayfasına gidilir ve **Check stock** butonuna basılır.
   - Burp Suite **Proxy > HTTP history** sekmesinden `POST /product/stock` isteği yakalanır ve **Repeater** sekmesine gönderilir (`Ctrl+R` / `Cmd+R`).

2. **Girdi Parametrelerinin Test Edilmesi:**
   - İstek gövdesinde yer alan `storeId` (veya `productId`) parametresi incelenir:
     ```http
     POST /product/stock HTTP/1.1
     Host: lab-id.web-security-academy.net
     
     productId=1&storeId=1
     ```

3. **Komut Enjeksiyonu Yükünün (Payload) Gönderilmesi:**
   - `storeId` parametresine komut ayırıcı karakter ile birlikte `whoami` komutu eklenir:
     `productId=1&storeId=1|whoami` veya `productId=1&storeId=1;whoami`
   - İstek gönderilir.

4. **Sonucun İncelenmesi:**
   - Sunucu yanıtı incelendiğinde, stok sorgulama sonucunun hemen ardından sunucunun çalıştırdığı `whoami` komutunun çıktısının (örneğin `peter-xxxxx`) ekrana basıldığı görülür ve lab çözülür.
