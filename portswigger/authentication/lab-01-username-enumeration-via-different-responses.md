# Username enumeration via different responses

## Konu Açıklaması (Authentication Fundamentals & Brute Force)

### 1. Temel Kavramlar

#### What is Authentication? (Kimlik Doğrulama Nedir?)
* **Authentication**, kullanıcının veya istemcinin (client) kimliğini doğrulama işlemidir.
* Web siteleri internete bağlı herkesin erişimine açıktır; bu nedenle sağlam bir kimlik doğrulama mekanizması zorunludur.

#### What is the Difference Between Authentication and Authorization?
* **Authentication (Kimlik Doğrulama):** Bir kullanıcının olduğunu iddia ettiği kişi olup olmadığını doğrulamaktır ("Kimsin?").
* **Authorization (Yetkilendirme):** Kimliği doğrulanmış bir kullanıcının hangi kaynaklara erişim hakkına/yetkisine sahip olduğunu belirlemektir ("Neleri yapmaya yetkin var?").

#### How Do Authentication Vulnerabilities Arise? (Zafiyetler Nasıl Ortaya Çıkar?)
Çoğu zafiyet temelde iki şekilde ortaya çıkar:
1. **Doğrulama mekanizması zayıftır.**
2. **Mantıksal hatalar (logic flaws) ve zayıf kod kullanımı.**

#### What is the Impact of Vulnerable Authentication? (Zafiyetli Kimlik Doğrulamanın Etkisi Nedir?)
* Zayıf doğrulamanın çok ciddi sonuçları olabilir.
* Eğer bir saldırgan brute-force saldırısıyla başka bir kullanıcının bilgilerine erişim sağlarsa, bütün veriler ve izinler tehlikeye girmiş olur.

---

### 2. Parola Tabanlı Giriş Zafiyetleri & Brute-Force

#### Vulnerabilities in Password-Based Login
Kullanıcının giriş yapmak için bir kullanıcı adı ve gizli bir şifre kullandığı sistemlerde, eğer saldırgan bu bilgileri ele geçirirse hesap tamamen tehlike altına girer.

#### Brute-Force Attacks (Kaba Kuvvet Saldırıları)
* **Brute-Force:** Saldırganın kullanıcı bilgilerini deneme-yanılma yöntemiyle bulmaya çalışmasıdır.
* Genellikle otomatikleştirilmiş araçlar ve **wordlist**'ler ile gerçekleştirilir.
* Her zaman tamamen rastgele denemelerden ibaret değildir; topluma açık kaynaklardan elde edilmiş verilerle veya özel algoritmalardan beslenerek de yapılabilir.
* Sadece şifreyle giriş yapılan ve arkasında sağlam bir koruma mekanizması bulunmayan web siteleri bu saldırılara karşı aşırı savunmasızdır.

#### Brute-Forcing Usernames (Kullanıcı Adı Tespiti)
Eğer sistemdeki kullanıcı adları belirli bir örüntüyü (pattern) takip ediyorsa, brute-force saldırılarına karşı özellikle savunmasız kalır.
* **İnceleme Aşaması:** Web sitesinin kullanıcı adlarını gizli tutup tutmadığı kontrol edilmelidir.
* **Profil Verileri:** Profil içerisindeki bilgiler gizli olsa dahi, genellikle profil için kullanılan isim ile sisteme giriş yapılırken kullanılan isim aynı olabilmektedir.
* **HTTP Yanıtları:** HTTP yanıtlarında e-posta adresleri görünüyor mu kontrol edilmelidir; zira kimi zaman yanıtlar yüksek öncelikli/yetkili kullanıcıların e-posta adreslerini ifşa edebilir.

#### Brute-Forcing Passwords (Parola Tespiti)
* Kullanıcı adları gibi parolalar da brute-force ile kırılabilir.
* Çoğu web sitesi zayıf parolaları önlemek amacıyla parola oluşturma kuralları (karmaşıklık şartları vb.) içerir.

---

### 3. Username Enumeration (Kullanıcı Adı Numaralandırma)
Saldırganın, web sitesine girdiği kullanıcı adının sistemde geçerli olup olmadığını anlayabildiği durumlardır.
* **Örnek:** Doğru kullanıcı adı girildiğinde "şifre yanlış" denmesi ya da girilen kullanıcı adının doğrudan dikkate alınması/farklı işlenmesi.

Brute-force kullanarak sisteme girmeye çalışan saldırganın dikkat etmesi gereken temel yanıt işaretleri:
* **Status Codes:** Brute-force saldırısı sırasında yapılan her denemede çoğunlukla aynı HTTP status code görülür. Ancak bir tanesinin farklı olması önemli bir ipucu (güçlü bir işaret) olabilir.
* **Error Messages:** Girilen bilgilerden hangisinin yanlış olduğuna bağlı olarak hata mesajları farklılık gösterebilir (örn. *"Invalid username"* vs *"Incorrect password"*).
* **Response Times:** Gönderilen isteklerin çoğu aynı sürede dönerken, bir tanesinin belirgin olarak daha farklı bir sürede dönmesi (örn. arka plandaki hash işleminin zaman alması); girilen kullanıcı adı ve parolanın geçerli bir deneme olduğunu gösterebilir.


---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Username enumeration via different responses
- **Zafiyet Türü:** Authentication / Brute Force (Username Enumeration)
- **Amaç:** Farklı yanıtlar üzerinden kullanıcı adı numaralandırması ve parola Brute Force yapıp hesaba giriş sağlamak.

### Çözüm Adımları
1. **İsteğin Yakalanması ve Intruder'a Gönderilmesi:**
   - Login sayfasında rastgele kullanıcı adı ve parola girilerek hatalı bir giriş yapılır.
   - Burp Suite **Proxy > HTTP history** sekmesinden `/login` isteği yakalanır ve **Intruder** aracına gönderilir (`Ctrl+I` / `Cmd+I`).

2. **Kullanıcı Adı Numaralandırma (Username Enumeration):**
   - Intruder sekmesinde **Sniper** saldırı türü seçilir ve `username` parametresi payload pozisyonu olarak işaretlenir.
   - Verilen kullanıcı adı listesi (usernames wordlist) payload olarak eklenir ve saldırı başlatılır.
   - Yanıtlar ve yanıt uzunlukları (Length/Response) incelendiğinde, belirli bir kullanıcı adı için sunucunun diğerlerinden farklı bir hata mesajı döndürdüğü görülür (örneğin diğerlerinde *"Invalid username"*, geçerli kullanıcı adında *"Incorrect password"*).
   - Böylece sistemde tanımlı geçerli kullanıcı adı tespit edilmiş olur.

3. **Parola Brute Force Saldırısı:**
   - Bulunan geçerli kullanıcı adı `username` parametresine sabit olarak yazılır.
   - Bu kez `password` parametresi payload pozisyonu olarak işaretlenir.
   - Verilen parola listesi (passwords wordlist) payload olarak yüklenir ve Brute Force saldırısı başlatılır.
   - HTTP `302 Found` yönlendirmesi veya başarılı yanıt veren parola tespit edilerek hedef hesaba giriş sağlanır.
