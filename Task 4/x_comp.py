import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import inv
from scipy.stats import norm
from  mpl_toolkits.mplot3d import Axes3D


filename  = "Data1.csv"
zs_x = np.array(pd.read_csv(filename,usecols=[2]),dtype= np.float32)
zs1 = np.array([x * 1000 for x in zs_x])

zs_x1 = np.array(pd.read_csv(filename,usecols=[5]),dtype= np.float32)
zs11 = np.array([x * 1000 for x in zs_x1])



def Kalman(zs,R_var,Q_var):
    dt = 1
    X = np.array([[zs[0], 2]]).T
    P = np.diag([10, 10])
    F = np.array([[1, dt],
                [0,  1]])
    H = np.array([[1., 0.]])
    R = np.array([[R_var]])
    Q = np.array([[.25*dt**4, .5*dt**3],
                [ .5*dt**3,    dt**2]] )*Q_var
        
    x_pos = [zs[0]]
    count =0
    factor = 9
    tracker  =0
    x_f = []

    for z  in zs:
        count += 1
        X = F @ X
        P = F @ P @F.T + Q

        S = H @ P @ H.T + R
        K = P @ H.T @ inv(S)
        Y = z - H@X
        X += K @ Y
        P = P - K @ H @ P

        x_pos.append(X[0])


        if count == factor:
            sum_x = 0
            
            for e in range(count):
                sum_x += float(x_pos[tracker +e])
            avg = float(sum_x/count)
            for i in range (count) :
                 x_f.append(avg)
            count =0
            tracker += factor
    return x_f




x1 = np.array(Kalman(zs1,5000,0.2))
print(x1.shape)
x2 = np.array(Kalman(zs11,8000,0.02))
result =[]

for i in range(9999):
    result.append(-(x2[i])+(x1[i]))

plt.hist(result)

plt.show()