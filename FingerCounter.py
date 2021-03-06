import cv2
import Tracker as Tracker

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

handDetector = Tracker.handDetector()

fingerTips = [8, 12, 16, 20]

while True:
    totalFingers = 0
    totalFingers2 = 0
    success, img = cap.read()

    img = handDetector.detectHands(img, display=True)
    landmarkList = handDetector.findPosition(img, 0)
    if len(landmarkList) != 0:
        fingerCount = []
        if landmarkList[4][1] > landmarkList[17][1]:
            rightHand = False
            if landmarkList[3][1] < landmarkList[4][1]:
                fingerCount.append(1)
            else:
                fingerCount.append(0)

        else:
            rightHand = True
            if landmarkList[4][1] < landmarkList[2][1]:
                fingerCount.append(1)
            else:
                fingerCount.append(0)
        for id in range(0, 4):
            if landmarkList[fingerTips[id]][2] < landmarkList[fingerTips[id] - 1][2]:
                fingerCount.append(1)
            else:
                fingerCount.append(0)
        totalFingers = fingerCount.count(1)

    if handDetector.noOfHands() == 2:

        landmarkList2 = handDetector.findPosition(img, 1)
        if len(landmarkList2) != 0:
            fingerCount2 = []
            if landmarkList2[4][1] > landmarkList2[17][1]:
                rightHand = False
                if landmarkList2[3][1] < landmarkList2[4][1]:
                    fingerCount2.append(1)
                else:
                    fingerCount2.append(0)

            else:
                rightHand = True
                if landmarkList2[4][1] < landmarkList2[2][1]:
                    fingerCount2.append(1)
                else:
                    fingerCount2.append(0)
            for id in range(0, 4):
                if landmarkList2[fingerTips[id]][2] < landmarkList2[fingerTips[id] - 1][2]:
                    fingerCount2.append(1)
                else:
                    fingerCount2.append(0)
            totalFingers2 = fingerCount2.count(1)
    elif handDetector.noOfHands() == 0:
        cv2.putText(img, "No Hands Found", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1.5,
                    (255, 255, 255),
                    2)

    Fingers = totalFingers + totalFingers2
    if handDetector.noOfHands() != 0:
        cv2.putText(img, "Hands: " + str(int(handDetector.noOfHands())) + " Fingers: " + str(int(Fingers)), (10, 50),
                    cv2.FONT_HERSHEY_DUPLEX, 1.5,
                    (255, 255, 255),
                    2)
    cv2.imshow("Calcul Air", img)
    cv2.waitKey(1)
