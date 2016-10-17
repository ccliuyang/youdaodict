#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2014 Deepin, Inc.
#               2011~2014 Kaisheng Ye
#
# Author:     Kaisheng Ye <kaisheng.ye@gmail.com>
# Maintainer: Kaisheng Ye <kaisheng.ye@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtCore import QObject, pyqtSlot, QVariant, pyqtSignal
from configparser import RawConfigParser as ConfigParser
import sys
import os
import traceback

from utils import get_config_file
from xdg.DesktopEntry import DesktopEntry

DEFAULT_CONFIG = {
    "basic_option": dict([
        ("boot_start", True),
        ("start_mini", False),
        ("main_window_topmost", False),
        ("close_to_tray", True),
    ]),
    "getword": dict([
        ("ocr", True),
        ("stroke", True),
        ("ocr_mode", 1),
        ("stroke_mode", 0),
    ])
}

class Config(object):
    def __init__(self, config_file):
        self.config_parser = ConfigParser()
        self.remove_option = self.config_parser.remove_option
        self.has_option = self.config_parser.has_option
        self.add_section = self.config_parser.add_section
        self.getboolean = self.config_parser.getboolean
        self.getint = self.config_parser.getint
        self.getfloat = self.config_parser.getfloat
        self.options = self.config_parser.options
        self.items = self.config_parser.items
        self.config_file = config_file

    def load(self):
        self.config_parser.read(self.config_file)

    def has_option(self, section, option):
        return self.config_parser.has_option(section, option)

    def get(self, section, option, default=None, debug=False):
        try:
            return self.config_parser.get(section, option)
        except Exception as e:
            if debug:
                print("function get got error: %s" % (e))
                traceback.print_exc(file=sys.stdout)
            return default

    def set(self, section, option, value, debug=False):
        if not self.config_parser.has_section(section):
            if debug:
                print("Section \"%s\" not exist. create..." % (section))
            self.add_section(section)
        self.config_parser.set(section, option, value)

    def write(self, given_filepath=None):
        if given_filepath:
            f = open(given_filepath, "w")
        else:
            f = open(self.config_file, "w")
        self.config_parser.write(f)
        f.close()

class SettingConfig(QObject):

    configChanged = pyqtSignal(str, str, arguments=["section", "option"])
    hasSaved = pyqtSignal(QVariant, arguments=["change_options"])

    def __init__(self):
        QObject.__init__(self)
        self.config_file = get_config_file("config.ini")
        self.config = None
        self.load()

        self.change_options = []

        self.autostart_desktop = os.path.expanduser("~/.config/autostart/youdao-dict-autostart.desktop")
        self.sys_autostart_desktop = "/etc/xdg/autostart/youdao-dict-autostart.desktop"

        self._autostart = self.get_autostart()

    def get_autostart(self):
        if os.path.exists(self.autostart_desktop):
            desktop_entry = DesktopEntry(self.autostart_desktop)
            return not desktop_entry.getHidden()
        elif os.path.exists(self.sys_autostart_desktop):
            desktop_entry = DesktopEntry(self.sys_autostart_desktop)
            return not desktop_entry.getHidden()
        else:
            return False

    def set_autostart(self, enable):
        if not os.path.exists(self.autostart_desktop):
            if os.path.exists(self.sys_autostart_desktop):
                os.system("mkdir -p %s" % os.path.dirname(self.autostart_desktop))
                os.system("cp %s %s" % (self.sys_autostart_desktop, self.autostart_desktop))
            else:
                return False

        desktop_entry = DesktopEntry(self.autostart_desktop)
        if desktop_entry.getHidden() == enable:
            hidden_word = "false" if enable else "true"
            desktop_entry.set("Hidden", hidden_word)
            desktop_entry.write()

    def load(self):
        self.config = Config(self.config_file)
        self.config.load()

    def reload(self):
        if self.config:
            del self.config
        self.load()

    @pyqtSlot(str, str, result=QVariant)
    def get(self, section, config_key):
        if self.config.has_option(section, config_key):
            value = self.config.get(section, config_key)
            if value == "True":
                return True
            elif value == "False":
                return False
            else:
                return value
        else:
            values = DEFAULT_CONFIG.get(section)
            if values:
                return values.get(config_key)
            else:
                return None

    @pyqtSlot(str, str, QVariant)
    @pyqtSlot(str, str, QVariant, bool)
    def set(self, section, config_key, config_value, write=True):
        self.config.set(section, config_key, config_value)
        change_option = (section, config_key)
        if write:
            self.config.write()
            self.remove_change_option(change_option)
        else:
            self.add_change_option(change_option)

    def add_change_option(self, change_option):
        if not change_option in self.change_options:
            self.change_options.append(change_option)
            self.configChanged.emit(*change_option)

    def remove_change_option(self, change_option):
        if change_option in self.change_options:
            self.change_options.remove(change_option)
            self.configChanged.emit(*change_option)

    @pyqtSlot()
    def save(self):
        self.config.write()
        self.hasSaved.emit(self.change_options)
        for (section, config_key) in self.change_options:
            if section == "basic_option" and config_key == "boot_start":
                self.set_autostart(self._autostart)
        self.change_options = []

    @pyqtSlot(str, QVariant)
    @pyqtSlot(str, QVariant, bool)
    def set_getword(self, config_key, config_value, write=True):
        self.set("getword", config_key, config_value, write)

    @pyqtSlot(str, result=QVariant)
    def get_getword(self, config_key):
        return self.get("getword", config_key)

    @pyqtSlot(str, QVariant)
    @pyqtSlot(str, QVariant, bool)
    def set_basic_option(self, config_key, config_value, write=True):
        if config_key == "boot_start":
            self._autostart = config_value
            if write:
                self.set_autostart(self._autostart)
        self.set("basic_option", config_key, config_value, write)

    @pyqtSlot(str, result=QVariant)
    def get_basic_option(self, config_key):
        if config_key == "boot_start":
            return self._autostart
        return self.get("basic_option", config_key)

setting_config = SettingConfig()
