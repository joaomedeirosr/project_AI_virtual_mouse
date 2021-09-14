import cv2 as cv
import numpy as np
import HandTrackingModule as htm
import time
import autopy



wCam, hCam = 640,480
frameR = 100
smoothening = 7

cap = cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
plocX,plocY = 0,0
clocX , clocY = 0,0
track = htm.handDetector(maxHands = 1)
wScr, hScr = autopy.screen.size()
#print(wScr,hScr)

while True:

    # 1. Find a hand landmarks
    success,img = cap.read()
    img=track.findHands(img)
    lmList,bbox = track.findPosition(img)

    
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        #print(x1,y1,x2,y2)
        
    # 3. Check wich finger are up
    
    fingers = track.fingersUp()
    #print(fingers)
    cv.rectangle(img,(frameR,frameR),(wCam-frameR, hCam-frameR),
        (255,0,2))
    # 4. Only Index Finger : Moving Mode
    if fingers [1] == 1 and fingers[2] == 0:
        # 5. Convert Cordinates
        
        x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
        y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScr))
    # 6. Smoothen Values
        clocX = plocX +(x3-plocX)/smoothening
        clocX = plocY +(y3-plocY)/smoothening
    # 7. Move Mouse
        autopy.mouse.move(wScr - clocX,clocY)

        cv.circle(img,(x1,y1), 15,(255,0,255),cv.FILLED)
        plocX,plocY = clocX,clocY
    # 8. Both Index  and Middle fingerrs are up: Clicking Mode
    if fingers [1] == 1 and fingers[2] == 1:
        length,img, lineInfo = track.findDistance(8,12,img)
        print(length)
        if length < 40:
            cv.circle(img,(lineInfo[4] , lineInfo[5]),
            15,(0,255,255),cv.FILLED)

            autopy.mouse.click()


    # 9. Find Distance between fingers
    # 10. Click mouse if distance short
    # 11. Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img,str(int(fps)),(20,50),cv.FONT_HERSHEY_PLAIN,
    3,(255,0,0),3)

    # 12. Visual Display 
    cv.imshow("Video is On",img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cv.destroyAllWindows()