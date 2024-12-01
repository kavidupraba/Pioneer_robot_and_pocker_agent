import numpy as np

import vrep, math, time, random

# stop the robot
def STOP():
    setMotorSpeeds(dict(speedLeft=0, speedRight=0))

# get some information from one of the sensors
def getSensorReading():
    def getObstacleDist(sensorHandler_):
        rawSR=vrep.simxReadProximitySensor(robot.clientID,sensorHandler_,vrep.simx_opmode_oneshot_wait)
        #print(rawSR)
        if rawSR[1]:
            return math.sqrt(rawSR[2][0]**2 + rawSR[2][1]**2 + rawSR[2][2]**2)
        else:
            return float('inf')

    #front sensors readings
    leftf_list=[]#left of the front
    for i in range(2,4,1):
        namefl=f"ultraSonicSensorFL{i}"
        leftf_distance=getObstacleDist(robot[namefl])
        leftf_list.append(leftf_distance)
    rightf_list=[]#right of the front
    for i in range(6,8,1):
        namefr=f"ultraSonicSensorFR{i}"
        rightf_distance=getObstacleDist(robot[namefr])
        rightf_list.append(rightf_distance)

    front_left=getObstacleDist(robot.ultraSonicSensorFront4)
    front_right=getObstacleDist(robot.ultraSonicSensorFront5)

    #side readings
    front_east=getObstacleDist(robot.ultraSonicSensorFR8)
    front_west=getObstacleDist(robot.ultraSonicSensorFL1)

    #collecting_for_better_movement
    #right
    front_r1=getObstacleDist(robot.ultraSonicSensorFR6)
    front_r2 = getObstacleDist(robot.ultraSonicSensorFR7)
    #left
    front_l1 = getObstacleDist(robot.ultraSonicSensorFL2)
    front_l2 = getObstacleDist(robot.ultraSonicSensorFL3)



    #behind sensors reading
    leftb_list=[]#behind left readings
    for i in range(14,16,1):
        namebl=f"ultraSonicSensorBL{i}"
        leftb_distance=getObstacleDist(robot[namebl])
        leftb_list.append(leftb_distance)
    rightb_list=[]#behind right readings
    for i in range(10,12,1):
        namebr=f"ultraSonicSensorBR{i}"
        rightb_distance=getObstacleDist(robot[namebr])
        rightb_list.append(rightb_distance)

    behind_left = getObstacleDist(robot.ultraSonicSensorBehind13)
    behind_right = getObstacleDist(robot.ultraSonicSensorBehind12)

    back_east=getObstacleDist(robot.ultraSonicSensorBL16)
    back_west=getObstacleDist(robot.ultraSonicSensorBR9)

    #collecting_for_better_movement
    #right
    back_r1=getObstacleDist(robot.ultraSonicSensorBR10)
    back_r2=getObstacleDist(robot.ultraSonicSensorBR11)
    #left
    back_l1=getObstacleDist(robot.ultraSonicSensorBL14)
    back_l2=getObstacleDist(robot.ultraSonicSensorBL15)

    #filtering the data
     #filtering front data
    leftf_list=np.array(leftf_list)#getting the data of front left side
    fld=leftf_list!=float('inf')
    rightf_list=np.array(rightf_list)#getting the data of front right side
    frd=rightf_list!=float('inf')

    # if there is distance reading that not equal to float('inf') 'large number' we will get closest distance else assign large number
    if len(leftf_list[fld])>0:
        f_left=min(leftf_list[fld])
    else:
        f_left=float('inf')

    if len(rightf_list[frd])>0:
        f_right=min(rightf_list[frd])
    else:
        f_right=float('inf')

       #filtering back data
    leftb_list=np.array(leftb_list)
    bld=leftb_list!=float('inf')
    rightb_list=np.array(rightb_list)
    brd=rightb_list!=float('inf')

    # if there is distance reading that not equal to float('inf') 'large number' we will get closest distance else assign large number
    if len(leftb_list[bld])>0:
        b_left=min(leftb_list[bld])
    else:
        b_left=float('inf')

    if len(rightb_list[brd])>0:
        b_right=min(rightb_list[brd])
    else:
        b_right=float('inf')



    blockHandle, blockName, distance, direction,deltax,deltay = findEnergyBlocks()[0]
    energy_data=EasyDict(distance=distance, direction=direction,mdeltax=deltax,mdeltay=deltay)
    return {
        "fr_left":f_left,#left sensor-front
        "fr_right":f_right,#right sensor-front

        "front_left":front_left,#front sensor to the left
        "front_right":front_right,#front sensor to the right

        "front_r1":front_r1,# I took sensor to the right separatly if you check the code up you can see that I build a method to select sensors separatly
        "front_r2":front_r2,

        "front_l1":front_l1,# same as front_r1 I separate them
        "front_l2":front_l2,


        "front_east":front_east,# sensor to the right side
        "front_west":front_west,# sensor to the left side

        "ba_left":b_left,# back left side
        "ba_right":b_right,# back right side

        "back_r1":back_r1,# just like front_r1 I just simply get things removed
        "back_r2":back_r2,

        "back_l1":back_l1,# like front_r1
        "back_l2":back_l2,

        "back_left":behind_left,#straight back sensor to the left
        "back_right":behind_right,#straight back sensor to the right

        "back_east":back_east,# back right side
        "back_west":back_west,# back left side

        "energy":energy_data# just get the box data
    }

