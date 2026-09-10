# TryHackMe: Bash Scripting

Terminalde tek seferlik komutlar yerine, tekrar edilebilir script'ler yazmak. Pentest otomasyonunun temeli.

## Shebang — `#!/bin/bash`
Her script'in ilk satırı bu olmalı:

```bash
#!/bin/bash
```

**Ne diyor:** "Bu dosyayı çalıştırırken bash yorumlayıcısını kullan." Farklı yorumlayıcılar (`#!/usr/bin/env python3`, `#!/bin/sh`) da mümkün — shebang neyi çağıracağını belirliyor.

## Script'i çalıştırmak
İki yol var:

```bash
bash script.sh          # bash'ı elle çağırıyorsun
./script.sh             # dosyanın execute izni olmalı — chmod +x script.sh
```

Debug modu:
```bash
bash -x script.sh       # her satırı çalıştırırken ekrana basıyor
```

Sorunlu bir script'i tespit etmek için altın araç.

## Değişkenler
```bash
isim="Mert"
echo $isim              # Mert
```

**Önemli:** `=` etrafında boşluk YOK. `isim = "Mert"` hata verir. Bash'in en tuzaklı yerlerinden.

## `read` — kullanıcıdan girdi al
```bash
read -p "İsminizi girin: " isim
echo "Merhaba $isim"
```

`-p` prompt (soru) gösteriyor. Etkileşimli script yazarken temel.

## Diziler (arrays)
```bash
transport=('car' 'train' 'bike' 'bus')

echo "${transport[@]}"      # tüm elemanlar: car train bike bus
echo "${transport[1]}"      # ikinci eleman (0'dan başlıyor): train
echo "${#transport[@]}"     # eleman sayısı: 4
```

**`unset` — eleman silme**
```bash
unset transport[1]
```

Ama dikkat: eleman siliniyor ama **indeks boşluğu kalıyor**. Yani `transport[1]` artık yok, `transport[2]` hâlâ yerinde. Bu bash'in klasik gotcha'sı.

## Koşullar (conditionals)
```bash
if [ koşul ]
then
    komut
else
    başka-komut
fi
```

**Önemli:** `[` ve `]` içinde **boşluklar zorunlu**. `[koşul]` hata verir, `[ koşul ]` çalışır.

Örnek:
```bash
if [ "$isim" = "Mert" ]
then
    echo "Merhaba Mert"
else
    echo "Kimsin sen?"
fi
```

## Koşul operatörleri

**String karşılaştırma:**
- `=` veya `==` — eşit
- `!=` — eşit değil
- `-z` — boş string
- `-n` — boş değil

**Sayı karşılaştırma:**
- `-eq` — eşit
- `-ne` — eşit değil
- `-lt`, `-le` — küçük, küçük eşit
- `-gt`, `-ge` — büyük, büyük eşit

**Dosya kontrolü:**
- `-f dosya` — dosya var mı
- `-d dizin` — dizin var mı
- `-r`, `-w`, `-x` — okuma/yazma/çalıştırma izni

**Neden karışık:** String için `=`, sayı için `-eq` — bash'in en çok yanılan yeri. Genel kural: string'de sembolik, sayıda `-`'li operatör.

## Neden pentest için önemli
Elde tek script'le yapabildiğin şeyler:

- **Recon otomasyonu** — bir domain listesi ver, her birine `whois`, `dig`, `nmap -Pn -F` çek, çıktıyı dosyalara yaz
- **Log parsing** — büyük log dosyalarından belirli pattern'leri çekmek
- **Payload üretimi** — belirli formatta çok sayıda payload üretmek
- **CTF çözümü** — brute force gerektiren durumlar (aynı işlemi 1000 farklı input'la denemek)

Python daha güçlü ama bash bir sistemde çoğunlukla hazır bulunuyor — hızlı iş için ideal.

## Kaynak
TryHackMe — Bash Scripting room
