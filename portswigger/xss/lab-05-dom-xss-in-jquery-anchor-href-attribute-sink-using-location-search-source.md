# DOM XSS in jQuery anchor href attribute sink using location.search source

## Konu Açıklaması (DOM-based XSS: jQuery attr() Sink & Pseudo-Protocols)

**DOM-based Cross-Site Scripting (DOM XSS)**, istemci tarafındaki JavaScript veya kütüphanelerin (örneğin jQuery), saldırgan kontrolündeki bir kaynaktan (**Source**) aldığı veriyi denetlemeden DOM yapısını veya eleman özniteliklerini değiştiren bir alıcıya (**Sink**) yazması sonucu ortaya çıkar.

Bağlantı etiketlerinin (`<a>`) `href` özniteliği tehlikeli bir sink'tir. Çünkü modern web tarayıcıları `http:` veya `https:` protokollerinin yanı sıra `javascript:` sözde protokolünü (pseudo-protocol) de destekler. Bu öznitelik kullanıcı kontrolündeki bir veriyle beslendiğinde, kullanıcı bağlantıya tıkladığında zararlı JavaScript kodu çalıştırılabilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** DOM XSS in jQuery anchor `href` attribute sink using `location.search` source
- **Platform:** PortSwigger Web Security Academy
- **Zorluk Seviyesi:** Apprentice
- **Kütüphane:** jQuery
- **Zafiyet Türü:** DOM-based Cross-Site Scripting (DOM XSS)
- **Kaynak (Source):** `location.search` (`returnPath` parametresi)
- **Alıcı Fonksiyon (Sink):** jQuery `attr()` fonksiyonu (`href` özniteliği)
- **Tetikleme Yöntemi:** `javascript:` Sözde Protokolü (Pseudo-Protocol) / Kullanıcı Tıklama Etkileşimi
- **Hedef:** Geri bildirim sayfasındaki "Back" bağlantısını manipüle ederek `alert()` fonksiyonunu tetiklemek.

---

### Kaynak Kod ve Taint Flow Analizi

Geliştirici Araçları (DevTools) ile geri bildirim sayfası ve form yapısı incelendiğinde arka planda çalışan jQuery betiği:

```javascript
$(function() {
    $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
});
```

- **Source (Kaynak):** `window.location.search` içindeki `returnPath` parametresi.
- **Sink (Alıcı):** `$('#backLink').attr("href", ...)`
- **Mekanizma:** Sayfa yüklendiğinde jQuery betiği, `#backLink` seçicisine sahip bağlantı elemanının (`<a id="backLink">`) `href` değerine doğrudan URL'deki `returnPath` girdisini yazar. Herhangi bir şema veya protokol doğrulaması yapılmamaktadır.

---

### İstismar Mantığı: `javascript:` Sözde Protokolü

Tarayıcılar, `<a href="...">` bağlantılarında standart web protokollerinin (`http`, `https`) yanı sıra `javascript:` şemasını da destekler:

```html
<a id="backLink" href="javascript:alert(document.domain)">Back</a>
```

Kullanıcı bu bağlantıya tıkladığında tarayıcı harici bir sayfaya yönlendirme yapmak yerine, iki nokta üst üste (`:`) simgesinden sonra gelen JavaScript komutunu mevcut sayfa bağlamında çalıştırır.

---

### Adım Adım Çözüm Metodolojisi

1. **Feedback Sayfasına Geçiş:**
   Ana sayfadaki **Submit feedback** butonuna tıklanarak geri bildirim formunun bulunduğu sayfaya gidilir.

2. **URL ve Kaynak İncelemesi:**
   Sayfa adres çubuğunda URL'in şu parametreyle bittiği görülür:
   ```text
   /feedback?returnPath=/
   ```

3. **DevTools ile Sink Tespiti:**
   DevTools (`F12`) konsol/kaynak sekmesinden form scripti incelendiğinde, `#backLink` elemanına `.attr()` fonksiyonu ile `returnPath` parametresinin atandığı doğrulanır.

4. **Payload Enjeksiyonu:**
   URL'deki `returnPath` parametresine kötü amaçlı betik içeren sözde protokol yerleştirilir:
   ```text
   /feedback?returnPath=javascript:alert(document.cookie)
   ```
   *(veya alternatif olarak `javascript:alert(1)` / `javascript:alert(document.domain)`)*

5. **İstismar ve Tetikleme:**
   Sayfa bu yeni URL ile yüklendikten sonra formun altındaki **Back** bağlantısına tıklanır (veya form gönderiminden sonra geri dönülür). jQuery tarafından bağlantının `href` değerine aktarılan betik çalışır ve `alert()` tetiklenerek laboratuvar başarıyla tamamlanır.

---

### Güvenli Kodlama (Remediation)

Kullanıcı kontrolündeki dinamik geri dönüş/yönlendirme bağlantılarında yalnızca güvenli göreli (relative) yollara veya izin verilen protokollere izin verilmelidir. Girdinin `javascript:`, `data:` veya `vbscript:` gibi tehlikeli sözde protokollerle başlamadığı doğrulanmalıdır:

```javascript
$(function() {
    const returnPath = (new URLSearchParams(window.location.search)).get('returnPath');
    
    // Güvenlik Doğrulaması: Yalnızca tek bir slash '/' ile başlayan göreli yollara izin ver
    // Protokol içeren (javascript:, data:) veya şema bağımsız (//evil.com) değerleri reddet
    if (returnPath && returnPath.startsWith('/') && !returnPath.startsWith('//')) {
        $('#backLink').attr("href", returnPath);
    } else {
        $('#backLink').attr("href", "/"); // Varsayılan güvenli anasayfa
    }
});
```
