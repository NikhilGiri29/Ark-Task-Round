import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import inv
from scipy.stats import norm
from  mpl_toolkits.mplot3d import Axes3D


filename  = "Data4.csv"
zs_x = np.array(pd.read_csv(filename,usecols=[0]),dtype= np.float32)
zs_y = np.array(pd.read_csv(filename,usecols=[1]),dtype= np.float32)
zs_z = np.array(pd.read_csv(filename,usecols=[2]),dtype= np.float32)
zs1 = np.array([x * 1000 for x in zs_x])
zs2 = np.array([x * 1000 for x in zs_y])
zs3 = np.array([x * 1000 for x in zs_z])


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

              
R = np.array([[8000,0,0],
              [0,8000,0],
              [0,0,8000]])


Q_var = 0.5
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
dist = 0
count =0
counto =0
factor = 100
tracker  =0
for i in range(zs_x.size):
    count +=1
    z = [zs1[i],zs2[i],zs3[i]]
    if i >0 :
        dist = (np.sqrt((zs1[i] -zs1[i-1])**2 + (zs2[i] -zs2[i-1])**2 +(zs3[i] -zs3[i-1])**2 ))
    if dist > 100:
        counto+=1
        x_pos.append(X[0])
        y_pos.append(X[2])
        z_pos.append(X[4])
        continue
    
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

    if count >= factor or i == zs_x.size -1:
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
o = 0
print(counto)
ax = plt.axes(projection = '3d')

#ax.plot3D(zs1.flatten(),zs3.flatten(),zs2.flatten(),'red')
ax.plot3D(np.array(x_pos[o:]).flatten(),np.array(z_pos[o:]).flatten(),np.array(y_pos[o:]).flatten(),'green')
#ax.plot3D(np.array(x_f[o:]).flatten(),np.array(z_f[o:]).flatten(),np.array(y_f[o:]).flatten(),'blue')


ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
#plt.plot(zs1)

plt.show()