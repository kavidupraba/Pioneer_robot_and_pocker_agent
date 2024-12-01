
from fixed_world import *

def navigate():
    stuck_counter = 0
    last_position = None

    while True:
        sensor_data = getSensorReading()
        nearest_block = findEnergyBlocks()[0]
        block_distance = nearest_block[2]
        block_direction = nearest_block[3]

        # Obstacle detection
        if (
            sensor_data["front_left"] < 0.5 or
            sensor_data["front_right"] < 0.5 or
            sensor_data["fr_left"] < 0.5 or
            sensor_data["fr_right"] < 0.5
        ):
            print("Obstacle detected! Avoiding...")
            avoid_obstacle(sensor_data)
            continue

        # If close to the block, attempt collection
        if block_distance <= 0.5:
            result = collectNearestBlock()
            print(result)
            if result == "Energy collected :)":
                last_position = nearest_block[-2:]  # Store the last block position
            continue

        # Move toward the block
        move_toward_block(block_direction, block_distance)

        # Check if the robot is stuck
        if is_stuck(sensor_data):
            stuck_counter += 1
            if stuck_counter > 3:  # If stuck for too long
                print("Stuck! Attempting to recover...")
                recover(last_position)
                stuck_counter = 0
        else:
            stuck_counter = 0

        time.sleep(0.1)

def avoid_obstacle(sensor_data):
    """
    Avoid obstacles based on sensor data.
    """
    if sensor_data["front_left"] < sensor_data["front_right"]:
        execute({"speedLeft": -2, "speedRight": 2}, simulationTime=1, clockTime=1)  # Turn right
    else:
        execute({"speedLeft": 2, "speedRight": -2}, simulationTime=1, clockTime=1)  # Turn left
    execute({"speedLeft": 2, "speedRight": 2}, simulationTime=1, clockTime=1)  # Move forward

def move_toward_block(direction, distance):
    """
    Move toward the block by aligning with its direction.
    """
    if abs(direction) > 0.1:  # Need to adjust alignment
        turn_speed = -2 if direction > 0 else 2
        execute({"speedLeft": turn_speed, "speedRight": -turn_speed}, simulationTime=0.5, clockTime=0.5)
    else:  # Move forward
        execute({"speedLeft": 2, "speedRight": 2}, simulationTime=distance / 2, clockTime=distance / 2)

def is_stuck(sensor_data):
    """
    Determine if the robot is stuck by checking for lack of movement or repeated obstacle readings.
    """
    return all(
        sensor_data[key] < 0.2 for key in ["front_left", "front_right", "fr_left", "fr_right"]
    )

def recover(last_position):
    """
    Recover from being stuck by moving randomly or heading to the last known block position.
    """
    if last_position:
        print("Returning to last block position...")
        move_to_position(last_position)
    else:
        print("Moving randomly to recover...")
        random_direction = random.choice([-1, 1])
        execute({"speedLeft": random_direction * 2, "speedRight": -random_direction * 2}, simulationTime=1, clockTime=1)
        execute({"speedLeft": 2, "speedRight": 2}, simulationTime=1, clockTime=1)

def move_to_position(position):
    """
    Move to a specific position (approximate navigation).
    """
    current_pos = vrep.simxGetObjectPosition(robot.clientID, robot.pioneerRobotHandle, -1, vrep.simx_opmode_oneshot_wait)[1]
    direction_to_target = math.atan2(position[1] - current_pos[1], position[0] - current_pos[0])
    robot_direction = robotDirection()
    angle_to_turn = normaliseAngle(direction_to_target - robot_direction)

    if abs(angle_to_turn) > 0.1:  # Turn towards the target
        turn_speed = -2 if angle_to_turn > 0 else 2
        execute({"speedLeft": turn_speed, "speedRight": -turn_speed}, simulationTime=0.5, clockTime=0.5)

    execute({"speedLeft": 2, "speedRight": 2}, simulationTime=1, clockTime=1)  # Move forward

# Initialize the robot and start navigation
robot = init()
if robot:
    navigate()
