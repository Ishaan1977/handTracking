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

#LOOP
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=False) # false will remove all the dots and box around hand
    # we will create ou separate bonding box by using 'bbox' from cvzone

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
        cvzone.putTextRect(img, f'{distanceCMs} cm', (x+10,y+h+47))   # just added 10 and 47 acc to my observation
        cv2.rectangle(img, (x,y), (x+w, y+h), (185, 219, 11), 3)


    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break