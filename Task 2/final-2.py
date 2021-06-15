##ATK TASK 2


from cv2 import cv2
import numpy as np
import math
import random
def resetgame():
    xb = 120
    yb = 120
    angle =  random.randrange(20,70)
    dx,dy =int(10*math.cos(math.radians(angle))),int(10*math.sin(math.radians(angle)))
    score = 0
    return xb,yb,angle,dx,dy,score

def addText(img,text,position,color =(0,255,0) ):
    cv2.putText(img,text, 
            position, 
            font, 
            fontScale,
            color,
            lineType)


face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')

video = cv2.VideoCapture(0)


h0 = 480
w0 = 640
cx = 0
cy = 0
radius = 0
speed = 10
angle =  random.randrange(20,70)  #Random Angle generation
dx,dy =int(speed*math.cos(math.radians(angle))),int(speed*math.sin(math.radians(angle)))
xb,yb = 120,120
pad = 100

score = 0
font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (0,255,0)
lineType               = 2

win = "Lets Play a Game"
empty = np.zeros((680,840,3))

#Start Page 
while True :

    cv2.imshow(win,empty)
    addText(empty,"Press A to Begin!!!!!!!",(250,350))

    k = cv2.waitKey(1)
    if k == ord('a'):
        cv2.waitKey(1000)
        for i in range(3):
            empty = np.zeros((680,840,3))

            addText(empty,"Starting in " + str(3-i) ,(280,320))
            cv2.imshow(win,empty)
            cv2.waitKey(1000)
            
        break

    
#Main Game play
while True:
    
    check, frame = video.read()
    frame = cv2.flip(frame,1)
    frame = cv2.copyMakeBorder( frame, pad, pad, pad, pad, cv2.BORDER_CONSTANT,value = 0)
    mask = np.zeros_like(frame)
    #(frame.shape) --> [480,640,3]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in faces:
        cx =(x + w // 2)
        cy = y + h // 2
        radius = h // 2 
        cv2.circle(frame, (cx,cy), radius, (255, 0,255),2)
    
    
    # Masking
    mask = cv2.circle(mask, (cx,cy), radius, (255,255,255), -1)

    result = cv2.bitwise_and(frame, mask)
    cv2.rectangle(result,(100,100),(100+w0,100+h0),(0,255,255),2)
    
    #too big player Objection
    if radius > 120 :
        
        addText(result,"Please move Back",(300,300))
        cv2.imshow(win, result) # to update the image before exit
        cv2.waitKey(20)

        continue

    xb = xb+dx
    yb = yb+dy
    
    cv2.circle(result,(xb,yb),20,(255,0,0),-1)

    #colision detect::
    
    cb_x = (cx - xb)
    cb_y = (cy - yb)

    dist = math.sqrt(cb_y**2 + cb_x**2)

    #Ball Palyer collision Logic
    if dist<= radius + 20 + 10 and dist > radius + 3: #if ball is deep then no direction changeso it goes more deep and reset
        score += 10
        phi = math.atan(cb_y/cb_x)
        
        if xb <= cx:
            
            dx = -1*int(speed*(math.cos(-1*math.radians(angle) + (2*phi))))
            dy = -1*int(speed*(math.sin(math.radians(angle) + (2*phi))))
        else : 
        
            dx = -1*int(speed*(math.cos(1*math.radians(angle) - (2*phi))))
            dy = -1*int(speed*(math.sin(1*math.radians(angle) - (2*phi))))


    #If the Ball enters the player object
    if dist< radius +20 - 5 :
        xb,yb,angle,dx,dy,score = resetgame()
        addText(result,"Please move slowly",(300,300))
        cv2.waitKey(300)
        
    if yb<=120 :
        dy *= -1
    if xb >=720 or xb<=120:
        dx *= -1

    
    addText(result,"Score =" + str(score) ,(650,35))
    addText(result,"Made by Nikhil Giri" ,(20,35))

    #Game over condition
    if yb >=560: 
        print("Game Over!!!")
        addText(result,"Game Over!!!!!!", (300,300))
        addText(result," Press R to Restart ",(280,330))
        addText(result,"Press Q to Quit", (290,360))
        cv2.imshow(win, result) # to update the image before exit
        k = cv2.waitKey(20000)
        if k == ord('q'):
            break
        elif k == ord('r'):
            xb,yb,angle,dx,dy,score = resetgame()
        else:
            #ends game if no response for 20 secs
            break
            
        
  
    cv2.imshow(win, result)
    
    # Stop if escape key is pressed
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
