# TryHackMe: DNS in Detail

DNS'in katmanlı hiyerarşisi, kayıt tipleri ve pratik sorgulama araçları.

## DNS hiyerarşisi
Bir domain adı sağdan sola doğru okunuyor:

```
tryhackme.com
    |       |
    |       └── TLD (Top-Level Domain) — .com, .org, .tr
    └────────── Second-Level Domain — "tryhackme"
```

**Subdomain** — ikinci düzey domain'in altında oluşturulan alt bölümler (ör: `blog.tryhackme.com`, `admin.tryhackme.com`).

**Pentest bakışı:** Subdomain enumeration recon'un en verimli adımlarından. `admin.`, `dev.`, `staging.`, `test.` gibi subdomainler genelde daha az güvenli — organizasyonun asıl sitesi sertken bir dev subdomain'inde açık olabiliyor.

## DNS Record tipleri

- **A** — domain adını IPv4 adresine eşleştiriyor
- **AAAA** — domain adını IPv6 adresine eşleştiriyor
- **CNAME** — bir domain'i başka bir domain'e yönlendiriyor (alias)
- **MX** — o domain'in mail sunucusu (Mail Exchange)
- **TXT** — serbest metin. SPF, DKIM, DMARC (mail güvenliği); domain sahiplik doğrulaması; genel notlar

**Pentest bakışı:**
- **MX** kayıtları hedefin mail altyapısını gösteriyor — Google Workspace mi, Microsoft 365 mi, kendi sunucusu mu? Phishing kampanyalarını buna göre şekillendiriyorsun.
- **TXT** kayıtları çok bilgi sızdırıyor: SPF kayıtları hangi sunucuların mail göndermeye yetkili olduğunu söyler; sahiplik doğrulama token'ları hangi third-party servislerin kullanıldığını gösterir.
- **CNAME** kayıtları eskimişse "dangling CNAME" saldırısı — silinmiş bir servise işaret eden CNAME'i saldırgan kendi hesabına ekleyerek subdomain takeover yapabilir.

## Pratik sorgulama araçları

### `nslookup`
```
nslookup domain-name
nslookup -type=TYPE domain-name [server]
```

Basit ama eski. `-type=` ile hangi kaydı istediğini belirtiyorsun (A, MX, TXT, NS).

### `dig`
```
dig [@server] domain-name [TYPE]
```

Modern muadili. Çıktısı çok daha detaylı — QUESTION, ANSWER, AUTHORITY, ADDITIONAL bölümleri. TTL değerleri açık, hangi otoriter sunucudan geldiği açık.

`dig +short` sadece cevap satırını verir, script'lerde kullanışlı.

### DNSDumpster
Web tabanlı, public DNS verilerini aggregate eden servis. Subdomain'leri, mail sunucularını, ağ haritasını grafik halinde çıkarıyor. Passive recon'un temel araçlarından — hedefe hiç paket göndermeden ciddi bilgi topluyor.

## Kaynak
TryHackMe — DNS in Detail room
