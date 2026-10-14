# SQL injection with filter bypass via XML encoding

## Konu Açıklaması (SQL Injection in Different Contexts & Second-Order SQLi)

### 1. Second-Order SQL Injection

* **First-Order Injection:** Uygulamanın kullanıcıdan gelen girdiyi doğrudan alıp hemen ilgili SQL sorgusunda çalıştırması durumudur.
* **Second-Order Injection:** 
  * Kullanıcının uygulamaya verdiği veri ilk HTTP isteği anında işlenip veritabanında saklanır.
  * İlerleyen aşamalarda bu saklanan veri başka bir işlemde veya sorguda kullanılmak üzere tekrar çağrıldığında injection zafiyeti tetiklenir.
  * Genelde geliştiriciler veritabanına bir defa kaydedilmiş olan veriyi "güvenilir" kabul ederler; bu yüzden veri tekrar işlenirken filtreleme/parametrelendirme yapılmadığında zafiyet sonradan ortaya çıkar.

---

### 2. SQL Injection in Different Contexts

Önceki laboratuvarlarda doğrudan SQL sorgularına zararlı SQL payload'ları enjekte edilmiştir. Fakat uygulamanın kontrol ettiği/işlediği farklı formatlardaki girdiler üzerinden de SQL sorguları enjekte edilebilir.

* **Farklı Formatlar:** Bazı uygulamalar verileri **JSON** ya da **XML** formatında alıp bunları arka planda veritabanında sorgulatabilir.
* **Filtre Atlatma (Bypass):**
  * Zayıf yapılandırmalar yalnızca standart SQL anahtar kelimelerine (`SELECT`, `UNION` vb.) bakarak güvenlik sağlamaya çalışabilir (WAF veya zayıf regex filtreleri).
  * Bu filtreleri atlatmak için karakterleri kodlayarak (**encoding**, örn. XML entity encoding `&#...;`) geçirmek mümkündür.

#### Örnek XML Payload İskeleti

```xml
<stockCheck>
    <productId>120</productId>
    <storeId>999 &#x23;&#x35;&#x30;ELECT * FROM information_schema.tables</storeId>
</stockCheck>
```

> **Not:** Örnekte XML entity encoding kullanılarak filtrenin SQL kelimesini tanıması engellenmekte, XML parser veriyi çözdüğünde ise sorgu veritabanına ham haliyle iletilmektedir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** SQL injection with filter bypass via XML encoding
- **Zafiyet Türü:** SQL Injection (Filter Bypass via XML Entity Encoding)
- **Amaç:** XML formatında veri alan stok kontrolü fonksiyonundaki WAF/filtre engelini Hackvertor eklentisiyle XML entity kodlaması kullanarak atlatmak, `users` tablosundan kimlik bilgilerini (`username` ve `password`) çekerek sisteme giriş yapmak.

### Çözüm Adımları

1. **Eklenti Kurulumu:**
   * Bu laboratuvarı tamamlamak için Burp Suite'e **Hackvertor** eklentisini ekleyin (*BApp Store* üzerinden kurulabilir).

2. **İsteği İnceleme & Test:**
   * Uygulamada bir ürünün **"Stock Check"** (stok kontrolü) fonksiyonunu tetikleyin ve yakalanan isteği Burp Suite **Repeater**'a gönderin.
   * `storeId` alanına `1+1` yazarak sorgu girdisini kabul edip etmediğini test edin (hesaplama sonucunu kontrol edin).

3. **Filtre Kontrolü:**
   * Daha sonra `1 SELECT * FROM users` gibi bir sorguyla veri çekmeyi deneyin.
   * Uygulamanın doğrudan hata (`Attack detected` vb.) verdiğini göreceksiniz.

4. **Filtreyi Hackvertor ile Aşma:**
   * Filtreyi aşmak için yazdığınız SQL sorgusunu **Hackvertor** kullanarak XML encode formatına dönüştürün.

5. **Hedef Payload'ı Hazırlama:**
   * İlk olarak almak istediğiniz sorguyu hazırlayın:
     ```sql
     1 UNION SELECT username || '~' || password FROM users
     ```

6. **Encode İşlemi:**
   * Bu sorgu ifadesini seçip Hackvertor ile XML entity kodlaması uygulayın (örn. `hex_entities` etiketi arasına alın).

7. **Sorguyu Gönderme ve Giriş:**
   * **Send** butonuna basarak isteği iletin.
   * Dönen yanıt içerisinden gelen kullanıcı adı ve parola bilgileri ile sisteme giriş yapın.
