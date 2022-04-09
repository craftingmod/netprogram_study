import socket
import struct
import sys

class DnsClient:
  def __init__(self, hostip:str):
    self.hostip = hostip

    # DNS Query Header
    self.transactionId = 1
    self.flag = 0x0100
    self.questions = 1
    self.answerRRs = 0
    self.authorityRRs = 0
    self.additionalRRs = 0

  def response(self, packet):
    dnsHeader = packet[:12]
    dnsData = packet[12:].split(b"\x00", 1)

    ansRR = packet[12+len(dnsData[0])+5:12+len(dnsData[0])+21]
    rr_unpack = struct.unpack("!2sHHIH4s", ansRR)
    ip_addr = socket.inet_ntoa(rr_unpack[5])
    return ip_addr

  # Create DNS Query
  def query(self, domainName:str):
    # DNS header Packing
    query = struct.pack("!HH", self.transactionId, self.flag)
    query += struct.pack("!HH", self.questions, self.answerRRs)
    query += struct.pack("!HH", self.authorityRRs, self.additionalRRs)

    part = domainName.split(".")

    for i in range(len(part)):
      query += struct.pack("!B", len(part[i]))
      query += part[i].encode()

    query += b"\x00"

    query_type = 1 # Type: A
    query_class = 1 # Class: IN
    query += struct.pack("!HH", query_type, query_class)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (self.hostip, 53) # DNS 주소
    sock.sendto(query, addr)
    packet, address = sock.recvfrom(65535)
    ip_addr = self.response(packet)
    print(domainName, ip_addr)
    return ip_addr