import mip
import network
import config

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config.SSID, config.PSK)

mip.install("umqtt.simple")
