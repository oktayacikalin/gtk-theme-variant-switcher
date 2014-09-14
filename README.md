# Gtk Theme Variant Switcher

A small service which forces certain windows to use a specific Gtk theme variant. E.g. force dark window borders.

## Requirements
* Python 3
* Gnome Shell or Pantheon Shell (e.g. Elementary OS)

## Installation
Running "make install" in the root of the repository will install everything
into "$HOME/.local". You should then be able to find the
"Gtk Theme Variant Switcher" in your launcher menu.

You might want to add it to your autostart apps.

## Configuration
You can find the "config.ini" with some default settings in
"$HOME/.local/share/gtk-theme-variant-switcher".

The format is simple. The left side is the WM_CLASS of a window, while having
the requested Gtk theme variant on the right (either "light" or "dark").

You can grab the WM_CLASS by executing "xprop WM_CLASS" in the shell and
clicking on the window you want to modify.

After modifying the config.ini, you have to restart the switcher. For this you
have to kill and restart it:

1. $ kill $(ps x | grep switcher.py | grep -v grep | cut -d' ' -f2)

2. And then start it again using your launcher.

## Todos
For starters I would like move the whole configuration into
something like dconf and write some configuration GUI for it. This would also
result in not having you to kill and restart it again.

Until then, please don't kill me for this little inconvinience. Thanks!