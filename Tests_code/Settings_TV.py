import sensor, tv, pyb

def Setting_Cam():

    # Настройка камеры
    sensor.reset()
    sensor.set_pixformat(sensor.GRAYSCALE)
    sensor.set_framesize(sensor.SIF)
    sensor.skip_frames(time=2000)


def Init_Device():
    # Инициализируем LCD-экран
    tv.init()
    # Инициализируем кнопку на контакте P0 как вход
    button = pyb.Pin('P0', pyb.Pin.IN, pyb.Pin.PULL_UP)
    # Инициализируем встроенный светодиод
    led = pyb.LED(3)

Init_Device()
Setting_Cam()

# Show image.
while(True):
    img = sensor.snapshot()
    tv.display(img)
