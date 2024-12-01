import fixed_world as world
import time


def memory_agent(robot):
    threshold = 1
    max_speed = 1
    turning_speed = 1
    memory = {"last_positions": [], "last_actions": [], "time_stuck": 0}
    stuck_threshold = 5  # Number of repeated actions to consider as "stuck"
    max_memory = 10  # Limit memory size for efficiency

    while robot:
        readings = world.getSensorReading()

        def move_back():
            mb = min(readings["back_left"], readings["back_right"])
            ms = readings["ba_right"] if mb == readings["back_left"] else readings["ba_left"]

            if mb > threshold and ms > threshold:
                if abs(mb - ms) < 0.1:  # Nearly equal distances
                    motor_speed = {"speedLeft": -turning_speed, "speedRight": -turning_speed}
                elif mb > ms:  # Favor the side with more distance
                    motor_speed = {"speedLeft": -turning_speed * 0.1, "speedRight": -turning_speed}
                else:
                    motor_speed = {"speedLeft": -turning_speed, "speedRight": -turning_speed * 0.1}

            elif mb > threshold:  # Primary back sensor detects space
                turn_adjust = 0.2 if mb > 1 else 0.5
                motor_speed = {"speedLeft": -turning_speed * turn_adjust, "speedRight": -turning_speed}

            elif ms > threshold:  # Secondary back sensor detects space
                turn_adjust = 0.2 if ms > 1 else 0.5
                motor_speed = {"speedLeft": -turning_speed, "speedRight": -turning_speed * turn_adjust}

            else:  # Default backup behavior
                motor_speed = {"speedLeft": turning_speed, "speedRight": -turning_speed}

            return motor_speed

        # Determine motor speeds based on sensor readings
        mf = min(readings["front_left"], readings["front_right"])
        sf = readings["fr_right"] if mf == readings["front_left"] else readings["fr_left"]

        if mf > threshold and sf > threshold:
            if readings["energy"]["direction"] > 0:
                motor_speed = {"speedLeft": max_speed, "speedRight": max_speed - 0.6}
            elif readings["energy"]["direction"] < 0:
                motor_speed = {"speedLeft": max_speed - 0.6, "speedRight": max_speed}
            else:
                motor_speed = {"speedLeft": max_speed, "speedRight": max_speed}
        elif mf > threshold:
            turn_adjust = 0.2 if mf > 1 else 0.5
            if mf == readings["front_left"]:
                motor_speed = {"speedLeft": turning_speed - turn_adjust, "speedRight": turning_speed}
            else:
                motor_speed = {"speedLeft": turning_speed, "speedRight": turning_speed - turn_adjust}
        elif sf > threshold:
            turn_adjust = 0.2 if sf > 1 else 0.5
            if sf == readings["fr_right"]:
                motor_speed = {"speedLeft": turning_speed, "speedRight": turning_speed - turn_adjust}
            else:
                motor_speed = {"speedLeft": turning_speed - turn_adjust, "speedRight": turning_speed}
        else:
            motor_speed = move_back()



        # Execute motor speeds and handle collection
        world.setMotorSpeeds(motor_speed)

        collect = world.collectNearestBlock()
        if collect == "Energy collected :)":
            memory["time_stuck"] = 0
            print(collect)
        time.sleep(0.05)


robot = world.init()
memory_agent(robot)
