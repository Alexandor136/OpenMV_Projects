import serial
import struct
import time

# Открытие USB-порта
ser = serial.Serial('COM4', baudrate=115200, timeout=1) 

while True:
    # Чтение размера изображения 
    size_data = ser.read(4)
    if len(size_data) != 4:
        continue

    size = struct.unpack("<L", size_data)[0]

    # Чтение изображения
    img_data = ser.read(size)
    if len(img_data) != size:
        continue

    # Сохранение изображения в файл
    with open("image.jpg", "wb") as img_file:
        img_file.write(img_data)
        time.sleep(1)

    print("Image saved!")
