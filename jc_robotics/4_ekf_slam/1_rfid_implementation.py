import math
import numpy as np
import matplotlib.pyplot as plt



#EKF state Cov
Cx = np.diag([0.5, 0.5, np.deg2rad(30.0)])**2


#Simulation Param
Qsim = np.diag([0.2, np.deg2rad(1.0)])**2
Rsim = np.diag([1.0, np.deg2rad(10.0)])**2


DT = 0.1 # time tick[s]
SIM_TIME = 50.0 #simulation time [s]
MAX_RANGE = 20.0 #maximum observation range
M_DIST_TH = 2.0 #Threshold of Mahalanobis distance for data association
STATE_SIZE = 3 # State size [x, y, yaw]
LM_SIZE = 2 #LM state size = [x,y]

show_animation = True


#control input vector
def calc_input():
    v = 1.0 # [m/s]
    yawrate = 0.1 # [rad/s]
    u = np.array([[v, yawrate]]).T
    return u


def motion_model(x, u):

    F = np.array([
        [1.0, 0, 0],
        [0, 1.0, 0],
        [0, 0, 1.0]
    ])

    #DT * cos(currnet_yaw)
    B = np.array([
        [DT * math.cos(x[2,0]),0],
        [DT * math.sin(x[2,0]),0],
        [0.0, DT]
    ])


    x = (F@x) +(B@u)
    return x


def pi_2_pi(angle):
    return (angle + math.pi)% (2*math.pi) - math.pi


def observation(xTrue, xd, u, RFID):

    xTrue = motion_model(xTrue,u)
    
    # z = [0, 0, 0]
    z = np.zeros((0,3))

    for i in range(len(RFID[:,0])):

        dx = RFID[i,0]- xTrue[0,0]
        dy = RFID[i,1]- xTrue[1,0]

        d = math.sqrt(dx**2+dy**2)
        angle = pi_2_pi(math.atan2(dy,dx)- xTrue[2,0])

        if d<=MAX_RANGE:
            dn = d + np.random.randn() *Qsim[0,0] #add noise
            anglen = angle + np.random.randn() *Qsim[1,1] # add noise
            zi = np.array([dn, anglen, i])
            z = np.vstack((z,zi))

    ud = np.array([
        [u[0,0] + np.random.randn() * Rsim[0,0],
        u[1,0] + np.random.randn() * Rsim[1,1]]
    ]).T

    xd = motion_model(xd,ud)

    return xTrue, z, xd, ud






def main():
    print(__file__ +" start!!")
    time = 0.0

    #RFID position [x, y]
    RFID = np.array([
        [10.0, -2.0],
        [15.0, 10.0],
        [3.0, 15.0],
        [-5.0, 20.0]
    ])

    #State Vector [x y yaw v]'
    xEst = np.zeros((STATE_SIZE, 1))
    xTrue = np.zeros((STATE_SIZE, 1))
    PEst = np.eye(STATE_SIZE)

    xDR = np.zeros((STATE_SIZE,1)) #Dead Recokning

    #history
    hxEst = xEst
    hxTrue = xTrue
    hxDR = xTrue

    while SIM_TIME >= time:
        time += DT
        u = calc_input()
        xTrue, z, xDR,ud = observation(xTrue, xDR, u, RFID)


        hxDR = np.hstack((hxDR, xDR))
        hxTrue = np.hstack((hxTrue, xTrue))


        if show_animation:
            plt.cla()

            plt.plot(RFID[:,0], RFID[:,1], "*k")
            plt.plot(xEst[0], xEst[1],".r")


            plt.plot(hxTrue[0,:], hxTrue[1,:],"-b")
            plt.plot(hxDR[0,:],hxDR[1,:],"-k")
            plt.axis("equal")
            plt.grid(True)
            plt.pause(0.001)






if __name__ == '__main__':
    main()
