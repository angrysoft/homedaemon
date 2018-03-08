path = src/static
dart = dart2js -m -o
sasss = sassc -t compressed

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
	install -d -m 755 $(DESTDIR)/var/www/smarthome/{static,templates}
	install -g http -o http src/static/*.dart $(DESTDIR)/var/www/smarthome/static/
	install -g http -o http src/static/*.dart.js $(DESTDIR)/var/www/smarthome/static/
	install -g http -o http src/static/*.css $(DESTDIR)/var/www/smarthome/static/
	# templates
	install -g http -o http src/templates/*.html $(DESTDIR)/var/www/smarthome/templates/
	# server file
	install -g http -o http -m 755 src/SmartHouse.py $(DESTDIR)/var/www/smarthome/
	# daemon files
	install -D -m 755 src/housed.py $(DESTDIR)/usr/bin
	install -D -m 655 housed.service $(DESTDIR)/usr/lib/systemd/system
	# config files
	install -D -m 755 files/*.json $(DESTDIR)/etc/smarthouse
