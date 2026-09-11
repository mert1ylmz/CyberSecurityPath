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






OverTheWire Bandit — Level 26 → 27 Writeup

Platform: OverTheWire Bandit Konu: SUID binary ile yetki yükseltme (privilege escalation)

Özet

Bandit26'ya (25→26 seviyesindeki shell escape ile) ulaştıktan sonra home dizininde iki dosya buluyoruz: bandit27-do ve text.txt. bandit27-do bir SUID binary — yani kendi sahibinin (bandit27) yetkileriyle çalışıyor, kim çalıştırırsa çalıştırsın. Bu, daha önce görülmüş klasik bir SUID sömürüsü: binary'nin çalıştırdığı yetkiyi kullanarak bandit27'nin parola dosyasını doğrudan okuyabiliyoruz.

Adım Adım Çözüm
1. Verilen dosyaları incele

25→26 shell escape'i ile bandit26 hesabında gerçek bir bash oturumuna düştükten sonra ls ile dizindeki iki dosyayı görüyoruz: bandit27-do ve text.txt.

2. bandit27-do ne yapıyor?

Dosyayı çalıştırdığımızda, bunun bize başka bir kullanıcı olarak (bandit27 yetkisiyle) komut çalıştırma imkânı sağladığını görüyoruz. Bu, dosyanın SUID bit'i set edilmiş bir binary olduğunu ve sahibi bandit27 olduğu için, kim çalıştırırsa çalıştırsın komutun bandit27 yetkisiyle yürütüldüğünü gösteriyor — daha önceki seviyelerde (ör. setuid pratiği yaptığımız seviyelerde) gördüğümüz mantığın aynısı.

3. Parolayı doğrudan oku

SUID sayesinde bandit27'nin kendi parola dosyasını okuma yetkisine erişebiliyoruz:

./bandit27-do cat /etc/bandit_pass/bandit27

Bu komut, cat işlemini bandit27 yetkisiyle çalıştırıyor ve bandit27'nin parolasını doğrudan ekrana basıyor.

Öğrenilenler
SUID bit, dosyanın çalıştırılma yetkisini sahibine bağlar. Normal şartlarda bandit26, bandit27'nin parola dosyasını okuyamaz; ama SUID'li bir binary aracılığıyla dolaylı olarak bandit27 kimliğiyle komut çalıştırabiliyor.
"Bu binary ne yapıyor?" sorusu her zaman ilk adım olmalı. Dosyayı argümansız çalıştırıp davranışını gözlemlemek, ne tür bir yetki/işlev sunduğunu hızlıca ortaya koyuyor.
Bu, önceki seviyelerde görülen setuid mantığının doğrudan tekrarı. Aynı zafiyet sınıfı (SUID yanlış/kasıtlı yapılandırması), farklı bir binary üzerinden tekrar karşımıza çıktı — desen tanımak, çözüm süresini kısaltıyor.
text.txt bu seviyede kullanılmadı. Muhtemelen sadece dizini dolduran/dikkat dağıtan bir dosya; çözüm tamamen bandit27-do'nun SUID davranışına dayanıyor.
Kaynaklar
OverTheWire Bandit
GTFOBins — SUID/SGID binary sömürü teknikleri referans




OverTheWire Bandit — Level 28 → 29 Writeup

Platform: OverTheWire Bandit Konu: Git commit geçmişi üzerinden hassas veri sızıntısı

Özet

Bandit29'a geçiş için yine bir git reposu veriliyor. Repoyu klonladığımızda README.md dosyasında bandit29 için credential bilgileri var, ama parola kısmı düzenlenerek (redact edilerek) gizlenmiş. Ancak git, dosyanın geçmişindeki her commit'i saklar — dosyanın güncel hali temizlenmiş olsa bile eski commit'lerde parola hâlâ açık halde durabiliyor. git log -p ile commit geçmişini diff'leriyle birlikte incelediğimizde, parolanın daha önce eklenip sonradan kaldırıldığı commit'i görüp şifreye ulaşabiliyoruz.

Adım Adım Çözüm
1. Repoyu klonla

