# Raw Socket MUST need UAC(sudo) in windows

import socket
import struct
import random

from iphdr import Iphdr
from udphdr import Udphdr
from numpy import short, byte

class UDPSocket:
  def __init__(self, source:tuple[str, short], dest:tuple[str, short] = None):
    self.source = source
    self.buffsize = 1024
    # Create socket
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    self.sock.bind((source[0], source[1]))
    # Include Header
    self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # IP Header
    self.ipHeader = None

    if dest is not None:
      self.connect(dest)

  def connect(self, dest:tuple[str, short]):
    self.dest = dest
    # Update IP Header
    self.ipHeader = Iphdr(1000, socket.IPPROTO_UDP, self.source[0], self.dest[0])

  def send(self, message:bytes):
    if self.ipHeader is None:
      raise Exception("[UDPSocket] No destination set")
    # Shuffle ID
    self.ipHeader.id = short(random.randint(0, 32767))

    # Change IP Length Header
    self.ipHeader.length = 20 + 8 + len(message)
    
    # Make UDP Header
    udpLen = 8 + len(message)
    udpHeader = Udphdr(self.source[1], self.dest[1], udpLen, 0)

    # Send to socket
    # IP Header + UDP Header + Message
    self.sock.sendto(self.ipHeader.pack_Iphdr() + udpHeader.pack_Udphdr() + message, (self.dest[0], 0))

  def receive(self):
    while True:
      # Receive from socket
      buffer, apiAddr = self.sock.recvfrom(self.buffsize)
      # Extract IP Header
      unpacked_ipheader = Iphdr.unpack_Iphdr(buffer)
      protocolId = Iphdr.getProtocolId(unpacked_ipheader)
      # Check if packet is UDP
      if protocolId != socket.IPPROTO_UDP:
        continue
      # Extract UDP Header
      unpacked_udpheader = Udphdr.unpack_Udphdr(buffer[20:28])
      # Check if dest matches
      ips = Iphdr.getIP(unpacked_ipheader)
      if ips[1] != self.source[0] or Udphdr.getDstPort(unpacked_udpheader) != self.source[1]:
        continue
      # Print where
      print(f"[UDPSocket] ===========================")
      print(f"[UDPSocket] Packet received from {ips[0]}:{Udphdr.getSrcPort(unpacked_udpheader)} - API Address: {apiAddr[0]}:{apiAddr[1]}")
      # Print IPv4 Header
      print(f"[UDPSocket] IPv4 Header")
      ipheader = list(unpacked_ipheader)
      ipheader[8] = socket.inet_ntoa(ipheader[8])
      ipheader[9] = socket.inet_ntoa(ipheader[9])
      self.printChart(
        ("VER", "TOS", "LEN", "ID", "F_OFF", "TTL", "PTCOL", "CKSUM", "SRC_IP", "DST_IP"),
        [ipheader]
      )
      # Print UDP Header
      print(f"[UDPSocket] UDP Header")
      self.printChart(
        ("SRC_P", "DST_P", "LEN", "CKSUM"),
        [unpacked_udpheader]
      )
      # Return message
      # print(f"[Test] Length: {len(buffer)}")
      messageLen = unpacked_udpheader[2] - 8
      addr = (ips[0], Udphdr.getSrcPort(unpacked_udpheader))
      if messageLen <= 0:
        print("[UDPSocket] Message is empty")
        return (b"", addr)
      else:
        return (buffer[28:28+messageLen], addr)

  # https://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data
  def printChart(self, head:tuple | list, content:tuple | list):
    row_format = "> "
    for h in head:
      if h == "SRC_IP" or h == "DST_IP":
        row_format += "{:>15}"
      else:
        row_format += "{:>6}"
    print(row_format.format(*head))
    for team, row in zip(head, content):
      print(row_format.format(*row))
  
  def close(self):
    self.sock.close()
