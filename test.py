import threading
import numpy as np
import cv2

# Создание блокировки
lock = threading.Lock()


# Функция для получения изображения в дополнительном потоке
def get_image():
    # Получение изображения в виде numpy array
    image = cv2.imread("lol1.jpg")
    # Заблокировать блокировку
    lock.acquire()
    # Передать изображение основному потоку
    with open("lol1.jpg", "wb") as file:
        np.save(file, image)
    # Разблокировать блокировку
    lock.release()


# Создание и запуск дополнительного потока
image_thread = threading.Thread(target=get_image)
image_thread.start()

# Основной поток

# Ждать, пока дополнительный поток не завершится и передаст изображение
image_thread.join()
