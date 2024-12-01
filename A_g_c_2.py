import fixed_world as world

def reflex_agent(robot):
    threshold = 0.7
    turning_speed = 1
    max_speed = 2

    while robot:
        readings = world.getSensorReading()

        # Moving toward energy box
        def move_to_box():
            speed_factor = 1
            if readings["energy"]["distance"] < 0.5:
                speed_factor = 0.6
            elif readings["energy"]["distance"] < 0.3:
                speed_factor = 0.3

            adjusted_speed = max_speed * speed_factor
            if readings["energy"]["direction"] > 0:
                return {'speedLeft': adjusted_speed, 'speedRight': adjusted_speed - 0.5}
            elif readings["energy"]["direction"] < 0:
                return {'speedLeft': adjusted_speed - 0.5, 'speedRight': adjusted_speed}
            else:
                return {'speedLeft': adjusted_speed, 'speedRight': adjusted_speed}

        # Avoiding obstacles
        front_left = readings['front_left']
        front_right = readings['front_right']
        back_left = readings['back_left']
        back_right = readings['back_right']

        if front_left > threshold and front_right > threshold:
            # Path clear; move toward energy
            motor_speed = move_to_box()
        elif front_left > threshold:
            # Obstacle on the right; veer left
            motor_speed = {'speedLeft': max_speed - 1.5, 'speedRight': max_speed}
        elif front_right > threshold:
            # Obstacle on the left; veer right
            motor_speed = {'speedLeft': max_speed, 'speedRight': max_speed - 1.5}
        else:
            # Both sides blocked; reverse or turn
            if back_left > threshold and back_right > threshold:
                motor_speed = {'speedLeft': -turning_speed, 'speedRight': -turning_speed}
            else:
                motor_speed = {'speedLeft': turning_speed, 'speedRight': -turning_speed}

        # Debugging info
        print(f"Readings: {readings}")
        print(f"Motor speeds: {motor_speed}")

        # Set motor speeds
        world.setMotorSpeeds(motor_speed)

        # Attempt to collect energy
        collect = world.collectNearestBlock()
        if collect == "Energy collected :)":
            print(collect)

# Initialize robot and run agent
robot = world.init()
reflex_agent(robot)
