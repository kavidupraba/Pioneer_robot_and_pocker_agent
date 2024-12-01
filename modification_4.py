import fixed_world as world
import time

def reflex_agent(robot):
    while robot:
        max_speed = 1
        readings = world.getSensorReading()
        threshold = 0.3  # Obstacle threshold for safety

        def proportional_speed(reading, max_speed):
            """Scale speed based on proximity to an obstacle."""
            if reading > threshold:
                return max_speed * min(1, reading / 1.5)  # Scale down smoothly
            else:
                return 0  # Stop if too close

        def move_toward_energy():
            """Adjust motor speeds to move toward the energy source."""
            direction = readings["energy"]["direction"]
            if direction > 0:  # Energy to the right
                speed_left = max_speed
                speed_right = max_speed * (1 - abs(direction))  # Adjust right motor
            elif direction < 0:  # Energy to the left
                speed_left = max_speed * (1 - abs(direction))  # Adjust left motor
                speed_right = max_speed
            else:  # Energy straight ahead
                speed_left = max_speed
                speed_right = max_speed
            return {"speedLeft": speed_left, "speedRight": speed_right}

        # Smooth movement logic
        if readings["front_left"] > threshold+0.7 and readings["front_right"] > threshold+0.7:
            motor_speed = move_toward_energy()
        else:
            # Slow down proportionally when obstacles are close
            speed_left = proportional_speed(readings["front_left"], max_speed)
            speed_right = proportional_speed(readings["front_right"], max_speed)
            if speed_left == 0 or speed_right == 0:
                # Turn back or adjust when blocked
                motor_speed = {"speedLeft": -max_speed * 0.5, "speedRight": -max_speed * 0.5}
            else:
                motor_speed = {"speedLeft": speed_left, "speedRight": speed_right}

        # Set motor speeds dynamically
        world.setMotorSpeeds(motor_speed)
        if world.collectNearestBlock() == "Energy collected :)":
            print("Energy collected!")

        # Add a small delay to simulate continuous polling
        time.sleep(0.05)


robot = world.init()
reflex_agent(robot)