Bandit28'de öğrendiğimiz gibi git reposunu klonluyoruz (git clone ssh://bandit29-git@localhost/home/bandit29-git/repo).

2. README.md'yi incele

Klonlanan repoda README.md dosyasını açtığımızda bandit29 için kullanıcı adı ve parola bilgisi olduğunu görüyoruz — ama parola alanı sansürlenmiş/boş bırakılmış durumda.

3. Commit geçmişini görüntüle
git log -p

Bu komut, repodaki tüm commit'leri diff (-p / --patch) içerikleriyle birlikte listeliyor. Yani her commit'te hangi satırların eklendiğini/silindiğini doğrudan görebiliyoruz.

4. Geçmişte açık bırakılan parolayı bul

Commit geçmişini takip ettiğimizde, README.md'ye parolanın önce açık halde eklendiğini, sonraki bir commit'te ise satırın düzenlenip gizlendiğini görüyoruz. Diff çıktısında - ile başlayan (silinen) satır, eski hâliyle parolayı içeriyor — böylece bandit29'un parolasına ulaşıyoruz.

Öğrenilenler
Git hiçbir şeyi gerçekten "silmez." Bir dosyadan hassas veri kaldırılsa bile, o veri geçmiş commit'lerde erişilebilir kalır — repo history'si her zaman bir bilgi sızıntısı kaynağıdır.
git log -p, git log'a göre çok daha fazla bilgi verir. Sadece commit mesajlarını değil, her commit'in gerçek içerik değişikliğini (diff) gösterir; bu da "ne değişti" sorusuna doğrudan cevap verir.
Gerçek dünyada da sık karşılaşılan bir hata sınıfı. Geliştiricilerin .env, config veya credential dosyalarını yanlışlıkla commit'leyip sonra "düzeltmesi" — ama geçmişi temizlemeden — GitHub'da halka açık repolarda gerçekten yaşanan bir güvenlik açığı türü.
28→29'un mantığı, 27→28'in doğal devamı. Git clone becerisi aynı kalıyor, ama artık dosyanın sadece güncel haline değil, tüm geçmişine bakmayı öğreniyoruz.
Kaynaklar
OverTheWire Bandit
git log man page — -p / --patch seçeneği



OverTheWire Bandit — Level 29 → 30 Writeup

Platform: OverTheWire Bandit Konu: Git branch'leri ve tüm commit geçmişini (--all) tarama

Özet

Bandit30'a geçiş için yine bir git reposu veriliyor. Repoyu klonlayıp README.md'yi incelediğimizde bu sefer parola hiç verilmemiş. Önceki seviyeden farklı olarak burada mesele tek bir branch'in geçmişini incelemek değil — parola, o an checkout edilmiş branch'te görünmeyen başka bir commit'te saklı. git log --all ile repodaki tüm branch'lere ait commit'leri (sadece mevcut branch'i değil) listeleyip, şüpheli commit'leri git show <commit-hash> ile tek tek inceleyerek parolayı buluyoruz.

Adım Adım Çözüm
1. Repoyu klonla ve README'yi kontrol et

Repoyu klonluyoruz ve README.md dosyasını açıyoruz. Ancak bu sefer dosyada parola bilgisi hiç yok — önceki seviyedeki gibi "sansürlenmiş" bir satır da değil, doğrudan eksik.

2. Tüm commit'leri görüntüle
git log --all

Normal git log, yalnızca o an bulunduğumuz branch'in geçmişini gösterir. --all bayrağı ise repodaki bütün branch'lerdeki (ve HEAD'e bağlı olmayan referanslardaki) commit'leri listeler. Bu sayede, checkout etmediğimiz başka bir branch'te bırakılmış commit'leri de görebiliyoruz.

3. Commit'leri tek tek incele
git show <commit-hash>

git log --all çıktısındaki her commit hash'ini git show ile açıp içeriğine (diff'ine) bakıyoruz. Bu komut, ilgili commit'te hangi değişikliklerin yapıldığını doğrudan gösteriyor.

4. Parolayı bul

