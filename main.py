import network
import time
import gc
import machine
import sys
import config
import ubinascii
from machine import UART
from machine import Pin
from machine import WDT
from simple import MQTTClient
from obis import *

def DebugPrint(topic, txt):
    mqc.publish(str.encode(config.MQTTTopic + '/debug/' + topic), str.encode(txt))

unittest = 0

if unittest:
    try:
       uart = open("example.msg.crlf", "rb")
    except:
       print('Please do "mpremote cp unit-test/example.msg.crlf :"')
       sys.exit(-1)
else:
    uart = UART(1, baudrate=115200, invert=UART.INV_RX, rx=Pin(5), timeout=11000)

led = machine.Pin("LED", machine.Pin.OUT)
led.on()

version = "4"

hostname = config.ID + ubinascii.hexlify(machine.unique_id()).decode()

network.hostname(hostname)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config.SSID, config.PSK)
led.off()

waitcount = 0
while wlan.status() != 3:
   waitcount+=1
   time.sleep(0.5)
   led.toggle()
   if waitcount > 120:
      led.off()
      machine.reset()

# led on when connected to wlan
led.on()

mqc = MQTTClient(hostname, config.MQTTHost, 1883)
try:
   mqc.connect()
except:
   print('error')
   #machine.reset()

mqc.publish(str.encode(config.MQTTTopic + '/P1mqttID'), str.encode(hostname))
DebugPrint('version', version)

workbuffert = bytearray(1024)
mv = memoryview(workbuffert)
PublishedModel = b''

s = b''
MeterModel = b''

#wdt = WDT(timeout=8000)
a = 0
while True:
   mvpos=0
   if unittest:
      a += 1
      if a > 3:
          sys.exit(0)

   if unittest:
      DebugPrint('log', 'search start of frame')

   # Sync in to start of frame, "/<meter model>"
   while True:
      s = uart.readline()
      if (s != None) and (s[0] == b'/'[0]):
         MeterModel = s[1:].split(b'\r\n')[0]
         mv[mvpos : mvpos+len(s)] = s
         mvpos += len(s)
         break

   if s == None:
      continue

   if unittest:
      DebugPrint('log', 'frame found')
      DebugPrint('log', '  reading data...')

   while True:
      s = uart.readline()
      if s[0] == b'!'[0]:
         mv[mvpos] = ord('!')
         mvpos += 1
         msgcrc = s[1:].split(b'\r\n')[0]
         break
      mv[mvpos : mvpos+len(s)] = s
      mvpos += len(s)

   led.off()

   if unittest:
      DebugPrint('log', '   calculating crc')

   # Verify CRC
   calculatedcrc = OBIS_crc(workbuffert[0:mvpos])
   framecrc = int(msgcrc.decode(),16)
   if framecrc != calculatedcrc:
      DebugPrint('log', 'CRC ERROR')
      time.sleep(2)
      gc.collect()
      led.on()
      #wdt.feed()
      continue

   if MeterModel != PublishedModel:
      PublishedModel = MeterModel
      mqc.publish(str.encode(config.MQTTTopic + '/model'), PublishedModel)

   for p1msg in workbuffert.split(b'\r\n'):
      if len(p1msg) == 0:
         continue
      if p1msg[0] >= b'0'[0] and p1msg[0] <= b'9'[0]:
         obis = p1msg.split(b'(')[0]
         if obis == b'0-0:1.0.0':
             value = p1msg.split(b'(')[1].split(b'W')[0].lstrip(b'0')
         else:
             value = p1msg.split(b'(')[1].split(b'*')[0].lstrip(b'0')
         if value != OBIS_db[obis.decode()][1]:
            try:
               mqc.publish(str.encode(config.MQTTTopic + '/' + obis.decode()), value)
            except:
               machine.reset()
            OBIS_db[obis.decode()][1] = value

   if unittest:
       uart.seek(0)

   gc.collect()
   led.on()
   #wdt.feed()
