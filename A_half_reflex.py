import fixed_world as world
import time


def sequanc_agent(robot):
    # {'fr_left': inf, 'fr_right': inf, 'front_left': inf, 'front_right': inf, 'front_r1': inf, 'front_r2': inf,
    # 'front_l1': inf, 'front_l2': inf, 'front_east': 0.9865700848382228, 'front_west': inf,
    # 'ba_left': np.float64(0.9411972145270591), 'ba_right': np.float64(0.9386362889674799), 'back_r1': inf,
    # 'back_r2': 0.9385343597712356, 'back_l1': 0.9408212914012777, 'back_l2': inf, 'back_left': 0.8844653350796499,
    # 'back_right': 0.8842472440387602, 'back_east': inf, 'back_west': 0.9872404338564605,
    # 'energy': {'distance': 1.6532026933667674, 'direction': -0.033451538229056776, 'mdeltax': 1.6524457931518555,
    # 'mdeltay': 0.050020456314086914}}
    while robot:
        max_speed=1
        readings=world.getSensorReading()

        #adjusting speed according to the distance to the target
        if readings["energy"]["distance"]<0.5:
            speed_factor=0.3
        elif readings["energy"]["distance"]<0.3:
            speed_factor=0.6
        else:
            speed_factor=1

        max_speed=max_speed*speed_factor

        # move toward the target
        if readings["energy"]["direction"]:
            if readings["energy"]["direction"]>0:
                motor_speed={"speedLeft":max_speed,"speedRight":0.5}
            elif readings["energy"]["direction"]<0:
                motor_speed={"speedLeft":0.5,"speedRight":max_speed}
            else:
                motor_speed={"speedLeft":max_speed,"speedRight":max_speed}
            world.setMotorSpeeds(motor_speed)
            collect=world.collectNearestBlock()
            if collect=="Energy collected :)":
               print(collect)



robot=world.init()
sequanc_agent(robot)