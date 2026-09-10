# Bandit 21-24: Cron ve zamanlanmış görevler

Bu aralık tamamen zamanlanmış görevler (cron) ve bunların güvenlik implikasyonları üzerine.

## Cron nedir
Linux'ta arka planda periyodik iş çalıştıran servis. Konfigürasyon dosyaları:

- `/etc/cron.d/` — sistem geneli tanımlı görevler
- `/etc/crontab` — ana cron tablosu
- `/var/spool/cron/crontabs/kullanici` — kullanıcı bazlı görevler

## Cron syntax'i
```
* * * * * kullanici komut
| | | | |
| | | | +-- haftanın günü (0-7)
| | | +---- ay (1-12)
| | +------ ayın günü (1-31)
| +-------- saat (0-23)
+---------- dakika (0-59)
```

## Cron'un pentest açısından önemi
Cron dosyaları genelde herkes tarafından okunabilir. Bu üç şey demek:

**1. Bilgi toplama:** Sistemde hangi görevler ne sıklıkla çalışıyor — bu sistemin nasıl kurgulandığına dair ciddi ipucu. Hangi servisler var, hangi script'ler nerede, çıktılar nereye yazılıyor.

**2. Yazılabilir script'ler:** Cron root olarak bir script çalıştırıyorsa ama script normal kullanıcı tarafından yazılabiliyorsa → o script'i değiştirerek root yetkisiyle istediğin komutu çalıştırabilirsin. Klasik privilege escalation.

**3. Çıktı dosyaları:** Bazen cron script'leri çıktılarını `/tmp/` gibi dizinlere yazıyor. Bu çıktılara erişebiliyorsan, root'un ürettiği veriye ulaşmış oluyorsun.

## Hash tabanlı geçici dosya deseni
Bir seviyede öğrendiğim kavram: script `whoami` çıktısını bir hash fonksiyonundan geçirip sonucu dosya adı olarak kullanıyor. Böyle sistemlerde:
- Dosya adını bilmek için o kullanıcı olman gerekiyor (veya hash'i tahmin edebilmen)
- Hangi hash algoritması olduğunu anlamak (`md5sum`, `sha1sum`, `sha256sum`) çözümü belirliyor

Bu desen (`echo $(whoami) | md5sum` gibi) gerçek sistemlerde de var — kullanıcıya özel geçici dosyalar için sık kullanılıyor.

## Script okuma alışkanlığı
Bu seviyelerden çıkardığım en önemli habit: bir cron dosyası gördüğümde sıralı olarak:

1. **Ne çalışıyor?** — komut/script yolu
2. **Kim çalıştırıyor?** — hangi kullanıcı
3. **Ne sıklıkla?** — cron expression
4. **Script'in kendisi ne yapıyor?** — `cat` ile içeriğini oku
5. **Script yazılabilir mi?** — `ls -la` ile izinlere bak

Bu 5 soru neredeyse tüm cron tabanlı privilege escalation senaryolarını kapsıyor.

## Kendi script'ini yazmak
Bandit 23-24 civarında ilk kez "kendi script'ini yaz, cron onu çalıştırsın" durumu geliyor. Bash scripting temellerinin nerede işe yaradığını burada gördüm — TryHackMe Bash Scripting odası tam zamanında gelmişti.

## Seviye referansı
- **21:** İlk cron karşılaşması, `/etc/cron.d/` yapısı
- **22:** Hash tabanlı dosya isimleri, cron script okuma
- **23:** Kendi script'ini yazma başlangıcı
- **24:** [devam eden notlar]
