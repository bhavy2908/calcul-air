import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectConfidence=0.75, trackConfidence=0.75):
        self.mode = mode
        self.maxHands = maxHands
        self.detectConfidence = detectConfidence
        self.trackConfidence = trackConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectConfidence, self.trackConfidence)
        self.drawHand = mp.solutions.drawing_utils

    def detectHands(self, img, display=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if display:
                    self.drawHand.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo):

        landmarkList = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                landmarkList.append([id, cx, cy])


        return landmarkList
    def noOfHands(self):
        if self.results.multi_hand_landmarks:
            return len(self.results.multi_hand_landmarks)
        return 0



def main():
    cap = cv2.VideoCapture(0)
    previousTime = 0
    currentTime = 0
    hand_detector = handDetector()

    while True:
        success, img = cap.read()
        img = hand_detector.detectHands(img)
        landmarkList = hand_detector.findPosition(img)

        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        cv2.imshow("Calcul Air", img)
        cv2.waitKey(1)
        print(hand_detector.noOfHands())



if __name__ == "__main__":
    main()
