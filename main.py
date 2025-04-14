import cv2
from cvzone.HandTrackingModule import HandDetector


# Button Class
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        return self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height


# Buttons Grid
buttonListValues = [['=', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '7']]
buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

# Variables
myEquation = ''
delayCounter = 0

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        continue  # Skip frame if camera fails
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # Draw Display Panel
    cv2.rectangle(img, (800, 70), (1200, 170), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800, 70), (1200, 170), (50, 50, 50), 3)

    # Draw Buttons
    for button in buttonList:
        button.draw(img)

    # Hand Detection & Button Click Logic
    if hands:
        lmList = hands[0]['lmList']
        if len(lmList) > 12:
            x, y = lmList[8][:2]  # Index finger tip
            length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
            if length < 50 and delayCounter == 0:
                for button in buttonList:
                    if button.checkClick(x, y):
                        myValue = button.value
                        if myValue == '=':
                            try:
                                myEquation = str(eval(myEquation))
                            except:
                                myEquation = "Error"
                        else:
                            myEquation += myValue
                        delayCounter = 1

    # Avoid multiple clicks
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # Display Equation
    cv2.putText(img, myEquation, (810, 130), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    # Show Output
    cv2.imshow("Virtual Calculator", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''
    elif key == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()