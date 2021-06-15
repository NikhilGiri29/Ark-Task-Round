import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import inv
from scipy.stats import norm

zs = np.array(pd.read_csv("Data1.csv",usecols=[3]),dtype= np.float32)
zs1 = [x * 1000 for x in zs]

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


dt = 1
X = np.array([[zs1[0], 2]]).T
P = np.diag([10, 10])
F = np.array([[1, dt],
              [0,  1]])
H = np.array([[1., 0.]])
R = np.array([[8000]])
Q_var = 0.01
Q = np.array([[.25*dt**4, .5*dt**3],
             [ .5*dt**3,    dt**2]] )*Q_var
    
x_pos = [zs1[0]]
x1_pos = Kalman(zs1)
for z  in zs1 :
    
    X = F @ X
    P = F @ P @F.T + Q

    S = H @ P @ H.T + R
    K = P @ H.T @ inv(S)
    Y = z - H@X
    X += K @ Y
    P = P - K @ H @ P

    x_pos.append(X[0])

plt.plot(x1_pos)
plt.plot(x_pos)

#plt.plot(zs1[0:200])

plt.show()