İncelediğimiz commit'lerden birinde, README.md'ye parolanın eklendiği bir değişiklik buluyoruz — bu commit, ana branch'e hiç merge edilmemiş, sadece başka bir branch'te veya "kopuk" bir commit olarak kalmış. Böylece bandit30'un parolasına ulaşıyoruz.

Öğrenilenler
git log varsayılan olarak sadece mevcut branch'i gösterir. Bir repoda "görünmeyen" veri arıyorsan, önce --all (tüm branch/ref'ler) veya --branches, --tags gibi bayraklarla kapsamı genişletmek gerekir.
Bir commit, bir branch'e merge edilmemiş olsa bile repoda kalıcı olarak durur. Git nesneleri (commit, blob, tree) branch'ten bağımsız olarak saklanır; bir branch'e "bağlı" görünmese de git log --all veya git fsck --unreachable gibi komutlarla hâlâ erişilebilir.
git show tek bir commit'in tam diff'ini görmek için en hızlı yol. git log -p tüm geçmişi dökerken, git show <hash> doğrudan hedeflenen commit'e odaklanmayı sağlıyor — çok commit'li repolarda arama sürecini hızlandırıyor.
Bu seviye, 28→29'un doğal bir üst seviyesi. Orada tek branch'in geçmişine bakmak yeterliydi; burada "geçmiş" kavramı branch sınırlarının ötesine taşınıyor.
Kaynaklar
OverTheWire Bandit
git log man page — --all seçeneği
git show man page

OverTheWire Bandit — Level 30 → 31 Writeup

Platform: OverTheWire Bandit Konu: Git tag'leri üzerinden gizlenmiş veriye ulaşma

Özet

Bandit31'e geçiş için yine bir git reposu veriliyor. Ancak bu seviyede README.md'de parola yok, git log --all ile bakıldığında da repoda yalnızca tek bir commit olduğunu görüyoruz — yani önceki seviyedeki gibi başka bir branch'te saklanan ek bir commit yok. Branch'lere bakmak bir sonuç vermiyor. Çözüm, git'in commit'lerden bağımsız başka bir referans türünde: git tag ile repoda etiketlenmiş bir commit olduğunu görüyoruz. git show <tag-adı> ile bu etiketin işaret ettiği commit'in içeriğini/diff'ini incelediğimizde parola ortaya çıkıyor.

Adım Adım Çözüm
1. Repoyu klonla, README'yi kontrol et

Repoyu klonluyoruz, README.md'de parola bilgisi bulamıyoruz.

2. Commit geçmişini kontrol et
git log --all

Bu komut repoda yalnızca bir commit olduğunu gösteriyor. Yani 29→30'daki gibi "başka bir branch'te unutulmuş commit" senaryosu burada geçerli değil — aranan veri commit geçmişinde değil.

3. Tag'leri kontrol et
git tag

Bu komut, repoda tanımlı git tag'lerini (etiketlenmiş referansları) listeliyor. Burada secret adında bir tag olduğunu görüyoruz. Git tag'leri, belirli bir commit'e verilen kalıcı, isimli işaretlerdir (genelde release/versiyon işaretlemek için kullanılır, ama burada veri saklamak için kullanılmış).

4. Tag'in işaret ettiği commit'i incele
git show secret

