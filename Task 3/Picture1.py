import numpy as np 
from cv2 import cv2


img = cv2.imread("Level1.png")
h,w,z = img.shape



gray1 = np.zeros((h,w,1), dtype = "uint8")

for i in range(h):
    for j in range(w):
        gray1[i,j,0] = ((img[i,j,0]/3) +(img[i,j,1]/3)+(img[i,j,2]/3))

cv2.namedWindow("Original")
cv2.imshow("Original",img)


for i in range(h):              #h is height of image
    for j in range(w):          #w is width of image
        print(chr(int(gray1[i][j])),end="")
    print()


k = cv2.waitKey(0)
if k == ord('q'):
    cv2.destroyAllWindows()