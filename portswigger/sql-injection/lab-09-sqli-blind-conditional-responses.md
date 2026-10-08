# Blind SQL injection with conditional responses

## Konu Açıklaması (Blind SQL Injection)
**Blind SQL Injection (Kör SQL Enjeksiyonu)**, uygulamanın SQL Injection zafiyetine karşı savunmasız olduğu, ancak HTTP yanıtlarında SQL sorgu sonuçlarının veya veritabanı hata mesajlarının doğrudan ekrana basılmadığı durumlarda ortaya çıkar.

Doğrudan veri dönmediği için `UNION` tabanlı klasik saldırılar bu senaryoda doğrudan sonuç vermez. Bunun yerine uygulamanın farklı girdi durumlarında verdiği farklı yanıtlar (koşullu yanıtlar / conditional responses) analiz edilir.

---

### Koşullu Yanıtlar ile Veri Sızdırma (Triggering Conditional Responses)
Örneğin uygulamanın bir `TrackingId` çerezi kullandığını ve arka planda şu sorguyu çalıştırdığını varsayalım:
```sql
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = '...'
```

Eğer sorguya mantıksal (Boolean) koşullar eklersek:
- `TrackingId=xyz' AND '1'='1` -> Koşul doğru olduğu için sorgu satır döndürür ve uygulamada örneğin `"Welcome back"` mesajı görünür.
- `TrackingId=xyz' AND '1'='2` -> Koşul yanlış olduğu için sorgu boş döner ve `"Welcome back"` mesajı **görünmez**.

Bu fark sayesinde veritabanına Evet/Hayır soruları sorarak karakter karakter veri sızdırılabilir:
```sql
TrackingId=xyz' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'), 1, 1) = 'a'
```

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Blind SQL injection with conditional responses
- **Zafiyet Türü:** Blind SQL Injection (Boolean / Conditional Responses)
- **Amaç:** `TrackingId` çerezindeki Blind SQLi açıklığını kullanarak mantıksal koşullar ile `administrator` parolasını karakter karakter çıkarmak ve oturum açmak.

### Çözüm Adımları
1. **İstekin Yakalanması ve Mantıksal Koşul Testi:**
   - Web sitesinin ana sayfasına istek gönderilir ve Burp Suite **HTTP history** üzerinden `Cookie: TrackingId=...` içeren istek **Repeater**'a gönderilir.
   - Doğru koşul testi: `TrackingId=xyz' AND '1'='1` gönderilir -> Yanıtta `"Welcome back"` mesajı teyit edilir.
   - Yanlış koşul testi: `TrackingId=xyz' AND '1'='2` gönderilir -> `"Welcome back"` mesajının **kaybolduğu** teyit edilir.

2. **Tablo ve Kullanıcı Doğrulaması:**
   - `users` tablosu doğrulanır:
     `TrackingId=xyz' AND (SELECT 'a' FROM users LIMIT 1)='a`
   - `administrator` kullanıcısı doğrulanır:
     `TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator')='a`

3. **Parola Uzunluğunun Tespiti:**
   - Parolanın kaç karakter olduğunu bulmak için uzunluk sınaması yapılır:
     `TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a`
   - Sayı artırılarak test edilir. Örneğin `LENGTH(password)>19` doğru dönerken `LENGTH(password)>20` yanlış döner. Parola uzunluğunun **20 karakter** olduğu belirlenir.

4. **Burp Intruder ile Parolanın Sızdırılması:**
   - İstek **Burp Intruder** sekmesine gönderilir (`Ctrl+I` / `Cmd+I`).
   - `Positions` sekmesinde `TrackingId` çerezi ayarlanır:
     ```http
     TrackingId=xyz' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='§a§
     ```
   - **Payloads** sekmesinde `Payload type: Simple list` seçilir ve `a-z`, `0-9` karakterleri eklenir.
   - **Settings > Grep - Match** sekmesine gidilerek sadece `Welcome back` filtresi eklenir.
   - `Start attack` başlatılır. `Welcome back` sütununda tik işareti alan karakter, parolanın 1. harfidir.
   - `SUBSTRING` fonksiyonundaki ofset sırasıyla `2`, `3`, ..., `20` yapılarak 20 karakterlik parolanın tamamı elde edilir.

5. **Giriş ve Labın Tamamlanması:**
   - Elde edilen parola ile `/login` sayfasından `administrator` hesabına giriş yapılır ve lab tamamlanır.
