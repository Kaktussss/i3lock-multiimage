#!/usr/bin/env python3

# Copyright (C) 2017  Piotr Czajka <piotr_czajka@protonmail.com>
# Author: Piotr Czajka <piotr_czajka@protonmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re
import subprocess
import os
import imghdr
from PIL import Image

FOLDER = '/home/ginkooo/soft/i3lock-multiimage'
IMAGE_FOLDER = 'images'


def get_monitor_resolutions():
    """calls xrandr and returns monitor resolutions in a tuple"""
    output = subprocess.check_output(['xrandr'])
    lines = [x.decode().strip() for x in output.splitlines()]
    connected_lines = [line for line in lines if
                       re.search('\sconnected\s', line)]

    res = []
    for line in connected_lines:
        match = re.search('\d+x\d+', line)
        res.append(match.group(0))
    str_res = tuple([x.split('x') for x in res])
    return [tuple([int(x), int(y)]) for x, y in str_res]


def asert_only_pngs():
    """raises exception if any file in IMAGE_FOLDER is not a png file"""
    for filename in os.listdir(IMAGE_FOLDER):
        ftype = imghdr.what(os.path.join(IMAGE_FOLDER, filename))
        if ftype != 'png':
            raise Exception('All files in image folder must be png format')


def crop_images_to_resolutions(resolutions):
    """takes monitor resolutions and resizes images to match themm

    :param resolutions: list of tuples, containing monitor resolutions

    :return ret: list of images
    """
    images = os.listdir(IMAGE_FOLDER)
    if len(images) != len(resolutions):
        raise Exception('There should be the same number of images,'
                        'as monitors')
    ret = []
    for image, resolution in zip(os.listdir(IMAGE_FOLDER), resolutions):
        f = Image.open(os.path.join(IMAGE_FOLDER, image))
        f = f.resize(resolution)
        ret.append(f)
    return ret


def get_fi_res(images):
    """Determines final image resolution

    :param images: list of images to be combined
    """
    return tuple([sum([image.size[0] for image in images]),
                 get_monitor_resolutions()[0][1]])


def combine_images(images):
    """Copies images into one final_image

    :param images: list of images to combine
    """
    final_image_resolution = get_fi_res(images)
    final_image = Image.new(images[0].mode, final_image_resolution)
    sum_ = 0
    for image in images:
        final_image.paste(image, (sum_, 0))
        sum_ += image.size[0]
    return final_image


def main():
    os.chdir(FOLDER)
    resolutions = get_monitor_resolutions()
    asert_only_pngs()
    images = crop_images_to_resolutions(resolutions)
    image = combine_images(images)
    for i in images:
        i.close()
    image.save('/tmp/background.png')
    image.close()
    subprocess.call('i3lock -i /tmp/background.png', shell=True)


if __name__ == '__main__':
    main()
