#!/usr/bin/env python3

# Copyright 2017 Piotr Czajka <piotr_czajka@protonmail.com>
# Author: Piotr Czajka <piotr_czajka@protonmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


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
