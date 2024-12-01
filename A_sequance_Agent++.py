from check1_world import *
import time

def sequence_agent(robot):
    collect_distance_threshold = 0.5  # Distance threshold to collect the box
    timeout_duration = 5  # Max time (in seconds) to reach a box before changing direction
    max_speed = 1.5  # Speed to approach the box
    turning_speed = 1.0  # Speed for turning towards box
    start_time = time.time()  # Track when the robot starts moving toward a box

    while robot:
        # Get energy box data
        energy_info = getSensorReading("energySensor")  # Dictionary containing box distance and direction

        if energy_info:
            distance_to_box = energy_info["distance"]
            direction_to_box = energy_info["direction"]

            # Check if timeout duration has been exceeded
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > timeout_duration:
                # Timeout reached; change strategy (e.g., reverse direction)
                print("Timeout reached, changing strategy.")
                motor_speed = {'speedLeft': -max_speed, 'speedRight': -max_speed}  # Move backward briefly
                start_time = time.time()  # Reset start time after changing direction
            else:
                # Turn towards the box based on its direction
                if abs(direction_to_box) > 0.1:
                    if direction_to_box > 0:
                        motor_speed = {'speedLeft': turning_speed, 'speedRight': -turning_speed}  # Turn right
                    else:
                        motor_speed = {'speedLeft': -turning_speed, 'speedRight': turning_speed}  # Turn left
                else:
                    # If aligned, move towards the box
                    motor_speed = {'speedLeft': max_speed, 'speedRight': max_speed}

                # Attempt to collect box if within the collection distance
                if distance_to_box < collect_distance_threshold:
                    collect_result = collectNearestBlock()
                    print("Collected:", collect_result)
                    start_time = time.time()  # Reset start time after collection

        else:
            # No box detected; idle or could initiate a searching behavior
            motor_speed = {'speedLeft': 0, 'speedRight': 0}

        # Set motor speeds
        setMotorSpeeds(motor_speed)
        time.sleep(1)

        # Simulation time debugging
        simulationTime = getSimulationTime()
        if simulationTime % 1000 == 0:
            print(f"Simulation time: {simulationTime} seconds")

# Initialize robot and run sequence agent
robot = init()
sequence_agent(robot)
