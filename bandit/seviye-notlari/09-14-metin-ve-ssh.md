# Bandit 09-14: Metin işleme, encoding ve SSH temelleri

Bu aralıkta metnin farklı temsilleri (binary, base64, basit şifreleme), Linux komut zinciri ve SSH ile dosya izinlerinin nasıl birbirine bağlı olduğunu öğrendim.

## `strings` — binary'den okunabilir çıkarmak
Bir dosyanın içindeki insan-okunabilir karakter dizilerini çıkarıyor. Binary bir dosyaya `cat` yapınca karakter kirliliği görünüyor; `strings` sadece basılabilir karakterleri filtreliyor.

Adli analiz (forensics) ve reverse engineering'de temel araç — bir binary'nin içindeki string'lere bakmak, ne yaptığına dair ilk fikir veriyor.

## `base64` — encoding, şifreleme değil
Base64 bir şifreleme yöntemi değil, encoding. Binary veriyi ASCII karakterlerle ifade etmenin standart yolu. Yaygın kullanım: e-posta ekleri, JWT token'lar, HTTP Basic Auth.

`base64 -d` ile decode edilebiliyor. Güvenlik açısından önemli nokta: base64 gördüğünde "şifreli" düşünme, sadece encoded.

## ROT13 ve `tr` komutu
ROT13 en basit substitution cipher — her harfi alfabede 13 basamak sonrasıyla değiştiriyor. `tr` (translate) komutu genel karakter dönüşümü için:

```
cat dosya.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Kavramsal olarak: ROT13 şifreleme sayılmaz, obfuscation. Ama Caesar cipher ailesinin mantığını anlamak, klasik kriptografiye giriş.

## Bandit 12 — recursive decompression
[Notu sonradan ekle: hex dump'tan başlayarak `xxd -r` ile binary'ye çevirme, sonra dosya tipini `file` ile kontrol edip gzip/bzip2/tar zincirini geri çözme. Öğrenilen kavram: `file` komutuyla dosya tipi tespiti ve sıkıştırma format çeşitliliği.]

## SSH private key ve dosya izinleri
Bir SSH private key kullanılabilmesi için dosya izinlerinin **sıkı** olması gerekiyor: sahibi hariç kimse okuyamamalı.

```
chmod 600 keydosyasi
```

SSH, izinler gevşekse anahtarı kullanmayı reddediyor — bilinçli bir güvenlik önlemi. "Bu senin özel anahtarın, kimseyle paylaşma" prensibinin dosya sistemi seviyesindeki karşılığı.

## `scp` — SSH üzerinden dosya transferi
Uzak sunucuda dosya izinlerini değiştiremediğin durumlarda dosyayı yerele indirmenin en pratik yolu:

```
scp kullanici@sunucu:/uzak/yol/dosya ./yerel-yol/
```

SSH kullandığı için aynı port ve kimlik doğrulama mantığı geçerli.

## `ssh -i` — belirli bir key ile bağlanmak
Varsayılan `~/.ssh/id_rsa` yerine belirli bir private key kullanmak için:

```
ssh -i keydosyasi kullanici@sunucu
```

## Kavramların birbirine bağlanması
Bu aralık tek bir hikâye anlatıyor: dosyanın içindeki bilgiyi çıkarmak için doğru araç lazım (strings/base64/tr/file), ama araçları sunucuda kullanamıyorsan dosyayı yerele indirmek gerek (scp), transfer için de kimlik doğrulama lazım (SSH keys + doğru izinler).

## Seviye referansı
- **09:** `strings`
- **10:** `base64`
- **11:** ROT13 + `tr`
- **12:** [notu tamamla]
- **13-14:** SSH keys, `chmod`, `scp`, `ssh -i`
