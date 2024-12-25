# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Single Color Grayscale Blob Tracking Example
#
# This example shows off single color grayscale tracking using the OpenMV Cam.

import sensor
import time
import math

# Color Tracking Thresholds (Grayscale Min, Grayscale Max)
# The below grayscale threshold is set to only find extremely bright white areas.
thresholds = (254, 255)
cnt = 0

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
# must be turned off for color tracking
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)  # must be turned off for color tracking
clock = time.clock()
gain = 20

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

while True:
    clock.tick()
    img = sensor.snapshot()
    cnt = 0
    for blob in img.find_blobs(
        [thresholds], pixels_threshold=100, area_threshold=100, merge=True
    ):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=0)
            img.draw_line(blob.major_axis_line(), color=0)
            img.draw_line(blob.minor_axis_line(), color=0)
        # These values are stable all the time.
        img.draw_rectangle(blob.rect(), color=127)
        img.draw_cross(blob.cx(), blob.cy(), color=127)
        # Note - the blob rotation is unique to 0-180 only.
        img.draw_keypoints(
            [(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))],
            size=40,
            color=127,
        )
        cnt = cnt + 1
    if cnt > 1:
        gain = gain - 0.05
        sensor.set_auto_gain(False, gain_db=gain)
    if cnt < 1:
        gain = gain + 0.05
        sensor.set_auto_gain(False, gain_db=gain)

    print(clock.fps(), cnt, gain, sensor.get_gain_db())
