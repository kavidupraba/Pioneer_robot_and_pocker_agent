import fixed_world as world
import time

def reflex_agent(robot):
    max_attempts = 3  # Maximum attempts to collect energy before fallback
    attempt_duration = 20  # Time in seconds for each attempt
    wander_time = 10  # Time in seconds to wander if all attempts fail

    attempts = 0  # Track failed attempts
    start_time = time.time()  # Track time spent on the current attempt

    while robot:
        max_speed = 1
        readings = world.getSensorReading()
        threshold = 1

        # Helper function: Move back to avoid obstacles
        def move_back():
            readings = world.getSensorReading()
            if readings["back_left"] > threshold and readings["back_right"] > threshold:
                if readings["ba_left"] > threshold and readings["ba_right"] > threshold:
                    motor_speed = {"speedLeft": -1, "speedRight": -1}
                elif readings["ba_left"] > threshold:
                    motor_speed = {"speedLeft": -1 * 0.8, "speedRight": -1}
                elif readings["ba_right"] > threshold:
                    motor_speed = {"speedLeft": -1, "speedRight": -1 * 0.8}
                else:
                    motor_speed = {"speedLeft": 1, "speedRight": -1}
            elif readings["back_left"] > threshold and readings["ba_left"] > threshold:
                motor_speed = {"speedLeft": -1 * 0.8, "speedRight": -1}
            elif readings["back_right"] > threshold and readings["ba_right"] > threshold:
                motor_speed = {"speedLeft": -1, "speedRight": -1 * 0.8}
            else:
                motor_speed = {"speedLeft": 1, "speedRight": -1}
            return motor_speed

        # Adjust speed based on proximity to target
        if readings["energy"]["distance"] < 0.5:
            speed_factor = 0.3
        elif readings["energy"]["distance"] < 0.3:
            speed_factor = 0.6
        else:
            speed_factor = 1

        max_speed = max_speed * speed_factor

        # Navigate towards energy source
        if readings["energy"]["direction"]:
            if min(readings["front_left"], readings["front_right"]) > 0.5:
                if readings["energy"]["direction"] > 0:
                    if readings["fr_right"] > 0.5:
                        motor_speed = {"speedLeft": max_speed, "speedRight": max_speed - 0.7}
                    else:
                        motor_speed = move_back()
                elif readings["energy"]["direction"] < 0:
                    if readings["fr_left"] > 0.5:
                        motor_speed = {"speedLeft": max_speed - 0.7, "speedRight": max_speed}
                    else:
                        motor_speed = move_back()
                else:
                    motor_speed = {"speedLeft": max_speed, "speedRight": max_speed}
            else:
                motor_speed = move_back()
        else:
            world.STOP()

        # Execute movement
        world.execute(motor_speed, 6000, -1)

        # Attempt to collect energy
        collect = world.collectNearestBlock()
        if collect == "Energy collected :)":
            print(collect)
            attempts = 0  # Reset attempts after success
            start_time = time.time()  # Reset the timer for new attempt

        # Timeout logic
        if time.time() - start_time > attempt_duration:
            attempts += 1
            start_time = time.time()
            print(f"Attempt {attempts} failed. Trying fallback behavior...")

            # Fallback behavior
            if attempts >= max_attempts:
                print("All attempts failed. Wandering randomly...")
                wander_start = time.time()
                while time.time() - wander_start < wander_time:

                    motor_speed = {"speedLeft": max_speed * 0.5, "speedRight": max_speed * -0.5}
                    world.execute(motor_speed, 2000, -1)
                print("Resuming search...")
                attempts = 0

        #time.sleep(0.05)


robot = world.init()
reflex_agent(robot)
