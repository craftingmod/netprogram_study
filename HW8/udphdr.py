import struct
import socket
import struct
import binascii

from numpy import byte, short

class Udphdr:
  def __init__(self, senderPort:short, receiverPort:short, packetSize:short, checksum:short):
    self.sport = senderPort
    self.dport = receiverPort
    self.ulen = packetSize
    self.check = checksum

  def pack_Udphdr(self):
    packed = b""
    # Source Port
    packed += struct.pack("!H", self.sport)
    # Destination Port
    packed += struct.pack("!H", self.dport)
    # Length
    packed += struct.pack("!H", self.ulen)
    # Checksum
    packed += struct.pack("!H", self.check)
    return packed

  def packWithoutCheck(self):
    packed = b""
    # Source Port
    packed += struct.pack("!H", self.sport)
    # Destination Port
    packed += struct.pack("!H", self.dport)
    # Length
    packed += struct.pack("!H", self.ulen)
    # Checksum..? = 0
    packed += struct.pack("!H", 0)
    return packed

  def unpack_Udphdr(buffer:bytes):
    unpacked = struct.unpack("!HHHH", buffer[:8])
    return unpacked
  
  def getSrcPort(unpacked_udpheader:tuple) -> short:
    return unpacked_udpheader[0]
  
  def getDstPort(unpacked_udpheader:tuple) -> short:
    return unpacked_udpheader[1]

  def getLength(unpacked_udpheader:tuple):
    return unpacked_udpheader[2]

  def getChecksum(unpacked_udpheader:tuple):
    return unpacked_udpheader[3]

  # https://github.com/houluy/UDP/blob/master/udp.py
  # https://limjunho.github.io/2021/06/05/UDP-cksum.html
  def makeChecksum(data:bytes):
    checksum = 0
    data_len = len(data)
    if (data_len % 2):
      data_len += 1
      data += struct.pack("!B", 0)
    
    for i in range(0, data_len, 2):
      w = (data[i] << 8) + data[i + 1]
      checksum += w
    
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = ~checksum & 0xffff

    return checksum