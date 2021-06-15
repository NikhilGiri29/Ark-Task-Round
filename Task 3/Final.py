import sys
import numpy as np 
from cv2 import cv2
import math

img = cv2.imread("treasure_mp3.png")
h,w ,z= img.shape


if(z != 3):
    print("Please upload a colored image")
    exit()

gray1 = np.zeros((h,w,1), dtype = "uint8")

arr = []

for i in range(h):
    for j in range(w):
        gray1[i,j,0] = ((img[i,j,0]/3) +(img[i,j,1]/3)+(img[i,j,2]/3))
        arr.append(gray1[i][j][0])


songo = bytearray(arr)
file1 = open("Song.mp3","wb+")
file1.write(songo)
file1.close()