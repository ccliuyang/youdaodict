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

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5 import QtGui
from Xlib import X
from threading import Timer

from dae import xrobot

class EventRecord(QThread):

    capture_event = pyqtSignal("QVariant")

    def __init__(self):
        QThread.__init__(self)

    def record_callback(self, reply):
        xrobot.check_valid_event(reply)

        data = reply.data
        while len(data):
            event, data = xrobot.get_event_data(data)
            self.capture_event.emit(event)

    def run(self):
        xrobot.record_event(self.record_callback)

class EventHandler(QObject):

    press_alt = pyqtSignal()
    release_alt = pyqtSignal()
    press_ctrl = pyqtSignal()
    release_ctrl = pyqtSignal()

    ctrl_pressed = pyqtSignal()
    ctrl_released = pyqtSignal()
    alt_pressed = pyqtSignal()
    alt_released = pyqtSignal()
    shift_pressed = pyqtSignal()
    shift_released = pyqtSignal()
    double_ctrl_released = pyqtSignal()

    wheel_key_released = pyqtSignal()

    esc_pressed = pyqtSignal()

    left_button_press = pyqtSignal(int, int, int)
    right_button_press = pyqtSignal(int, int, int)
    wheel_press = pyqtSignal()

    key_pressed = pyqtSignal(str)
    key_released = pyqtSignal(str)

    translate_selection = pyqtSignal(int, int, str)
    cursorPositionChanged = pyqtSignal(int, int)

    def __init__(self, clipboard):
        QObject.__init__(self)
        self.clipboard = clipboard

        self.press_alt_flag = False
        self.press_ctrl_flag = False
        self.stop_timer = None
        self.stop_delay = 0.5

        self.press_alt_timer = None
        self.press_alt_delay = 0.1

        self.press_ctrl_timer = None
        self.press_ctrl_delay = 0.1

        self.hover_flag = False

        self.double_click_flag = False
        self.double_click_counter = 0
        self.double_click_timeout = True
        self.double_reset_timer = None
        self.double_click_delay = 0.3

        # Delete selection first.
        self.clear_clipbaoard()

        self._key_trigger_select = False

        self.cursor_stop_pos = None
        self.mouse_pos = (0, 0)

    def is_view_visible(self):
        return False

    def is_cursor_in_view_area(self):
        return False

    def reset_double_click(self):
        self.double_click_flag = False
        self.double_click_timeout = True

    def emit_press_ctrl(self):
        self.press_ctrl.emit()

    def emit_press_alt(self):
        if self.cursor_stop_pos:
            x, y = self.cursor_stop_pos
            self.press_alt.emit(x, y)

    def try_stop_timer(self, timer):
        if timer and timer.is_alive():
            timer.cancel()

    def translate_selection_area(self):
        #selection_content = commands.getoutput("xsel -p -o")
        #@ 获取选择字符
        selection_content = self.clipboard.text(QtGui.QClipboard.Selection)
        if len(selection_content) > 1 and not selection_content.isspace():
            mouse_x, mouse_y = self.mouse_pos
            self.translate_selection.emit(mouse_x, mouse_y, selection_content)

    def clear_clipbaoard(self):
        self.clipboard.clear(QtGui.QClipboard.Selection)

    def handle_double_ctrl_released(self):
        if not hasattr(self, "_ctrl_release_count_reset_timer") or not self._ctrl_release_count_reset_timer.is_alive():
            self._ctrl_release_count_reset_timer = Timer(0.6, self.reset_double_ctrl_release)
            self._ctrl_release_count_reset_timer.start()
        if hasattr(self, "_ctrl_release_count"):
            self._ctrl_release_count += 1
            if self._ctrl_release_count >= 2:
                self.double_ctrl_released.emit()
                self._ctrl_release_count = 0
        else:
            self._ctrl_release_count = 1

    def reset_double_ctrl_release(self):
        self._ctrl_release_count = 0

    @pyqtSlot("QVariant")
    def handle_event(self, event):

        # KeyPress event
        if event.type == X.KeyPress:
            keyname = xrobot.get_keyname(event)
            self.key_pressed.emit(keyname)
            if xrobot.is_alt_key(keyname):
                self.alt_pressed.emit()
            elif xrobot.is_ctrl_key(keyname):
                self.ctrl_pressed.emit()
            elif keyname in ["Escape"]:
                self.esc_pressed.emit()
            elif keyname in ["Shift_L", "Shift_R"]:
                self.shift_pressed.emit()

        # KeyRelease event
        elif event.type == X.KeyRelease:
            keyname = xrobot.get_keyname(event)
            self.key_released.emit(keyname)
            if xrobot.is_alt_key(keyname):
                self.alt_released.emit()
            elif xrobot.is_ctrl_key(keyname):
                self.ctrl_released.emit()
                self.handle_double_ctrl_released()
            elif keyname in ["Shift_L", "Shift_R"]:
                self.shift_released.emit()

        elif event.type == X.ButtonPress:
            if event.detail == 1:
                self.left_button_press.emit(event.root_x, event.root_y, event.time)

                # Set hover flag when press.
                self.hover_flag = False

                if self.double_click_timeout:
                    self.double_click_flag = False
                    self.double_click_timeout = False
                    self.double_click_counter = 0

                    self.double_reset_timer = Timer(self.double_click_delay, self.reset_double_click)
                    self.double_reset_timer.start()

            elif event.detail == 3:
                self.right_button_press.emit(event.root_x, event.root_y, event.time)
            elif event.detail == 5:
                self.wheel_press.emit()
        elif event.type == X.ButtonRelease:
            if event.detail == 1:
                self.double_click_counter += 1
                if self.double_click_counter == 2:
                    if self.double_reset_timer != None:
                        self.try_stop_timer(self.double_reset_timer)

                    self.double_click_flag = True
                    self.double_click_timeout = True

                # import time
                if not self.is_view_visible() or not self.is_cursor_in_view_area():
                    # print "1", time.time()
                    # Trigger selection handle if mouse hover or double click.
                    if self.hover_flag or self.double_click_flag:
                        if not self._key_trigger_select or self.press_ctrl_flag:
                            self.translate_selection_area()
                # Delete clipboard selection if user selection in visible area to avoid next time to translate those selection content.
                elif self.is_view_visible() and self.is_cursor_in_view_area():
                    # print "2", time.time()
                    self.clear_clipbaoard()
                self.hover_flag = False
            elif event.detail == 2:
                self.wheel_key_released.emit()

        elif event.type == X.MotionNotify:
            # Set hover flag to prove selection action.
            self.hover_flag = True
            self.cursor_stop_pos = None
            self.mouse_pos = (event.root_x, event.root_y)

            self.cursorPositionChanged.emit(event.root_x, event.root_y)

            self.try_stop_timer(self.stop_timer)
