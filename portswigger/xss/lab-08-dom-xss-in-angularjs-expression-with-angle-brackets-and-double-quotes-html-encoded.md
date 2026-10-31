# DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded

## Konu Açıklaması (DOM-based XSS: CSTI ve AngularJS İfadeleri)

### A. Client-Side Template Injection (CSTI) Nedir?

Sunucu taraflı şablon enjeksiyonu (SSTI) mantığına benzer şekilde, istemci tarafında bir JavaScript framework'ü (AngularJS, Vue.js vb.) HTML içindeki özel şablon sözdizimlerini ayrıştırıyorsa ve kullanıcı girdisi bu direktiflerin sınırları içerisine filtresiz yansıtılıyorsa **Client-Side Template Injection (CSTI)** meydana gelir.

### B. `ng-app` Direktifinin Rolü

AngularJS yüklendiğinde, DOM ağacında `ng-app` direktifini arar. Bu direktifin altındaki tüm HTML öğeleri artık bir AngularJS uygulaması olarak değerlendirilir. AngularJS bu kapsamdaki her şeyi ayrıştırırken çift süslü parantez `{{ ... }}` arasındaki metinleri **AngularJS İfadeleri (Expressions)** olarak ele alır ve istemci tarafında derler.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Practitioner
- **Framework:** AngularJS (1.x)
- **Zafiyet Türü:** DOM-based Cross-Site Scripting / Client-Side Template Injection (CSTI)
- **Kaynak (Source):** URL arama parametresi (`search=...`)
- **Uygulanan Filtreleme:** Açılı parantezler (`< >`) ve çift tırnak (`"`) HTML entity formatında kodlanmaktadır (`&lt;`, `&gt;`, `&quot;`).
- **Etkilenen Kapsam:** `ng-app` direktifi tanımlı DOM elemanları
- **Hedef:** AngularJS ifadesi enjekte ederek `alert()` fonksiyonunu tetiklemek.

---

### Filtre Atlatma ve Payload Analizi

#### 1. Filtre Atlatma Mekanizması

Web uygulaması güvenlik önlemi olarak `< >` ve `"` karakterlerini HTML entity formatında kodlamaktadır. Bu durum klasik `<script>` veya HTML attribute kaçışlarını engeller; ancak:

1. AngularJS derleyicisi HTML ayrıştırıldıktan sonra DOM üzerinde çalışır.
2. Sayfada yeni bir HTML etiketi oluşturmaya gerek kalmadan doğrudan `{{ ... }}` sözdizimi aranır.
3. Çift süslü parantezler sunucu tarafından filtrelenmediği için şablon motoruna doğrudan iletilir.

#### 2. Payload Analizi: `$on.constructor` ve Function Constructor

AngularJS ifadelerinde `window` veya `document` nesnelerine doğrudan erişilemez (`{{window.alert(1)}}` çalışmaz). Kapsam kısıtlamasını aşmak için JavaScript nesne modelindeki **Constructor** zincirinden yararlanılır:

```javascript
{{$on.constructor('alert(1)')()}}
```

1. **`$on`:** AngularJS kapsamındaki yerleşik bir olay dinleyici fonksiyonudur.
2. **`$on.constructor`:** Fonksiyonun yapıcı nesnesi olan `Function` kurucusunu verir (`$on.constructor === Function`).
3. **`Function('alert(1)')`:** Dinamik bir JavaScript fonksiyonu derler (`eval()` gibi çalışır, ancak global kapsamda yürütülür).
4. **`(...)()`:** Derlenen anonim fonksiyon anında çağrılır.
5. Filtre yalnızca çift tırnakları kodladığından, dize içerisinde tek tırnak (`'`) kullanılarak filtre aşılır.

---

### Adım Adım Çözüm Metodolojisi

1. **Bağlamı Tespit Edin:**
   Arama kutusuna rastgele bir değer girip DevTools üzerinden girdinin `ng-app` kapsamındaki bir etikete yansıdığını gözlemleyin.

2. **CSTI Doğrulama:**
   Arama alanına `{{7*7}}` yazıp aratın; ekranda `49` sonucunu görerek şablon enjeksiyonunu doğrulayın.

3. **Payload Girişi:**
   Arama kutusuna payload'ı girin:
   ```javascript
   {{$on.constructor('alert(1)')()}}
   ```

4. **Çözüm:**
   Aramayı gerçekleştirdiğinizde `alert(1)` penceresi açılacak ve laboratuvar tamamlanacaktır.

---

### Güvenli Kodlama (Remediation)

* **`ng-non-bindable` Kullanımı:** Dinamik kullanıcı girdisinin basıldığı kapsayıcıya `ng-non-bindable` direktifi eklenerek şablon derlemesi engellenmelidir:
  ```html
  <p ng-non-bindable>Arama sonucu: {{ search_query }}</p>
  ```
* **Modern Framework Geçişi:** AngularJS (1.x) yerine statik şablon derlemesi (AOT) ve sıkı bağlam güvenliğine sahip modern Angular (2+), React veya Vue.js kullanılmalıdır.

