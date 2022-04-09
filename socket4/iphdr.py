import struct
import socket
import struct
import binascii

from numpy import byte, short

class Iphdr:
  def __init__(self, tot_len:short, protocol:byte, saddr:str, daddr:str):
    self.ver_len = 4 << 4 | 5
    self.tos = 0
    self.tot_len = tot_len
    self.id = 0
    self.frag_off = 0
    self.ttl = 255
    self.protocol = protocol
    self.check = 0
    self.saddr = socket.inet_aton(saddr)
    self.daddr = socket.inet_aton(daddr)

  def pack_Iphdr(self):
    packed = b""
    packed += struct.pack("!BBH", self.ver_len, self.tos, self.tot_len)
    packed += struct.pack("!HH", self.id, self.frag_off)
    packed += struct.pack("!BBH", self.ttl, self.protocol, self.check)
    packed += struct.pack("!4s4s", self.saddr, self.daddr)
    return packed

  def unpack_Iphdr(buffer:bytes):
    unpacked = struct.unpack("!BBHHHBBH4s4s", buffer[:20])
    return unpacked

  def getPacketSize(unpacked_ipheader:bytes):
    return unpacked_ipheader[2]

  def getProtocolId(unpacked_ipheader:bytes):
    return unpacked_ipheader[6]

  def getIP(unpacked_ipheader:bytes):
    src_ip = socket.inet_ntoa(unpacked_ipheader[8])
    dest_ip = socket.inet_ntoa(unpacked_ipheader[9])
    return (src_ip, dest_ip)