PICO_RST=https://datasheets.raspberrypi.com/soft/flash_nuke.uf2
MP=https://micropython.org/resources/firmware/RPI_PICO_W-20240222-v1.22.2.uf2
UMQTT=https://github.com/micropython/micropython-lib/raw/master/micropython/umqtt.simple/umqtt/simple.py

all: deploy

$(shell basename $(PICO_RST)):
	curl -O $(PICO_RST)

$(shell basename $(MP)):
	curl -O $(MP)

$(shell basename $(UMQTT)):
	curl -LRJO $(UMQTT)

.PHONY: dependencies
dependencies: $(shell basename $(PICO_RST)) $(shell basename $(MP)) $(shell basename $(UMQTT))

.PHONY: deploy
deploy: dependencies
	cp $(shell basename $(PICO_RST)) /run/media/per/RPI-RP2
	sleep 15
	cp $(shell basename $(MP)) /run/media/per/RPI-RP2
	sleep 5
	# upgrade version string so we can follow we run the latest...
	before=$$(cat main.py | grep ^version | cut -d\" -f2) ;\
	sed -i s/^version.*/version\ =\ \"$$(($$before+1))\"/g main.py
	grep ^version main.py
	mpremote cp config.py :config.py
	mpremote cp boot.py simple.py obis.py :
	mpremote cp main.py :

.PHONY: redeploy
redeploy:
	mpremote bootloader
	sleep 4
	make deploy

.PHONY: unit-test
unit-test:
	sudo stty -F /dev/ttyUSB0 raw
	sudo stty -F /dev/ttyUSB0 -echo -echoe -echok
	sudo stty -F /dev/ttyUSB0 115200
	sudo stty -F /dev/ttyUSB0
	while true; do cat unit-test/example.msg.crlf >> /dev/ttyUSB0; sleep 10; done

.PHONY: mqtt-viewer
mqtt-viewer:
	sub --auto-reconnect \
		--broker tcp://$$(grep MQTTHost config.py.home | cut -d\' -f2):1883 \
		--topic $$(grep MQTTTopic config.py.home | cut -d\' -f2)/#

.PHONY: clean
clean:
	$(RM) $(shell basename $(PICO_RST)) $(shell basename $(MP)) $(shell basename $(UMQTT))
