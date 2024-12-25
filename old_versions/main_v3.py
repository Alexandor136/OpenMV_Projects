import sensor
import image
import time
import tv
import pyb
import math

## DEF ##

def Detecting_Object(img, thresholds, max_blob_area_limit, max_blob_area, max_blob):
    # Обнаружение blob-ов
    for blob in img.find_blobs(
        [thresholds], pixels_threshold=2000, area_threshold=2000, merge=True):

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

    return max_blob, max_blob_area, cnt

def Set_Gain(gain, min_area_threshold, max_blob_area):

    max_blob_, max_blob_area_, cnt_ = Detecting_Object(img, thresholds, max_blob_area_limit,
                                                    max_blob_area, max_blob)

    # Регулирование усиления
    if cnt > 1 and max_blob_area > min_area_threshold:
        gain -= 0.05
        sensor.set_auto_gain(False, gain_db=gain)
    elif cnt < 1 and max_blob_area < min_area_threshold:
        gain += 0.05
        sensor.set_auto_gain(False, gain_db=gain)

    #print(cnt, gain, sensor.get_gain_db())
    if max_blob_ is not None:
        print('Уровень усиления найден!')

    return gain, max_blob_

def Final_Detecting_Object():

    max_blob = Detecting_Object(img, thresholds, max_blob_area_limit, max_blob_area, max_blob)

    # Вывод
    if max_blob:
        print('Белый объект обноружен!')
    else:
        print('Белый обект не был найден!')

def Set_Gain_Max(img, thresholds, max_blob_area_limit, max_blob_area, max_blob, min_area_threshold):
    # Начальное значение усиления
    gain = 50
    sensor.set_auto_gain(False, gain_db=gain)

    max_blob_, max_blob_area_, cnt_ = Detecting_Object(img, thresholds, max_blob_area_limit,
                                                       max_blob_area, max_blob)

    if max_blob_ == None:
        max_blob_, max_blob_area_, cnt_ = Detecting_Object(img, thresholds, max_blob_area_limit,
                                                           max_blob_area, max_blob)
    else:

        while True:
            # Обнаружение объектов с текущим значением усиления
            max_blob_, max_blob_area_, cnt_ = Detecting_Object(img, thresholds, max_blob_area_limit,
                                                           max_blob_area, max_blob)
            #print(max_blob_)

            # Если объекты не обнаружены, возвращаем текущее значение усиления
            if max_blob_ is None:
                print('Максимальный уровень усиления найден!', gain)
                return gain
            else:
                # Уменьшаем значение усиления
                gain -= 0.1
                sensor.set_auto_gain(False, gain_db=gain)
                sensor.snapshot()
                print (gain)

def Setting_Cam():

    # Настройка камеры
    sensor.reset()
    sensor.set_pixformat(sensor.GRAYSCALE)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_auto_gain(False)  # must be turned off for color tracking
    sensor.set_auto_whitebal(False)  # must be turned off for color tracking
    sensor.set_auto_exposure(False)
    sensor.set_framerate(40)
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
    img.draw_rectangle(0, 0, img.width(), img.height(), fill=True, color=(R, G, B))

def PText (text, x, y):
    #Текст
    img.draw_string(x, y, text, color=(255, 255, 0), scale=2, mono_space = False)


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
thresholds = (254, 255)
# Часы
clock = time.clock()

# Начальное значение усиления
gain = 1


# Минимальный порог площади для регулирования усиления
min_area_threshold = 2000
# Максимальная площадь blob-а (% от площади изображения)
max_blob_area_limit = int((sensor.width() * sensor.height()) * 2)
# Обнуление счетчика blob-ов
cnt = 0
# Обнуление максимальной площади blob-а
max_blob_area = 0
# Обнуление максимального blob-а
max_blob = None

while True:
    print(0)
    # Захват изображения
    img = sensor.snapshot()

    # Проверяем, нажата ли кнопка (т. е. низкий уровень на выводе)
    if button.value() == 0:
        print (1)
        # Запускаем таймер
        start_time = time.time()
        while button.value() == 0:
            print (2)
            # Подождите, пока кнопка будет отпущена или пройдет 5 секунд
            if time.time() - start_time >= 3:
                print("Button was pressed for 5 seconds!")
                # Режим настройки......
                print (3)
                # Фон
                Background()
                # Надпись
                PText("setup mode", 5, 5)
                # Надпись
                PText("1) Remove the detail from the frame \n2) hold the button for 3 seconds", 25, 90)
                img = sensor.snapshot()

                while True:
                    # Проверяем, нажата ли кнопка (т. е. низкий уровень на выводе)
                    if button.value() == 0:
                        # Запускаем таймер
                        start_time = time.time()
                        while button.value() == 0:
                            # Подождите, пока кнопка будет отпущена или пройдет 5 секунд
                            if time.time() - start_time >= 3:

                                print('Калибровка Max_Gain')

                                gain = Set_Gain_Max(img, thresholds, max_blob_area_limit,
                                                    max_blob_area, max_blob, min_area_threshold)
                                sensor.snapshot()
                                print (gain)






    else:

        # Применение порога яркости для получения бинарного изображения
        img = img.binary([thresholds])

        Detecting_Object(img, thresholds, max_blob_area_limit, max_blob_area, max_blob)

        print(5)

        # Инициализируем LCD-экран
        #tv.init()
        # Выводим изображение на LCD-экран
        #tv.display(img)










