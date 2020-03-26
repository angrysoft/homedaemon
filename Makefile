path = www/static
dart = dart2js -m -o
sasss = sassc -t compressed
INSTALL=install -C
USR=http
GRP=http
USRPAN=http
GRPPAN=uwsgi
PREFIX = /usr

all: alldart allcss

alldart: main tvpilot ledpilot login admindevices

main: $(path)/main.dart
	$(dart) $(path)/main.dart.js $(path)/main.dart

login: $(path)/login.dart
	$(dart) $(path)/login.dart.js $(path)/login.dart

devices: $(path)/devices/devices.dart
	$(dart) $(path)/devices/devices.dart.js $(path)/devices/devices.dart
	$(dart) www/sw.dart.js $(path)/devices/sw.dart

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
	python3 setup.py -v install --prefix=$(DESTDIR)$(PREFIX) --record files.txt

install_www:
	install -v -m 755  -g $(GRP) -o $(USR) -d $(DESTDIR)/var/www/angryhome
	install -v -m 775  -g $(GRP) -o $(USR) -d $(DESTDIR)/var/run/angryhome
	install -v -m 655 angryhome.service -D $(DESTDIR)/usr/lib/systemd/system/angryhome.service
	cp -rv www/* $(DESTDIR)/var/www/angryhome
	chown -R $(USR).$(GRP) $(DESTDIR)/var/www/angryhome
	chmod -R a+r $(DESTDIR)/var/www/angryhome
	chmod -R g+w $(DESTDIR)/var/www/angryhome

install_panel:
	install -v -m 755  -g $(GRPPAN) -o $(USRPAN) -d $(DESTDIR)/var/www/adminpanel
	cp -rv panel/* $(DESTDIR)/var/www/adminpanel
	chown -R $(USRPAN).$(GRPPAN) $(DESTDIR)/var/www/adminpanel
	chmod -R a+r $(DESTDIR)/var/www/adminpanel
	chmod -R g+w $(DESTDIR)/var/www/adminpanel

uninstall:
	rm -rvf $(DESTDIR)/etc/angryhome
	rm -vf $(DESTDIR)/usr/lib/systemd/system/homed.service
	./uninstall.py

uninstall_www:
	rm -rvf $(DESTDIR)/var/www/angryhome
	rm -vf $(DESTDIR)/usr/lib/systemd/system/angryhome.service

uninstall_panel:
	rm -rvf $(DESTDIR)/var/www/adminpanel
