import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

zs = np.array(pd.read_csv("Data1.csv",usecols=[0]),dtype= np.float32)
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

np.random.seed(13)

process_var = 0.4
sensor_var = 10.
x = gaussian(0., 10.**2)  
dx = 1
dt = 1.
process_model = gaussian(dx*dt, process_var) 

x_pos = [x.mean()]

for z in zs1[:100]:    
    prior = predict(x, process_model)
    likelihood = gaussian(z, sensor_var)
    x = update(prior, likelihood)
    x_pos.append(x.mean())
    #print('{:.9f}     {:.9f}'.format(int(x.mean()),int(x.var()) ))


plt.plot(x_pos)
#plt.plot(zs1)

plt.show()