# Broken brute-force protection, IP block

## Konu Açıklaması (Flawed Brute-Force Protection & Logic Flaws)

### Flawed Brute-Force Protection (Kusurlu Brute-Force Koruması)
Başarılı bir sonuç alana kadar sistemde çok sayıda hatalı deneme gerçekleşecektir. Mantıksal olarak brute-force saldırılarından korunmak için yapılacak temel hamleler süreci otomatize etmeyi zorlaştırmak ve saldırganın giriş denemelerini yavaşlatmaktır.

En yaygın koruma yöntemleri:
* **Hesap Kilitleme:** Belirli sayıda hatalı deneme yapan kullanıcının hesabını geçici veya kalıcı olarak dondurmak.
* **IP Engelleme:** Çok hızlı ve yoğun şekilde istek gönderen IP adresini bloklamak.

> **Uyarı:** Bu iki yöntem yaygın olarak uygulansa da mantıksal kurguları doğru yapılandırılmadığında kesin ve kusursuz bir koruma sağlamazlar.

### Mantıksal Sayaç Sıfırlama Açığı
* Bazı kimlik doğrulama sistemleri, brute-force sayacını ardışık hatalı denemelere (consecutive failures) bağlar.
* Örneğin: Sistem ardışık 3 hatalı denemede IP'yi engelliyorsa, fakat araya 1 adet geçerli oturumla başarılı giriş yapıldığında sayaç sıfırlanıyorsa, saldırgan her 2 hatalı denemeden sonra kendi geçerli hesabıyla sisteme başarılı bir login isteği göndererek engelleme mekanizmasını tamamen baypas edebilir.
* Bu işlem Burp Suite **Macros** ve **Session Handling Rules** kullanılarak tamamen otomatik hale getirilebilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Broken brute-force protection, IP block
- **Zafiyet Türü:** Authentication / Brute Force (Flawed Logic & Counter Reset)
- **Amaç:** Brute-force koruması kusurlu olan (ardışık hatalı girişlerde IP bloklayan) sistemde sayaç sıfırlama tekniği kullanarak `carlos` adlı kullanıcının şifresini bulup giriş yapmak.

### Çözüm Adımları

1. **Uygulama İncelemesi ve Oturum Doğrulama:**
   * Uygulamanın login sayfasına gidin, lab tarafından sağlanan geçerli kullanıcı adı ve şifreyle (`wiener:peter`) hesaba erişim sağlayabildiğinizi doğrulayın.

2. **İsteği Yakalama ve Bloklama Mekanizmasını İnceleme:**
   * Burp Suite üzerinden giden login isteğini inceleyin ve **Repeater**'a gönderin.
   * Kullanıcı adı ve şifre kombinasyonlarını denerken arka arkaya 3 hatalı deneme yapıldığında sistemin IP'yi blokladığını göreceksiniz.
   * IP bloklamasından kaçmak için `X-Forwarded-For` parametresini deneyin; fakat bu sistemde işe yaramadığını göreceksiniz.

3. **Sayaç Sıfırlama Mantığı (Macro Çözümü):**
   * IP bloklamasından kaçmanın mantıksal yolu: Sistem sayacı 3 hatalı denemede tetiklendiği için, bloklama gelmeden hemen önce (her 2 hatalı denemeden sonra) **araya 1 adet geçerli oturum bilgisi ile başarılı login isteği sokmaktır**. Başarılı giriş sayacı sıfırlayacaktır. Bunu manuel yapmak yerine en hızlı yol bir **Burp Macro** oluşturmaktır.

4. **Burp Macro Tanımlama:**
   * Burp menüsünden **Settings -> Sessions** sayfasına gidin.
   * **Macros** başlığı altındaki **Add** butonuna basın ve açılan pencerede az önce yaptığınız **başarılı giriş (valid credentials) isteğini** seçin.

5. **Session Handling Rule Oluşturma:**
   * Macros başlığının hemen üstündeki **Session Handling Rules** bölümünde **Add** butonuna basın.
   * Kurala bir isim verin. **Rule Actions** sekmesinde *Add -> Run a macro* seçeneğini seçip az önce oluşturduğunuz makroyu bağlayın.
   * **Scope** sekmesine geçerek Intruder dışındaki tüm araçları kaldırın ve *Include all URLs* seçeneğini işaretleyin.

6. **Intruder Yapılandırması (Single-Thread):**
   * **Intruder**'a gelin.
   * **Resource Pool** sekmesine tıklayın, *Create new resource pool* seçeneğini seçerek **Maximum concurrent requests** değerini `1` yapın (isteklerin sırayla gitmesi ve makronun her adımda çalışabilmesi için tek thread şarttır).

7. **Saldırıyı Başlatma ve Giriş:**
   * `carlos` kullanıcısı için şifre payload listesini yükleyin ve saldırıyı başlatın.
   * Saldırı bittiğinde **302** status code dönen isteğin parolasını alarak sisteme giriş yapın.
