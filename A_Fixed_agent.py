import random

import fixed_world as world
import time
import numpy

def attempt_collection():
    collect = world.collectNearestBlock()
    if collect == "Energy collected :)":
        print(collect)

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

def adjust_speed():

    if time.time()<10:
        return 1.2
    else:
        return 0.2

def move_forward():
    ad = adjust_speed()
    motor_speed = {"speedLeft": ad, "speedRight": ad}
    world.execute(motor_speed, 5, -1)
    attempt_collection()

def fixed_agent(robot):
    while robot:
        action_list=[move_forward,turn_90_left,turn_90_right,turn_90_left(),turn_90_left(),turn_180_right(),turn_180_left]
        for action in action_list:
            action()
            for i in range(10):
                turning_bit_to_right()
                turning_bit_to_left()






robot=world.init()
fixed_agent(robot)

