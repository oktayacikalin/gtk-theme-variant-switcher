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
import configparser
from os.path import join, dirname
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
        config_filepath = join(dirname(__file__), 'config.ini')
        config = configparser.ConfigParser()
        config.readfp(open(config_filepath))
        self.variants = dict(config.items('variants'))
        self.connect('activate', self.on_activate)

    def on_window_opened(self, screen, window):
        # logger.info('Window opened: %s' % window.get_xid())
        instance_name = window.get_class_instance_name()
        try:
            variant = self.variants[instance_name]
            set_theme(variant, window.get_xid())
            logger.info('Set theme variant for window %s of %s to %s.' % (window.get_xid(), window.get_class_group_name(), variant))
            logger.debug('Window name = "%s"' % window.get_name())
        except KeyError:
            pass

    def on_activate(self, data=None):
        window = Gtk.ApplicationWindow(application=self)
        self.add_window(window)

        screen = Wnck.Screen.get_default()
        screen.connect('window-opened', self.on_window_opened)
        logger.info('Listening for newly opened windows.')


if __name__ == "__main__":
    # Install keyboard interrupt handler. (http://stackoverflow.com/a/16486080)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
