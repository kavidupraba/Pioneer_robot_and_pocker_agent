import fixed_world as world
import numpy as np
import time


def turn_90_left():
    motor_speed = {"speedLeft": -0.5, "speedRight": -0.5}
    world.setMotorSpeeds(motor_speed)
    time.sleep(1.2)
    motor_speed = {"speedLeft": -0.5, "speedRight": 0.5}
    world.setMotorSpeeds(motor_speed)
    time.sleep(1.2)
    world.STOP()

def turning_bit_to_right():
    motor_speed = {"speedLeft": 1, "speedRight": 0.2}
    world.setMotorSpeeds(motor_speed)
    time.sleep(0.5)
    world.STOP()
    collect = world.collectNearestBlock()
    if collect == "Energy collected :)":
        print(collect)



def turning_bit_to_left():
    motor_speed = {"speedLeft": 0.2, "speedRight": 1}
    world.setMotorSpeeds(motor_speed)
    time.sleep(0.5)
    world.STOP()
    collect = world.collectNearestBlock()
    if collect == "Energy collected :)":
        print(collect)



def move_to_box(readings):

    if readings["energy"]["direction"]:
        if -0.1<=readings["energy"]["direction"]<=0.1:
            motor_speed = {"speedLeft": 1, "speedRight": 1}
            world.setMotorSpeeds(motor_speed)
        else:
            if readings["energy"]["direction"] > 0:
                turning_bit_to_right()
            elif readings["energy"]["direction"] < 0:
                turning_bit_to_left()


def find_densest_sector():
    """
    Identifies the sector with the highest number of energy boxes.
    :param blocks: List of tuples (blockHandle, blockName, distance, direction, deltax, deltay).
    :param num_sectors: Number of sectors to divide the 360° view into.
    :return: Center of the densest sector in polar coordinates (average distance, average direction).
    """
    num_sectors = 8
    blocks=world.findEnergyBlocks()
    sector_width = 2 * np.pi / num_sectors  # Angular width of each sector
    sectors = [[] for _ in range(num_sectors)]  # List of lists to hold blocks in each sector

    for block in blocks:
        _, _, distance, direction, _, _ = block
        # Determine the sector index
        sector_index = int((direction + np.pi) // sector_width) % num_sectors
        sectors[sector_index].append((distance, direction))

    # Find the densest sector
    densest_sector = max(sectors, key=len)
    if not densest_sector:
        return None  # No blocks found

    # Calculate the center of the densest sector (average distance and direction)
    avg_distance = sum(block[0] for block in densest_sector) / len(densest_sector)
    avg_direction = sum(block[1] for block in densest_sector) / len(densest_sector)

    return avg_distance, avg_direction


def move_to_densest_area():
    """
    Moves the robot toward the densest area of energy boxes.
    :param dense_area: Tuple (distance, direction) of the densest area.
    """
    dense_area=find_densest_sector()
    if dense_area is None:
        print("No dense area found.")
        return

    avg_distance, avg_direction = dense_area
    if -0.1 <= avg_direction <= 0.1:  # Facing directly toward the area
        motor_speed = {"speedLeft": 1, "speedRight": 1}  # Move forward
        world.setMotorSpeeds(motor_speed)
    elif avg_direction > 0:  # Turn right toward the area
        turning_bit_to_right()
    else:  # Turn left toward the area
        turning_bit_to_left()


def reflex(robot):
    max_speed=1
    while robot:
        readings = world.getSensorReading()
        if readings["front_left"]>1.5 and readings["front_right"]>1.5 and readings["fr_left"]>0.6 and readings["fr_right"]>0.6:
          move_to_densest_area()
        else:
            print("almost there")

robot=world.init()
reflex(robot)