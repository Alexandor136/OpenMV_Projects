import os
import uio

# Создаем каталог для хранения переменной, если он не существует
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
variable_value = 123
file.write(str(variable_value))
file.close()

# Читаем значение переменной из файла
file = uio.open(file_path, "r")
read_value = int(file.read())
print("Read value:", read_value)
file.close()
