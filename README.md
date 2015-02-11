# Gtk Theme Variant Switcher

A small service which forces certain windows to use a specific Gtk theme variant. E.g. force dark window borders.

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/theblacklion/gtk-theme-variant-switcher?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Requirements
* Python 3
* Gnome Shell or Pantheon Shell (e.g. elementary OS)

## Installation
Running "make install" in the root of the repository will install everything
into "$HOME/.local". It will also try to symlink it's glib schema into the system
schema folder and recompile them.

You should then be able to find the "Gtk Theme Variant Switcher" in your
launcher menu.

You might want to add it to your autostart apps.

## Configuration
You can find the configuration via dconf-editor in:
/org/gtk/settings/theme-variant-switcher/

The format of the key "**by-class**" is simple and consists of an array of 3 strings
each:
* WM_CLASS of a window
* requested Gtk theme variant (either "light" or "dark")
* Human readable description/comment (e.g. for cryptic classes)

You can grab the WM_CLASS by executing "xprop WM_CLASS" in the shell and
clicking on the window you want to modify.

You can also just run the switcher.py in the console and look for the open window in the output. But before running it, make sure that you change the line defining the LOG_LEVEL to 'DEBUG'. You can find that relatively at the beginning of the installed switcher.py file.

Any change to the "**by-class**" key should be reflected instantly. You should
also see some output in the console if you're having it open currently.

## Todos
* Write some configuration GUI for it.

Please tell me your impressions, ideas and critics. Feel free to open a bug
report if necessary.

Thanks!
