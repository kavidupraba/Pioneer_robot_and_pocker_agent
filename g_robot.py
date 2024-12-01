import Lab1_Agents_Task1_World as World
import random
import time

# Initialize connection to the robot
robot = World.init()
max_count=10
count=0
max_time=2000
# Main control loop for the random agent with collision avoidance


def roming(robot):
    print("it's ran out of time")
    r_count=0
    global max_count
    global count
    while robot:
        sensor_left = World.getSensorReading("ultraSonicSensorLeft")
        sensor_right = World.getSensorReading("ultraSonicSensorRight")
        energy_sensor = World.getSensorReading("energySensor")

        # Default random speeds
        #speed_left = random.uniform(1, 2)
        #speed_right = random.uniform(1, 2)

        # Collision avoidance logic
        # If the left sensor detects an obstacle within a certain distance, turn right
        if sensor_left > 0.5 and sensor_right > 0.5:
                speed_left = 1  # Turn right
                speed_right = 1
        # If the right sensor detects an obstacle within a certain distance, turn left
        elif sensor_right > 0.5:
            speed_left = 1.5
            speed_right = -1  # Turn left
        elif sensor_left > 0.5:
            speed_left = -1.5
            sensor_right = 1
        else:
            speed_left = -1
            speed_right = -1
        # else:
        # No obstacle detected close by; continue random movement
        # speed_left = random.uniform(1, 2)
        # speed_right = random.uniform(1, 2)

        # Set motor speeds based on updated values
        motor_speeds = dict(speedLeft=speed_left, speedRight=speed_right)
        World.setMotorSpeeds(motor_speeds)
        r_count+=1
        if r_count>=max_count:
            count=0
            Memory_agent(robot)

        # Attempt to collect an energy block if within range
        if energy_sensor.distance <= 0.5:  # Adjust this range if needed
            print("Attempting to collect a block...", World.collectNearestBlock())
            count = 0
            Memory_agent(robot)


        # Print current simulation time and sensor readings periodically
        simulation_time = World.getSimulationTime()
        if simulation_time % 1000 == 0:
            print(
                "Time:", simulation_time,
                "ultraSonicSensorLeft:", sensor_left,
                "ultraSonicSensorRight:", sensor_right,
                "EnergySensor:", energy_sensor.distance
            )

        # Wait for a short period before setting new random speeds
        time.sleep(0.5)  # Adjust to control how quickly the agent changes direction
        # Get sensor readings
        sensor_left = World.getSensorReading("ultraSonicSensorLeft")
        sensor_right = World.getSensorReading("ultraSonicSensorRight")
        energy_sensor = World.getSensorReading("energySensor")
        robot_direction=World.robotDirection()

def Memory_agent(robot):
    # Default random speeds
    global max_count
    global count
    global max_time
    while robot:
        sensor_left = World.getSensorReading("ultraSonicSensorLeft")
        sensor_right = World.getSensorReading("ultraSonicSensorRight")
        energy_sensor = World.getSensorReading("energySensor")
        robot_direction = World.robotDirection()

        speed_left = random.uniform(1, 2)
        speed_right = random.uniform(1, 2)

        # Collision avoidance logic
        # If the left sensor detects an obstacle within a certain distance, turn right
        if sensor_left > 0.5 and sensor_right > 0.5:
            if energy_sensor['direction'] > 0:
                speed_left = 1
                speed_right = 0.7
                # counter+=1
            elif energy_sensor['direction'] < 0:
                speed_left = 0.7
                speed_right = 1
                # counter+=1
            else:
                speed_left = 1  # Turn right
                speed_right = 1
                # counter+=1
        # If the right sensor detects an obstacle within a certain distance, turn left
        elif sensor_right > 0.5:
            speed_left = 1.5
            speed_right = -1  # Turn left
        elif sensor_left > 0.5:
            speed_left = -1.5
            sensor_right = 1
        else:
            speed_left = -1
            speed_right = -1
        # else:
        # No obstacle detected close by; continue random movement
        # speed_left = random.uniform(1, 2)
        # speed_right = random.uniform(1, 2)

        # Set motor speeds based on updated values
        motor_speeds = dict(speedLeft=speed_left, speedRight=speed_right)
        World.setMotorSpeeds(motor_speeds)

        # Attempt to collect an energy block if within range
        if energy_sensor.distance <= 0.5:  # Adjust this range if needed
            print("Attempting to collect a block...", World.collectNearestBlock())

        # Print current simulation time and sensor readings periodically
        simulation_time = World.getSimulationTime()
        if max_count <= count and simulation_time - World.getSimulationTime() <= max_time:
            roming(robot)
        if simulation_time % 1000 == 0:
            print(
                "Time:", simulation_time,
                "ultraSonicSensorLeft:", sensor_left,
                "ultraSonicSensorRight:", sensor_right,
                "EnergySensor:", energy_sensor.distance
            )

        # Wait for a short period before setting new random speeds
        time.sleep(0.5)  # Adjust to control how quickly the agent changes direction

Memory_agent(robot)