path = www/static
dart = dart2js -m -o
sasss = sassc -t compressed
INSTALL=install -C
USR=nginx
GRP=uwsgi
PREFIX = /usr

all: alldart allcss

alldart: main tvpilot ledpilot login admindevices

main: $(path)/main.dart
	$(dart) $(path)/main.dart.js $(path)/main.dart

login: $(path)/login.dart
	$(dart) $(path)/login.dart.js $(path)/login.dart

devices: $(path)/devices/devices.dart
	$(dart) $(path)/devices/devices.dart.js $(path)/devices/devices.dart
	$(dart) $(path)/devices/sw.dart.js $(path)/devices/sw.dart

tvpilot: $(path)/tvpilot/tvpilot.dart
	$(dart) $(path)/tvpilot/tvpilot.dart.js $(path)/tvpilot/tvpilot.dart
	$(dart) $(path)/tvpilot/sw.dart.js $(path)/tvpilot/sw.dart

admindevices: $(path)/admin/devices.dart
	$(dart) $(path)/admin/devices.dart.js $(path)/admin/devices.dart

allcss: stylescss devicesscss tvpilotcss ledpilotcss admincss

admincss: $(path)/admin.scss
	sassc -t compressed $(path)/admin.scss $(path)/admin.css

stylescss: $(path)/styles.scss
	sassc -t compressed $(path)/styles.scss $(path)/styles.css

devicesscss: $(path)/devices/devices.scss
	sassc -t compressed $(path)/devices/devices.scss $(path)/devices/devices.min.css

tvpilotcss: $(path)/tvpilot/tvpilot.scss
	sassc -t compressed $(path)/tvpilot/tvpilot.scss $(path)/tvpilot/tvpilot.min.css

ledpilotcss: $(path)/ledpilot/ledpilot.scss
	sassc -t compressed $(path)/ledpilot/ledpilot.scss $(path)/ledpilot/ledpilot.min.css

install:
	python3 setup.py -v install --prefix=$(PREFIX) --record files.txt

install_www:
	install -v -m 755  -g $(GRP) -o $(USR) -d /var/www/angryhome
	install -v -m 755  -g $(GRP) -o $(USR) -D www/* /var/www/angryhome

install_panel:
	install -v -m 755  -g $(GRP) -o $(USR) -d /var/www/panel
	install -v -m 755  -g $(GRP) -o $(USR) -D www/* /var/www/panel

uninstall:
	rm -rf $(DESTDIR)/var/www/smarthouse
	./uninstall.py
