OBIS_name = 0
OBIS_published = 1

OBIS_db = {
  '0-0:1.0.0' : [ 'Datum/tid', 0 ],
  '1-0:1.8.0' : [ 'Total aktiv energi uttag', 0 ],
  '1-0:2.8.0' : [ 'Total aktiv energi inmatning', 0 ],
  '1-0:3.8.0' : [ 'Total reaktiv energi uttag', 0 ],
  '1-0:4.8.0' : [ 'Total reaktiv energi inmatning', 0 ],
  '1-0:1.7.0' : [ 'Aktiv effekt uttag', 0 ],
  '1-0:2.7.0' : [ 'Aktiv effekt inmatning', 0 ],
  '1-0:3.7.0' : [ 'Reaktiv effekt uttag', 0 ],
  '1-0:4.7.0' : [ 'Reaktiv effekt inmatning', 0 ],
  '1-0:21.7.0' : [ 'L1 aktiv effekt uttag', 0 ],
  '1-0:22.7.0' : [ 'L1 aktiv effekt inmatning', 0 ],
  '1-0:41.7.0' : [ 'L2 aktiv effekt uttag', 0 ],
  '1-0:42.7.0' : [ 'L2 aktiv effekt inmatning', 0 ],
  '1-0:61.7.0' : [ 'L3 aktiv effekt uttag', 0 ],
  '1-0:62.7.0' : [ 'L3 aktiv effekt inmatning', 0 ],
  '1-0:23.7.0' : [ 'L1 reaktiv effekt uttag', 0 ],
  '1-0:24.7.0' : [ 'L1 reaktiv effekt inmatning', 0 ],
  '1-0:43.7.0' : [ 'L2 reaktiv effekt uttag', 0 ],
  '1-0:44.7.0' : [ 'L2 reaktiv effekt inmatning', 0 ],
  '1-0:63.7.0' : [ 'L3 reaktiv effekt uttag', 0 ],
  '1-0:64.7.0' : [ 'L3 reaktiv effekt inmatning', 0 ],
  '1-0:32.7.0' : [ 'L1 fasspänning', 0 ],
  '1-0:52.7.0' : [ 'L2 fasspänning', 0 ],
  '1-0:72.7.0' : [ 'L3 fasspänning', 0 ],
  '1-0:31.7.0' : [ 'L1 fasström', 0 ],
  '1-0:51.7.0' : [ 'L2 fasström', 0 ],
  '1-0:71.7.0' : [ 'L3 fasström', 0 ],
}

crc16data = []

def OBIS_crcold(buf):
    crc = 0
    for b in buf:
        crc ^= b
    return crc


def OBIS_crc(buf):
    crcValue = 0x0000

    if len(crc16data) == 0:
        for i in range(0, 256):
            crc = i & 0xFFFF
            for j in range(0, 8):
                if crc & 0x0001:
                    crc = ((crc >> 1) & 0xFFFF) ^ 0xA001
                else:
                    crc = (crc >> 1) & 0xFFFF
            crc16data.append(hex(crc))

    for c in buf:
        d = c
        tmp = crcValue ^ d
        rotated = (crcValue >> 8) & 0xFFFF
        crcValue = rotated ^ int(crc16data[(tmp & 0x00FF)], 0)

    return crcValue
