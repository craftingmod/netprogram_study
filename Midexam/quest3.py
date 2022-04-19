import socket
import random

ip = "220.69.189.125"
port = 443

# A
host = socket.gethostbyaddr(ip)
print(host[0])

# B
proto = socket.getservbyport(port)
print(proto)

# C
print(f"{proto}://{host[0]}")

# D
ip_binary = socket.inet_aton(ip)
print(ip_binary)