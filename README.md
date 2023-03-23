
Installera micropython

Installera paketet umqtt.simple
```python
import mip
mip.install("umqtt.simple")
```

Modifiera config.py.

kopiera boot.py main.py och config.py till rpi'n

med till exempel `mpremote.py fs cp config.py  :config.py` och så vidare. 

koppla in rpi till din elmätares HAN port med en rak RJ-12 kabel.



# Kopplingstabell


| RJ-12   |RJ- 12| RPI |
|---------|------|-----|
| 1 (Vcc) | 2 (dataReq)    | 39 (VSYS) |
| 3 (dataGnd) | | 8 (GND)
| 5 (data out) | | 7 (UART1 Rx)
| 6 (GND) | | 38 (GND)|

Sätt ett pull upp motstånd på 3,3 Kohm mellan 7 (UART1 Rx) 36 (3,3V) på rpi'n




