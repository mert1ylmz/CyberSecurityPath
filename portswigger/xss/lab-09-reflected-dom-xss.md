# Reflected DOM XSS

## Konu Açıklaması (Hibrit Zafiyet: Reflected DOM XSS)

**Reflected DOM XSS**, sunucu taraflı yansıma (reflection) ile istemci taraflı güvensiz DOM/JavaScript yürütmesinin birleştiği hibrit bir zafiyet türüdür:

1. **Sunucu Tarafı (Server-Side Reflection):** Sunucu, gelen HTTP isteğindeki bir parametreyi alır ve HTTP yanıtının (örneğin bir JSON yanıtının veya JS dize sabitinin) içerisine yansıtır.
2. **İstemci Tarafı (Client-Side Execution):** İstemci tarafında çalışan bir JavaScript dosyası, sunucudan dönen bu yanıtı okur ve `eval()` gibi tehlikeli bir alıcıya (**Sink**) doğrudan aktarır.

Sunucu tarafında eksik uygulanan karakter kaçırma (örneğin `"` karakterinin escape edilip `\` karakterinin unutulması), istemci tarafındaki `eval()` çağrısında dize bağlamından çıkılarak rastgele JavaScript çalıştırılmasına olanak tanır.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** Reflected DOM XSS
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Practitioner
- **Zafiyet Türü:** Reflected DOM-based Cross-Site Scripting
- **Kaynak (Source):** Sunucudan dönen JSON yanıtı (`/search-results`)
- **Alıcı Fonksiyon (Sink):** `eval()` fonksiyonu (`searchResults.js` içerisinde)
- **Filtre / Kaçış Mekanizması:** Sunucu çift tırnakları (`"`) kaçırmaktadır (`\"`), ancak ters eğik çizgi (`\`) karakterini kaçırmamaktadır.
- **Hedef:** JSON yanıtındaki kaçış mekanizmasını atlatıp `eval()` sink'i üzerinden `alert(1)` fonksiyonunu çalıştırmak.

---

### Kaynak Kod ve Taint Flow Analizi

1. Burp Suite Proxy üzerinden arama isteği incelendiğinde, aranan terimin sunucudan dönen dinamik bir JSON yanıtı (`/search-results?search=...`) içerisine yansıtıldığı görülür.
2. Sitenin JavaScript dosyalarından `searchResults.js` açıldığında gelen JSON verisinin doğrudan `eval()` içine verildiği tespit edilir:
   ```javascript
   // searchResults.js
   eval('var searchResultsObj = ' + this.responseText);
   ```
3. Arama kutusuna farklı karakterler girildiğinde sunucunun çift tırnak (`"`) karakterinin önüne ters eğik çizgi eklediği (`\"`), ancak ters eğik çizgi (`\`) karakterine herhangi bir kaçış işlemi uygulamadığı saptanır.

---

### Atlatma (Bypass) ve İstismar Mekanizması

#### A. Kaçış Karakterini İptal Etme (Escape Canceling)

Sunucu çift tırnakları escape etmek için önüne `\` koyar. Eğer saldırgan girdinin başına bizzat bir `\` eklerse:

* Saldırgan girdisi: `\"`
* Sunucunun çıktısı: `\\"`

Burada oluşan çift ters eğik çizgi (`\\`), JavaScript ayrıştırıcısı için **kaçırılmış bir ters eğik çizgi (escaped backslash)** anlamına gelir. Sonuç olarak:
* `\\` kendi içinde tamamlanır ve bir metin karakterine dönüşür.
* Hemen ardından gelen çift tırnak (`"`) artık kaçırılmamış (unescaped) bir tırnak haline gelir ve dize sabitini (string literal) kapatır!

#### B. Aritmetik Operatör ve JSON Nesnesini Erken Kapatma

Dize kapatıldıktan sonra JavaScript kodunun sözdizimi hatası vermeden yürütülmesi için:
1. **`-` (Eksi Operatörü):** Dize ile çağrılacak fonksiyon arasında aritmetik bir operatör kullanılarak iki bağımsız ifade ayrılır.
2. **`alert(1)`:** Çalıştırılmak istenen zararlı fonksiyon çağrılır.
3. **`}`:** JSON nesnesini vaktinden önce kapatır.
4. **`//`:** Orijinal JSON yanıtının devamında gelen arta kalan kısımları (`", "results":[]}`) tek satırlık yorum satırına alarak syntax hatasını engeller.

#### C. Sonuçta Oluşan Kodun Ayrıştırılması

Kullanılan nihai arama girdisi:
```text
\"-alert(1)}//
```

Sunucunun ürettiği ve `eval()` içine giren nihai dize:
```json
{"searchTerm":"\\"-alert(1)}//", "results":[]}
```

JavaScript motoru bunu şu şekilde yorumlar ve çalıştırır:
1. `{"searchTerm":"\\" ` ➔ Bir nesne özelliği tanımlanır.
2. `- alert(1)` ➔ Aritmetik çıkarma işlemi sırasında `alert(1)` çalıştırılır.
3. `}` ➔ JSON nesnesi tamamlanır.
4. `//", "results":[]}` ➔ Geri kalan her şey yorum satırı olarak yoksayılır.

---

### Adım Adım Çözüm Metodolojisi

1. **Proxy'yi Etkinleştirin:**
   Burp Suite Proxy sekmesinde trafiği izleyin (HTTP history veya Intercept).

2. **İsteği İnceleyin:**
   Hedef sitede arama kutusuna `XSS` yazıp aratın. Burp üzerinden dönen `/search-results` JSON yanıtını gözlemleyin.

3. **JS Dosyasını Bulun:**
   `Target > Site map` altından `searchResults.js` dosyasını açıp yanıtın `eval()` fonksiyonuna aktarıldığını doğrulayın.

4. **Filtre Davranışını Doğrulayın:**
   Çift tırnağın escape edildiğini (`\"`), ancak backslash'in (`\`) filtrelenmediğini teyit edin.

5. **Payload'ı Gönderin:**
   Arama kutusuna aşağıdaki payload'ı girin ve arama yapın:
   ```text
   \"-alert(1)}//
   ```

6. **Çözüm:**
   `alert(1)` kutusu ekranda belirecek ve laboratuvar başarıyla tamamlanacaktır.

---

### Güvenli Kodlama (Remediation)

* **`eval()` Kullanımını Terk Edin:** JSON verilerini ayrıştırmak için asla `eval()` kullanılmamalıdır. Bunun yerine standart ve güvenli olan `JSON.parse()` fonksiyonu tercih edilmelidir:
  ```javascript
  // Güvenli Ayrıştırma
  var searchResultsObj = JSON.parse(this.responseText);
  ```
  `JSON.parse()` kendisine verilen girdiyi yürütülebilir kod olarak derlemez; yalnızca veri nesnesi olarak ayrıştırır ve sözdizimi enjeksiyonlarını imkansız hale getirir.
* **Doğru Kaçırma (Escaping):** Sunucu tarafında kullanıcı girdileri JSON veya dize içerisine basılıyorsa standart bir JSON serileştirici kullanılmalı ve hem `"` hem de `\` karakterleri uygun şekilde escape edilmelidir (`\` karakteri `\\` yapılmalıdır).

