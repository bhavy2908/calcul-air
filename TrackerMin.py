import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
drawHand = mp.solutions.drawing_utils

previousTime = 0
currentTime = 0

while True:
    success, img =cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)


    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(handLandmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)

            drawHand.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)

    currentTime = time.time()
    fps = 1/(currentTime-previousTime)
    previousTime = currentTime

    cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)