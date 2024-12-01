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

def attempt_collection():
    collect = world.collectNearestBlock()
    if collect == "Energy collected :)":
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



def reflex(robot):
    max_speed=0.3
    while robot:
        readings = world.getSensorReading()
        if readings["front_left"]>0.5 and readings["front_right"]>0.5 and readings["fr_left"]>0.2 and readings["fr_right"]>0.2:
            print("moving forward")
            if readings["energy"]["distance"]>1.5:
                adjuset_s=adjust_speed(max_speed,readings)
                motor_speed = {"speedLeft": adjuset_s, "speedRight": adjuset_s}
                world.setMotorSpeeds(motor_speed)
                attempt_collection()
            else:
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
reflex(robot)