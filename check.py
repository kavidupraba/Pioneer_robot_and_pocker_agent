import random
import Lab1_Agents_Task1_World as World

def memory_agent(robot):
    memory = []
    stuck_counter = 0  # To track if the agent is stuck
    max_stuck_time = 3000  # Define threshold time before changing strategy

    while robot:
        # Get sensor readings
        ultra_left = World.getSensorReading("ultraSonicSensorLeft")
        ultra_right = World.getSensorReading("ultraSonicSensorRight")
        energy_sensor_data = World.getSensorReading("energySensor")  # This will be an EasyDict

        # Extract the actual distance value from the energy sensor data
        energy_distance = energy_sensor_data['distance']  # Access the 'distance' value from the EasyDict

        # Store sensor readings and action taken in memory
        memory.append((ultra_left, ultra_right, energy_distance))

        # If agent is stuck for too long, change strategy
        if stuck_counter > max_stuck_time:
            print("Agent seems stuck. Changing strategy.")
            motor_speed = {'speedLeft': 2, 'speedRight': -2}  # Try turning
            stuck_counter = 0  # Reset stuck counter
        else:
            # Regular decision-making: Move forward if no obstacles
            if ultra_left >= 1.0 and ultra_right >= 1.0:
                motor_speed = {'speedLeft': 1, 'speedRight': 1}
            else:
                # If there's an obstacle, adjust direction
                motor_speed = {'speedLeft': -1, 'speedRight': 1}  # Turn right to avoid wall

            stuck_counter += 1  # Increment stuck counter as long as it’s moving

        # Check if energy block is within range
        if energy_distance < 0.5:  # If within 0.5 meters of the energy block
            print("Energy block nearby. Trying to collect...")
            collection_result = World.collectNearestBlock()  # Attempt to collect block
            if collection_result:
                print("Energy block collected!")
            else:
                print("Failed to collect the block. Keep trying!")

        # Set motor speeds
        World.setMotorSpeeds(motor_speed)

        # Optional: print information for debugging
        simulationTime = World.getSimulationTime()
        if simulationTime % 1000 == 0:
            print("Time:", simulationTime, "Left Sensor:", ultra_left, "Right Sensor:", ultra_right)


# Initialize robot and run memory agent
robot = World.init()
memory_agent(robot)
