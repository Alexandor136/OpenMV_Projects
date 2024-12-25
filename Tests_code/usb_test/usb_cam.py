import sensor, image, pyb, ustruct

# Инициализация камеры
sensor.reset()                      # Сброс сенсора
sensor.set_pixformat(sensor.RGB565) # Установка формата пикселей
sensor.set_framesize(sensor.QVGA)   # Установка размера кадров
sensor.skip_frames(time = 2000)     # Пропуск кадров для настройки

# Инициализация USB
usb = pyb.USB_VCP() # Создание объекта для USB

while(True):
    img = sensor.snapshot() # Захват изображения

    # Преобразование изображения в байты
    img_bytes = img.compress(quality=90) # Сжатие изображения для уменьшения размера

    # Отправка размера изображения usb.send(ustruct.pack("<L", img_bytes.size()))

    # Отправка данных изображения usb.send(img_bytes)
