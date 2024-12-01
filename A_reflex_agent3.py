import fixed_world as world

def reflex2_agen(robot):
    max_speed=1
    turning_speed=1
    threshold=0.1
    while robot:
        readings=world.getSensorReading()
        def move_back():
            if readings['back_left']>threshold and readings['ba_right']>threshold:
                motor_speed={'speedLeft':-turning_speed,'speedRight':-turning_speed}
            elif readings['back_left']>threshold:
                motor_speed={'speedLeft':-turning_speed*0.5,'speedRight':-turning_speed}
            elif readings['back_right']>threshold:
                motor_speed={'speedLeft':-turning_speed,'speedRight':-turning_speed*0.5}
            else:
                if readings['back_left']>readings['ba_right']:
                    motor_speed={'speedLeft':-1,'speedRight':1}
                else:
                    motor_speed = {'speedLeft': 1, 'speedRight': -1}

            return motor_speed

        def move_to_box():
            max_speed=1
            #adjusting the speed according to distance
            if readings["energy"]["distance"]<0.5:
                speed_factor=0.3
            elif readings["energy"]["distance"]<0.3:
                speed_factor=0.6
            else:
                speed_factor=1
            max_speed=max_speed*speed_factor
            if readings["energy"]["direction"]:
                if readings["energy"]["direction"]>0:
                    if readings['front_right']>threshold and readings['fr_right']>threshold:
                        motor_speed={'speedLeft':max_speed,'speedRight':max_speed-0.5}
                    else:
                        motor_speed = {'speedLeft': max_speed, 'speedRight': max_speed}
                elif readings["energy"]["direction"]<0:
                    if readings['front_left']>threshold and readings['fr_left']>threshold:
                        motor_speed={'speedLeft':max_speed-0.5,'speedRight':max_speed}
                    else:
                        motor_speed = {'speedLeft': max_speed, 'speedRight': max_speed}

                else:
                    motor_speed={'speedLeft':max_speed,'speedRight':max_speed}
            else:
                motor_speed = None
            return motor_speed

        if readings['front_right']>threshold and readings['fr_left']>threshold:
            motor_speed=move_to_box()
        elif readings['front_right']>threshold:
            motor_speed={'speedLeft':max_speed,'speedRight':max_speed-1.7}
        elif readings['fr_left']>threshold:
            motor_speed = {'speedLeft': max_speed-1.7, 'speedRight': max_speed}
        else:
            motor_speed=move_back()

        world.setMotorSpeeds(motor_speed)
        collect = world.collectNearestBlock()
        if collect == "Energy collected :)":
            print(collect)



robot=world.init()
reflex2_agen(robot)