import cv2
import mediapipe as mp
import time

# url = "http://192.168.43.180:8080/video"
# cap = cv2.VideoCapture(url)
class handDetector():
    
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            for handLns in self.results.multi_hand_landmarks:
                # mpDraw.draw_landmarks(img, handLns, mpHands.HAND_CONNECTIONS)
                for id, lm in enumerate(handLns.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                    cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1,
                    (255, 0, 255), 1)
                    # if id ==1:
                    #     cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    # print(lmList)
        return lmList
    
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
    
def main():
    pTime = 0
    cTime = 0
    detector = handDetector()
    while True:
        # success, img = cap.read()
        img = cv2.imread("./Images/hand1.jpg")
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
                    
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        print(img.shape)
        cv2.waitKey(0)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        else:
            break


if __name__ == "__main__":
    main()
# cap.release()
    cv2.destroyAllWindows()