import sensor
import image
import time
import tv
import pyb
import math
import os
import uio
import ustruct
import machine


## DEF ##

def Init_Device():
    # Инициализируем кнопку на контакте P4, P6 как вход
    button_4 = pyb.Pin('P4', pyb.Pin.IN, pyb.Pin.PULL_UP)
    button_5 = pyb.Pin('P5', pyb.Pin.IN, pyb.Pin.PULL_UP)
    button_6 = pyb.Pin('P6', pyb.Pin.IN, pyb.Pin.PULL_UP)

    # Инициализируем встроенный светодиод
    led = pyb.LED(3)
    return button_4, button_5, button_6, led

# Функция для включения и выключения реле
def control_relay(state):
    if state:
        relay_pin.high()  # Включаем реле
        print("Подан разрешающий сигнал!")
    else:
        relay_pin.low()   # Выключаем реле
        #print("Реле выключено")

def Save_Image_Sd(img, img_counter, path_s = "/images"):

    #Создает каталог, если он не существует, и записывает переменную в файл
    save_path = path_s
    try:
        os.mkdir(save_path)
    except OSError as e:
        if e.errno != 17:  # EEXIST
            print('EEXIST')
            raise

    # Формирование имени файла с счетчиком, датой и временем
    filename = "%s/%d_image.jpg" % (save_path, img_counter)

    # Сохранение изображения на SD-карту
    img.save(filename)
    print("Image saved:", filename)

def delete_oldest_photos(directory, max_photos):
    # Получаем список файлов в каталоге
    files = os.listdir(directory)

    # Проверяем количество файлов
    if len(files) > max_photos:
        # Сортируем файлы по имени (или по другому критерию, если нужно)
        files.sort()  # Сортировка по имени

        # Удаляем самые старые файлы, пока количество не станет допустимым
        while len(files) > max_photos:
            oldest_file = files.pop(0)  # Берем самый старый файл
            os.remove(directory + '/' + oldest_file)  # Удаляем файл
            print(f'Удален файл: {oldest_file}')

# Функция для загрузки изображения из внутренней памяти
def load_image_from_internal_memory(filename):
    try:
        img = image.Image(filename)
        return img

    except Exception as e:
        print("Ошибка загрузки изображения:", e)
        return None

def Write_Gain(gain):
    "Создает каталог, если он не существует, и записывает переменную в файл"
    file_path = "/flash/data.txt"
    dir_path = "/flash"
    try:
        os.mkdir(dir_path)
    except OSError as e:
        if e.errno != 17:  # EEXIST
            print('EEXIST')
            raise

    # Создаем файл для хранения переменной
    file = uio.open(file_path, "w")

    # Записываем значение переменной в файл
    file.write(str(gain))
    file.close()

def Read_Gain(file_path):
    "Читает переменную из файла"
    file = uio.open(file_path, "r")
    read_value = float(file.read())
    file.close()
    return read_value

def Detecting_Object(img, thresholds, max_blob_area, max_blob,
                     pixels_threshold_ = 1000, area_threshold_ = 1000):
    # Обнаружение blob-ов
    for blob in img.find_blobs(
        [thresholds], pixels_threshold=pixels_threshold_, area_threshold=area_threshold_, merge=True):

        # Обновление максимальной площади blob-а
        if blob.area() > max_blob_area:
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

