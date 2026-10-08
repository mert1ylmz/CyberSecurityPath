# SQL injection UNION attack, finding a column containing text

## Konu Açıklaması (Finding Columns with Useful Data Type in UNION Attacks)
Bir SQL injection UNION saldırısında, veritabanından çekilmek istenen veriler genellikle metin (string) türündedir. Bu nedenle, `UNION SELECT` ile veri sızdırmadan önce dönen sütunlardan hangilerinin metin verilerini desteklediğini tespit etmek gerekir.

---

### Metin (String) Destekleyen Sütunları Bulma Adımları:
1. **Kolon Sayısını Belirleme:** İlk olarak kaç adet sütun döndüğü tespit edilir (örneğin `NULL, NULL, NULL`).
2. **Sırasıyla String İfade Gönderme:** Her bir sütun konumuna sırasıyla metin (string) bir değer yerleştirilerek uygulamanın yanıtı izlenir:
   ```sql
   ' UNION SELECT 'a', NULL, NULL --
   ' UNION SELECT NULL, 'a', NULL --
   ' UNION SELECT NULL, NULL, 'a' --
   ```
3. **Yanıtı Değerlendirme:**
   - Eğer test edilen sütun string veri tipini desteklemiyorsa veritabanı tür uyumsuzluğu hatası döndürür.
   - Destekliyorsa istek başarılı (HTTP 200 OK) olur ve iletilen string değer yanıt içerisinde görüntülenir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** SQL injection UNION attack, finding a column containing text
- **Zafiyet Türü:** SQL Injection (UNION Attack - Finding Text Column)
- **Amaç:** Ürün kategorisi filtresindeki zafiyeti sömürerek `category` sorgusunun döndürdüğü sütunlardan hangisinin metin (string) verisi içerebildiğini tespit etmek ve verilen string değerini ekranda bastırmak.

### Çözüm Adımları
1. **Zafiyetin Tespiti ve İstekin Yakalanması:**
   - Hedef sitede bir ürün kategorisi seçilir ve istek Burp Suite üzerinden **Repeater** sekmesine aktarılır.

2. **Kolon Sayısının Tespit Etmesi:**
   - Sırayla `NULL` değerleri denenerek sorgunun 3 adet sütun döndürdüğü doğrulanır:
     `category=' UNION SELECT NULL, NULL, NULL --`

3. **String Destekleyen Sütunun Bulunması:**
   - Lab ekranında verilen hedef string (örneğin 'a' veya labın belirlediği rastgele string) sütunlara sırasıyla denenir.
   - 1. sütun kontrol edilir: `category=' UNION SELECT 'a', NULL, NULL --` (Hata alınır)
   - 2. sütun kontrol edilir: `category=' UNION SELECT NULL, 'a', NULL --` (Başarılı yanıt alınır)

4. **Sonucun İncelemesi:**
   - 2. sütunun metin (string) veri tipini desteklediği teyit edilir ve ekrana string değer basılarak lab tamamlanır.
