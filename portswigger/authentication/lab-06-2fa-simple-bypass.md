# 2FA simple bypass

## Konu Açıklaması (Multi-Factor Authentication & 2FA Simple Bypass)

### 1. Multi-Factor Authentication (MFA / 2FA) Zafiyetleri
Biyometrik faktörler web siteleri için her zaman pratik değildir. Bu nedenle son zamanlarda **İki Aşamalı Doğrulama (2FA)** mekanizmasının zorunlu veya opsiyonel olarak kullanımı yaygınlaşmıştır. Bu mekanizma; *bildiğin bir şey* (şifre) ile *sahip olduğun bir şeyi* (kod/token) birleştirir. Kullanıcıdan geleneksel şifreye ek olarak geçici bir doğrulama kodu istenir.

Saldırganlar parola bilgisini ele geçirmiş olsalar bile tek kullanımlık bu kodları harici olarak elde etmekte zorlanırlar. Ancak 2FA sisteminin hatalı mantıkla (flawed logic) geliştirilmiş veya kötü yapılandırılmış olması durumunda bu koruma mekanizmaları atlatılabilir.

---

### 2. Two-Factor Authentication Tokens (Doğrulama Belirteçleri)
* **Fiziksel Donanımlar:** Doğrulama kodları genellikle fiziksel bir cihaz üzerinden okunur. Yüksek güvenlikli sitelerde kullanıcılar için özel üretilmiş donanımlar (örneğin RSA token veya tuş takımlı cihazlar) kullanılır.
* **Alternatif Yöntemler:** 
  * Google Authenticator / TOTP uygulamaları,
  * Doğrudan telefona gönderilen SMS/Metin mesajları.

> **Risk:** SMS ile gönderilen kodlar potansiyel olarak risklidir; SIM Swap (SIM kopyalama) veya SS7 protokol zafiyetleri ile araya girilerek iletilen mesajlar saldırganlarca okunabilir.

---

### 3. Bypassing Two-Factor Authentication (2FA Atlama Mantığı)
Bazı durumlarda iki aşamalı doğrulama kurgusu hatalı tasarlanır ve 2FA adımı doğrudan bypass edilebilir.

* **Zafiyet Senaryosu:** Kullanıcıdan önce şifre istenir; şifre doğrulandıktan sonra doğrulama kodu sayfasına geçilir. Ancak sistem mimarisinde kullanıcı şifreyi doğru girdiği anda arka planda oturum başlamış (oturum çerezi atanmış) kabul edilebilir. Kullanıcı henüz 2FA kodunu girmemiş olsa dahi yetkilendirilmiş duruma geçer.
* **Saldırı Yöntemi:** Bu durumda 2FA kodunu girmeden, sadece başarılı giriş yapmış kullanıcıların erişebildiği hedef adrese (`/my-account`, `/dashboard` vb.) doğrudan gitmeyi denemek yeterli olabilir.

---

## Lab Çözümü

### Lab Bilgileri
- **Lab Adı:** 2FA simple bypass
- **Zafiyet Türü:** Multi-Factor Authentication (2FA Simple Bypass)
- **Amaç:** Doğrulama mantığı bypass edilebilen bir 2FA sistemini aşarak `carlos` adlı kullanıcının hesabına erişmek.
- **Referans Bilgiler:**
  - **Kendi Hesabımız:** `wiener:peter`
  - **Hedef Kullanıcı:** `carlos:montoya`

### Çözüm Adımları

1. **Normal Giriş Akışının Analiz Edilmesi:**
   * Bize verilen geçerli kimlik bilgileriyle (`wiener:peter`) giriş yapın ve gelen 2FA doğrulama kodunu girerek başarılı akışı tamamlayın.
   * Oturum açıldığında yönlendirilen `/my-account` sayfasının URL yapısını inceleyin.

2. **Hedef Kullanıcı ile Giriş:**
   * Çıkış yapın (`/logout`). Ardından hedef kullanıcı `carlos` için bilinen şifre ile giriş yapın.

3. **2FA Adımının Atlatılması (Bypass):**
   * Sistem 2FA doğrulama kodunu girmenizi istediği ekrana geldiğinde, kodu girmek yerine tarayıcının adres çubuğundaki URL'i doğrudan `/my-account` olarak değiştirin ve sayfaya gidin.

4. **Giriş ve Labın Tamamlanması:**
   * İki aşamalı doğrulama atlatılarak doğrudan `carlos` hesabına erişilmiş olur ve lab tamamlanır.
