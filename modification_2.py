import random
import Lab1_Agents_Task1_World as World

def memory_agent(robot):
    stuck_counter = 0  # To track if the agent is stuck


    while robot:
        # Get sensor readings
        ultra_left = World.getSensorReading("ultraSonicSensorLeft")
        ultra_right = World.getSensorReading("ultraSonicSensorRight")
        energy_sensor_data = World.getSensorReading("energySensor")  # This will be an EasyDict
        max_speed=1

        # Extract the actual distance value from the energy sensor data
        energy_distance = energy_sensor_data['distance']  # Access the 'distance' value from the EasyDict

        # Store sensor readings and action taken in memory
        if ultra_left >= 0.5 and ultra_right >= 0.5:
            if energy_sensor_data["distance"] < 0.5:
                speed_factor = 0.3
            elif energy_sensor_data["distance"] < 0.3:
                speed_factor = 0.6
            else:
                speed_factor = 1

            max_speed = max_speed * speed_factor

            # move toward the target
            if energy_sensor_data["direction"]:
                if energy_sensor_data["direction"] > 0:
                    motor_speed = {"speedLeft": max_speed, "speedRight": max_speed - 0.7}
                elif energy_sensor_data["direction"] < 0:
                    motor_speed = {"speedLeft": max_speed - 0.7, "speedRight": max_speed}
                else:
                    motor_speed = {"speedLeft": max_speed, "speedRight": max_speed}
            else:
                motor_speed={"speedLeft":0,"speedRight":0}
        elif ultra_left>=0.5:
            motor_speed = {'speedLeft': 0.5, 'speedRight': 1}
        elif ultra_right>=0.5:
            motor_speed = {'speedLeft': 1, 'speedRight': 0.5}
        else:
            motor_speed = {'speedLeft': -1, 'speedRight': 1}
        World.setMotorSpeeds(motor_speed)
        World.collectNearestBlock()

        # Optional: print information for debugging
        simulationTime = World.getSimulationTime()
        if simulationTime % 1000 == 0:
            print("Time:", simulationTime, "Left Sensor:", ultra_left, "Right Sensor:", ultra_right)


# Initialize robot and run memory agent
robot = World.init()
memory_agent(robot)
