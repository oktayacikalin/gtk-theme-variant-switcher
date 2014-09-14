ROOT := $(shell pwd)
PREFIX := $(shell readlink -f ~/.local)
OBJECTS := config.ini switcher.py

uninstall:
	rm -r $(PREFIX)/share/gtk-theme-variant-switcher
	rm $(PREFIX)/share/icons/gtk-theme-variant-switcher.png
	rm $(PREFIX)/share/applications/gtk-theme-variant-switcher.desktop

install:
	mkdir -p $(PREFIX)/share/icons
	mkdir -p $(PREFIX)/share/applications
	mkdir -p $(PREFIX)/share/gtk-theme-variant-switcher
	cp -a $(OBJECTS) $(PREFIX)/share/gtk-theme-variant-switcher/
	cp -a switcher.png $(PREFIX)/share/icons/gtk-theme-variant-switcher.png
	cp -a switcher.desktop $(PREFIX)/share/applications/gtk-theme-variant-switcher.desktop
	sed -i 's!switcher.py!$(PREFIX)/share/gtk-theme-variant-switcher/switcher.py!' $(PREFIX)/share/applications/gtk-theme-variant-switcher.desktop

all:
	@echo "Usage: $0 [install|uninstall]"

