import sensor
import time
import math

# Пороги для обнаружения blob-ов
thresholds = (250, 255)

# Инициализация переменных
cnt = 0
max_blob_area = 0
max_blob = None

# Настройка камеры
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time=2000)

# Выключение автоматической настройки усиления и белого баланса
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

# Инициализация таймера
clock = time.clock()

# Начальное значение усиления
gain = 1

# Минимальный порог площади для регулирования усиления
min_area_threshold = 5000

# Максимальная площадь blob-а (50% от площади изображения)
max_blob_area_limit = int((sensor.width() * sensor.height()) * 0.5)

while True:
    # Обновление таймера
    clock.tick()

    # Захват изображения
    img = sensor.snapshot()

    # Применение порога яркости для получения бинарного изображения
    img = img.binary([thresholds])

    # Обнуление счетчика blob-ов
    cnt = 0

    # Обнуление максимальной площади blob-а
    max_blob_area = 0

    # Обнуление максимального blob-а
    max_blob = None

    # Обнаружение blob-ов
    for blob in img.find_blobs(
        [thresholds], pixels_threshold=1000, area_threshold=10000, merge=True
    ):
        # Увеличение счетчика blob-ов
        cnt += 1

        # Обновление максимальной площади blob-а
        if blob.area() > max_blob_area and blob.area() < max_blob_area_limit:
            max_blob_area = blob.area()
            max_blob = blob

        # Рисование контура blob-а
        img.draw_rectangle(blob.rect(), color=127)

        # Рисование центра blob-а
        img.draw_cross(blob.cx(), blob.cy(), color=127)

        # Рисование осей blob-а
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=0)
            img.draw_line(blob.major_axis_line(), color=0)
            img.draw_line(blob.minor_axis_line(), color=0)

        # Рисование ключевых точек blob-а
        img.draw_keypoints(
            [(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))],
            size=40,
            color=127,
        )

    # Рисование максимального blob-а
    if max_blob:
        img.draw_rectangle(max_blob.rect(), color=255)

    # Регулирование усиления
    if cnt > 1 and max_blob_area_limit > min_area_threshold:
        gain -= 0.02
        sensor.set_auto_gain(False, gain_db=gain)
    elif cnt < 1 and max_blob_area < min_area_threshold:
        gain += 0.02
        sensor.set_auto_gain(False, gain_db=gain)

    # Вывод информации
    print(clock.fps(), cnt, gain, sensor.get_gain_db(), max_blob_area_limit)
