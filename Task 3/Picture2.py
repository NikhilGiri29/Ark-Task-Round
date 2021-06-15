import sys
import numpy as np 
from cv2 import cv2
import math

img = cv2.imread("Level1.png")
target = cv2.imread("zucky_elon.png")
h,w,z = img.shape


if(z != 3):
    print("Please upload a colored image")
    exit()

gray1 = np.zeros((h,w,1), dtype = "uint8")
roi = np.zeros((200,150,3), dtype = "uint8")


for i in range(h):
    for j in range(w):
        gray1[i,j,0] = ((img[i,j,0]/3) +(img[i,j,1]/3)+(img[i,j,2]/3))
row_num = 0
col_num = 0
exit = False
for i in range(h):
    for j in range(w):
        if chr(int(gray1[i][j])) ==':':
            col_num = (j+1)%w
            row_num = i + math.floor((j+1)/w)
            print("Starting pixel of second image : " ,row_num,",",col_num)
            exit = True
            break
    if exit == True:
        break

cv2.namedWindow("Original")
cv2.imshow("Original",img)
x =row_num
y =col_num
for a in range(200):
    for b in range(150):
        roi[a][b] = img[x][y]
        y+=1
        if (y == w):
            x+=1
            y =0


cv2.namedWindow("Roi")
cv2.imshow("Roi",roi)
#cv2.imwrite("roi.png",roi)


match = False
h1,w1,z1 = target.shape

for i in range(h1-200-1):
    for j in range(w1-150-1):
        if(target[i][j][0] == roi[0][0][0]):
            match =True
            #print(target[i][j][0])
            for a in range(200):
                for b in range(150):
                    if (target[i+a][j+b][0] != roi[a][b][0]):
                        #print("not here")
                        match =False
                        break
        
        if match == True:
            m=i
            n=j
            print("here----------------------------(x, y)",n,m)
            cv2.rectangle(target, (n,m), (n+150,m+200), (0,255,0), 2)
            match = False
            break
print("=========================================================================")
cv2.namedWindow("Target",cv2.WINDOW_NORMAL)
cv2.imshow("Target",target)
k = cv2.waitKey(0)
if k == ord('q'):
    cv2.destroyAllWindows()


#Final Answer : 460,230