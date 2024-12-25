import sensor
import image
import time
import os
import pyb

# Инициализация камеры
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Установка формата изображения (RGB565)
sensor.set_framesize(sensor.QVGA)    # Установка размера изображения (QVGA)
sensor.skip_frames(time=2000)        # Задержка для настройки камеры

# Инициализация счетчика изображений
img_counter = 0

# Захват и сохранение изображения
while True:
    print(pyb.info)
