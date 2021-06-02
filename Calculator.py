import cv2
import Tracker as Tracker
import time
import numpy as np

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

handDetector = Tracker.handDetector()

fingerTips = [8, 12, 16, 20]
previousTime = 0
currentTime = 0

begin = 0
beginBool = False

firstNumberCount = 0
firstArr = []
firstArr = [0 for x in range(100)]
firstNumber = 0
firstNumberBool = False

secondNumber = 0
secondNumberCount = 0
secondNumberBool = False
secondArr = []
secondArr = [0 for x in range(100)]

operationNumber = 0
operationNumberCount = 0
operationNumberBool = 0
operationArr = []
operationArr = [0 for x in range(130)]

result = 0

reset = 0

operationList = [2, 4, 6, 8]

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

    Fingers = totalFingers + totalFingers2
    if Fingers == 10:
        begin += 1

    if begin <= 50:
        cv2.putText(img, "Show both Hands to initiate", (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 1,
                    (255, 255, 255),
                    2)


    else:
        cv2.putText(img, "Initiated", (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 1,
                    (181, 143, 49),
                    2)
        beginBool = True

    if beginBool == True and firstNumberCount < 100:
        cv2.putText(img, "Enter First Number", (500, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 1,
                    (255, 255, 255),
                    2)
    if (beginBool == True and firstNumberCount < 100) and handDetector.noOfHands() != 0:
        firstArr[firstNumberCount] = Fingers
        firstNumberCount += 1
    if firstNumberCount >= 100:
        firstNumber = np.bincount(firstArr).argmax()

        cv2.putText(img, "First Number: " + str(firstNumber), (10, 100),
                    cv2.FONT_HERSHEY_DUPLEX, 1,
                    (255, 255, 255),
                    2)
        firstNumberBool = True

    if firstNumberBool == True and secondNumberCount < 100:
        cv2.putText(img, "Enter Second Number", (500, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 1,
                    (255, 255, 255),
                    2)

    if firstNumberBool == True and secondNumberCount < 100 and handDetector.noOfHands() != 0:
        secondArr[secondNumberCount] = Fingers
        secondNumberCount += 1
    if secondNumberCount >= 100:
        secondNumber = np.bincount(secondArr).argmax()

        cv2.putText(img, "Second Number: " + str(secondNumber), (10, 150),
                    cv2.FONT_HERSHEY_DUPLEX, 1,
                    (255, 255, 255),
                    2)
        secondNumberBool = True
        if secondNumberBool == True and operationNumberCount < 130 and operationNumberBool == False:
            cv2.putText(img, "Select Operation", (500, 30),
                        cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 255, 255),
                        2)
            cv2.putText(img, "Show '2' for '+'", (500, 70),
                        cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 255, 255),
                        2)
            cv2.putText(img, "Show '4' for '-'", (500, 100),
                        cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 255, 255),
                        2)
            cv2.putText(img, "Show '6' for 'x'", (500, 130),
                        cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 255, 255),
                        2)
            cv2.putText(img, "Show '8' for '/'", (500, 160),
                        cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 255, 255),
                        2)
        if secondNumberBool == True and operationNumberCount < 100 and handDetector.noOfHands() != 0:
            if Fingers not in operationList:
                cv2.putText(img, "Please select an Valid Operation", (850, 80),
                            cv2.FONT_HERSHEY_DUPLEX, 0.75,
                            (0, 0, 255),
                            2)
            operationArr[operationNumberCount] = Fingers
            operationNumberCount += 1
        if operationNumberCount >= 100:
            operationNumber = np.bincount(operationArr).argmax()
            if operationNumber == 2:
                cv2.putText(img, "Operation: Addition", (10, 200),
                            cv2.FONT_HERSHEY_DUPLEX, 1,
                            (255, 255, 255),
                            2)
                result = firstNumber + secondNumber
                cv2.putText(img, "Result: ", (10, 300),
                            cv2.FONT_HERSHEY_DUPLEX, 2,
                            (255, 255, 255),
                            3)
                operationNumberBool = True
                cv2.putText(img, str(result), (250, 300),
                            cv2.FONT_HERSHEY_DUPLEX, 2,
                            (181, 143, 49),
                            3)
            elif operationNumber == 4:
                cv2.putText(img, "Operation: Subtraction", (10, 200),
                            cv2.FONT_HERSHEY_DUPLEX, 1,
                            (255, 255, 255),
                            2)
                result = firstNumber - secondNumber
                cv2.putText(img, "Result: ", (10, 300),
                            cv2.FONT_HERSHEY_DUPLEX, 2,
                            (255, 255, 255),
                            3)
                operationNumberBool = True
                cv2.putText(img, str(result), (250, 300),
                            cv2.FONT_HERSHEY_DUPLEX, 2,
                            (181, 143, 49),
                            3)
            elif operationNumber == 6:
                cv2.putText(img, "Operation: Multiplication", (10, 200),
                            cv2.FONT_HERSHEY_DUPLEX, 1,
                            (255, 255, 255),
                            2)
                result = firstNumber * secondNumber
                cv2.putText(img, "Result: ", (10, 300),
                            cv2.FONT_HERSHEY_DUPLEX, 2,
                            (255, 255, 255),
                            3)
                cv2.putText(img, str(result), (250, 300),
                            cv2.FONT_HERSHEY_DUPLEX, 2,
                            (181, 143, 49),
                            3)
                operationNumberBool = True
            elif operationNumber == 8:
                cv2.putText(img, "Operation: Division", (10, 200),
                            cv2.FONT_HERSHEY_DUPLEX, 1,
                            (255, 255, 255),
                            2)
                result = firstNumber / secondNumber
                cv2.putText(img, "Result: ", (10, 300),
                            cv2.FONT_HERSHEY_DUPLEX, 2,
                            (255, 255, 255),
                            3)
                cv2.putText(img, str(result), (250, 300),
                            cv2.FONT_HERSHEY_DUPLEX, 2,
                            (181, 143, 49),
                            3)
                operationNumberBool = True
            else:
                secondNumberBool = False
                operationNumberCount = 0


        if operationNumberBool == True:
            cv2.putText(img, "Show Both Hands to RESET", (430, 30),
                        cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 255, 255),
                        2)
        if Fingers == 10 and operationNumberBool == True:
            reset += 1
        if reset > 100:
            begin = 0
            beginBool = False

            firstNumberCount = 0
            firstArr = []
            firstArr = [0 for x in range(100)]
            firstNumber = 0
            firstNumberBool = False

            secondNumber = 0
            secondNumberCount = 0
            secondNumberBool = False
            secondArr = []
            secondArr = [0 for x in range(100)]

            operationNumber = 0
            operationNumberCount = 0
            operationNumberBool = 0
            operationArr = []
            operationArr = [0 for x in range(130)]

            result = 0

            reset = 0

    cv2.putText(img, str(int(Fingers)), (1220, 30),
                cv2.FONT_HERSHEY_DUPLEX, 1,
                (181, 143, 49),
                2)
    cv2.putText(img, "github.com/bhavy2908", (1090, 713),
                cv2.FONT_HERSHEY_DUPLEX, 0.5,
                (0, 0, 0),
                1)

    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(img, "Frames: " + str(int(fps)), (1150, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    if handDetector.noOfHands() == 0:
        cv2.putText(img, "No Hands Found", (1040, 80),
                    cv2.FONT_HERSHEY_DUPLEX, 0.75,
                    (0, 0, 255),
                    2)
    cv2.imshow("Calcul Air", img)
    cv2.waitKey(1)
