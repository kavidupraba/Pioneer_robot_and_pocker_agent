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



def reflex(robot):
    max_speed=0.3
    while robot:
        readings = world.getSensorReading()
        if readings["front_left"]>0.5 and readings["front_right"]>0.5 and readings["fr_left"]>0.2 and readings["fr_right"]>0.2:
            print("moving forward")
            adjuset_s=adjust_speed(max_speed,readings)
            motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
            world.setMotorSpeeds(motor_speed)
            collect=world.collectNearestBlock()
            if collect == "Energy collected :)":
                print(collect)

        elif readings["front_east"]>0.5 and readings["front_west"]>0.5:
            print("moving right or left")
            if readings["front_east"]>readings["front_west"]:
                turn_90_right()
            else:
                turn_90_left()

            adjuset_s = adjust_speed(max_speed, readings)
            motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
            world.setMotorSpeeds(motor_speed)
            collect=world.collectNearestBlock()
            if collect == "Energy collected :)":
                print(collect)

        elif readings["front_east"]>0.5:
            print("moving right")
            turn_90_right()

            adjuset_s = adjust_speed(max_speed, readings)
            motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
            world.setMotorSpeeds(motor_speed)
            collect=world.collectNearestBlock()
            if collect == "Energy collected :)":
                print(collect)

        elif readings["front_west"]>0.5:
            print("moving left")
            turn_90_left()

            adjuset_s = adjust_speed(max_speed, readings)
            motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
            world.setMotorSpeeds(motor_speed)
            collect=world.collectNearestBlock()
            if collect == "Energy collected :)":
                print(collect)

        else:
            print("moving right or left")
            if readings["front_east"]>readings["front_west"]:
                turn_180_right()
            else:
                turn_180_left()

            adjuset_s = adjust_speed(max_speed, readings)
            motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
            world.setMotorSpeeds(motor_speed)
            collect=world.collectNearestBlock()
            if collect == "Energy collected :)":
                print(collect)








robot=world.init()
reflex(robot)


'''
ori = world.robot_or()
    nori=np.array(ori)
    ra=np.radians(90)
    s=np.sin(ra)
    c=np.cos(ra)
    ma=[[c,-s,0],[s,c,0],[0,0,1]]
    rotate=np.dot(ma,nori)
    print(f"before: {nori}")
    print(rotate)
    ori2 = np.array(world.robot_or())


'''







