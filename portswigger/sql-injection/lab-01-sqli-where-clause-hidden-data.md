# SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

## Konu Açıklaması (SQL Injection)
**SQL Injection (SQLi)**, uygulamanın veritabanı sorguları oluştururken kullanıcıdan aldığı girdileri yeterince doğrulamaması veya parametrize etmemesi sonucu saldırganın arka plandaki SQL sorgusunu değiştirebilmesidir.

- Saldırganlar bu açıklık sayesinde veri sızdırabilir, veritabanı yapısını öğrenebilir, verileri değiştirebilir veya kimlik doğrulama mekanizmalarını atlatabilirler.

### SQLi Tespit ve Doğrulama Yöntemleri:
1. **Sözdizimi Hatası Oluşturma:** Tek tırnak (`'`) veya çift tırnak (`"`) göndererek sunucudan SQL hata mesajı alıp almadığını kontrol etmek.
2. **Mantıksal/Boolean İfadeler:** `OR 1=1` (her zaman doğru) veya `OR 1=2` (her zaman yanlış) koşulları göndererek uygulamanın davranış farkını izlemek.
3. **Aritmetik İşlemler:** Sayısal parametrelere `id=2-1` gönderip `id=1` ile aynı sonucun dönüp dönmediğini sınamak.
4. **Time-Based (Zaman Odaklı):** Veritabanına bekleme fonksiyonları (`pg_sleep()`, `SLEEP()`) göndererek yanıt süresini izlemek.
5. **Out-of-Band (OAST):** DNS veya HTTP istekleri tetikleyerek veritabanının dış sunucularla bağlantı kurmasını sağlamak.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
- **Zafiyet Türü:** SQL Injection
- **Amaç:** Ürün kategorisi filtresindeki SQLi zafiyetini sömürerek yayında olmayan (unreleased) gizli ürünler dahil tüm verileri listelemek.

### Çözüm Adımları
1. **Zafiyetin Tespiti:**
   - Web sitesinde bir ürün kategorisine (örneğin *Gifts*) tıklanır.
   - URL adresi incelenir: `https://lab-id.web-security-academy.net/filter?category=Gifts`
   - Arka planda çalışan sorgunun şu şekilde olduğu tahmin edilir:
     `SELECT * FROM products WHERE category = 'Gifts' AND released = 1`

2. **SQL Injection Payload'unun Yerleştirilmesi:**
   - `category` parametresinin sonuna tek tırnak ve mantıksal `OR 1=1` koşulu ile SQL yorum satırı karakterleri (`--`) eklenir:
     `category=Gifts'+OR+1=1--`
   - Oluşan yeni SQL sorgusu:
     `SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1`
   - `--` ifadesi sorgunun kalan kısmını (yani `AND released = 1` şartını) pasif hale getirir, `1=1` ise tüm ürünlerin dönmesini sağlar.

3. **Sonucun İncelemesi:**
   - Sayfa yenilendiğinde, henüz piyasaya sürülmemiş gizli ürünler de dahil olmak üzere veritabanındaki bütün ürünlerin listelendiği görülür ve lab tamamlanır.
