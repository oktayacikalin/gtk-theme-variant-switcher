ROOT := $(shell pwd)
PREFIX := $(shell readlink -f ~/.local)
OBJECTS := switcher.py

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
	cp -a gschema.xml $(PREFIX)/share/glib-2.0/schemas/org.gtk.Settings.ThemeVariantSwitcher.gschema.xml
	sudo ln -snf $(PREFIX)/share/glib-2.0/schemas/org.gtk.Settings.ThemeVariantSwitcher.gschema.xml /usr/share/glib-2.0/schemas/
	sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

all:
	@echo "Usage: $0 [install|uninstall]"

