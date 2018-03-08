path = src/static
dart = dart2js -m -o
sasss = sassc -t compressed
INSTALL=install -C

all: alldart allcss

alldart: leds main rf rfpilot

leds: $(path)/leds.dart
	$(dart) $(path)/leds.dart.js $(path)/leds.dart

main: $(path)/main.dart
	$(dart) $(path)/main.dart.js $(path)/main.dart

rf: $(path)/rf.dart
	$(dart) $(path)/leds.dart.js $(path)/leds.dart

rfpilot: $(path)/rfpilot.dart
	$(dart) $(path)/rfpilot.dart.js $(path)/rfpilot.dart
	$(dart) $(path)/sw.dart.js $(path)/sw.dart

allcss: stylescss rfpilotcss

stylescss: $(path)/styles.css
	sassc -t compressed $(path)/styles.css $(path)/styles.min.css

rfpilotcss: $(path)/rfpilot.scss
	sassc -t compressed $(path)/rfpilot.scss $(path)/rfpilot.min.css

install:
	$(INSTALL) -d -m 755 $(DESTDIR)/var/www/smarthouse/{static,templates}
	$(INSTALL) -g http -o http src/static/* $(DESTDIR)/var/www/smarthouse/static/
	#$(INSTALL) -g http -o http src/static/*.dart $(DESTDIR)/var/www/smarthouse/static/
	#$(INSTALL) -g http -o http src/static/*.dart.js $(DESTDIR)/var/www/smarthouse/static/
	#$(INSTALL) -g http -o http src/static/*.css $(DESTDIR)/var/www/smarthouse/static/
	# templates
	$(INSTALL) -g http -o http src/templates/*.html $(DESTDIR)/var/www/smarthouse/templates/
	# server file
	$(INSTALL) -g http -o http -m 755 src/SmartHouse.py $(DESTDIR)/var/www/smarthouse/
	# daemon files
	$(INSTALL) -d -m 755 $(DESTDIR)/usr/bin
	$(INSTALL) -d -m 755 $(DESTDIR)/usr/lib/systemd/system
	$(INSTALL) -m 755 src/housed.py $(DESTDIR)/usr/bin
	$(INSTALL) -m 644 housed.service $(DESTDIR)/usr/lib/systemd/system
	# config files
	$(INSTALL) -d -m 755 $(DESTDIR)/etc/smarthouse
	$(INSTALL) -m 755 files/*.json $(DESTDIR)/etc/smarthouse/

uninstall:
	rm -rf $(DESTDIR)/var/www/smarthouse
	rm -f $(DESTDIR)/usr/lib/systemd/system/housed.service
	rm -f $(DESTDIR)/usr/bin/housed.py
