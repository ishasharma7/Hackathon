import numpy as np
import cv2
from collections import deque
import random

# giving different ways to handle colour points of different color
bluep = [deque(maxlen=1024)]
redp = [deque(maxlen=1024)]
greenp = [deque(maxlen=1024)]
yellowp = [deque(maxlen=1024)]

while True:
    success, image1 = cap.read()
    image1 = cv2.filp(image1, 1)
    imgHSV = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 99, 158])
    upper = np.array([10, 255, 233])

    image1 = cv2.rectangle(image1, (50, 30), (110, 80), (0, 0, 0), -1)
    image1 = cv2.rectangle(image1, (120, 30), (170, 80), colors[0], -1)
    image1 = cv2.rectangle(image1, (180, 30), (230, 80), colors[1], -1)
    image1 = cv2.rectangle(image1, (240, 30), (290, 80), colors[2], -1)
    image1 = cv2.rectangle(image1, (300, 30), (350, 80), colors[3], -1)

    cv2.putText(image1, "Clear", (62, 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(image1, b, (62, 110), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 1, cv2.LINE_AA)

    Mask = cv2.inRange(imgHSV, lower, upper)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.inRange(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.inRange(Mask, kernel, iterations=1)

    contours, heirc = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centre = None

if len(contours) > 0:
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    ((x, y), radius) = cv2.minEnclosingCircle(contours)
    cv2.circle(image1, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    P = cv2.moments(contours)
    centre = (int(P['m10']/P['m00']), int(P['m01']/P['m00']))
    points = [bluep, greenp, redp, yellowp]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(image1, points[i][j][k - 1], points[i][j][k], colors[i], 2)
    cv2.imshow("Air Doodle", image1)

    if cv2.waitkey(35) & 0xff == ord('q'):
          break
