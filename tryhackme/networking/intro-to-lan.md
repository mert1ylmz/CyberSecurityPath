# TryHackMe: Intro to LAN

Local Area Network — yerel ağın nasıl kurulduğu, cihazların nasıl birbirini bulduğu.

## LAN nedir
Fiziksel olarak sınırlı bir alanda (ev, ofis, kampüs) bulunan cihazların oluşturduğu ağ. İnternete çıkışı bir noktadan (genellikle router) yapıyor.

## Ağ Topolojileri
Cihazların birbirine nasıl bağlandığının fiziksel/mantıksal düzeni:

**Star (Yıldız)** — tüm cihazlar merkezi bir noktaya (switch) bağlı. Modern LAN standardı. Merkez çökerse her şey çöker ama tek bir cihaz sorunu yaymaz.

**Ring (Halka)** — cihazlar dairesel şekilde birbirine bağlı, veri belirli yönde dolaşıyor. Eski token ring ağlarında kullanıldı. Bir kopukluk tüm halkayı bozar.

**Bus (Yol)** — tek bir kablo hattına tüm cihazlar bağlanıyor. Eski koaksiyel kablo ağları. Bir çarpışma tüm ağı etkiliyor.

**Neden hâlâ önemli:** Modern ağlar star'a yakınsamış olsa da endüstriyel ortamlarda (SCADA, ICS) hâlâ bus ve ring topolojileri var — pentest yaparken karşına çıkabiliyor.

## Switch vs Router

**Switch** — birden fazla cihazı aynı ağda birleştiriyor. MAC adresine göre çerçeve yönlendiriyor. Layer 2 cihazı.

**Router** — farklı ağları birbirine bağlıyor, aralarında paket iletiyor. IP adresine göre yönlendirme yapıyor. Layer 3 cihazı.

Kısaca: switch bir odayı, router odaları birbirine bağlıyor.

## Subnetting temel kavramları

**Network Address** — bir ağı temsil eden adres (ör: 192.168.1.0)
**Host Address** — o ağdaki bir cihazın adresi (ör: 192.168.1.42)
**Default Gateway** — ağın dışına çıkarken kullanılan router IP'si (ör: 192.168.1.1)

Subnetting = büyük bir ağı mantıksal olarak daha küçük ağlara bölmek. Hem yönetim hem güvenlik açısından kritik — bir subnetteki cihaz diğer subnetteki cihaza direkt konuşamıyor, arada router gerekiyor.

## ARP — Address Resolution Protocol
IP adresini MAC adresine çevirmenin protokolü. Bir cihaz "192.168.1.5 kimde?" diye tüm ağa soruyor (**ARP request**), sahibi "bende, MAC'im şu" diye cevaplıyor (**ARP reply**).

**Pentest bakışı:** ARP güvensiz bir protokol — hiçbir doğrulama yok. **ARP spoofing / poisoning** klasik man-in-the-middle saldırısının temeli. Ettercap, arpspoof gibi araçlar tam olarak bunu yapıyor: "Ben 192.168.1.1'im (gateway'im)" diye yalan ARP reply göndererek trafiği kendine yönlendirmek.

## DHCP — Dynamic Host Configuration Protocol
Ağa yeni giren cihaza otomatik IP adresi atayan protokol. 4 adımlı bir el sıkışması var (DORA):

1. **Discover** — client "ağda DHCP sunucusu var mı?" diye broadcast atıyor
2. **Offer** — sunucu "sana şu IP'yi verebilirim" diye teklif ediyor
3. **Request** — client "kabul, o IP'yi istiyorum" diyor
4. **ACK** — sunucu "onayladım, senin" diyor

**Pentest bakışı:** Sahte DHCP sunucusu kurmak (rogue DHCP) — yeni ağa katılan cihazlara kendi belirlediğin gateway ve DNS bilgisini vermek. MITM saldırılarının başka bir yolu.

## Kaynak
TryHackMe — Intro to LAN room
