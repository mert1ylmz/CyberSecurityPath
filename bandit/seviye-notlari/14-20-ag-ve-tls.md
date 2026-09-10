# Bandit 14-20: Ağ, TLS ve ilk shell kavramları

Offensive security açısından çok önemli bir aralık: port kavramı, ağ üzerinden veri gönderip almak, TLS handshake, ve setuid ile ilk privilege escalation mantığı burada oturuyor.

## `netcat` (nc) — ağın İsviçre çakısı
İki temel modu var:
- **Client:** `nc host port` — bir porta bağlan
- **Listener:** `nc -l port` — bir portu dinle

Ek olarak `-z` (zero I/O, sadece port kontrol) ve `-v` (verbose) çok işe yarıyor: `nc -zv host port` ile bir portun açık olup olmadığını hızlıca test edersin.

**Neden önemli:** Reverse shell ve bind shell mantığının temeli bu. Bir tarafta listener, diğer tarafta client — pentest'te sürekli kuruyorsun.

## `echo | nc` deseni — porta text data göndermek
Bir porta text data göndermenin en pratik yolu:

```
echo 'gonderilecek-veri' | nc host port
```

Pipe (`|`) ile echo çıktısını nc'nin stdin'ine bağlıyorsun. Sadece Bandit için değil, gerçek testlerde de sık lazım.

## `openssl s_client` — TLS bağlantısını manuel kurmak
```
openssl s_client -connect host:port
```

Bu komut TLS handshake'i senin adına yapıyor ve şifreli kanaldan text göndermene izin veriyor. Çıktıda sertifika zinciri, cipher suite, protokol sürümü — hepsi görünür.

**Neden önemli:** HTTPS trafiğini debug etmenin ve sertifika sorunlarını teşhis etmenin standart yolu. Web sunucularla düşük seviyede konuşabilmek pentest'te sık lazım — eski TLS versiyonlarını test etmek, HTTP metodlarını manuel göndermek, hepsi bu araçla.

## Nmap ile port taraması
Bir aralıkta hangi portların açık olduğunu görmek:

```
nmap -p 31000-32000 host
```

`-sV` ile servis versiyonu tespiti, `-sC` ile default script'ler. Bu seviyede nmap ile ilk tanışma — Hafta 3'te detaylı çalışacağım.

## `diff -u` — dosya karşılaştırması
İki dosya arasındaki farkı görmek için:

```
diff -u eski.txt yeni.txt
```

`-u` unified format, en okunabilir çıktı. Git'in altında yatan mantık da bu. Log analizi, konfig karşılaştırması, backup doğrulaması için sık kullanılıyor.

## Shell seçenekleri ve `.bashrc` bypass
Bir sunucuda `.bashrc` modifiye edilmişse (mesela login'de otomatik logout eden bir script varsa), standart bağlantı işe yaramıyor. `/etc/shells` sistemdeki tüm shell'leri listeliyor. Farklı bir shell ile bağlanmak (mesela `ssh ... -t /bin/sh`) bu tuzaktan kaçmanın yolu.

**Neden önemli:** Gerçek dünyada da benzer durumlar var — sınırlandırılmış shell'ler (rbash), `.bashrc`'ye konmuş kontroller. Alternatif shell'lerle bunları bypass etmek klasik bir teknik.

## `setuid` bit — ilk privilege escalation kavramı
Bir dosyanın setuid bit'i set edilmişse (`-rwsr-xr-x`), o dosya kim tarafından çalıştırılırsa çalıştırılsın **dosyanın sahibi kim ise onun yetkisiyle** çalışıyor. `ls -la` çıktısında `s` gördüğünde bu.

Meşru kullanım: `passwd` komutu her kullanıcı çalıştırabilsin ama `/etc/shadow`'a yazabilsin diye root sahipli ve setuid.

Saldırgan bakışı: Yanlış yapılandırılmış setuid binary'ler klasik privilege escalation vektörü. Sistemdeki tüm setuid binary'leri bulmak için:

```
find / -perm -4000 2>/dev/null
```

## Kavramların bir arada — Bandit 20'nin öğrettiği
Bu seviyede öğrendiğim en güçlü kavram: bir binary belirli bir davranış gösteriyor (bir port'a bağlanıp veri bekliyor) → sen o davranışın karşı tarafını kendin sağlayabilirsin (nc ile listener aç, binary'yi kendi listener'ına yönlendir).

Bu düşünce şekli — "programın beklediği ortamı kendim yaratırım" — pentest'te sürekli lazım.

## Seviye referansı
- **14:** `nc` ile ilk port bağlantısı
- **15:** `openssl s_client`
- **16:** Nmap ile port taraması + TLS + local private key oluşturma
- **17:** `diff -u`
- **18:** Alternatif shell ile `.bashrc` bypass
- **19:** setuid binary
- **20:** Kendi listener'ını çalıştırıp binary ile konuşturmak
