import random
from collections import deque
import fixed_world as world
import numpy as np

def move_robot(di):
    max_speed=1
    threshold=0.5
    up=[-1,0]
    readings=world.getSensorReading()
    if all(i in up for i in di):
        if readings["front_left"]>threshold and readings["front_right"]>threshold:
            motor_speed={"speedLeft":max_speed,"speedRight":max_speed}
            world.setMotorSpeeds(motor_speed)
            return True
        else:
            return False


def maze_logic():
    maze={}
    #max_speed=random.uniform(1,2)
    #threshold=0.5
    #readings=world.getSensorReading()
    #maze_size=5
    #while robot:
    #z=np.ones((5,5),dtype=int)*-1
    #print(np.tile(z,(5,1)))
    robot_pos=(2,2)
    directions=[(0,1),(1,0),(0,-1),(-1,0)]
    print(directions)
    maze[(1,2)]=1
    print(maze)
    for dx,dy in directions:
        r=move_robot([dx,dy])
        if r:
            nx,ny=dx+robot_pos[0],dy+robot_pos[1]
            maze[(nx,ny)]=0
        else:
            nx,ny=dx+robot_pos[0],dy+robot_pos[1]
            maze[(nx,ny)]=1





#robot=world.init()
#robot_move()