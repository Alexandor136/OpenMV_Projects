import time
import pyb

# Инициализируем вывод P0 как вход с подтягивающим резистором
button = pyb.Pin('P0', pyb.Pin.IN, pyb.Pin.PULL_UP)
# Инициализируем встроенный светодиод
led = pyb.LED(3)

while True:
    # Проверяем, нажата ли кнопка (т. е. низкий уровень на выводе)
    if button.value() == 0:
        # Запускаем таймер
        start_time = time.time()
        while button.value() == 0:
            # Подождите, пока кнопка будет отпущена или пройдет 5 секунд
            print (2)
            if time.time() - start_time >= 5:
                print("Button was pressed for 5 seconds!")

                break

