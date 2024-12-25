import sensor, image, time, tv, pyb

## DEF ##
def Detecting_Object(img, min_area_object = 2000):
'''
    # Нахождение blob'ов (непрерывных областей) в бинарном изображении
    blobs = binary_img.find_blobs([threshold], area_threshold = min_area_object)

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

        # Отображение кадра на дисплее (если он подключен)
        img.draw_string(0, 5, "Max size: {}x{}".format(w, h), color=(255, 255, 0), scale=2)
        img.draw_string(0, 30, "FPS: {}".format(clock.fps()), color=(255, 255, 0), scale=2)

    else:
        # Сообщаем об отсутствии белых объектов в кадре
        print("Белых объектов не найдено.")

    return binary_img
    '''


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
    return img, sensor.get_gain_db()

def Setting_Cam():

    # Настройка камеры
    sensor.reset()
    sensor.set_pixformat(sensor.GRAYSCALE)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_auto_gain(False)  # must be turned off for color tracking
    sensor.set_auto_whitebal(False)  # must be turned off for color tracking
    sensor.set_auto_exposure(False)
    sensor.set_framerate(24)
    #sensor.set_gainceiling(8)
    sensor.skip_frames(time = 2000)


def Init_Device():
    # Инициализируем кнопку на контакте P0 как вход
    button = pyb.Pin('P0', pyb.Pin.IN, pyb.Pin.PULL_UP)
    # Инициализируем встроенный светодиод
    led = pyb.LED(3)
    # Инициализируем LCD-экран
    tv.init()

def Background(R=0, G=0, B=0):
    # Заполняем весь экран черным цветом
    frame.draw_rectangle(0, 0, frame.width(), frame.height(), fill=True, color=(R, G, B))

def PText (text, x, y):
    #Текст
    frame.draw_string(x, y, text, color=(255, 255, 0), scale=2, mono_space = False)


## DEF ##
#
#
#
## MAIN ##


# Иницилицация устройств
Init_Device()
# Начальные настройки камеры
Setting_Cam()

# Настройка порога яркости для белого цвета
threshold = (250, 255)

# Часы
clock = time.clock()

# Начальное значение усиления
gain = 1

# Минимальный порог площади для регулирования усиления
min_area_threshold = 5000

# Максимальная площадь blob-а (50% от площади изображения)
max_blob_area_limit = int((sensor.width() * sensor.height()) * 0.5)

while (True):
    # Снимок кадра
    frame = sensor.snapshot()

    # Фон
    Background()

    # Надпись
    PText("Hold the button for 5 sec \n   to enter setup mode", 70, 90)
    break

while (True):

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

    # Обноружение наибольшего белого объекта
    img_detection = Detecting_Object(img)

    print(clock.fps())

    # Выводим изображение на LCD-экран
    tv.display(img_detection)









