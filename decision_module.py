from yolo_predict import YoloWorldModel
from enum import Enum
import math
from output import press, long_press
from time import sleep, process_time


class TramState(Enum):
    move = 1
    fast_stop = 2
    stoplight_wait = 3
    fast_move = 4
    boarding = 5
    boarding_stop = 6


prev_model = None
prev_state = TramState.move
moving_timer = process_time()
stop_timer = process_time()


# определяет на основе новых данных о мире, что должен делать трамвай и возвращает состояние
def make_decision(new_model: YoloWorldModel, speed: float):
    global prev_model, prev_state, moving_timer, stop_timer
    tram_state = prev_state

    def end_make_decision():
        global prev_model, prev_state
        prev_model = new_model
        prev_state = tram_state
        return tram_state

    def check_obstacles():
        for obstacle in new_model.obstacles:
            range_to_obstacle = math.sqrt(
                obstacle.x * obstacle.x + obstacle.y * obstacle.y
            )
            if abs(obstacle.x) <= 0.3 and range_to_obstacle <= 0.9:
                return True
        return False

    def calculate_near_object_count():
        count = 0
        for obstacle in new_model.obstacles:
            range_to_obstacle = math.sqrt(
                obstacle.x * obstacle.x + obstacle.y * obstacle.y
            )
            if range_to_obstacle <= 10:
                count += 1
        return count

    now_time = process_time()
    # если трамвай ехал
    if prev_state == TramState.move or prev_state == TramState.fast_move:
        if check_obstacles():
            tram_state = TramState.fast_stop
        # и увидел кружок остановки
        elif new_model.range_to_stop != None:
            tram_state = TramState.boarding_stop
            stop_timer = process_time()
        # и увидел светофор с сигналом остановки
        elif new_model.range_to_stoplight != None and not new_model.stoplight_signal:
            tram_state = TramState.stoplight_wait
            stop_timer = process_time()
        # и рядом мало объектов и трамвай едет несколько секунд
        elif now_time - moving_timer >= 5.0:
            tram_state = TramState.fast_move
        else:
            tram_state = TramState.move
    # если трамвай останавливался перед остановкой
    elif prev_state == TramState.boarding_stop:
        # и перестал видеть знак остановки, когда тот был близко
        if (
            prev_model.range_to_stop != None
            and prev_model.range_to_stop <= 5.0
            and new_model.range_to_stop == None
        ):
            tram_state = TramState.boarding
        # и трамвай уж больно долго ждёт окончания остановки
        elif now_time - stop_timer > 5:
            tram_state = TramState.move
    # если трамвай ждёт светофор
    elif prev_state == TramState.stoplight_wait:
        # и видит разрешающий сигнал на светофоре
        if (
            new_model.range_to_stoplight != None
            and new_model.stoplight_signal
            and prev_model.range_to_stoplight != None
            and prev_model.stoplight_signal
        ):
            tram_state = TramState.move
        # и потерял светофор на долгое время
        elif (
            new_model.range_to_stoplight == None
            and prev_model.range_to_stoplight == None
            and now_time - stop_timer > 5
        ):
            tram_state = TramState.move
        # и увидел кружочек остановки
        elif new_model.range_to_stop != None:
            tram_state = TramState.boarding_stop
            stop_timer = process_time()
    # если трамвай на посадке
    elif prev_state == TramState.boarding:
        # так как это состояние скриптованное, то в следующем кадре мы сразу знаем, что посадка завершилась
        tram_state = TramState.move
    # если трамвай резко остановился и больше этого не требуется
    elif prev_state == TramState.fast_stop:
        if check_obstacles():
            tram_state = TramState.fast_stop
        elif speed == 0:
            tram_state = TramState.move

    if (
        tram_state != TramState.move
        and tram_state != TramState.fast_move
        or calculate_near_object_count() >= 3
    ):
        moving_timer = process_time()

    return end_make_decision()


def implementation_of_decision(state, speed, acceleration):
    max_acceleration = 100
    stop_move_speed = 3
    lower_move_speed = 10
    upper_move_speed = 15

    if state == TramState.move or state == TramState.fast_move:
        if state == TramState.fast_move:
            speed /= 2
        if lower_move_speed <= speed <= upper_move_speed:
            if speed <= (upper_move_speed + lower_move_speed) / 2:
                if acceleration > max_acceleration / 3:
                    long_press("y")
            else:
                press("a")
        elif lower_move_speed > speed and acceleration < max_acceleration:
            long_press("q")
        elif speed > upper_move_speed:
            long_press("y")
    elif state == TramState.boarding_stop:
        if acceleration > 0:
            press("a")
        if stop_move_speed <= speed:
            long_press("y")
        else:
            press("a")
            # TODO акселерацию другую прикрутить, с минусом
    elif state == TramState.stoplight_wait:
        if speed > 0:
            long_press("y")
        else:
            press("a")
    elif state == TramState.boarding:
        press("a")
        if speed > 0:
            long_press("y", 1)
            sleep(3)
        press("p")
        sleep(15)
        press("l")
        sleep(3)
        press("a")
    elif state == TramState.fast_stop:
        long_press("x")
