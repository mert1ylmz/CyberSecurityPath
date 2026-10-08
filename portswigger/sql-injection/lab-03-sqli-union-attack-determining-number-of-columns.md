# SQL injection UNION attack, determining the number of columns returned by the query

## Konu Açıklaması (SQL Injection UNION Attacks)
Bir uygulamada SQL injection zafiyeti varsa ve sorgu cevapları alınıyorsa, geri dönüşleri `UNION` kullanılarak diğer tablolardan veri getirmek için kullanılabilir.
`UNION` anahtar kelimesi birden fazla `SELECT` sorgusunu birleştirir ve başka bir tabloya sorgu atılarak iki sorgu sonucunun bir arada dönmesini sağlar:
```sql
SELECT a, b FROM table1 UNION SELECT c, d FROM table2
```

### UNION Sorgusunun Çalışması İçin İki Gereklilik Vardır:
1. Her iki sorgu aynı sayıda kolon getirmelidir.
2. Her kolondaki veri tipi (data type) birbiriyle uyumlu olmalıdır.

---

### Kolon Sayısını Belirleme Yöntemleri:

#### 1. Sıralı Olarak ORDER BY Enjekte Etmek
Hata alana kadar sorguya sırasıyla kolon indeksi eklenir:
```sql
' ORDER BY 1 --
' ORDER BY 2 --
' ORDER BY 3 --
```

#### 2. Sıralı Olarak UNION SELECT İfadeleri Eklemek
```sql
' UNION SELECT NULL --
' UNION SELECT NULL, NULL --
' UNION SELECT NULL, NULL, NULL --
```
Eğer `NULL` ifadelerin sayısı arka plandaki sorgunun kolon sayısına eşit olmazsa veritabanı hata verecektir. `NULL` kullanılmasının sebebi `SELECT` sorgusunda gelen kolonların türlerinin uyumlu olması gerekliliğidir (`NULL` her veri türüne dönüştürülebilir).

#### Database-Specific Syntax (Oracle Notu):
Oracle veritabanlarında her `SELECT` sorgusundan sonra `FROM` anahtar kelimesinin kullanılması zorunludur. Bu nedenle `FROM dual` şeklinde bir tablo belirtilmesi gerekir:
```sql
' UNION SELECT NULL FROM dual --
```

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** SQL injection UNION attack, determining the number of columns returned by the query
- **Zafiyet Türü:** SQL Injection (UNION Attack - Determining Columns)
- **Amaç:** Ürün kategori filtresindeki zafiyeti sömürerek `category` sorgusunun kaç adet sütun döndürdüğünü tespit etmek.

### Çözüm Adımları
1. **Zafiyetin Tespiti ve İstekin Yakalanması:**
   - Burp Suite aktifken hedef sitede herhangi bir ürün kategorisi seçilir.
   - Gelen HTTP isteği Burp Proxy history üzerinden incelenir ve **Repeater** sekmesine gönderilir.

2. **Kolon Sayısının Tespit Edilmesi (`UNION SELECT` Kullanımı):**
   - `category` parametresi düzenlenerek `category=' UNION SELECT NULL --` ifadesi gönderilir.
   - Veritabanından hata yanıtı dönüyorsa `NULL` sayısı artırılır:
     - `category=' UNION SELECT NULL, NULL --`
     - `category=' UNION SELECT NULL, NULL, NULL --`
   - Sorguda 3 adet `NULL` gönderildiğinde sunucudan 200 OK yanıtı alındığı ve hatanın kaybolduğu görülür.

3. **Sonucun İncelemesi:**
   - Sorgunun tam olarak **3 sütun** döndürdüğü doğrulanır ve lab tamamlanır.