# set speeds for robot wheels
def setMotorSpeeds(motorSpeed):
    try:
        vrep.simxPauseCommunication(robot.clientID,True)
        vrep.simxSetJointTargetVelocity(robot.clientID, robot.leftMotorHandle, motorSpeed.get('speedLeft',0), vrep.simx_opmode_oneshot )
        vrep.simxSetJointTargetVelocity(robot.clientID, robot.rightMotorHandle, motorSpeed.get('speedRight',0), vrep.simx_opmode_oneshot )
    finally:
        vrep.simxPauseCommunication(robot.clientID,False)

# execute an action for a given time, then stop the robot and return control
def execute(motorSpeed,simulationTime,clockTime):
    startTimeSim = getSimulationTime()
    startTimeClock = time.time()
    setMotorSpeeds(motorSpeed)
    while True:
        if simulationTime>0 and getSimulationTime()>startTimeSim+simulationTime: break
        if clockTime>0 and time.time()>startTimeClock+clockTime: break
        time.sleep(0.1)
    STOP()

# which direction robot is facing?
def robotDirection():
    retCode, robotOrientation = vrep.simxGetObjectOrientation(robot.clientID, robot.pioneerRobotHandle, -1, vrep.simx_opmode_oneshot_wait)
    direction = math.pi/2 - robotOrientation[2]
    return normaliseAngle(direction)

def robot_or():
    retCode, robotOrientation = vrep.simxGetObjectOrientation(robot.clientID, robot.pioneerRobotHandle, -1, vrep.simx_opmode_oneshot_wait)
    #direction = math.pi / 2 - robotOrientation[2]
    return robotOrientation


# time is useful
def getSimulationTime():
    vrep.simxGetPingTime(robot.clientID)
    return vrep.simxGetLastCmdTime(robot.clientID)-connectionTime

#get time to close the distance
def get_time_d(lefts,rights,dist):
    avgs=(lefts+rights)/2
    timed=dist/avgs
    return timed
#sensor_maping
def get_sensor_map(sensor_name):
    sensor_map = {
        "front_left": robot.ultraSonicSensorFront4,
        "front_right": robot.ultraSonicSensorFront5,
        "front_east": robot.ultraSonicSensorFR8,
        "front_west": robot.ultraSonicSensorFL1,
        "front_r1": robot.ultraSonicSensorFR6,
        "front_r2": robot.ultraSonicSensorFR7,
        "front_l1": robot.ultraSonicSensorFL2,
        "front_l2": robot.ultraSonicSensorFL3,
        "behind_left": robot.ultraSonicSensorBehind13,
        "behind_right": robot.ultraSonicSensorBehind12,
        "back_east": robot.ultraSonicSensorBL16,
        "back_west": robot.ultraSonicSensorBR9,
        "back_r1": robot.ultraSonicSensorBR10,
        "back_r2": robot.ultraSonicSensorBR11,
        "back_l1": robot.ultraSonicSensorBL14,
        "back_l2": robot.ultraSonicSensorBL15,
    }
    return sensor_map.get(sensor_name,None)