def Final_Detecting_Object():

    def check_object_in_frame():

        start_time = time.time()  # Запоминаем время начала
        duration = 0.2  # 200 миллисекунд
        object_present = True  # Предполагаем, что объект присутствует

        while (time.time() - start_time) < duration:
            img = sensor.snapshot()  # Захватываем изображение с камеры
            tv.display(img) # Выводим изображение на экран

            max_blob_, _, __ = Detecting_Object(img, thresholds, max_blob_area, max_blob)

            if not max_blob_:  # Если объект не найден
                object_present = False  # Устанавливаем флаг в false
                if (time.time() - start_time) == duration:
                    break  # Выходим из цикла, так как объект появился

        return 1 if object_present else 0  # Возвращаем 1, если объект был в кадре все время, иначе 0

    start_time = time.time()  # Запоминаем время начала мониторинга
    error_start_time = time.time()  # Запоминаем время начала мониторинга аварии
    signal = 1  # Начальное значение сигнала
    img = switch_mod_img(img_binary_flag, thresholds)


    while (time.time() - start_time) < 5:
        result = check_object_in_frame()

        if result == 1:
            signal = 1
            if result == 0: # Ппроверака на появление объекта
                signal = 1 # Объект обноружен нет разрешающего сигнала
                break

        elif result == 0:
            signal = 0
            if result == 1: # Ппроверака на проподание объекта
                signal = 1 # Объект обноружен нет разрешающего сигнала
                break

        if (time.time() - start_time) == 1 and signal == 0:

            # Подать сигнал на реле
            control_relay(True)
            time.sleep(1)
            control_relay(False)
            print('relay')

            # Сохраняем изображение
            Save_Image_Sd(img, sensor_counter)
            break

        if (time.time() - start_time) > 4.9 and signal == 1:

            print("Объект обнаружен.")
            erorr = load_image_from_internal_memory("/img/error_1.jpg")
            tv.display(erorr)
            Save_Image_Sd(img, sensor_counter, "/images_error")
            pyb.delay(1000)

            while True:

                # Если нажата зелённая кнопка или поступили сигнал от термопласта
                if (button_4.value() == 1) or (button_5.value() == 0 and button_6.value() == 1):
                    break


def Set_Gain_Max(img, thresholds, max_blob_area, max_blob):
    # Начальное значение усиления
    gain = 100
    sensor.set_auto_gain(False, gain_db=gain)

    max_blob_, max_blob_area_, cnt_ = Detecting_Object(img, thresholds,
                                                       max_blob_area, max_blob, 10, 10)

    if max_blob_ == None:
        max_blob_, max_blob_area_, cnt_ = Detecting_Object(img, thresholds,
                                                           max_blob_area, max_blob, 10, 10)
    else:

        while True:

            # Обнаружение объектов с текущим значением усиления
            max_blob_, max_blob_area_, cnt_ = Detecting_Object(img, thresholds,
                                                           max_blob_area, max_blob, 300, 300)
            tv.display(img)

            # Если объекты не обнаружены, возвращаем текущее значение усиления
            if max_blob_ == None:
                print('Максимальный уровень усиления найден!', gain, max_blob_, 3.1)
                img.draw_string(5,5, "Gain: {}".format(gain),
                                color = (255,255,0), scale = 3, mono_space = False)
                return gain

            elif gain <= 0:

                error_detaction_img = load_image_from_internal_memory("/img/error_detaction.jpg")
                tv.display(error_detaction_img)
                print("Ошибка при настройке, gain меньше 0")

                return

            else:
                # Уменьшаем значение усиления
                gain -= 0.3
                sensor.set_auto_gain(False, gain_db=gain)
                sensor.skip_frames(4)
                img.draw_string(5,5, "Gain: {}".format(gain),
                                color = (255,255,0), scale = 3, mono_space = False)
                sensor.snapshot()


                print (gain, max_blob_, 3.2)


def Setting_Gain():

    calibration_mode = False
    print("Button was pressed for 5 seconds!")

    # Режим настройки
    #sensor.set_framerate(120)
    print (3)

    setup_mode_img = load_image_from_internal_memory("/img/setup_mode.jpg")
    tv.display(setup_mode_img)

    while True:
        if button_4.value() == 0:
            break
        time.sleep(0.01)

    print("Режим настройки")

    # Задержка перед следующей итерацией
    #pyb.delay(1000)

    img = sensor.snapshot()

    while True:

        # Проверяем, нажата ли кнопка (т. е. низкий уровень на выводе)
        if button_4.value() == 1:

            print('Калибровка Max_Gain')

            max_gain = Set_Gain_Max(img, thresholds,
                                max_blob_area, max_blob)

            sensor.snapshot()

            if max_gain is not None:
                print(max_gain, 'main')
                sensor.set_auto_gain(False, gain_db=max_gain)
                # Запись значения в память
                Write_Gain(max_gain)
                # Читаем значение переменной из файла
                sensor.set_auto_gain(False, gain_db=(Read_Gain("/flash/data.txt")))
                calibration_mode = True

            if calibration_mode:
                break

        else:
            if calibration_mode:
                break

