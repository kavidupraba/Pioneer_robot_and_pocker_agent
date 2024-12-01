from check1_world import  *

def sequnce_agent(robot):
    stuck_counter = 0  # To track if the agent is stuck
    max_stuck_time = 3000  # Define threshold time before changing strategy

    while robot:
        # Get sensor readings
        ultra_left = getSensorReading("ultraSonicSensorLeft")
        ultra_right = getSensorReading("ultraSonicSensorRight")



        # If agent is stuck for too long, change strategy
        if stuck_counter > max_stuck_time:
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
                # Default turning if both sensors are close to obstacles
                motor_speed = {'speedLeft': -1, 'speedRight': 1}  # Turn to avoid hitting walls

            stuck_counter += 1  # Increment stuck counter as long as it’s moving

        # Set motor speeds
        setMotorSpeeds(motor_speed)

        # Optional: Print information for debugging
        simulationTime = getSimulationTime()
        if simulationTime % 1000 == 0:
            print("Time:", simulationTime, "Left Sensor:", ultra_left, "Right Sensor:", ultra_right)

        # Attempt to collect nearest block if in range and path is clear
        collect_result = collectNearestBlock()
        print(collect_result)  # For debugging, print result of collection attempt

# Initialize robot and run memory agent
robot = init()
sequnce_agent(robot)