#get the itarception
def get_inter(sen1,sen2,box_dis):
    sen1_obj=get_sensor_map(sen1)
    sen2_obj=get_sensor_map(sen2)
    if sen2_obj is None or sen1_obj is None:
        raise ValueError(f"Invalid sensor name(s): {sen1}, {sen2}")
    #result = vrep.simxReadProximitySensor(robot.clientID, sen1_obj,vrep.simx_opmode_oneshot_wait)
    #print(f"pack value {result}")

    error_cod1,detect_1,row_vector1,surface1,_=vrep.simxReadProximitySensor(robot.clientID,sen1_obj,vrep.simx_opmode_oneshot_wait)
    error_cod2,detect_2,row_vector2,surface2,_=vrep.simxReadProximitySensor(robot.clientID,sen2_obj,vrep.simx_opmode_oneshot_wait)
    retCode, robotPos = vrep.simxGetObjectPosition(robot.clientID, robot.pioneerRobotHandle, -1,vrep.simx_opmode_oneshot_wait)
    robotdirection = robotDirection()
    #y=mx+b

    if not detect_1 or not detect_2:
        return float('inf')
    x1,y1=row_vector1[0]-robotPos[0],row_vector1[1]-robotPos[1]
    x2,y2=row_vector2[0]-robotPos[0],row_vector2[1]-robotPos[1]
    alg1=math.atan2(y1,x1)-robotdirection
    alg2=math.atan2(y2,x2)-robotdirection
    algf1=normaliseAngle(alg1)
    algf2=normaliseAngle(alg2)

    #if detect_1 and detect_2:
        #if (x2-x1)!=0:
            #m=(y2-y1)/(x2-x1)
    m=float('inf')if algf1==algf2 else (algf2-algf1)/(x2-x1)


    # y=box_dis*x-1
    # y=mx+b-2
    if m!=float('inf') and (box_dis-m)!=0:
       b=y1-m*x1
       x3=b/(box_dis-m)
       y3=box_dis*x3
       d_align=np.sqrt(x3**2+y3**2)
       #print(d_align)
    else:
       d_align=float('inf')

    return d_align






################################################################################
################################################################################
# Helper functions below... not all that interesting...                        #
################################################################################
################################################################################

class EasyDict(dict):
    def __init__(self, *args, **kwargs):
        super(EasyDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

# a function to initialise connection to the server... hides a lot of uninteresting technical details.
def init():
    global robot
    global blockHandleArray, connectionTime
    print('Program started')
    vrep.simxFinish(-1) # just in case, close all opened connections
    int_portNb = 19999 # define port_nr
    clientID = vrep.simxStart('127.0.0.1', int_portNb, True, True, 5000, 5) # connect to server
    if clientID != -1:
        print('Connected to remote API server')
        res,objs = vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_oneshot_wait) # get all objects in the scene
        if res == vrep.simx_return_ok: # Remote function call succeeded
            print('Number of objects in the scene: ',len(objs))# print number of object in the scene

            ret_lm,  leftMotorHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
            ret_rm,  rightMotorHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
            ret_pr,  pioneerRobotHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
            ret_sl,  ultraSonicSensorFL3 = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_ultrasonicSensor3',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorFront5 = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_ultrasonicSensor5',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorFront4 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor4',vrep.simx_opmode_oneshot_wait )
            ret_sr,  ultraSonicSensorFL2= vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor2',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorFL1=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor1',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorFR6=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor6',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorFR7=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor7',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorFR8=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor8',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorBehind13=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor13',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorBehind12=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor12',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorBL14=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor14',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorBL15=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor15',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorBL16=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor16',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorBR11=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor11',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorBR10=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor10',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorBR9=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor9',vrep.simx_opmode_oneshot_wait)



            blockHandleArray = []
            for i_block in range(12):
                blockName = 'ConcretBlock#'+str(i_block)
                retCode, handle = vrep.simxGetObjectHandle(clientID, blockName, vrep.simx_opmode_oneshot_wait)
                assert retCode==0, retCode
                if i_block>6:
                    rand_loc = [random.random()*6-1.5, random.random()*7-2.5, 0.0537] # x[-1.5,4.5] y[-2.5,-4.5]
                    vrep.simxSetObjectPosition(clientID, handle, -1, rand_loc, vrep.simx_opmode_oneshot_wait)
                retCode,position = vrep.simxGetObjectPosition(clientID, handle, -1, vrep.simx_opmode_oneshot_wait)
                assert retCode==0, retCode
                blockHandleArray.append([handle,i_block,position])
            robot = EasyDict(clientID=clientID,
                             leftMotorHandle=leftMotorHandle,
                             rightMotorHandle=rightMotorHandle,
                             pioneerRobotHandle=pioneerRobotHandle,
                             ultraSonicSensorFront5=ultraSonicSensorFront5,
                             ultraSonicSensorFront4=ultraSonicSensorFront4,
                             ultraSonicSensorFL1=ultraSonicSensorFL1,
                             ultraSonicSensorFL2=ultraSonicSensorFL2,
                             ultraSonicSensorFL3=ultraSonicSensorFL3,
                             ultraSonicSensorFR6=ultraSonicSensorFR6,
                             ultraSonicSensorFR7=ultraSonicSensorFR7,
                             ultraSonicSensorFR8=ultraSonicSensorFR8,
                             ultraSonicSensorBehind13=ultraSonicSensorBehind13,
                             ultraSonicSensorBehind12=ultraSonicSensorBehind12,
                             ultraSonicSensorBL14=ultraSonicSensorBL14,
                             ultraSonicSensorBL15=ultraSonicSensorBL15,
                             ultraSonicSensorBL16=ultraSonicSensorBL16,
                             ultraSonicSensorBR11=ultraSonicSensorBR11,
                             ultraSonicSensorBR10=ultraSonicSensorBR10,
                             ultraSonicSensorBR9=ultraSonicSensorBR9,
                             energySensor=None)
            connectionTime = vrep.simxGetLastCmdTime(robot.clientID)
            return robot
        else:
            print('Remote API function call returned with error code: ',res)
        vrep.simxFinish(clientID) # close all opened connections
    else:
        print('Failed connecting to remote API server')
        print('Program finished')
    return {}

