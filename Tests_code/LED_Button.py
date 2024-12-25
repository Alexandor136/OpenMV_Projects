import pyb
import time


# Инициализируем кнопку на контакте P4 как вход
button = pyb.Pin('P4', pyb.Pin.IN)

# Инициализируем встроенный светодиод
led = pyb.LED(3)


while True:

    # Проверяем, нажата ли кнопка
    if button.value() == 1:
        # Включаем светодиод
        print(button.value())
        led.on()
    else:
        # Выключаем светодиод
        print(button.value())
        led.off()
    # Ожидание
    time.sleep(0.01)
