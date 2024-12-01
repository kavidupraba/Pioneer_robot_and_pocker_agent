import random
import  fixed_world as world
import  time


def random_agent(robot):
    while robot:
        # Generate a random speed between 1 and 2 (inclusive).
        max_speed = random.randrange(1, 3, 1)

        # Generate a random value between 0 and 2 to decide on actions
        g = random.uniform(0, 2)

        if 0.1 <= g < 0.5:
            motor_speed = {'speedLeft': max_speed - 0.5, 'speedRight': max_speed}
        elif g < 0.1:
            motor_speed = {'speedLeft': max_speed, 'speedRight': max_speed - 0.5}
        else:
            motor_speed = {'speedLeft': random.choice([0.5,1]), 'speedRight': random.choice([0.5,1])}

        # Get the current simulation time and execute the movement command
        current_time = world.getSimulationTime()
        world.execute(motor_speed, current_time + random.choice([1, 1.5]), -1)
        collected = world.collectNearestBlock()
        world.setMotorSpeeds({'speedLeft': max_speed, 'speedRight': -max_speed})
        time.sleep(1)

        print(collected)



robot=world.init()
random_agent(robot)
