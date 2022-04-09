from socket import *
import struct
from iphdr import Iphdr

s = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)
s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

data = b'TestTestTest'
sport = 17300    # arbitrary source port
dport = 2500   # arbitrary destination port
length = 8+len(data)
checksum = 0
udp_header = struct.pack('!HHHH', sport, dport, length, checksum)

ip = Iphdr(1000, IPPROTO_UDP, "127.0.0.1", "127.0.0.1")
packed_iphdr = ip.pack_Iphdr()

s.sendto(packed_iphdr+udp_header+data, ("127.0.0.1", 2500))