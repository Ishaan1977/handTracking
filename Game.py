import random
import time
import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone


#webcam
cap = cv2.VideoCapture(0)
width = 1280
height = 720
cap.set(3, width)
cap.set(4, height)

#Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)  # (detectionConfidence = 80%)

X = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57] # in pixel (bw pts)
Y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100] # in cms (bw webcam and hand)


# y = Ax^2 + Bx + C quadratic polynomial or eqn format
coeff = np.polyfit(X, Y, 2) # 2 is for second degree. It will generate the coefficients

# Game Variables
cx, cy = 250, 250  # initial coods of pt circle centre
color = (185, 219, 11)
counter = 0
score = 0
timeStart = time.time()
totalTime = 40     # 40 secs

#LOOP
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # 1 means flip along horizontal axis, so now left is let in webcam.
    if time.time() - timeStart < totalTime:
        hands, img = detector.findHands(img, draw=False) # false will remove all the dots and box around hand
        # we will create our separate bonding box by using 'bbox' from cvzone

        if hands:
            lmlist = hands[0]["lmList"]  # [0] indicates first hand
            #print(lmlist)
            x, y, w, h = hands[0]['bbox']

            x1,y1,z1 = lmlist[5] # pt is having three cood values in new HandDetector package
            x2,y2,z2 = lmlist[17]
            distance = int(math.sqrt((x2-x1)**2 + (y2-y1)**2)) # just ingnoring z cood

            A, B, C = coeff
            distanceCMs = int(A * (distance ** 2) + B * distance + C)
            # print(distance, distanceCMs)

            # Color Change
            if distanceCMs < 40:
                if x < cx < x+h and y < cy < y+h:
                    counter = 1

            cvzone.putTextRect(img, f'{distanceCMs} cm', (x+10,y+h+47))   # just added 10 and 47 acc to my observation
            cv2.rectangle(img, (x,y), (x+w, y+h), (185, 219, 11), 3)

        if counter:
            counter += 1
            color = (0, 255, 0)
            if counter == 3:
                cx = random.randint(100, 800)  # Random integer in b/w 100 and 800
                cy = random.randint(100, 600)  # Random integer in b/w 100 and 600
                color = (185, 219, 11)
                score += 1
                counter = 0



        #drawButton
        cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (59, 17, 245), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (59, 17, 245), 2)

        # gameHUD
        cvzone.putTextRect(img, f'Time: {int(totalTime - (time.time() - timeStart))}', (1000, 75), scale=3, offset=20)
        cv2.rectangle(img, (970, 15), (1245, 110), (255, 255, 255), 2)  # white box created by me
        cvzone.putTextRect(img, f'Score: {str(score).zfill(2)}', (1000, 200), scale=3, offset=20) #str().zfill(2)=> 2 places
        cv2.rectangle(img, (970, 140), (1275,230), (255, 255, 255), 2)  # white box created by me

    else:
        cvzone.putTextRect(img,'Game Over',(400, 300), scale=5, offset=10)
        cvzone.putTextRect(img, f'Score: {score}', (450, 400), scale=5, offset=10)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

