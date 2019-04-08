path = www/static
dart = dart2js -m -o
sasss = sassc -t compressed
INSTALL=install -C
USR=nginx
GRP=uwsgi
PREFIX = /usr

all: alldart allcss

alldart: leds main rf rfpilot tvpilot ledpilot

leds: $(path)/leds.dart
	$(dart) $(path)/leds.dart.js $(path)/leds.dart

main: $(path)/main.dart
	$(dart) $(path)/main.dart.js $(path)/main.dart

lights: $(path)/lights/lights.dart
	$(dart) $(path)/lights/lights.dart.js $(path)/lights/lights.dart
	$(dart) $(path)/lights/sw.dart.js $(path)/lights/sw.dart

tvpilot: $(path)/tvpilot/tvpilot.dart
	$(dart) $(path)/tvpilot/tvpilot.dart.js $(path)/tvpilot/tvpilot.dart
	$(dart) $(path)/tvpilot/sw.dart.js $(path)/tvpilot/sw.dart

ledpilot: $(path)/ledpilot/ledpilot.dart
	$(dart) $(path)/ledpilot/ledpilot.dart.js $(path)/ledpilot/ledpilot.dart
	$(dart) $(path)/ledpilot/sw.dart.js $(path)/ledpilot/sw.dart

allcss: stylescss rfpilotcss tvpilotcss ledpilotcss

stylescss: $(path)/styles.css
	sassc -t compressed $(path)/styles.css $(path)/styles.min.css

lightscss: $(path)/lights/lights.scss
	sassc -t compressed $(path)/lights/lights.scss $(path)/lights/lights.min.css

tvpilotcss: $(path)/tvpilot/tvpilot.scss
	sassc -t compressed $(path)/tvpilot/tvpilot.scss $(path)/tvpilot/tvpilot.min.css

ledpilotcss: $(path)/ledpilot/ledpilot.scss
	sassc -t compressed $(path)/ledpilot/ledpilot.scss $(path)/ledpilot/ledpilot.min.css

install:
	python3 setup.py -v install --prefix=$(PREFIX) --record files.txt

uninstall:
	rm -rf $(DESTDIR)/var/www/smarthouse
	./uninstall.py
