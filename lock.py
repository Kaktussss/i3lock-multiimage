#!/usr/bin/env python3

import PIL
import re
import subprocess
import os

IMAGE_FOLDER = 'images'


def get_monitor_resolutions():
    """calls xrandr and returns monitor resolutions in a tuple"""
    output = subprocess.check_output(['xrandr'])
    lines = [x.decode().strip() for x in output.splitlines()]
    connected_lines = [line for line in lines if
                       re.search('\sconnected\s', line)]

    ret = []
    for line in connected_lines:
        match = re.search('\d+x\d+', line)
        ret.append(match.group(0))
    return tuple(ret)



def main():
    resolutions = get_monitor_resolutions()

if __name__ == '__main__':
    main()
