#!/usr/bin/env python3
#
# Switcher which enforces the theme variant.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from gi.repository import Gtk, Gio, Gdk, Wnck
import subprocess
import sys
import signal
import logging


LOG_LEVEL = 'INFO'
LOG_FORMAT = '[%(asctime)-15s] [%(module)s.%(funcName)s.%(levelname)s] %(message)s'

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger('switcher')


def set_theme(variant, window_id):
    subprocess.call(["xprop", "-id", str(window_id), "-f", "_GTK_THEME_VARIANT", "8u",
                     "-set", "_GTK_THEME_VARIANT", variant])


class Application(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self, application_id='de.gtk-theme-variant-switcher',
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        # http://zderadicka.eu/gsettings-flexible-configuration-system/
        self.settings = Gio.Settings('org.gtk.Settings.ThemeVariantSwitcher')
        self.settings.connect('changed', self.on_settings_changed)
        self.by_class = dict((item[0].lower(), item[1]) for item in self.settings.get_value('by-class').unpack())
        self.connect('activate', self.on_activate)

    def on_window_class_changed(self, window):
        logger.debug('Window class changed: %s' % window.get_xid())
        self.update_window(window)

    def on_screen_window_opened(self, screen, window):
        logger.debug('New window: %s' % window.get_xid())
        window.connect('class-changed', self.on_window_class_changed)
        self.update_window(window)

    def update_window(self, window):
        window_id = window.get_xid()
        window_name = window.get_name().lower()
        window_group = window.get_class_group_name()
        instance_name = window.get_class_instance_name()
        if instance_name is None:
            return
        instance_name = instance_name.lower()
        logger.debug('Got window: %s ("%s"/"%s")' % (instance_name, window_group, window_name))
        variant = self.by_class.get(instance_name, None)
        if variant:
            set_theme(variant, window_id)
            logger.info('Setting window "%s" to "%s".' % (instance_name, variant))

    def on_settings_changed(self, settings, keys):
        by_class = dict((item[0].lower(), item[1]) for item in settings.get_value('by-class').unpack())
        changes = []
        for key, val in by_class.items():
            if key in self.by_class and self.by_class[key] != val:
                changes.append(key)
            elif key not in self.by_class:
                changes.append(key)
        self.by_class = by_class
        screen = Wnck.Screen.get_default()
        for window in screen.get_windows():
            instance_name = window.get_class_instance_name()
            if instance_name is None:
                continue
            instance_name = instance_name.lower()
            if instance_name in changes:
                window.connect('class-changed', self.on_window_class_changed)
                self.update_window(window)

    def on_activate(self, data=None):
        window = Gtk.ApplicationWindow(application=self)
        self.add_window(window)

        screen = Wnck.Screen.get_default()
        screen.connect('window-opened', self.on_screen_window_opened)
        logger.info('Listening for newly opened windows.')


if __name__ == "__main__":
    # Install keyboard interrupt handler. (http://stackoverflow.com/a/16486080)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
