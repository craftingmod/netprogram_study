import binascii
from iphdr import Iphdr
import socket

ip = Iphdr(1000, 6, "10.0.0.1", "11.0.0.1")
packed_iphdr = ip.pack_Iphdr()
print(binascii.b2a_hex(packed_iphdr))

unpacked_iphdr = Iphdr.unpack_Iphdr(packed_iphdr)
print(unpacked_iphdr)
print(f"Packet Size: {Iphdr.getPacketSize(unpacked_iphdr)}, Protocol ID: {Iphdr.getProtocolId(unpacked_iphdr)}, IP: {Iphdr.getIP(unpacked_iphdr)}")

