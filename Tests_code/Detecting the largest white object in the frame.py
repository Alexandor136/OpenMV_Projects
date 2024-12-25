import sensor, image, time, tv

# Настройка камеры
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.SIF)
sensor.skip_frames(time=2000)

# Инициализируем LCD-экран
tv.init()

# Настройка порога яркости для белого цвета
threshold = (250, 255)

clock = time.clock() # fps

while True:
    clock.tick() # fps

    # Снимок кадра
    img = sensor.snapshot()

    # Применение порога яркости для получения бинарного изображения
    binary_img = img.binary([threshold])

    # Нахождение blob'ов (непрерывных областей) в бинарном изображении
    blobs = binary_img.find_blobs([threshold], area_threshold=2000)

    # Если найдены blob'ы, то находим наибольший по площади
    if blobs:
        max_blob = max(blobs, key=lambda b: b.pixels())
        x = max_blob[0]
        y = max_blob[1]
        w = max_blob[2]
        h = max_blob[3]

        # Рисуем прямоугольник вокруг наибольшего blob'а с зеленой границей толщиной 3 пикселя
        img.draw_rectangle([x, y, w, h], color=(0, 255, 0), thickness=3)

        # Сообщаем об обнаружении наибольшего белого объекта
        print("Наибольший белый объект найден! Размер: {}x{} пикселей".format(w, h))

        # Отображение кадра на дисплее (если он подключен) с цветными надписями
        #img.draw_string(0, 0, "White object detection", color=(255, 0, 0), scale=2)
        binary_img.draw_string(0, 5, "Max size: {}x{}".format(w, h), color=(255, 255, 0), scale=2)
        #img.draw_string(0, 60, "Threshold: {}".format(threshold), color=(0, 0, 255), scale=2)
        binary_img.draw_string(0, 30, "FPS: {}".format(clock.fps()), color=(255, 255, 0), scale=2)
        #img.draw_string(0, 120, "Resolution: {}x{}".format(img.width(), img.height()), color=(255, 0, 255), scale=2)

    else:
        # Сообщаем об отсутствии белых объектов в кадре
        print("Белых объектов не найдено.")

    # Выводим изображение на LCD-экран
    tv.display(img)