Bu komut, secret tag'inin işaret ettiği commit'in tam içeriğini (diff'ini) gösteriyor. Bu değişiklik içinde bandit31'in parolası yer alıyor.

Öğrenilenler
Git'te veri sadece commit geçmişinde değil, referanslarda da (tag, branch, ref) saklanabilir. git log --all yalnızca commit zincirini gösterir; tag'ler ayrı bir referans türü olduğu için bu komutla görünmeyebilir.
git tag (argümansız), repodaki tüm etiketleri listeler. Bir şüpheli/isimli etiket bulunduğunda, git show <tag-adı> ile doğrudan o commit'e atlanabilir — tıpkı bir commit hash'i kullanır gibi.
"Commit geçmişinde bir şey yok" sonucu araştırmanın bittiği anlamına gelmez. Bu seviye, git'in farklı veri saklama mekanizmalarını (commit, branch, tag) tek tek elemeyi öğretiyor — biri boş çıkarsa bir sonrakine bakmak gerekiyor.
29→30 ile 30→31 birbirini tamamlayan iki senaryo. Biri "branch'e bak", diğeri "branch'e bakma, tag'e bak" diyerek aynı temel git bilgisini (referans türleri) farklı açılardan pekiştiriyor.
Kaynaklar
OverTheWire Bandit
git tag man page
git show man page


# OverTheWire Bandit — Level 31 → 32 Writeup

**Platform:** OverTheWire Bandit
**Konu:** Git'e commit oluşturup uzak repoya push etme (.gitignore kısıtlamasını aşma)

---

## Özet

Önceki git seviyelerinden farklı olarak burada repodan bilgi *okumuyoruz*, aksine repoya bir şey *push ediyoruz*. Seviye bizden belirli bir içeriğe sahip bir dosyayı, belirtilen branch'e commit'leyip push etmemizi istiyor. Dosya adı, içeriği ve hedef branch bilgisi bize veriliyor. İstenen push başarıyla sunucuya ulaştığında, sunucu geri bir mesaj döndürüyor ve bu mesajın içinde bandit32'nin parolası yer alıyor.

---

## Adım Adım Çözüm

### 1. Görevi oku
Repoyu klonladıktan sonra README, bizden ne istendiğini söylüyor: belirtilen adda bir dosya oluştur, içine istenen içeriği yaz, ve bunu belirtilen branch'e push et.

### 2. Dosyayı oluştur
İstenen dosyayı `nano` ile oluşturup içine görevde belirtilen içeriği yazıyoruz:
```
nano key.txt
```

### 3. Dosyayı stage'e ekle
```
git add key.txt
```
Bu komut, oluşturduğumuz dosyayı commit'e dahil edilmek üzere hazırlıyor (staging area'ya alıyor).

> **Not:** Bu seviyede repoda genellikle bir `.gitignore` dosyası bulunur ve `*.txt` gibi bir kural ile `.txt` dosyalarının eklenmesini engeller. Bu durumda `git add key.txt` reddedilir; `git add -f key.txt` (force) ile bu kısıtlama aşılabilir.

### 4. Commit oluştur
```
git commit -m "commit mesajı"
```
Yaptığımız değişikliği bir açıklama mesajıyla birlikte kaydediyoruz.

### 5. Push et
```
git push
```
Commit'i uzak repoya (belirtilen branch'e) gönderiyoruz.

### 6. Parolayı al
Push sırasında repoya erişim için bölümün (bandit31) parolasını giriyoruz. Push başarıyla tamamlandığında sunucu bir cevap mesajı döndürüyor — bu mesajın içinde bandit32 için gerekli olan parola yer alıyor.

---

## Öğrenilenler

- **Git yalnızca okuma değil, yazma yönünde de kullanılır.** Önceki seviyeler (log, branch, tag) repodan veri *çekmeye* odaklıyken, bu seviye tam git iş akışının diğer yarısını — `add → commit → push` — pratik ettiriyor.
- **`.gitignore` bir güvenlik sınırı değildir.** Bir dosyanın ignore edilmesi, onun eklenmesini kesin olarak engellemez; `git add -f` ile kural override edilebilir. Bu, "istemci tarafı kısıtlamalar güvenlik sağlamaz" prensibinin git'teki karşılığı.
- **Sunucu tarafı hook'lar davranışı tetikleyebilir.** Push edilen içerik doğrulandığında sunucunun geri bir parola mesajı döndürmesi, git sunucularında pre-receive/post-receive hook mantığının bir örneği — push'a tepki olarak sunucuda kod çalışabilir.
- **Bu, Bandit git serisinin (28→32) kapanışı.** clone → log -p → log --all → tag → push zinciriyle git'in hem okuma hem yazma tarafını baştan sona görmüş olduk.

---

## Kaynaklar
- [OverTheWire Bandit](https://overthewire.org/wargames/bandit/)
- `git add`, `git commit`, `git push` man page'leri
- `gitignore(5)` — `.gitignore` kuralları ve `-f` ile override

