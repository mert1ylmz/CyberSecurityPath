""" 2. String İşlemleri (slicing, f-string, split/join/strip/replace)

Isınma

Bir log satırını ("2026-09-10 14:32:11 [ERROR] Connection refused from 10.0.0.5") .split() ile parçalara ayır; tarih, saat, seviye ve IP'yi ayrı değişkenlere al.
Aynı satırı f-string ile yeniden, farklı bir formatta ("[10.0.0.5] ERROR @ 14:32:11") yazdır. """

""" 
log = "2026-09-10 14:32:11 [ERROR] Connection refused from 10.0.0.5"

log = log.split(" ")
print(len(log))
array_length = len(log)

 """
""" 
for index in range(array_length):
    if "-" in log[index]:
        date = log[index]
        print(date)
    elif ":" in log[index]:
        time = log[index]
        print(time)
    elif "[" in log[index] or "]" in log[index]:
        message_level = log[index]
        print(message_level)
    elif "." in log[index]:
        ip_address = log[index]
        print(ip_address) """



""" print(f"[{log[0]}] {log[2].strip("[]")} @ {log[-1]}") """

""" Uygulama

Bir /etc/passwd satırını ("root:x:0:0:root:/root:/bin/bash") : ile .split() edip kullanıcı adı, UID, shell'i çek. Shell'i /bin/bash veya /bin/sh olanları "interactive" diye işaretle.
Slicing pratiği: bir string'i (LeetCode klasiği) tersten yazdır, palindrome mu kontrol et — [::-1] kullanmadan da bir versiyonunu yaz.
Bir HTTP header bloğunu (çok satırlı string) .strip() ve .split("\n") ile satırlara böl, her satırdaki header adı ve değerini .split(":", 1) ile ayır (dikkat: değer içinde : olabilir, maxsplit burada kritik). """

""" passwd_path = "root:x:0:0:root:/root:/bin/bash"
passwd_path = passwd_path.split(":")
username = passwd_path[0]
userid = passwd_path[2]
shell = passwd_path[-1]
print(f"Username: {username},\nUID: {userid},\n{shell}")
if shell == "/bin/bash" or shell == "/bin/sh":
    print("Interactive Shell") """


message = "Slicing pratiği"
message = list(message)
i = len(message)
while i != 0:
    print(message[i-1])
    i = i-1