import cv2
import mediapipe as mp
import time
import handDetector as hd

pTime = 0
cTime = 0
det, op = 0, 0
myPoints =  []  ## [x , y , colorId ]
circle_color = [255,255,255]
detector = hd.handDetector(detectionCon=0.7)

# url = "./HandExercise.mp4"
cap = cv2.VideoCapture(0)

def drawOnCanvas(myPoints, draw=True):
    i = 0
    gap = 30
    if draw:
        circle_color = [255,255,255]
        for point in myPoints:
            if i != 0 and prevpoint[1]+gap >= point[1] >= prevpoint[1]-gap and prevpoint[2]+gap >= point[2] >= prevpoint[2]-gap:
                cv2.circle(imgResult, (point[1], point[2]), 10, circle_color, cv2.FILLED)
                #gradient color
                # if circle_color[1] <=10:
                #     circle_color = [255, 255, 255]
                # else:
                #     circle_color = [circle_color[0]-1, circle_color[1]-2, circle_color[2]-1]
                cv2.line(imgResult, (point[1], point[2]), (prevpoint[1], prevpoint[2]), circle_color, 20)
                # print(point, prevpoint)
            prevpoint = point
            i =1
    else:
        pass
    # print("mypoints    draw", myPoints)
    return imgResult

while True:
    success, img = cap.read()
    # img = cv2.imread("./Images/hand1.jpg")
    img = cv2.flip(img, 1)
    img = detector.findHands(img, draw=False)
    imgResult = img.copy()
    lmList = detector.findPosition(img)
    newPoints = []

    # print(lmList[2][0], type(lmList[2]))
    if len(lmList) != 0:
        # print("lmList",lmList[8])
        newPoints = [lmList[8]]
        # point4 = lmList[4]
        # point8 = lmList[8]
        # point7 = lmList[7]
        # print(point7[1], " ", point4[1], " ", point8[1])
        # print(point7[2], " ", point4[2], " ", point8[2])
        # cv2.circle(imgResult, (point[1], point[2]), 10, circle_color, cv2.FILLED)
        # if (point4[1]+25 >= point8[1] >= point4[1]-25 or point4[1]+25 >= point8[2] >= point4[1]-25) or (point4[1]+25 >= point7[1] >= point4[1]-25 or point4[1]+25 >= point7[2] >= point4[1]-25):
        #     cv2.circle(imgResult, (20, 10), 10, (255, 0, 0), cv2.FILLED)
        # else:
        #     newPoints = []
        cv2.circle(imgResult, (10, 10), 10, (0, 255, 0), cv2.FILLED)
        if det == 0 or op == 0:
            print("Hand Detceted")
            det = 1
            op = 1

    if len(lmList) == 0:
        cv2.circle(imgResult, (10, 10), 10,(0, 0, 255), cv2.FILLED)
        if det == 1 or op ==0:
            print("Hand not Detceted")
            det = 0
            op = 1

    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    # print("mypoints",myPoints)
    if len(myPoints)!=0:
        imgResult = drawOnCanvas(myPoints)
    
    cv2.imshow("Virtual pen", imgResult)
    if cv2.waitKey(25) & 0xFF == ord('c'):
        myPoints = []
    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime

    # cv2.putText(img, "FPS:"+str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2,
    #             (255, 0, 255), 2)

    # cv2.imshow("Image", img)
    # print(img.shape)
    cv2.waitKey(1)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    # else:
    #     break
