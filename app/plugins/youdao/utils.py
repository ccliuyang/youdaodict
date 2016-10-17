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

import os
import sys
import traceback
import shutil
import fcntl
import pickle
import collections
import threading

from functools import wraps
from PyQt5.QtCore import QTimer
import urllib
import deepin_dict

true = True
false = False
null = None

PROGRAM_NAME = "youdao-dict"

_home = os.path.expanduser('~')
xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or \
            os.path.join(_home, '.cache')

xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.join(_home, '.config')

class open_offline_dict:
    def __enter__(self):
        deepin_dict.open(os.path.join(get_parent_dir(__file__), "youdao.db"))
        return deepin_dict
    def __exit__(self, *args):
        deepin_dict.close()

def get_cache_file(path):
    ''' get cache file. '''
    cachefile = os.path.join(xdg_cache_home, PROGRAM_NAME, path)
    cachedir = get_parent_dir(cachefile)
    if not os.path.isdir(cachedir):
        os.makedirs(cachedir)
    return cachefile

def get_config_file(path):
    ''' get config file. '''
    configfile = os.path.join(xdg_config_home, PROGRAM_NAME, path)
    configdir = get_parent_dir(configfile)
    if not os.path.isdir(configdir):
        os.makedirs(configdir)
    return configfile

def touch_file_dir(filepath):
    # Create directory first.
    dir = os.path.dirname(filepath)
    if not os.path.exists(dir):
        os.makedirs(dir)

def touch_file(filepath):
    '''
    Touch file, equivalent to command `touch filepath`.

    If filepath's parent directory is not exist, this function will create parent directory first.

    @param filepath: Target path to touch.
    '''
    # Create directory first.
    touch_file_dir(filepath)

    # Touch file.
    if os.path.exists(filepath):
        os.utime(filepath, None)
    else:
        open(filepath, 'w').close()

def get_parent_dir(filepath, level=1):
    '''
    Get parent directory with given return level.

    @param filepath: Filepath.
    @param level: Return level, default is 1
    @return: Return parent directory with given return level.
    '''
    parent_dir = os.path.realpath(filepath)

    while(level > 0):
        parent_dir = os.path.dirname(parent_dir)
        level -= 1

    return parent_dir

def is_true(string_value):
    if isinstance(string_value, bool):
        return string_value
    else:
        try:
            return string_value.lower() == "true"
        except:
            return False

def safe_eval(string):
    global true
    global false
    global null
    return eval(string)

def timered(time):
    """
        A decorator that will make any function run after a QTimer timeout
    """
    def wrap_timer(f, time):
        t = QTimer()
        @wraps(f)
        def wrapper(*args, **kwargs):
            t.setInterval(time)
            t.setSingleShot(True)
            t.timeout.connect(lambda : f(*args, **kwargs))
            t.start()
        return wrapper

    if hasattr(time, "__call__"):
        f = time
        time = 2000
        return wrap_timer(f, time)
    else:
        def wrapper(f):
            return wrap_timer(f, time)
        return wrapper

def threaded(func):
    """
        A decorator that will make any function run in a new thread
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.setDaemon(True)
        t.start()

    return wrapper

def encode_params(data):
    """Encode parameters in a piece of data.

    Will successfully encode parameters when passed as a dict or a list of
    2-tuples. Order is retained if data is a list of 2-tuples but arbitrary
    if parameters are supplied as a dict.
    """

    if isinstance(data, (str, bytes)):
        return data
    elif hasattr(data, 'read'):
        return data
    elif hasattr(data, '__iter__'):
        result = []
        for k, vs in to_key_val_list(data):
            if isinstance(vs, basestring) or not hasattr(vs, '__iter__'):
                vs = [vs]
            for v in vs:
                if v is not None:
                    result.append(
                        (k.encode('utf-8') if isinstance(k, unicode) else k,
                         v.encode('utf-8') if isinstance(v, unicode) else v))
        return urllib.parse.urlencode(result, doseq=True)
    else:
        return data

def to_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,

    ::

        >>> to_key_val_list([('key', 'val')])
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
        [('key', 'val')]
        >>> to_key_val_list('string')
        ValueError: cannot encode objects that are not 2-tuples.
    """
    if value is None:
        return None

    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')

    if isinstance(value, collections.Mapping):
        value = value.items()

    return list(value)

class ThreadFetch(threading.Thread):

    def __init__(self, fetch_funcs, success_funcs=None, fail_funcs=None):
        super(ThreadFetch, self).__init__()
        self.setDaemon(True)
        self.fetch_funcs = fetch_funcs
        self.success_funcs = success_funcs
        self.fail_funcs = fail_funcs

    def run(self):
        result = self.fetch_funcs[0](*self.fetch_funcs[1])
        if self.success_funcs:
            self.success_funcs[0](result, *self.success_funcs[1])

def save_db(objs, fn):
    '''Save object to db file.'''
    try:
        f = open(fn + ".tmp", "wb")
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        pickle.dump(objs, f, -1)
        f.close()
        os.rename(fn + ".tmp", fn)
    except Exception as e:
        print("[Error] save_db:", e)
        traceback.print_exc(file=sys.stdout)

def load_db(fn):
    '''Load object from db file.'''
    objs = None
    if os.path.exists(fn):
        f = open(fn, "rb")
        try:
            objs = pickle.load(f)
        except:
            try:
                shutil.copy(fn, fn + ".not-valid")
            except: pass
            objs = None
        f.close()
    return objs


