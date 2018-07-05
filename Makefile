path = www/static
dart = dart2js -m -o
sasss = sassc -t compressed
INSTALL=install -C
USR=nginx
GRP=uwsgi
PREFIX = /usr

all: alldart allcss

alldart: leds main rf rfpilot

leds: $(path)/leds.dart
	$(dart) $(path)/leds.dart.js $(path)/leds.dart

main: $(path)/main.dart
	$(dart) $(path)/main.dart.js $(path)/main.dart

rf: $(path)/rf.dart
	$(dart) $(path)/leds.dart.js $(path)/leds.dart

rfpilot: $(path)/rfpilot/rfpilot.dart
	$(dart) $(path)/rfpilot/rfpilot.dart.js $(path)/rfpilot/rfpilot.dart
	$(dart) $(path)/rfpilot/sw.dart.js $(path)/rfpilot/sw.dart

tvpilot: $(path)/tvpilot/tvpilot.dart
	$(dart) $(path)/tvpilot/tvpilot.dart.js $(path)/tvpilot/tvpilot.dart
	$(dart) $(path)/tvpilot/sw.dart.js $(path)/tvpilot/sw.dart

allcss: stylescss rfpilotcss

stylescss: $(path)/styles.css
	sassc -t compressed $(path)/styles.css $(path)/styles.min.css

rfpilotcss: $(path)/rfpilot/rfpilot.scss
	sassc -t compressed $(path)/rfpilot/rfpilot.scss $(path)/rfpilot/rfpilot.min.css

tvpilotcss: $(path)/tvpilot/tvpilot.scss
	sassc -t compressed $(path)/tvpilot/tvpilot.scss $(path)/tvpilot/tvpilot.min.css

install:
	python3 setup.py -v install --prefix=$(PREFIX) --record files.txt

uninstall:
	rm -rf $(DESTDIR)/var/www/smarthouse
	rm -f $(DESTDIR)/usr/lib/systemd/system/housed.service
	rm -f $(DESTDIR)/usr/bin/housed.py
