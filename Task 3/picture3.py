import sys
import numpy as np 
from cv2 import cv2
import math

img = cv2.imread("maze_lv3.png")
h,w,z = img.shape


if(z != 3):
    print("Please upload a colored image")
    exit()

b = np.zeros((h,w,1), dtype = "uint8")
g = np.zeros((h,w,1), dtype = "uint8")
r = np.zeros((h,w,1), dtype = "uint8")

for i in range(h):
    for j in range(w):
        b[i,j] =  img[i,j,0]
        g[i,j] =  img[i,j,1]
        r[i,j] =  img[i,j,2]
for i in range(h):
    for j in range(w):
        if b[i,j] == 230:
               b[i,j] =255
        else:
            b[i,j] =0 
cv2.namedWindow("Original")
cv2.namedWindow("Red")
cv2.namedWindow("Green")
cv2.namedWindow("Blue")
cv2.imshow("Original",img)
cv2.imshow("Red",r)
cv2.imshow("Green",g)
cv2.imshow("Blue",b)

k = cv2.waitKey(0)
if k == ord('q'):
    cv2.destroyAllWindows()