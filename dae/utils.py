#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

def get_parent_dir(filepath, level=1):
    '''Get parent directory with given return level.

    @param filepath: Filepath.
    @param level: Return level, default is 1
    @return: Return parent directory with given return level.
    '''
    parent_dir = os.path.realpath(filepath)

    while(level > 0):
        parent_dir = os.path.dirname(parent_dir)
        level -= 1

    return parent_dir

def get_conf():
    import  json
    import os
    with open('configuration.json', 'r') as f:
        conf = json.load(f)
    return conf
