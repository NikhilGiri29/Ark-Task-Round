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



def gaussian(m,v):
    return norm(m,np.sqrt(v))
    
def update(prior, measurement):
    x, P = prior.mean(), prior.var()        # mean and variance of prior
    z, R = measurement.mean(), measurement.var()  # mean and variance of measurement
    
    y = z - x        # residual
    K = P / (P + R)  # Kalman gain

    x = x + K*y      # posterior
    P = (1 - K) * P  # posterior variance
    return gaussian(x, P)

def predict(posterior, movement):
    x, P = posterior.mean(), posterior.var() # mean and variance of posterior
    dx, Q = movement.mean(), movement.var() # mean and variance of movement
    x = x + dx
    P = P + Q
    return gaussian(x, P)

def Kalman(zs):
    process_var = 0.4
    sensor_var = 10.
    x = gaussian(zs[0], 10.**2)  
    dx = 1
    dt = 1.
    process_model = gaussian(dx*dt, process_var) 

    x_pos = [x.mean()]

    for z in zs:    
        prior = predict(x, process_model)
        likelihood = gaussian(z, sensor_var)
        x = update(prior, likelihood)
        x_pos.append(x.mean())
    
    return np.array(x_pos)
    #print('{:.9f}     {:.9f}'.format(int(x.mean()),int(x.var()) ))

x1_pos = Kalman(zs1)
y1_pos = Kalman(zs2)
z1_pos = Kalman(zs3)




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

              
R = np.array([[5000,0,0],
              [0,5000,0],
              [0,0,5000]])


Q_var = 0.02
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


for i in range(zs_x.size):
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
    
o = 0

ax = plt.axes(projection = '3d')
ax.plot3D(x1_pos[o:].flatten(),z1_pos[o:].flatten(),y1_pos[o:].flatten(),'red')
ax.plot3D(np.array(x_pos[o:]).flatten(),np.array(z_pos[o:]).flatten(),np.array(y_pos[o:]).flatten(),'green')
#ax.plot3D(zs1.flatten(),zs2.flatten(),zs3.flatten(),'green')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
#plt.plot(zs1)

plt.show()