def mod_button_4():
    global img_binary_flag

    start_time = None
    end_time = None

    if button_4.value() == 1:
        #print(1)
        start_time = time.time()

        while button_4.value() == 1:
            time.sleep(0.01)
            #print(2)

            # Проверка времени нажатия
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time >= 3.1:
                Setting_Gain()
                #print('Setting_Gain')
                break

            if button_4.value() == 0:
                end_time = time.time()
                #print(3)
                break

        # Проверка длительности нажатия после выхода из цикла
        if end_time is not None and end_time - start_time <= 3:
            img_binary_flag = not img_binary_flag


def switch_mod_img(img_binary_flag, thresholds):
    if img_binary_flag == True:
        img = sensor.snapshot()
        img = img.binary([thresholds])
        img.draw_string(5,5, "Gain: {}".format(sensor.get_gain_db()),
                        color = (255,255,0), scale = 3, mono_space = False)
        tv.display(img)
        return img

        print('mode_img_binary')
    else:
        img = sensor.snapshot()
        # Вывод значения усиления на изображение
        img.draw_string(5,5, "Gain: {}".format(sensor.get_gain_db()),
                        color = (255,255,0), scale = 3, mono_space = False)
        tv.display(img)
        return img



def Setting_Cam():

    # Настройка камеры
    sensor.reset()
    sensor.set_pixformat(sensor.GRAYSCALE)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_auto_gain(False)  # must be turned off for color tracking
    sensor.set_auto_whitebal(False)  # must be turned off for color tracking
    sensor.set_auto_exposure(False)
    #sensor.set_framerate(40)
    sensor.set_gainceiling(2)
    sensor.skip_frames(time = 2000)

    # Установка значения усиления из памяти
    sensor.set_auto_gain(False, gain_db=(Read_Gain("/flash/data.txt")))


## DEF ##
#
#
#
## MAIN ##


# Иницилицация устройств
button_4, button_5, button_6, led = Init_Device()
# Начальные настройки камеры
Setting_Cam()
# Настройка порога яркости для белого цвета
thresholds = (180, 255)
# Часы
clock = time.clock()
# Обнуление счетчика blob-ов
cnt = 0
# Обнуление максимальной площади blob-а
max_blob_area = 0
# Обнуление максимального blob-а
max_blob = None
# Счётчик срабатывания сенсора
sensor_counter = 0
# Время начала прошлего цикла
p_time = 0
# Настройка пина для управления реле
relay_pin = machine.Pin('P9', machine.Pin.OUT)
# Инициализируем LCD-экран
tv.init()
# Флаг для вывода бинарного изображения
img_binary_flag = False


while True:

    # Запоминаем время начала
    #start_time = time.ticks_ms()
    # Вычисляем время цикла
    #ticks_diff = start_time - p_time
    #p_time = time.ticks_ms()
    #print(ticks_diff)

    # Увеличение счёчика срабатывания сенсора
    sensor_counter += 1

    # Проверяем кнопку и тумблер (button_5 - тумблер, button_6 - выталкеватель закончил работу)
    if (button_5.value() == 0 and button_6.value() == 1):

        # Время задержки для выпадения детали
        time.sleep(1)

        # Вывод изображения
        switch_mod_img(img_binary_flag, thresholds)

        # Функция обноружения объекта
        Final_Detecting_Object()


        print(5)

    else:

        # Вывод изображения
        switch_mod_img(img_binary_flag, thresholds)
        # Ороботчик кнопки
        mod_button_4()

        print(6)
        #Очищение буфера
        delete_oldest_photos('/images', 100)

        #print(button_5.value(), button_6.value(), button_4.value())











