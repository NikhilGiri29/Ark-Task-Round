import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import inv
from scipy.stats import norm
from  mpl_toolkits.mplot3d import Axes3D


filename  = "Data2.csv"

#reference Station --> Station 1
ref_x = np.array(pd.read_csv(filename,usecols=[0]),dtype= np.float32)
ref_y = np.array(pd.read_csv(filename,usecols=[1]),dtype= np.float32)
ref_z = np.array(pd.read_csv(filename,usecols=[2]),dtype= np.float32)
refx = np.array([x * 1000 for x in ref_x])
refy = np.array([x * 1000 for x in ref_y])
refz = np.array([x * 1000 for x in ref_z])

#Station of interest
station_number = 3
factor = (station_number - 1) *3
int_x = np.array(pd.read_csv(filename,usecols=[factor]),dtype= np.float32)
int_y = np.array(pd.read_csv(filename,usecols=[factor + 1]),dtype= np.float32)
int_z = np.array(pd.read_csv(filename,usecols=[factor + 2]),dtype= np.float32)
intx = np.array([x * 1000 for x in int_x])
inty = np.array([x * 1000 for x in int_y])
intz = np.array([x * 1000 for x in int_z])


def Kalman(zs1,zs2,zs3,R_var,Q_var):

    dt = 1
    X = np.array([[zs1[0], 2,zs2[0],2,zs3[0],2]]).T
    P = np.diag([10, 10,10,10,10,10])
    F = np.array([[1,dt,0,0,0,0],
                [0, 1,0,0,0,0],
                [0,0,1,dt,0,0],
                [0,0,0,1,0,0],
                [0,0,0,0,1,dt],
                [0,0,0,0,0,1]])

    H = np.array([[1.,0,0,0,0,0],
                [0,0,1.,0,0,0],
                [0,0,0,0,1.,0]])

                
    R = np.array([[R_var,0,0],
                [0,R_var,0],
                [0,0,R_var]])


    Q = np.array([
                [.25*dt**4,.5*dt**3,0,0,0,0],
                [.5*dt**3,dt**2,0,0,0,0],
                [0,0,.25*dt**4,.5*dt**3,0,0],
                [0,0,.5*dt**3,dt**2,0,0],
                [0,0,0,0,.25*dt**4,5*dt**3],
                [0,0,0,0,.5*dt**3,dt**2]
                ])*Q_var


    x_pos = [X[0]]
    y_pos = [X[2]]
    z_pos = [X[4]]

    x_f = []
    y_f = []
    z_f = []

    count =0
    factor = 100
    tracker  =0
    for i in range(zs1.size):
        count +=1
        z = [zs1[i],zs2[i],zs3[i]]

        X = F @ X
        P = F @ P @F.T + Q

        S = H @ P @ H.T + R
        K = P @ H.T @ inv(S)
        Y = z - H@X

        X += K @ Y
        P = P - K @ H @ P

        x_pos.append(X[0])
        y_pos.append(X[2])
        z_pos.append(X[4])

        if count == factor or i == zs1.size -1:
            sum_x = 0
            sum_y = 0
            sum_z = 0

            for e in range(count):
                sum_x += x_pos[tracker +e]
                sum_y += y_pos[tracker +e]
                sum_z += z_pos[tracker +e]
            x_f.append([float(sum_x/count)]*factor)
            y_f.append([float(sum_y/count)]*factor)
            z_f.append([float(sum_z/count)]*factor)
            count =0
            tracker += factor
    return np.array(x_f[:]).flatten(),np.array(y_f[:]).flatten(),np.array(z_f[:]).flatten()

    
x1,y1,z1 = Kalman(refx,refy,refz,5000,0.2)
x2,y2,z2 = Kalman(intx,inty,intz,5000,0.2)

x =[]
y =[]
z =[]

for i in range(9999):
    x.append((x1[i])-(x2[i]))
    y.append((y1[i])-(y2[i]))
    z.append((z1[i])-(z2[i]))


a = plt.figure("X")
plt.hist(x)

b = plt.figure("Y")
plt.hist(y)

c = plt.figure("Z")
plt.hist(z)

plt.show()  