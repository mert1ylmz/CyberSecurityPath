""" Isınma """

""" 
Bir IP adresini string olarak al ("192.168.1.10"), .split(".") ile 4 parçaya ayır, her parçayı int'e çevirip topla.

type() kullanmadan, sadece operatörlerle bir değişkenin int mi float mı olduğunu anla (ipucu: // ve / farkı). 
"""

""" ip_adrress = input("Enter your IP Address: ")
octets = []
octets =  ip_adrress.split(".")
print(octets)
sum = 0
for octet in octets :
    
    sum = sum + int(octet)
print(f"Sum of your IP Address: {sum}") """

""" an_integer = 34
a_float = 25.7


print(a_float%1)
print(an_integer%1)
 """
""" If the mod 1 of a variable is equals to 0 then it's an integer. Else it's a float number.
This level achievement is that the / operand does not provides the right information of a variable. Whatever the type is it always 
returns float type. But with the // floor division operand we can guess at least one of the variables. Because if the to variables used in // operand is int => result is int, if one of them is float => result is float.  """


""" Uygulama

Bir port numarasını (int) al, 1-1023 arası ise "well-known port", 1024-49151 arası ise "registered port", üstü "dynamic/private port" yazdır (sadece if/elif, henüz döngü yok).
Basit bir subnet mask hesaplayıcı: CIDR (/24 gibi) verilince kaç host adresi olduğunu 2**(32-prefix) - 2 formülüyle hesapla. """

""" 
port_number = 12534


if (1<port_number<1024):
    print("Well-Known")
elif (1024<port_number<49151):
    print("Registered Port")
elif port_number==0:
    print("You've entered wrong port number.")
else:
    print("Dynamic/Private port") """


CIDR_Prefix = input("Enter your subnet prefix in CIDR notation: ")
CIDR_Prefix = int(CIDR_Prefix.split("/")[1])
print(CIDR_Prefix)
print("Your network can host up to :")
print(2**(32-CIDR_Prefix)-2)