import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import norm
from  mpl_toolkits.mplot3d import Axes3D

filename  = "Data3.csv"
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

x_pos = Kalman(zs1)
y_pos = Kalman(zs2)
z_pos = Kalman(zs3)


#fig = plt.figure(figsize = (10,10))
ax = plt.axes(projection = '3d')
ax.plot3D(x_pos.flatten(),z_pos.flatten(),y_pos.flatten(),'green')
#ax.plot3D(zs1.flatten(),zs2.flatten(),zs3.flatten(),'green')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
#plt.plot(zs1)

plt.show()