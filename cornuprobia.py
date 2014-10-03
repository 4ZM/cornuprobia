import sys, signal
import random
from time import sleep
from scapy.all import *
  
def rand_ssid(wordlist):
  return random.choice(wordlist).strip()[:32]


def send_probereq(intf='', ssid_gen=None, dst='', src='', bssid='', count=0):

  # Configure defaults
  if not ssid_gen: ssid_gen = lambda : 'w00p'
  if not dst: dst = 'ff:ff:ff:ff:ff:ff'
  if not src: src = RandMAC()
  if not bssid: bssid = RandMAC()
  if not intf: intf = 'mon0'
  if count < 1: count = random.randint(1,9)

  # Beacon interface
  conf.iface = intf

  # Build probe request package
  ssid = ssid_gen()
  param = Dot11ProbeReq()
  essid = Dot11Elt(ID='SSID',info=ssid)
  rates  = Dot11Elt(ID='Rates',info='\x03\x12\x96\x18\x24\x30\x48\x60')
  dsset = Dot11Elt(ID='DSset',info='\x01')
  pkt = RadioTap()/Dot11(type=0, subtype=4, addr1=dst, addr2=src, addr3=bssid)/param/essid/rates/dsset

  # Send the packets
  print '[*] Sending %d probe(s): %s  %s \'%s\'' % (count, bssid,src,ssid)
  try:
    sendp(pkt, count=count, inter=0.1, verbose=0)
  except:
    raise

# Handle Ctrl-C to exit
def sig_handler(sig, frame):
  print '[*] Turning of goodness'
  sys.exit(0)


if __name__ == "__main__":

  print '[*] Cornuprobia - Fountain of 802.11 Probe Requests'

  # Listen for termination requests
  signal.signal(signal.SIGINT, sig_handler)
  signal.signal(signal.SIGTERM, sig_handler)

  # Parse cmd line - todo

  # Configure ssid generator
  ssid_gen = None
  wordlist = 'wordlist'
  print '[*] SSID wordlist: %s' % wordlist
  with open(wordlist) as f:
    words = f.readlines()
  ssid_gen = lambda: rand_ssid(words)

  # Send probes    
  while True:
    send_probereq(ssid_gen=ssid_gen)
    sleep(random.uniform(0, 1))
