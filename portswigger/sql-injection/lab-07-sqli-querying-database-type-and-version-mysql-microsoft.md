# SQL injection attack, querying the database type and version on MySQL and Microsoft

## Konu Açıklaması (Querying the Database Type and Version)
SQL Injection saldırılarını ilerletirken ve veritabanına özel sömürü yöntemlerini seçerken arka planda koşan veritabanı yönetim sisteminin (RDBMS) türünü ve sürümünü öğrenmek kritik bir adımdır.

### Farklı Veritabanlarında Sürüm Sorgulama:
| Veritabanı Türü | Sürüm Sorgusu | Yorum Satırı |
| --- | --- | --- |
| **Microsoft SQL Server (MSSQL)** | `SELECT @@version` | `--` |
| **MySQL** | `SELECT @@version` | `#` veya `-- ` (boşluklu) |
| **Oracle** | `SELECT * FROM v$version` veya `SELECT banner FROM v$version` | `--` |
| **PostgreSQL** | `SELECT version()` | `--` |

> [!NOTE]
> MySQL üzerinde `--` yorum belirtecinden sonra bir boşluk karakteri bırakılması şarttır (`-- `). Alternatif olarak URL encode edilmiş hali (`--+`) ya da hash (`#`) sembolü kullanılabilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** SQL injection attack, querying the database type and version on MySQL and Microsoft
- **Zafiyet Türü:** SQL Injection (Database Examination - Version Detection)
- **Amaç:** Ürün kategorisi filtresindeki SQLi zafiyetini kullanarak MySQL/Microsoft veritabanının sürüm bilgisini ekrana yazdırmak.

### Çözüm Adımları
1. **İstekin Yakalanması:**
   - Kategori filtresine tıklanarak giden `GET /filter?category=...` isteği Burp Repeater'a gönderilir.

2. **Kolon Sayısı ve String Desteğinin Belirlenmesi:**
   - Sorgunun 2 adet sütun döndürdüğü ve her iki sütunun da string verileri desteklediği doğrulanır:
     `category='+UNION+SELECT+'a','b'#`

3. **Veritabanı Sürümünün Çekilmesi:**
   - MySQL/MSSQL için sürüm sorgusu olan `@@version` fonksiyonu sütunlardan birine yerleştirilir:
     ```sql
     '+UNION+SELECT+'8.0.22-0ubuntu0.20.04.1', @@version#
     ```
   - (Veya alternatif olarak: `category='+UNION+SELECT+@@version,+NULL#`)
   - İstek gönderildiğinde sayfada veritabanı sürüm detayları (örn. `8.0.x` veya Microsoft SQL Server build bilgisi) basılır.

4. **Sonucun İncelemesi:**
   - Sürüm dizesi ekranda başarıyla görüntülendiğinde lab tamamlanır.