# helper function
def findEnergyBlocks():
    res = []
    retCode, robotPos = vrep.simxGetObjectPosition(robot.clientID, robot.pioneerRobotHandle, -1, vrep.simx_opmode_oneshot_wait)
    robotdirection = robotDirection()
    for blockHandle,blockName,blockPosition in blockHandleArray:
        # retCode, relativePos = vrep.simxGetObjectPosition(robot.clientID, blockHandle, robot.pioneerRobotHandle, vrep.simx_opmode_oneshot_wait)
        # relativePos = [ robotPos[0]-blockPosition[0], robotPos[1]-blockPosition[1] ]
        relativePos = [ blockPosition[0]-robotPos[0], blockPosition[1]-robotPos[1] ]
        distance = math.sqrt(relativePos[0]**2 + relativePos[1]**2) # compute Euclidean distance (in 2-D)
        # TODO: Verify box_dis calculation logic; current approach relies on incorrect atan2 usage.
        absDirection = math.atan2(relativePos[0],relativePos[1])
        direction = normaliseAngle(absDirection - robotdirection)
        #mn_distance=abs(blockPosition[0]-robotPos[0])+abs(blockPosition[1]-robotPos[1])
        deltax=abs(blockPosition[0]-robotPos[0])
        deltay=abs(blockPosition[1]-robotPos[1])
        res.append((blockHandle,blockName,distance,direction,deltax,deltay))
    res.sort(key=lambda xx:xx[2])
    return res
# helper function
def collectNearestBlock():
    #global blockHandleArray
    blockHandle,blockName,distance,direction,_,_ = findEnergyBlocks()[0]
    if distance <= 0.7:
        vrep.simxSetObjectPosition(robot.clientID, blockHandle, -1, [1000,1000,-2], vrep.simx_opmode_oneshot)
        for block in blockHandleArray:
            if block[0] == blockHandle:  # Find the block by its handle
                block[-1] = [1000, 1000, -2]  # Update the block's position in the array
                break
        return('Energy collected :)')
    return('No blocks nearby :(')

def normaliseAngle(direction):
    while direction>math.pi: direction -= 2*math.pi
    while direction<-math.pi: direction += 2*math.pi
    assert -math.pi<=direction<=math.pi, direction
    return direction
