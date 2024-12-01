import fixed_world as world
import numpy as np
import time

stuck_time=20#time that tobot can attemt to collect boxes
search_box=0#this will increased along with robot try to collect bocws
dens_count=0#this will increase with the time robot trying toreach the area that have most energy boxes
start_time=None # starting to move to dance area
max_time_for_reach_dence_energy=200
r_start_time=None


def turn_90_left():
    motor_speed = {"speedLeft": -0.5, "speedRight": -0.5}
    world.setMotorSpeeds(motor_speed)
    time.sleep(1.2)
    motor_speed = {"speedLeft": -0.5, "speedRight": 0.5}
    world.setMotorSpeeds(motor_speed)
    time.sleep(1.2)
    world.STOP()

def turn_90_right():
    motor_speed = {"speedLeft": -0.5, "speedRight": -0.5}
    world.setMotorSpeeds(motor_speed)
    time.sleep(1.2)
    motor_speed = {"speedLeft": 0.5, "speedRight": -0.5}
    world.setMotorSpeeds(motor_speed)
    time.sleep(1.2)
    world.STOP()

def turn_180_left():
    motor_speed = {"speedLeft": -0.5, "speedRight": -0.5}
    world.setMotorSpeeds(motor_speed)
    time.sleep(1.2)
    motor_speed = {"speedLeft": -0.5, "speedRight": 0.5}
    world.setMotorSpeeds(motor_speed)
    time.sleep(2.5)
    world.STOP()

def turn_180_right():
    motor_speed = {"speedLeft": -0.5, "speedRight": -0.5}
    world.setMotorSpeeds(motor_speed)
    time.sleep(1.2)
    motor_speed = {"speedLeft": 0.5, "speedRight": -0.5}
    world.setMotorSpeeds(motor_speed)
    time.sleep(2.5)
    world.STOP()


def adjust_speed(max_speed,readings):
    if readings["front_left"]==float('inf') and readings["front_right"]==float('inf'):
        return 1.2
    else:
        if min(readings["front_left"],readings["front_right"])>1:
            return 0.5
        else:
            return max_speed

def attempt_collection():
    global search_box
    global dens_count
    collect = world.collectNearestBlock()
    if collect == "Energy collected :)":
        search_box=0
        dens_count=0
        print(collect)

def turning_bit_to_right():
    motor_speed = {"speedLeft": 1, "speedRight": 0.2}
    world.setMotorSpeeds(motor_speed)
    time.sleep(0.5)
    world.STOP()
    attempt_collection()



def turning_bit_to_left():
    motor_speed = {"speedLeft": 0.2, "speedRight": 1}
    world.setMotorSpeeds(motor_speed)
    time.sleep(0.5)
    world.STOP()
    attempt_collection()



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
    global max_time_for_reach_dence_energy
    global start_time
    global search_box
    global dens_count

    dense_area=find_densest_sector()
    if dense_area is None:
        print("No dense area found.")
        return

    avg_distance, avg_direction = dense_area
    if -0.1 <= avg_direction <= 0.1:  # Facing directly toward the area
        motor_speed = {"speedLeft": 1, "speedRight": 1}  # Move forward
        world.setMotorSpeeds(motor_speed)
        attempt_collection()
    elif avg_direction > 0:  # Turn right toward the area
        turning_bit_to_right()
    else:  # Turn left toward the area
        turning_bit_to_left()
    current_time=world.getSimulationTime()
    if current_time-start_time>=max_time_for_reach_dence_energy:
        search_box=0
        dens_count=0

def roaming_random(max_speed, readings):
    global r_start_time
    global search_box
    global dens_count
    adjuset_s = adjust_speed(max_speed, readings)
    motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
    world.setMotorSpeeds(motor_speed)
    attempt_collection()
    current_time = world.getSimulationTime()
    if current_time-r_start_time>=50:
        search_box = 0
        dens_count = 0



def memory(robot):
    global search_box
    global dens_count
    global start_time
    global r_start_time

    max_speed=0.3
    while robot:
        readings = world.getSensorReading()
        if readings["front_left"]>0.5 and readings["front_right"]>0.5 and readings["fr_left"]>0.3 and readings["fr_right"]>0.3:
            print("moving forward")
            if readings["energy"]["distance"]>1.5:
                adjuset_s=adjust_speed(max_speed,readings)
                motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
                world.setMotorSpeeds(motor_speed)
                attempt_collection()
            elif search_box>=stuck_time:
                print("TIME OUT SEARCHING ANOTHER ROUTE!")
                if dens_count>=stuck_time:
                    if r_start_time is None:
                       r_start_time=world.getSimulationTime()
                    print("Moving to dens energy area is failed roaming around randomly")
                    roaming_random(max_speed,readings)
                else:
                    dens_count+=1
                    if start_time is None:
                        start_time=world.getSimulationTime()
                    move_to_densest_area()
            else:
                search_box+=1
                move_to_box(readings)

        elif readings["front_east"]>0.5 and readings["front_west"]>0.5:
            print("moving right or left")
            if readings["front_east"]>readings["front_west"]:
                turn_90_right()
            else:
                turn_90_left()

            adjuset_s = adjust_speed(max_speed, readings)
            motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
            world.setMotorSpeeds(motor_speed)
            attempt_collection()

        elif readings["front_east"]>0.5:
            print("moving right")
            turn_90_right()

            adjuset_s = adjust_speed(max_speed, readings)
            motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
            world.setMotorSpeeds(motor_speed)
            attempt_collection()

        elif readings["front_west"]>0.5:
            print("moving left")
            turn_90_left()

            adjuset_s = adjust_speed(max_speed, readings)
            motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
            world.setMotorSpeeds(motor_speed)
            attempt_collection()

        else:
            print("moving right or left")
            if readings["front_east"]>readings["front_west"]:
                turn_180_right()
            else:
                turn_180_left()

            adjuset_s = adjust_speed(max_speed, readings)
            motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
            world.setMotorSpeeds(motor_speed)
            attempt_collection()








robot=world.init()
memory(robot)