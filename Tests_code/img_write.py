import sensor, image, pyb, tv

# Инициализируем камеру
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

# Инициализируем видеовыход
tv.init()

# Функция для загрузки изображения из внутренней памяти
def load_image_from_internal_memory(filename):
    try:
        img = image.Image(filename)
        return img
    except Exception as e:
        print("Ошибка загрузки изображения:", e)
        return None

# Основной цикл
while True:
    # Загружаем изображение из внутренней памяти
    img = load_image_from_internal_memory("/flash/img.jpg")

    if img:
        # Отображаем изображение на экране
        tv.display(img)
        sensor.snapshot(img)
    else:
        print("Не удалось загрузить изображение.")

    # Задержка перед следующей итерацией
    pyb.delay(1000)
