from dnsclient import DnsClient
import sys

if len(sys.argv) > 1:
  client = DnsClient("1.1.1.1")
  client.query(sys.argv[1])