OverTheWire Bandit — Level 25 → 26 Writeup

Tarih: 11.09.2026 Platform: OverTheWire Bandit Konu: Kısıtlı shell atlatma (restricted shell escape), SSH key izinleri, more üzerinden interaktif shell kaçışı

Özet

Bandit25, bandit26'ya geçiş için bir SSH private key sağlıyor. Ancak asıl zorluk key ile giriş yapmak değil — bandit26 hesabının login shell'i /bin/bash değil, kısıtlı ve alışılmadık bir shell. Bu shell'i /etc/passwd üzerinden tespit edip, shell'in çalıştırdığı more komutunu kötüye kullanarak (terminali küçültüp interaktif moda zorlayarak) vi/vim üzerinden gerçek bir bash shell'ine kaçış yapılıyor.

Adım Adım Çözüm
1. bandit25'e bağlan, key'i bul

Bandit25'e bağlandığımızda ls ile home dizininde bir SSH private key görüyoruz: bandit26.sshkey. Bu key, bandit26 hesabına giriş için kullanılacak.

2. Dosya izinlerini düzelt

Key dosyasının izinleri SSH'ın kabul edeceği şekilde ayarlanmamış (misconfigured). chmod 600 bandit26.sshkey komutunu doğrudan bandit25 üzerinde çalıştırmayı denediğimizde işletim sistemi seviyesinde hata alıyoruz (dosya bize ait değil / izin yetersiz).

Çözüm: Key içeriğini cat bandit26.sshkey ile okuyup, çıktıyı kendi local makinemizde nano bandit26.sshkey ile oluşturduğumuz boş dosyaya yapıştırıyoruz. Böylece dosya artık bizim sahipliğimizde oluyor ve chmod 600 sorunsuz uygulanabiliyor.

3. İlk bağlantı denemesi başarısız
ssh -i bandit26.sshkey bandit26@bandit.labs.overthewire.org

Bu komut beklenen sonucu vermiyor — normal bir shell'e düşmüyoruz, ne kadar denenirse denensin aynı sonuç tekrarlanıyor.

4. bandit26'nın shell'ini tespit et

Sorunun sebebini anlamak için bandit25 üzerinden bandit26 hesabının hangi login shell'ini kullandığını araştırıyoruz. /etc/shells dosyası sistemde tanımlı shell'lerin listesini veriyor ama hangisinin bandit26'ya atandığını göstermiyor. Bunun yerine:

cat /etc/passwd | grep bandit26

komutu ile bandit26'nın login shell'inin standart /bin/bash değil, özel bir script olduğunu görüyoruz — bu script içeride more komutunu çağırıyor.

5. more davranışını anla

more, uzun metin dosyalarını sayfa sayfa (satır satır) gösteren, klavyeden yukarı/aşağı ile gezilebilen interaktif bir sayfalama aracı. Ancak more interaktif moda yalnızca gösterilecek içerik terminal ekranından uzunsa geçiyor — içerik kısaysa dosyayı direkt basıp çıkıyor.

6. Terminali küçülterek interaktif modu tetikle

Shell'in okuduğu dosya (text.txt) içerik olarak kısa olduğu için normal boyuttaki bir terminalde more interaktif moda geçmiyor. Bunu aşmak için terminal penceresini elle en küçük boyuta getiriyoruz, böylece kısa metin bile ekrana sığmayıp more'u interaktif moda zorluyor. Bu haldeyken SSH bağlantısını kuruyoruz.

7. more içinden vi'ye geç

more interaktif moddayken v tuşuna basmak, o an görüntülenen dosyayı bir editörde (varsayılan olarak vi/vim) açıyor.

8. vim'den shell'e kaç

vim açıldıktan sonra komut moduna geçip:

:set shell=/bin/bash
:shell

komutlarını çalıştırıyoruz. İlk komut vim'in "shell açma" davranışında kullanacağı programı /bin/bash olarak ayarlıyor, ikincisi ise bu shell'i fiilen başlatıyor. Sonuç: kısıtlı shell'i atlatıp tam yetkili bir bash oturumuna düşüyoruz.

Öğrenilenler
Kısıtlı shell'ler her zaman güvenli değildir. Shell kısıtlaması genelde "hangi komutlar çalıştırılabilir" düzeyinde tanımlanır; ama izin verilen komutun kendisi (burada more) başka bir programı (vi) çağırma yeteneğine sahipse, kısıtlama kolayca delinebilir. Bu GTFOBins mantığının klasik bir örneği.
/etc/passwd sadece kullanıcı bilgisi değil, saldırı yüzeyi haritasıdır. Bir hesabın login shell alanı, o hesaba erişim sağlandığında karşılaşılacak ortamı önceden anlamak için kritik.
Ortam koşullarını (terminal boyutu gibi) kontrol etmek bir teknik. more'un interaktif moda geçme koşulunu (içerik ekran boyutunu aşması) tersine çevirip terminali küçülterek zorlamak, "beklenmeyen girdi/ortam ile davranışı manipüle etme" prensibine iyi bir örnek.
Dosya sahipliği SSH key izinlerini etkiler. chmod'un başka bir kullanıcıya ait dosya üzerinde çalışmaması, key'i kendi ortamımıza taşımamızı gerektirdi — pratikte sık karşılaşılan bir SSH izin problemi.
Kaynaklar
OverTheWire Bandit
more(1) man page
GTFOBins — kısıtlı shell / binary kaçış teknikleri referansı
