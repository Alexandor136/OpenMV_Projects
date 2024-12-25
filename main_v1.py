import sensor
import image
import time
import tv
import pyb
import math

## DEF ##

def Detecting_Object(img, thresholds, gain, min_area_threshold, max_blob_area_limit,
                     cnt, max_blob_area, max_blob):

    # Обнаружение blob-ов
    for blob in img.find_blobs(
        [thresholds], pixels_threshold=2000, area_threshold=2000, merge=True):
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
        print('Белый объект обноружен!')

    # Регулирование усиления
    if cnt > 1 and max_blob_area > min_area_threshold:
        gain -= 0.05
        sensor.set_auto_gain(False, gain_db=gain)
    elif cnt < 1 and max_blob_area < min_area_threshold:
        gain += 0.05
        sensor.set_auto_gain(False, gain_db=gain)

    print(cnt, gain, sensor.get_gain_db())

    return img, gain, max_blob


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

    return button, led

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
button, led = Init_Device()
# Начальные настройки камеры
Setting_Cam()

# Настройка порога яркости для белого цвета
thresholds = (255, 255)
# Часы
clock = time.clock()

# Начальное значение усиления
gain = 1
# Минимальный порог площади для регулирования усиления
min_area_threshold = 2000
# Максимальная площадь blob-а (% от площади изображения)
max_blob_area_limit = int((sensor.width() * sensor.height()) * 0.2)
# Обнуление счетчика blob-ов
cnt = 0
# Обнуление максимальной площади blob-а
max_blob_area = 0
# Обнуление максимального blob-а
max_blob = None

while (True):
    # Снимок кадра
    frame = sensor.snapshot()

    # Фон
    Background()

    # Надпись
    PText("Hold the button for 5 sec \n   to enter setup mode", 70, 90)

    # Проверяем, нажата ли кнопка (т. е. низкий уровень на выводе)
    if button.value() == 0:
        # Запускаем таймер
        start_time = time.time()
        while button.value() == 0:
            # Подождите, пока кнопка будет отпущена или пройдет 5 секунд
            if time.time() - start_time >= 1:
                print("Button was pressed for 5 seconds!")
                # Обноружение наибольшего белого объекта
                while (True):
                    img_detection, gain, blob = Detecting_Object(frame, thresholds, gain,
                                                          min_area_threshold, max_blob_area_limit,
                                                          cnt, max_blob_area, max_blob)
                    sensor.snapshot()
                    print(clock.fps(), gain, blob, 1)

                    if blob != None:
                        break
        break

while (True):

    # Обновление таймера
    clock.tick()
    # Захват изображения
    img = sensor.snapshot()
    # Применение порога яркости для получения бинарного изображения
    img = img.binary([thresholds])

    # Обноружение наибольшего белого объекта
    img_detection, gain, blob= Detecting_Object(img, thresholds, gain, min_area_threshold, max_blob_area_limit,
                                     cnt, max_blob_area, max_blob)

    print(clock.fps(), gain, 2)

    # Инициализируем LCD-экран
    tv.init()
    # Выводим изображение на LCD-экран
    tv.display(img_detection)









