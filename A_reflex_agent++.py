from check1_world import *

def sequnce_agent(robot):
    stuck_counter = 0  # Track if the agent is stuck
    max_stuck_time = 3000  # Threshold time before changing strategy
    collect_distance_threshold = 0.5  # Distance within which to collect energy box

    while robot:
        # Get sensor readings
        ultra_left = getSensorReading("ultraSonicSensorLeft")
        ultra_right = getSensorReading("ultraSonicSensorRight")
        energy_info = getSensorReading("energySensor")  # Get energy box info

        # Navigate toward the energy box if it's detected
        if energy_info:
            distance_to_box = energy_info["distance"]
            direction_to_box = energy_info["direction"]

            if distance_to_box < collect_distance_threshold:
                # Close enough to collect the box
                collect_result = collectNearestBlock()
                print("Collected:", collect_result)
                motor_speed = {'speedLeft': 0, 'speedRight': 0}  # Stop after collecting
            else:
                # Adjust direction to face the energy box
                if direction_to_box > 0.1:  # Box is to the right
                    motor_speed = {'speedLeft': 1, 'speedRight': -1}  # Turn right
                elif direction_to_box < -0.1:  # Box is to the left
                    motor_speed = {'speedLeft': -1, 'speedRight': 1}  # Turn left
                else:
                    motor_speed = {'speedLeft': 1, 'speedRight': 1}  # Move forward towards the box

        # Obstacle avoidance or regular movement if no energy box nearby
        elif stuck_counter > max_stuck_time:
            print("Agent seems stuck. Changing strategy.")
            motor_speed = {'speedLeft': 2, 'speedRight': -2}  # Try turning
            stuck_counter = 0  # Reset stuck counter
        else:
            # Regular decision-making: Move forward if no obstacles
            if ultra_left >= 1.0 and ultra_right >= 1.0:
                motor_speed = {'speedLeft': 1, 'speedRight': 1}

            elif ultra_left < 1.0:  # Obstacle on the left
                motor_speed = {'speedLeft': 1, 'speedRight': -1}  # Turn right
            elif ultra_right < 1.0:  # Obstacle on the right
                motor_speed = {'speedLeft': -1, 'speedRight': 1}  # Turn left
            else:
                motor_speed = {'speedLeft': -1, 'speedRight': 1}  # Default turn

            stuck_counter += 1  # Increment stuck counter

        # Set motor speeds
        setMotorSpeeds(motor_speed)

        # Debugging info
        simulationTime = getSimulationTime()
        if simulationTime % 1000 == 0:
            print("Time:", simulationTime, "Left Sensor:", ultra_left, "Right Sensor:", ultra_right)

# Initialize robot and run sequence agent
robot = init()
sequnce_agent(robot)
