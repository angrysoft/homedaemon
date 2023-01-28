path = www/static
admin_path = panel/static
dart = dart2js -m -o
sasss = sassc -t compressed
INSTALL=install -C
USR=http
GRP=http
USRPAN=http
GRPPAN=http
PREFIX = /usr

install:
	python3 setup.py -v install --prefix=$(DESTDIR)$(PREFIX) --record files.txt


install_panel:
	install -v -m 755  -g $(GRPPAN) -o $(USRPAN) -d $(DESTDIR)/var/www/homepanel
	cp -rv panel/* $(DESTDIR)/var/www/homepanel
	chown -R $(USRPAN).$(GRPPAN) $(DESTDIR)/var/www/homepanel
	install -v -m 655 homepanel.service -D $(DESTDIR)/usr/lib/systemd/system/homepanel.service
	chmod -R a+r $(DESTDIR)/var/www/homepanel
	chmod -R g+w $(DESTDIR)/var/www/homepanel

uninstall:
	# rm -rvf $(DESTDIR)/etc/angryhome
	rm -vf $(DESTDIR)/usr/lib/systemd/system/homed.service
	./uninstall.py

uninstall_panel:
	rm -rvf $(DESTDIR)/var/www/homepanel
