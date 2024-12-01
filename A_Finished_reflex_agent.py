import fixed_world as world
import time

def reflex_agent(robot):
    threshold=0.7
    turning_speed=1
    max_speed=2

    while robot:
        readings = world.getSensorReading()
        #moving to energy box
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
                    motor_speed={'speedLeft':max_speed,'speedRight':max_speed-0.5}
                elif readings["energy"]["direction"]<0:
                    motor_speed={'speedLeft':max_speed-0.5,'speedRight':max_speed}
                else:
                    motor_speed={'speedLeft':max_speed,'speedRight':max_speed}
            else:
                motor_speed = None
            return motor_speed


        mf=min(readings['front_left'],readings['front_right'])
        if mf==readings['front_left']:
           sf=readings['fr_right']
           if mf > threshold and sf > threshold:
               motor_speed=move_to_box()
           elif mf > threshold:
               motor_speed = {'speedLeft': max_speed - 1.7, 'speedRight': max_speed}
           elif sf > threshold+0.2:
               motor_speed = {'speedLeft': max_speed, 'speedRight': max_speed-1.7}
           else:
               if readings['back_right']>threshold and readings['back_left']>threshold:
                  motor_speed = {'speedLeft': -turning_speed, 'speedRight': -turning_speed}
               else:
                   motor_speed = {'speedLeft': 0.5, 'speedRight':0.5}



        elif mf==readings['front_right']:
            sf=readings['fr_left']
            if mf > threshold and sf > threshold:
                motor_speed = move_to_box()
            elif mf > threshold:
                motor_speed = {'speedLeft': max_speed, 'speedRight': max_speed - 1.7}
            elif sf > threshold+0.2:
                motor_speed = {'speedLeft': max_speed - 1.7, 'speedRight': max_speed}
            else:
                if readings['back_right'] > threshold and readings['back_left'] > threshold:
                    motor_speed = {'speedLeft': -turning_speed, 'speedRight': -turning_speed}
                else:
                    motor_speed = {'speedLeft': 0.5, 'speedRight': 0.5}
        else:
            motor_speed=move_to_box()
        world.setMotorSpeeds(motor_speed)
        collect=world.collectNearestBlock()
        if collect == "Energy collected :)":
            print(collect)


robot=world.init()
reflex_agent(robot)