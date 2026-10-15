# Brute-forcing a stay-logged-in cookie

## Konu Açıklaması (Vulnerabilities in Other Authentication Mechanisms - Keeping Users Logged In)

### 1. Vulnerabilities in Other Authentication Mechanisms
Temel giriş yapma fonksiyonuna ek olarak çoğu web sitesi kullanıcılara kendi hesaplarını yönetme özellikleri sunar (örneğin *"Şifremi Unuttum"* veya *"Beni Hatırla"* fonksiyonları). Bu ek mekanizmalar doğru yapılandırılmadığında beraberinde kritik güvenlik zafiyetleri getirir.

---

### 2. Keeping Users Logged In (Beni Hatırla Fonksiyonu)
Kullanıcının tarayıcıyı kapatsa bile tekrar giriş yapmasını gerektirmeyen yaygın bir özelliktir. Bu özellik genellikle istemciye bir **"Beni Hatırla" (stay-logged-in / remember-me)** çerezi atanmasıyla sağlanır. 

* Bu çerezin saldırganlarca ele geçirilmesi, doğrudan oturumun ele geçirilmesine yol açar.
* Saldırganın bu çerezi tahmin etmesi normalde zor olmalıdır; ancak bazı web siteleri bu çerezleri **statik ve tahmin edilebilir değerlerin birleşimiyle** üretir. Hatta bazı geliştiriciler doğrudan kullanıcının şifresini veya şifre hash'ini bu çerez formatının içine gömer.

---

### 3. Risk ve Atlatma Yöntemleri
* **Format Analizi:** Saldırgan kendi hesabını oluşturabildiği bir senaryoda, kayıt/giriş esnasında kendisine atanan çerezin formatını analiz ederek yapısını çözebilir.
* **Zayıf Algoritmalar:** Bazı siteler bu çerezi korumak amacıyla şifreleme yerine sadece `Base64` gibi tersine çevrilebilir algoritmalar veya `MD5` gibi zayıf hash fonksiyonları kullanır. Algoritma deşifre edildiğinde koruma tamamen ortadan kalkar.
* **Alternatif Vektörler:** Saldırgan kendi hesabını açamasa bile; XSS (Cross-Site Scripting) gibi istemci taraflı açıklarla kurbanın çerezini çalabilir veya web sitesi açık kaynaklı (open-source) bir framework kullanıyorsa kaynak koddan çerezin nasıl oluşturulduğunu tespit edebilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Brute-forcing a stay-logged-in cookie
- **Zafiyet Türü:** Authentication / Weak Cookie Mechanism (Stay-Logged-In Cookie Brute-Force)
- **Amaç:** Kullanıcıların giriş yapmış olarak kalmasını sağlayan zafiyetli çereze brute-force uygulayarak `carlos` kullanıcısının çerezini türetmek ve `/my-account` sayfasına yetkisiz giriş yapmak.
- **Referans Bilgiler:**
  - **Hedef Kullanıcı:** `carlos`
  - **Kendi Hesabımız:** `wiener:peter`

### Çözüm Adımları

1. **Çerez Formatının İncelenmesi:**
   * İlk olarak verilen geçerli kimlik bilgileriyle (`wiener:peter`) giriş sayfasına gidin. **"Stay logged in"** seçeneğini işaretleyerek giriş yapın.
   * Burp Suite üzerinden giden istekleri ve atanan çerezleri inceleyin. `stay-logged-in` çerezinin değerini kontrol edin.

2. **Çerezin Deşifre Edilmesi (Reverse Engineering):**
   * Çerezin **Base64** ile kodlandığını tespit edin. Değeri decode ettiğinizde şu yapıyla karşılaşılır:
     ```text
     username:md5(password)
     ```
     *(Örn: `wiener:51a3a...` yapısının MD5 çözümü yapıldığında parolanın `peter` olduğu doğrulanır).*
   * Buradan hareketle `stay-logged-in` çerezinin genel formülünün:
     $$\text{stay-logged-in} = \text{Base64}(\text{username} + ":" + \text{MD5}(\text{password}))$$
     olduğu anlaşılır.

3. **Intruder Yapılandırması:**
   * `/my-account` isteğini Burp Intruder'a gönderin.
   * Mevcut oturum çerezini (`session`) silin ve yetkilendirmenin yalnızca `stay-logged-in` çerezi üzerinden yapılmasını sağlayın:
     ```http
     Cookie: stay-logged-in=§payload§
     ```

4. **Payload Processing Kurallarının Tanımlanması:**
   * Payload olarak şifre listesini ekleyin ve **Payload Processing** kurallarını sırasıyla tanımlayın:
     1. **Hash:** MD5
     2. **Add prefix:** `carlos:`
     3. **Base64-encode**

5. **Saldırıyı Başlatma ve Labın Tamamlanması:**
   * Saldırıyı başlatın. Dönen HTTP yanıtlarını inceleyin; `200 OK` yanıtı veren isteğin parolasını belirleyin.
   * Elde edilen çerez ile Carlos hesabının oturumunu doğrulayarak laboratuvarı tamamlayın.
