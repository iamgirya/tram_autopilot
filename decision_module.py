from yolo_predict import YoloWorldModel
from enum import Enum
import math


# есть состояния: ехать (стандартное), резко_остановиться(когда детектим проблему),
# остановка(замедняем движение вперёд, чекаем светофоры или стопкружки), посадка (остановка, скрипт с посадкой в транспорт),
# ждать (смотрим на светофор и ждём разрешающего)
class TramState(Enum):
    move = 1
    stop = 2
    fast_stop = 3
    wait = 4
    boarding = 5


prev_model = None
prev_state = TramState.move


# определяет на основе новых данных о мире, что должен делать трамвай и возвращает состояние
def make_decision(new_model: YoloWorldModel, speed: float):
    global prev_model, prev_state
    tram_state = prev_state

    def end_make_decision():
        global prev_model, prev_state
        prev_model = new_model
        prev_state = tram_state
        return tram_state

    # Чекаем, нужно ли резко остановиться
    if len(new_model.obstacles) != 0 and (
        prev_state == TramState.move or prev_state == TramState.fast_stop
    ):
        for obstacle in new_model.obstacles:
            range_to_obstacle = math.sqrt(
                obstacle.x * obstacle.x + obstacle.y * obstacle.y
            )
            if abs(obstacle.x) <= 1 and range_to_obstacle <= 1.5:
                tram_state = TramState.fast_stop
                return end_make_decision()

    # если трамвай ехал
    if prev_state == TramState.move:
        # и увидел кружок остановки
        if new_model.range_to_stop != None:
            tram_state = TramState.stop
        # и увидел светофор с сигналом остановки
        if new_model.range_to_stoplight != None and new_model.stoplight_signal:
            tram_state = TramState.stop
    # если трамвай останавливался
    elif prev_state == TramState.stop:
        # и перестал видеть знак остановки
        if prev_model.range_to_stop != None and new_model.range_to_stop == None:
            tram_state = TramState.boarding
        # и успел остановиться
        if speed <= 1:
            tram_state = TramState.wait
    # если трамвай ждёт
    elif prev_state == TramState.wait:
        # и перестал видеть знак остановки на светофоре
        if not new_model.stoplight_signal:
            tram_state = TramState.move
    # если трамвай на посадке
    elif prev_state == TramState.boarding:
        # так как это состояние скриптованное, то в следующем кадре мы сразу знаем, что посадка завершилась
        tram_state = TramState.wait
    # если трамвай резко остановился и больше этого не требуется
    elif prev_state == TramState.fast_stop:
        tram_state = TramState.wait

    return end_make_decision()
