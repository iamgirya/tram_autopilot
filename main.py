from time import sleep
import cv2
import yolo_predict
import output
import speed_from_memory
import decision_module
import tramsim_windows_capture


def main_loop():
    # 0. Инициализация
    model = yolo_predict.init_yolo()
    lock = tramsim_windows_capture.init_capture()
    output.init_output()
    output.set_up_camera()
    sleep(1)

    old_state = None
    while True:
        # 1. Сбор данных и получение модели
        lock.acquire()
        frameg = tramsim_windows_capture.get_frame()
        world_model, yolo_frame = yolo_predict.use_yolo_with_model(
            frameg, model, need_annotation=True
        )
        lock.release()
        speed_value = speed_from_memory.get_speed()
        acceleration_value = speed_from_memory.get_acceleration()

        cv2.imshow("yolo_frame", yolo_frame)
        # print("speed = " + str(speed_value))
        # print("acceleration = " + str(acceleration_value))

        if output.autopilot_work:
            # 2. Принятие решения
            state = decision_module.make_decision(world_model, speed_value)
            if old_state != state:
                print("state = " + str(state))
            old_state = state

            # 3. Реализация решения
            decision_module.implementation_of_decision(
                state, speed_value, acceleration_value
            )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


# Код
main_loop()
